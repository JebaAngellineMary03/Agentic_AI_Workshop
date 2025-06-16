import asyncio
import os
import json
import requests
import google.generativeai as genai
from dotenv import load_dotenv
from logic.rag_system import RAGSystem
from implementation.paper_parser import PaperParser
from parsing.nlp_detector import AIDetector

load_dotenv()

class GeminiResearchAgent:
    def __init__(self):
        # Initialize Gemini
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Initialize other components
        self.rag = RAGSystem()
        self.parser = PaperParser()
        self.ai_detector = AIDetector()
        
    async def fetch_scholar_metadata(self, title):
        """Fetch citation and author metadata using SerpAPI (Google Scholar)"""
        try:
            if not title or not isinstance(title, str):
                return {"status": "invalid_title"}
                
            params = {
                "engine": "google_scholar",
                "q": str(title).strip(),
                "api_key": "2b832ce5d6c917c07478b99498d34635404eef913d7e0cee5dd81612fff8380b"
            }
            response = requests.get("https://serpapi.com/search", params=params)
            data = response.json()
            
            if not data.get("organic_results"):
                return {"status": "not_found"}
                
            result = data["organic_results"][0]  # First paper result
            
            # Safely extract authors and ensure they're strings
            pub_info = result.get("publication_info", {})
            authors_raw = pub_info.get("authors", [])
            
            # Handle different author formats
            authors = []
            if isinstance(authors_raw, list):
                authors = [str(author) for author in authors_raw if author]
            elif isinstance(authors_raw, str):
                authors = [authors_raw]
            elif isinstance(authors_raw, dict):
                authors = [str(authors_raw)]
            
            return {
                "title": str(result.get("title", "")),
                "authors": authors,
                "citation_count": int(result.get("inline_links", {}).get("cited_by", {}).get("total", 0)),
                "link": str(result.get("link", "")),
                "year": str(result.get("publication_info", {}).get("year", "")),
                "status": "success"
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
        
    async def process_submission(self, submission_data):
        """Main agent workflow with Gemini intelligence"""
        results = {
            "paper_info": {},
            "authorship": {},
            "ai_detection": {},
            "scholar_metadata": {},
            "quality_score": 0,
            "similar_papers": [],
            "recommendations": [],
            "flags": [],
            "gemini_analysis": {}
        }
        
        try:
            # Step 1: Parse paper - FIXED: Remove await from non-async method
            if submission_data.get('doi'):
                # Note: parser.parse_doi should be an async method if you want to await it
                # For now, making it synchronous
                paper_data = self.parser.parse_doi_sync(submission_data['doi'])  # Changed method name
            else:
                paper_data = {
                    'title': str(submission_data.get('title', 'Unknown Title')),
                    'authors': submission_data.get('authors', []),
                    'content': str(submission_data.get('content', 'Manual submission - limited analysis'))
                }
            
            # Ensure paper_data has proper structure
            if not isinstance(paper_data, dict):
                paper_data = {'title': 'Unknown', 'authors': [], 'content': ''}
            
            # Ensure authors is always a list of strings
            authors = paper_data.get('authors', [])
            if not isinstance(authors, list):
                authors = [str(authors)] if authors else []
            paper_data['authors'] = [str(author) for author in authors if author]
            
            results["paper_info"] = paper_data
            
            # Step 1.5: Fetch Google Scholar metadata
            if paper_data.get('title'):
                scholar_data = await self.fetch_scholar_metadata(paper_data['title'])
                results["scholar_metadata"] = scholar_data
                
                # Update paper data with scholar information if found
                if scholar_data.get('status') == 'success':
                    # Compare and merge author information
                    if scholar_data.get('authors') and not paper_data.get('authors'):
                        paper_data['authors'] = scholar_data['authors']
                    
                    # Add citation metrics
                    paper_data['citation_count'] = scholar_data.get('citation_count', 0)
                    paper_data['publication_year'] = scholar_data.get('year')
                    paper_data['scholar_link'] = scholar_data.get('link')
                    
                    # Flag for high-impact papers
                    if scholar_data.get('citation_count', 0) > 100:
                        results["flags"].append("High-impact paper detected (100+ citations)")
                    elif scholar_data.get('citation_count', 0) > 50:
                        results["flags"].append("Well-cited paper (50+ citations)")
            
            # Step 2: Enhanced authorship verification with Scholar data
            authorship_result = await self.verify_authorship_with_gemini(
                paper_data.get('authors', []), 
                submission_data.get('claimed_author'),
                paper_data.get('title', ''),
                results.get('scholar_metadata', {})
            )
            results["authorship"] = authorship_result
            
            # Step 3: Enhanced AI Detection with Gemini
            if paper_data.get('content'):
                # Local AI detection - FIXED: Remove await from synchronous method
                local_ai_result = self.ai_detector.analyze_text(paper_data['content'])
                
                # Gemini AI detection
                gemini_ai_result = await self.gemini_ai_detection(paper_data['content'])
                
                # Combine results
                combined_ai_prob = (local_ai_result['ai_probability'] + gemini_ai_result['ai_probability']) / 2
                
                results["ai_detection"] = {
                    "ai_probability": combined_ai_prob,
                    "local_analysis": local_ai_result,
                    "gemini_analysis": gemini_ai_result,
                    "confidence": 0.9
                }
                
                if combined_ai_prob > 0.7:
                    results["flags"].append("High probability of AI-generated content (Multi-model detection)")
            
            # Step 4: RAG - Find similar papers - FIXED: Remove await from synchronous method
            if paper_data.get('title'):
                similar_papers = self.rag.search_similar_papers(paper_data['title'])
                results["similar_papers"] = similar_papers
                
                # Gemini analysis of similar papers
                if similar_papers:
                    similarity_analysis = await self.analyze_similarity_with_gemini(
                        paper_data, similar_papers
                    )
                    results["gemini_analysis"]["similarity"] = similarity_analysis
            
            # Step 5: Gemini Quality Assessment (now includes scholar metrics)
            quality_analysis = await self.gemini_quality_assessment(paper_data, results)
            results["gemini_analysis"]["quality"] = quality_analysis
            
            # Step 6: Calculate enhanced quality score (now includes citation metrics)
            quality_score = await self.calculate_enhanced_quality_score(paper_data, results)
            results["quality_score"] = quality_score
            
            # Step 7: Generate intelligent recommendations
            recommendations = await self.generate_intelligent_recommendations(results)
            results["recommendations"] = recommendations
            
        except Exception as e:
            results["error"] = str(e)
            results["flags"].append(f"Processing error: {str(e)}")
        
        return results
    
    async def verify_authorship_with_gemini(self, authors, claimed_author, title, scholar_metadata=None):
        """Enhanced authorship verification using Gemini with Scholar data"""
        if not claimed_author or not authors:
            return {"status": "insufficient_data", "confidence": 0}
        
        # Basic name matching with type safety
        author_match = False
        position = -1
        
        # Ensure authors is a list and handle different data types
        if isinstance(authors, dict):
            authors = [str(authors)]  # Convert dict to string in list
        elif not isinstance(authors, list):
            authors = [str(authors)] if authors else []
        
        for i, author in enumerate(authors):
            # Ensure both claimed_author and author are strings
            author_str = str(author) if author is not None else ""
            claimed_author_str = str(claimed_author) if claimed_author is not None else ""
            
            if (claimed_author_str.lower() in author_str.lower() or 
                author_str.lower() in claimed_author_str.lower()):
                author_match = True
                position = i
                break
        
        # Check against Scholar metadata if available
        scholar_authors = scholar_metadata.get('authors', []) if scholar_metadata else []
        scholar_match = False
        
        # Ensure scholar_authors is a list and handle different data types
        if isinstance(scholar_authors, dict):
            scholar_authors = [str(scholar_authors)]
        elif not isinstance(scholar_authors, list):
            scholar_authors = [str(scholar_authors)] if scholar_authors else []
        
        if scholar_authors:
            claimed_author_str = str(claimed_author) if claimed_author is not None else ""
            for author in scholar_authors:
                author_str = str(author) if author is not None else ""
                if (claimed_author_str.lower() in author_str.lower() or 
                    author_str.lower() in claimed_author_str.lower()):
                    scholar_match = True
                    break
        
        # Gemini analysis for name variations with Scholar context
        scholar_context = f"Google Scholar authors: {scholar_authors}" if scholar_authors else "No Scholar data available"
        
        prompt = f"""
        Analyze if "{claimed_author}" could be the same person as any of these authors: {authors}
        Consider name variations, nicknames, cultural naming conventions, and author order significance.
        Title: {title}
        {scholar_context}
        
        Respond with JSON:
        {{
            "is_match": true/false,
            "confidence": 0.0-1.0,
            "reasoning": "explanation",
            "author_position_significance": "first/middle/last author implications",
            "scholar_consistency": "consistent/inconsistent/unknown"
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            gemini_result = json.loads(response.text.strip())
            
            # Enhanced confidence calculation with Scholar data
            base_confidence = 0.8 if author_match else 0.1
            scholar_bonus = 0.1 if scholar_match else 0
            gemini_confidence = gemini_result.get('confidence', 0)
            
            final_confidence = (base_confidence * 0.4 + gemini_confidence * 0.5 + scholar_bonus * 0.1)
            
            return {
                "status": "verified" if (author_match or scholar_match or gemini_result.get('is_match')) else "not_found",
                "position": position,
                "confidence": final_confidence,
                "total_authors": len(authors),
                "scholar_match": scholar_match,
                "gemini_reasoning": gemini_result.get('reasoning', ''),
                "position_significance": gemini_result.get('author_position_significance', ''),
                "scholar_consistency": gemini_result.get('scholar_consistency', 'unknown')
            }
        except:
            # Fallback to basic analysis
            confidence = 0.8 if (author_match or scholar_match) else 0.1
            return {
                "status": "verified" if (author_match or scholar_match) else "not_found",
                "position": position,
                "confidence": confidence,
                "total_authors": len(authors),
                "scholar_match": scholar_match
            }
    
    async def gemini_ai_detection(self, text):
        """Gemini-powered AI content detection"""
        prompt = f"""
        Analyze this text for AI-generated content indicators:
        
        TEXT: {text[:2000]}  # Limit for token efficiency
        
        Look for:
        1. Repetitive phrase patterns
        2. Overly formal or generic language
        3. Lack of personal insights or specific examples
        4. Consistent sentence structures
        5. Generic transitional phrases
        
        Respond with JSON:
        {{
            "ai_probability": 0.0-1.0,
            "indicators": ["list of specific indicators found"],
            "human_elements": ["list of human-like elements"],
            "confidence": 0.0-1.0
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text.strip())
            return result
        except:
            return {"ai_probability": 0.5, "confidence": 0.3, "error": "Gemini analysis failed"}
    
    async def analyze_similarity_with_gemini(self, paper_data, similar_papers):
        """Analyze paper similarity using Gemini"""
        prompt = f"""
        Analyze potential plagiarism or excessive similarity:
        
        SUBMITTED PAPER:
        Title: {paper_data.get('title', '')}
        Authors: {paper_data.get('authors', [])}
        Citation Count: {paper_data.get('citation_count', 'Unknown')}
        
        SIMILAR PAPERS FOUND:
        {json.dumps(similar_papers[:3], indent=2)}
        
        Assess:
        1. Risk of plagiarism
        2. Legitimate research in same field vs copying
        3. Author overlap significance
        4. Citation impact considerations
        
        Respond with JSON:
        {{
            "plagiarism_risk": "low/medium/high",
            "analysis": "detailed explanation",
            "recommendations": ["action items for mentor"],
            "citation_context": "how citation metrics affect assessment"
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text.strip())
        except:
            return {"plagiarism_risk": "unknown", "analysis": "Analysis failed"}
    
    async def gemini_quality_assessment(self, paper_data, results):
        """Overall quality assessment using Gemini with Scholar metrics"""
        scholar_data = results.get('scholar_metadata', {})
        citation_count = paper_data.get('citation_count', 0)
        
        prompt = f"""
        Assess research paper quality for academic submission:
        
        PAPER: {json.dumps(paper_data, indent=2)}
        SCHOLAR METRICS: Citations: {citation_count}, Year: {paper_data.get('publication_year', 'Unknown')}
        ANALYSIS: {json.dumps({k: v for k, v in results.items() if k != 'gemini_analysis'}, indent=2)}
        
        Evaluate:
        1. Academic rigor
        2. Originality
        3. Methodology soundness
        4. Writing quality
        5. Research contribution
        6. Citation impact and relevance
        
        Respond with JSON:
        {{
            "overall_score": 0-100,
            "strengths": ["list strengths"],
            "weaknesses": ["list weaknesses"],
            "academic_level": "undergraduate/graduate/professional",
            "citation_assessment": "impact of citation metrics on quality"
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text.strip())
        except:
            return {"overall_score": 50, "academic_level": "unknown"}
    
    async def calculate_enhanced_quality_score(self, paper_data, analysis_results):
        """Enhanced quality scoring with Gemini insights and citation metrics"""
        base_score = 50
        
        # Authorship verification
        if analysis_results.get('authorship', {}).get('status') == 'verified':
            base_score += 20
        
        # AI detection penalty
        ai_prob = analysis_results.get('ai_detection', {}).get('ai_probability', 0)
        base_score -= int(ai_prob * 35)
        
        # Similar papers analysis
        similar_count = len(analysis_results.get('similar_papers', []))
        base_score += min(similar_count * 3, 15)
        
        # Citation impact bonus
        citation_count = paper_data.get('citation_count', 0)
        if citation_count > 100:
            base_score += 15  # High-impact paper
        elif citation_count > 50:
            base_score += 10  # Well-cited paper
        elif citation_count > 10:
            base_score += 5   # Moderately cited
        
        # Scholar metadata availability bonus
        if analysis_results.get('scholar_metadata', {}).get('status') == 'success':
            base_score += 5
        
        # Gemini quality bonus
        gemini_quality = analysis_results.get('gemini_analysis', {}).get('quality', {})
        if gemini_quality.get('overall_score'):
            gemini_score = gemini_quality['overall_score']
            base_score = int(base_score * 0.6 + gemini_score * 0.4)
        
        return max(0, min(100, base_score))
    
    async def generate_intelligent_recommendations(self, results):
        """Generate intelligent recommendations using Gemini with Scholar context"""
        prompt = f"""
        Generate mentor recommendations for research paper submission:
        
        ANALYSIS RESULTS: {json.dumps(results, indent=2)}
        
        Provide actionable recommendations for:
        1. Immediate actions needed
        2. Areas requiring investigation
        3. Student guidance points
        4. Approval/rejection recommendation
        5. Citation and impact considerations
        
        Format as mentor-friendly bullet points with emoji indicators.
        Use ✅ for good, ⚠️ for caution, ❌ for problems, 🔍 for investigate, 📈 for citations.
        """
        
        try:
            response = self.model.generate_content(prompt)
            recommendations = response.text.strip().split('\n')
            return [rec.strip() for rec in recommendations if rec.strip()]
        except:
            # Fallback recommendations
            return self.generate_fallback_recommendations(results)
    
    def generate_fallback_recommendations(self, results):
        """Fallback recommendations if Gemini fails"""
        recommendations = []
        
        quality_score = results.get('quality_score', 0)
        ai_prob = results.get('ai_detection', {}).get('ai_probability', 0)
        authorship_status = results.get('authorship', {}).get('status')
        citation_count = results.get('paper_info', {}).get('citation_count', 0)
        
        if quality_score >= 80:
            recommendations.append("✅ High quality submission - recommend approval")
        elif quality_score >= 60:
            recommendations.append("⚠️ Moderate quality - detailed review required")
        else:
            recommendations.append("❌ Low quality - needs significant improvement")
        
        if ai_prob > 0.7:
            recommendations.append("🔍 High AI detection - interview student about methodology")
        elif ai_prob > 0.4:
            recommendations.append("⚠️ Moderate AI detection - verify key sections with student")
        
        if authorship_status != 'verified':
            recommendations.append("🔍 Authorship unverified - confirm student contribution")
        
        # Citation-based recommendations
        if citation_count > 100:
            recommendations.append("📈 High-impact paper - verify student's actual contribution")
        elif citation_count > 50:
            recommendations.append("📈 Well-cited work - excellent choice for submission")
        elif citation_count == 0:
            recommendations.append("📈 No citations found - may be very recent or unpublished work")
        
        return recommendations
    
    async def process_pdf(self, file_path, claimed_author):
        """Process uploaded PDF with enhanced analysis"""
        paper_data = self.parser.parse_pdf_enhanced(file_path)

    # ⚠️ Detect parsing error
        if 'error' in paper_data:
            raise ValueError(paper_data['error'])

        submission_data = {
        'title': paper_data.get('title'),
        'authors': paper_data.get('authors', []),
        'claimed_author': claimed_author,
        'content': paper_data.get('text', '')
    }

        return await self.process_submission(submission_data)