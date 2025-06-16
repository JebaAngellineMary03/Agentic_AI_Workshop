import chromadb
from sentence_transformers import SentenceTransformer
import json
import requests
from bs4 import BeautifulSoup
import time

class RAGSystem:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(
            name="research_papers",
            metadata={"hnsw:space": "cosine"}
        )
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.initialize_sample_data()
    
    def initialize_sample_data(self):
        """Add comprehensive sample papers to the database"""
        sample_papers = [
            {
                "title": "Deep Learning for Natural Language Processing: A Comprehensive Survey",
                "authors": ["John Smith", "Jane Doe", "Alice Johnson"],
                "abstract": "This paper presents a comprehensive survey of deep learning techniques applied to natural language processing tasks. We review recent advances in transformer architectures, attention mechanisms, and their applications to machine translation, sentiment analysis, and question answering systems.",
                "venue": "ACL 2023",
                "citations": 145,
                "keywords": ["deep learning", "NLP", "transformers", "attention"],
                "year": 2023
            },
            {
                "title": "Machine Learning Applications in Healthcare: Challenges and Opportunities",
                "authors": ["Dr. Sarah Wilson", "Prof. Michael Chen", "Dr. Lisa Rodriguez"],
                "abstract": "We explore the current state of machine learning applications in healthcare, focusing on medical diagnosis, drug discovery, and personalized treatment. This review identifies key challenges including data privacy, model interpretability, and regulatory compliance.",
                "venue": "Nature Medicine 2023",
                "citations": 267,
                "keywords": ["machine learning", "healthcare", "medical diagnosis", "AI ethics"],
                "year": 2023
            },
            {
                "title": "Computer Vision for Autonomous Vehicles: A Deep Learning Approach",
                "authors": ["Carol Brown", "David Lee", "Emma Thompson"],
                "abstract": "This work addresses fundamental challenges in computer vision for autonomous vehicles, including object detection, lane recognition, and depth estimation. We propose novel deep learning architectures that achieve state-of-the-art performance on standard benchmarks.",
                "venue": "CVPR 2023",
                "citations": 189,
                "keywords": ["computer vision", "autonomous vehicles", "deep learning", "object detection"],
                "year": 2023
            },
            {
                "title": "Blockchain Technology in Supply Chain Management: A Systematic Review",
                "authors": ["Robert Kim", "Maria Garcia", "James Wilson"],
                "abstract": "This systematic review examines the application of blockchain technology in supply chain management. We analyze 150 research papers to identify trends, challenges, and future research directions in blockchain-based supply chain solutions.",
                "venue": "IEEE Transactions on Industrial Informatics 2023",
                "citations": 98,
                "keywords": ["blockchain", "supply chain", "distributed systems", "traceability"],
                "year": 2023
            },
            {
                "title": "Quantum Computing Algorithms for Optimization Problems",
                "authors": ["Dr. Alan Turing", "Prof. Grace Hopper"],
                "abstract": "We present novel quantum algorithms for solving complex optimization problems, demonstrating quantum advantage over classical approaches. Our theoretical analysis and experimental validation show significant speedup for specific problem classes.",
                "venue": "Nature Quantum Information 2023",
                "citations": 234,
                "keywords": ["quantum computing", "optimization", "quantum algorithms", "QAOA"],
                "year": 2023
            },
            {
                "title": "Sustainable AI: Energy-Efficient Deep Learning Models",
                "authors": ["Green AI Collective", "Prof. Eco Friendly"],
                "abstract": "This paper addresses the environmental impact of large-scale AI models by proposing energy-efficient architectures and training methodologies. We demonstrate significant reduction in carbon footprint while maintaining model performance.",
                "venue": "ICML 2023",
                "citations": 156,
                "keywords": ["sustainable AI", "energy efficiency", "green computing", "model compression"],
                "year": 2023
            }
        ]
        
        # Check if data already exists
        existing_count = self.collection.count()
        if existing_count < len(sample_papers):
            print(f"Initializing RAG database with {len(sample_papers)} sample papers...")
            for i, paper in enumerate(sample_papers):
                self.add_paper(paper, f"sample_{i}")
    
    def add_paper(self, paper_data, paper_id):
        """Add paper to vector database with enhanced metadata"""
        # Create comprehensive text content
        text_content = f"""
        Title: {paper_data['title']}
        Authors: {', '.join(paper_data.get('authors', []))}
        Abstract: {paper_data.get('abstract', '')}
        Keywords: {', '.join(paper_data.get('keywords', []))}
        Venue: {paper_data.get('venue', 'Unknown')}
        Year: {paper_data.get('year', 'Unknown')}
        """
        
        try:
            # Generate embedding
            embedding = self.embedder.encode([text_content])[0].tolist()
            
            # Convert lists to strings for ChromaDB compatibility
            metadata = {
                'title': paper_data.get('title', ''),
                'authors_str': ', '.join(paper_data.get('authors', [])),  # Convert list to string
                'abstract': paper_data.get('abstract', ''),
                'venue': paper_data.get('venue', 'Unknown'),
                'year': int(paper_data.get('year', 0)),
                'citations': int(paper_data.get('citations', 0)),
                'keywords_str': ', '.join(paper_data.get('keywords', [])),  # Convert list to string
                'id': paper_id,
                'indexed_at': time.time()
            }
            
            # Add additional fields if present
            if 'claimed_author' in paper_data:
                metadata['claimed_author'] = paper_data['claimed_author']
            if 'submission_type' in paper_data:
                metadata['submission_type'] = paper_data['submission_type']
            if 'file_path' in paper_data:
                metadata['file_path'] = paper_data['file_path']
            
            self.collection.add(
                documents=[text_content],
                embeddings=[embedding],
                metadatas=[metadata],
                ids=[paper_id]
            )
            print(f"Successfully added paper: {paper_data.get('title', 'Unknown')[:50]}...")
        except Exception as e:
            print(f"Error adding paper {paper_id}: {e}")
    
    def search_similar_papers(self, query, k=5, similarity_threshold=0.3):
        """Enhanced search for similar papers with filtering"""
        try:
            # Check if collection has any documents
            collection_count = self.collection.count()
            if collection_count == 0:
                print("Warning: No papers in database")
                return []
            
            # Ensure k doesn't exceed collection size
            k = min(k, collection_count)
            
            results = self.collection.query(
                query_texts=[query],
                n_results=k
            )
            
            similar_papers = []
            if results['documents'] and results['metadatas']:
                for i in range(len(results['documents'][0])):
                    metadata = results['metadatas'][0][i]
                    distance = results['distances'][0][i] if results.get('distances') else 0.5
                    similarity = 1 - distance
                    
                    # Filter by similarity threshold
                    if similarity >= similarity_threshold:
                        # Convert string back to list for compatibility
                        authors_list = metadata.get('authors_str', '').split(', ') if metadata.get('authors_str') else []
                        keywords_list = metadata.get('keywords_str', '').split(', ') if metadata.get('keywords_str') else []
                        
                        similar_papers.append({
                            'title': metadata.get('title', 'Unknown'),
                            'authors': authors_list,
                            'abstract': metadata.get('abstract', '')[:200] + '...' if len(metadata.get('abstract', '')) > 200 else metadata.get('abstract', ''),
                            'venue': metadata.get('venue', 'Unknown'),
                            'year': metadata.get('year', 'Unknown'),
                            'citations': metadata.get('citations', 0),
                            'keywords': keywords_list,
                            'similarity': round(similarity, 3)
                        })
            
            return similar_papers
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def search_by_author(self, author_name, k=10):
        """Search papers by author name"""
        try:
            # Get all documents and filter by author
            all_results = self.collection.get()
            author_papers = []
            
            if all_results['metadatas']:
                for metadata in all_results['metadatas']:
                    authors_str = metadata.get('authors_str', '')
                    if author_name.lower() in authors_str.lower():
                        # Convert back to list format
                        authors_list = authors_str.split(', ') if authors_str else []
                        metadata_copy = metadata.copy()
                        metadata_copy['authors'] = authors_list
                        author_papers.append(metadata_copy)
            
            return author_papers[:k]
        except Exception as e:
            print(f"Author search error: {e}")
            return []
    
    def get_citation_context(self, paper_title):
        """Get citation context for a paper"""
        similar_papers = self.search_similar_papers(paper_title, k=10)
        
        citation_analysis = {
            'total_similar_papers': len(similar_papers),
            'high_similarity_papers': len([p for p in similar_papers if p['similarity'] > 0.8]),
            'citation_range': {
                'min': min([p['citations'] for p in similar_papers]) if similar_papers else 0,
                'max': max([p['citations'] for p in similar_papers]) if similar_papers else 0,
                'avg': sum([p['citations'] for p in similar_papers]) / len(similar_papers) if similar_papers else 0
            },
            'common_venues': list(set([p['venue'] for p in similar_papers])),
            'research_activity': 'active' if len(similar_papers) > 3 else 'limited'
        }
        
        return citation_analysis
    
    def add_student_paper(self, title, authors, abstract="", claimed_author="", file_path=None):
        """Add a student submission to the database"""
        import hashlib
        
        # Generate unique ID for student paper
        paper_id = f"student_{hashlib.md5(f'{title}{claimed_author}'.encode()).hexdigest()[:8]}"
        
        paper_data = {
            'title': title,
            'authors': authors if isinstance(authors, list) else [authors],
            'abstract': abstract,
            'venue': 'Student Submission',
            'year': 2024,
            'citations': 0,
            'keywords': [],
            'claimed_author': claimed_author,
            'submission_type': 'student',
            'file_path': file_path
        }
        
        self.add_paper(paper_data, paper_id)
        return paper_id
    
    def get_database_stats(self):
        """Get statistics about the RAG database"""
        try:
            total_papers = self.collection.count()
            all_data = self.collection.get()
            
            if all_data['metadatas']:
                venues = [meta.get('venue', 'Unknown') for meta in all_data['metadatas']]
                years = [meta.get('year', 0) for meta in all_data['metadatas'] if isinstance(meta.get('year'), (int, float)) and meta.get('year') > 0]
                
                stats = {
                    'total_papers': total_papers,
                    'unique_venues': len(set(venues)),
                    'year_range': f"{min(years)} - {max(years)}" if years else "Unknown",
                    'sample_venues': list(set(venues))[:5]
                }
            else:
                stats = {'total_papers': total_papers}
            
            return stats
        except Exception as e:
            return {'error': str(e)}
    
    def clear_database(self):
        """Clear all data from the database (use with caution)"""
        try:
            self.client.delete_collection("research_papers")
            self.collection = self.client.create_collection("research_papers")
            print("Database cleared successfully")
        except Exception as e:
            print(f"Error clearing database: {e}")
    
    def rebuild_database(self):
        """Rebuild database with proper metadata format"""
        print("Rebuilding database with fixed metadata format...")
        self.clear_database()
        self.collection = self.client.get_or_create_collection(
            name="research_papers",
            metadata={"hnsw:space": "cosine"}
        )
        self.initialize_sample_data()
        print("Database rebuilt successfully!")