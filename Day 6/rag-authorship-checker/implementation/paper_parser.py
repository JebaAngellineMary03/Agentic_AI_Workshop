import fitz  # PyMuPDF
import re
import asyncio
import aiohttp
from urllib.parse import urlparse

class PaperParser:
    def parse_pdf(self, pdf_path):
        """Parse PDF file and extract metadata"""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            
            # Extract text from all pages
            for page in doc:
                text += page.get_text()
            doc.close()
            
            # Extract metadata
            title = self.extract_title_from_text(text)
            authors = self.extract_authors_from_text(text)
            doi = self.parse_doi(text)
            
            return {
                'title': title,
                'authors': authors,
                'doi': doi,
                'text': text,
                'content': text[:2000]  # First 2000 chars for AI analysis
            }
        except Exception as e:
            return {'error': f"Failed to parse PDF: {str(e)}"}
    
    def parse_doi_sync(self, doi):
        """Synchronous DOI parsing - for when you need it immediately"""
        try:
            # This is a placeholder - you'd need to implement DOI-to-paper fetching
            # For now, return a basic structure
            return {
                'title': f"Paper from DOI: {doi}",
                'authors': ["DOI Author"],
                'doi': doi,
                'content': f"Paper retrieved from DOI {doi}",
                'text': f"Full text for DOI {doi}"
            }
        except Exception as e:
            return {'error': f"Failed to parse DOI: {str(e)}"}
    
    async def parse_doi(self, doi):
        """Async DOI parsing - for when you want to fetch from external APIs"""
        try:
            # Example of fetching paper data from DOI asynchronously
            async with aiohttp.ClientSession() as session:
                # This is a placeholder URL - replace with actual DOI resolver
                url = f"https://api.crossref.org/works/{doi}"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        work = data.get('message', {})
                        
                        return {
                            'title': work.get('title', ['Unknown Title'])[0],
                            'authors': [f"{author.get('given', '')} {author.get('family', '')}" 
                                      for author in work.get('author', [])],
                            'doi': doi,
                            'content': work.get('abstract', 'No abstract available'),
                            'text': work.get('abstract', 'No full text available')
                        }
                    else:
                        return self.parse_doi_sync(doi)  # Fallback to sync method
        except Exception as e:
            return {'error': f"Failed to parse DOI: {str(e)}"}
    
    def extract_title_from_text(self, text):
        """Extract title from plain text with heuristics"""
        lines = text.split('\n')[:15]  # Look at top lines
        for line in lines:
            line = line.strip()
            if (
                10 < len(line) < 150 and
                not any(keyword in line.lower() for keyword in [
                    "journal", "conference", "volume", "issue", "doi", "copyright",
                    "abstract", "keywords", "introduction", "received", "accepted"
                ])
            ):
                return line
        return "Extracted from PDF"
    
    def extract_authors_from_text(self, text):
        """Extract authors from plain text using regex and cleaning"""
        if not isinstance(text, str):
            return ["Unknown Author"]
            
        text_snippet = text[:1500]
        patterns = [
            r'Author[s]?:?\s*([^\n]+)',
            r'By:?\s*([^\n]+)',
            r'([A-Z][a-z]+ [A-Z][a-z]+(?:, [A-Z][a-z]+ [A-Z][a-z]+)*)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_snippet)
            if match:
                authors_line = match.group(1)
                # Split by common separators
                authors = re.split(',| and ', authors_line)
                cleaned_authors = [
                    str(a).strip() for a in authors
                    if isinstance(a, (str, int, float)) and 3 < len(str(a).strip()) < 100 
                    and not str(a).strip().lower().startswith("from ")
                ]
                if cleaned_authors:
                    return cleaned_authors[:5]
        
        return ["Unknown Author"]
    
    def parse_doi(self, text):
        """Extract DOI from text using multiple patterns"""
        # Common DOI patterns
        doi_patterns = [
            r'DOI:\s*(10\.\d+/[^\s]+)',
            r'doi:\s*(10\.\d+/[^\s]+)',
            r'https?://doi\.org/(10\.\d+/[^\s]+)',
            r'https?://dx\.doi\.org/(10\.\d+/[^\s]+)',
            r'\bdoi\s*[:=]\s*(10\.\d+/[^\s\]]+)',
            r'(10\.\d{4,}/[^\s\]]+)'  # Generic DOI pattern
        ]
        
        # Search in first 3000 characters where DOI is most likely to appear
        search_text = text[:3000]
        
        for pattern in doi_patterns:
            matches = re.findall(pattern, search_text, re.IGNORECASE)
            if matches:
                # Clean and validate the first match
                doi = matches[0].strip()
                # Remove trailing punctuation
                doi = re.sub(r'[.,;)\]]+$', '', doi)
                if self.validate_doi(doi):
                    return doi
        
        return None
    
    def validate_doi(self, doi):
        """Basic validation for DOI format"""
        if not doi:
            return False
        
        # DOI should start with "10." and contain a "/"
        if not (doi.startswith('10.') and '/' in doi):
            return False
        
        # Should not be too short or too long
        if len(doi) < 7 or len(doi) > 200:
            return False
        
        # Should not contain spaces or other invalid characters
        if re.search(r'\s', doi):
            return False
        
        return True
    
    def extract_abstract(self, text):
        """Extract abstract from the paper text"""
        # Look for abstract section
        abstract_patterns = [
            r'ABSTRACT\s*\n\s*([^A-Z\n]{50,1000})',
            r'Abstract\s*\n\s*([^A-Z\n]{50,1000})',
            r'abstract\s*\n\s*([^A-Z\n]{50,1000})',
            r'Abstract[:\-\s]*([^A-Z\n]{50,1000})'
        ]
        
        for pattern in abstract_patterns:
            match = re.search(pattern, text[:2000], re.IGNORECASE | re.DOTALL)
            if match:
                abstract = match.group(1).strip()
                # Clean up the abstract
                abstract = re.sub(r'\s+', ' ', abstract)
                return abstract
        
        return None
    
    def extract_keywords(self, text):
        """Extract keywords from the paper text"""
        keyword_patterns = [
            r'Keywords?[:\-\s]*([^\n]{10,200})',
            r'Key words?[:\-\s]*([^\n]{10,200})',
            r'Index terms?[:\-\s]*([^\n]{10,200})'
        ]
        
        search_text = text[:3000]
        
        for pattern in keyword_patterns:
            match = re.search(pattern, search_text, re.IGNORECASE)
            if match:
                keywords_text = match.group(1).strip()
                # Split by common separators
                keywords = re.split(r'[,;·•]', keywords_text)
                cleaned_keywords = [
                    kw.strip() for kw in keywords 
                    if kw.strip() and len(kw.strip()) > 2
                ]
                return cleaned_keywords[:10]  # Limit to 10 keywords
        
        return []
    
    def parse_pdf_enhanced(self, pdf_path):
        """Enhanced PDF parsing with additional metadata extraction"""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            
            # Extract text from all pages
            for page in doc:
                text += page.get_text()
            
            page_count = len(doc)
            doc.close()
            
            # Extract all metadata
            metadata = {
                'title': self.extract_title_from_text(text),
                'authors': self.extract_authors_from_text(text),
                'doi': self.parse_doi(text),
                'abstract': self.extract_abstract(text),
                'keywords': self.extract_keywords(text),
                'text': text,
                'content': text[:2000],  # First 2000 chars for AI analysis
                'word_count': len(text.split()),
                'page_count': page_count
            }
            
            return metadata
            
        except Exception as e:
            return {'error': f"Failed to parse PDF: {str(e)}"}

# Example usage and testing
if __name__ == "__main__":
    parser = PaperParser()
    
    # Test DOI extraction with sample text
    test_text = """
    This is a sample paper title
    John Doe, Jane Smith
    
    Abstract: This paper presents a novel approach to...
    
    DOI: 10.1234/example.2024.001
    Keywords: machine learning, natural language processing, AI
    """
    
    print("Testing DOI extraction:")
    print(f"DOI: {parser.parse_doi(test_text)}")
    print(f"Abstract: {parser.extract_abstract(test_text)}")
    print(f"Keywords: {parser.extract_keywords(test_text)}")
    
    # Test async DOI parsing
    async def test_async():
        result = await parser.parse_doi("10.1234/example.2024.001")
        print(f"Async DOI result: {result}")
    
    # Uncomment to test async functionality
    # asyncio.run(test_async())