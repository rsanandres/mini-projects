from typing import List, Dict
from collections import Counter
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class TrendAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
    def extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text."""
        # Remove special characters and convert to lowercase
        text = re.sub(r'[^\w\s]', '', text.lower())
        # Split into words and remove common words
        words = text.split()
        return [word for word in words if len(word) > 3]
    
    def analyze_trends(self, trends: List[Dict]) -> Dict:
        """Analyze trends and extract patterns."""
        # Extract all titles
        titles = [trend['title'] for trend in trends]
        
        # Get keyword frequencies
        all_keywords = []
        for title in titles:
            all_keywords.extend(self.extract_keywords(title))
        
        keyword_freq = Counter(all_keywords)
        
        # Get TF-IDF features
        tfidf_matrix = self.vectorizer.fit_transform(titles)
        feature_names = self.vectorizer.get_feature_names_out()
        
        # Get top keywords by TF-IDF
        top_keywords = []
        for i in range(len(titles)):
            tfidf_scores = tfidf_matrix[i].toarray()[0]
            top_indices = np.argsort(tfidf_scores)[-5:]  # Get top 5 keywords
            top_keywords.extend([feature_names[idx] for idx in top_indices])
        
        # Analyze model types
        model_types = Counter()
        for trend in trends:
            if 'type' in trend:
                model_types[trend['type']] += 1
        
        return {
            'top_keywords': dict(keyword_freq.most_common(10)),
            'top_tfidf_keywords': list(set(top_keywords)),
            'model_types': dict(model_types),
            'total_trends': len(trends)
        }
    
    def get_trend_summary(self, trends: List[Dict]) -> Dict:
        """Generate a summary of the current AI trends."""
        analysis = self.analyze_trends(trends)
        
        return {
            'summary': {
                'total_trends_analyzed': analysis['total_trends'],
                'most_common_keywords': analysis['top_keywords'],
                'emerging_topics': analysis['top_tfidf_keywords'],
                'model_distribution': analysis['model_types']
            },
            'recommendations': self._generate_recommendations(analysis)
        }
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate recommendations based on trend analysis."""
        recommendations = []
        
        # Add recommendations based on keyword frequency
        for keyword, freq in analysis['top_keywords'].items():
            if freq > 5:  # If keyword appears more than 5 times
                recommendations.append(f"Consider implementing {keyword}-based solutions")
        
        # Add recommendations based on model types
        for model_type, count in analysis['model_types'].items():
            if count > 3:  # If model type appears more than 3 times
                recommendations.append(f"Focus on {model_type} implementations")
        
        return recommendations

if __name__ == "__main__":
    # Example usage
    analyzer = TrendAnalyzer()
    sample_trends = [
        {"title": "New advances in transformer models", "type": "research_paper"},
        {"title": "Efficient implementation of BERT", "type": "implementation"},
        {"title": "Latest developments in computer vision", "type": "research_paper"}
    ]
    
    summary = analyzer.get_trend_summary(sample_trends)
    print("Trend Summary:")
    print(summary) 