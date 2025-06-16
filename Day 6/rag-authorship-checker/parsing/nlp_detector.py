import re
from collections import Counter
import numpy as np

class AIDetector:
    def __init__(self):
        # Common AI-generated phrases and patterns
        self.ai_phrases = [
            "in conclusion", "it is important to note", "furthermore", "moreover",
            "in summary", "it should be noted", "in addition", "as a result",
            "on the other hand", "in other words", "for instance", "in particular",
            "delve into", "intricate", "multifaceted", "comprehensive", "nuanced"
        ]
        
        self.ai_patterns = [
            r'\bdelv[ei]ng?\b',
            r'\bintricate\b',
            r'\bmultifaceted\b',
            r'\bcomprehensive analysis\b',
            r'\bnuanced understanding\b'
        ]
    
    def analyze_text(self, text):
        """Main AI detection analysis"""
        if not text or len(text) < 100:
            return {"ai_probability": 0, "confidence": 0, "analysis": "Text too short"}
        
        # Multiple detection methods
        phrase_score = self.detect_ai_phrases(text)
        pattern_score = self.detect_ai_patterns(text)
        consistency_score = self.analyze_consistency(text)
        perplexity_score = self.simple_perplexity(text)
        
        # Weighted combination
        ai_probability = (
            phrase_score * 0.3 +
            pattern_score * 0.2 +
            consistency_score * 0.2 +
            perplexity_score * 0.3
        )
        
        return {
            "ai_probability": min(1.0, ai_probability),
            "confidence": 0.7,  # Simplified confidence
            "phrase_score": phrase_score,
            "pattern_score": pattern_score,
            "consistency_score": consistency_score,
            "analysis": self.generate_analysis(ai_probability)
        }
    
    def detect_ai_phrases(self, text):
        """Detect common AI-generated phrases"""
        text_lower = text.lower()
        phrase_count = 0
        
        for phrase in self.ai_phrases:
            phrase_count += text_lower.count(phrase)
        
        # Normalize by text length
        phrase_density = phrase_count / (len(text.split()) / 100)
        return min(1.0, phrase_density / 5)  # Normalize to 0-1
    
    def detect_ai_patterns(self, text):
        """Detect AI-specific patterns"""
        pattern_count = 0
        
        for pattern in self.ai_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            pattern_count += len(matches)
        
        pattern_density = pattern_count / (len(text.split()) / 100)
        return min(1.0, pattern_density / 3)
    
    def analyze_consistency(self, text):
        """Analyze writing style consistency"""
        sentences = re.split(r'[.!?]+', text)
        if len(sentences) < 5:
            return 0
        
        # Analyze sentence length variation
        lengths = [len(sentence.split()) for sentence in sentences if sentence.strip()]
        if not lengths:
            return 0
        
        # AI tends to have more consistent sentence lengths
        length_std = np.std(lengths)
        avg_length = np.mean(lengths)
        
        if avg_length == 0:
            return 0
        
        consistency = 1 - min(1.0, length_std / avg_length)
        return consistency * 0.5  # Moderate weight
    
    def simple_perplexity(self, text):
        """Simplified perplexity calculation"""
        words = text.lower().split()
        if len(words) < 10:
            return 0
        
        # Count word frequencies
        word_freq = Counter(words)
        total_words = len(words)
        
        # Calculate simple perplexity based on word repetition
        unique_words = len(word_freq)
        repetition_ratio = total_words / unique_words if unique_words > 0 else 1
        
        # AI text often has lower perplexity (more predictable)
        # Higher repetition = lower perplexity = higher AI probability
        perplexity_score = min(1.0, (repetition_ratio - 1) / 3)
        return perplexity_score
    
    def generate_analysis(self, ai_probability):
        """Generate human-readable analysis"""
        if ai_probability > 0.8:
            return "Very high likelihood of AI generation"
        elif ai_probability > 0.6:
            return "High likelihood of AI generation"
        elif ai_probability > 0.4:
            return "Moderate likelihood of AI generation"
        elif ai_probability > 0.2:
            return "Low likelihood of AI generation"
        else:
            return "Very low likelihood of AI generation"
