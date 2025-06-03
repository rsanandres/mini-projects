import unittest
from src.scraper.trend_scraper import TrendScraper
from src.analyzer.trend_analyzer import TrendAnalyzer
from src.models.basic_models import ModelFactory

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.scraper = TrendScraper()
        self.analyzer = TrendAnalyzer()
        self.model_factory = ModelFactory()
    
    def test_trend_analysis_pipeline(self):
        # Get trends
        trends = self.scraper.get_all_trends()
        self.assertIsInstance(trends, list)
        
        # Analyze trends
        analysis = self.analyzer.get_trend_summary(trends)
        self.assertIn('summary', analysis)
        self.assertIn('recommendations', analysis)
    
    def test_model_implementation(self):
        # Get available models
        models = self.model_factory.get_available_models()
        self.assertIsInstance(models, list)
        self.assertTrue(len(models) > 0)
        
        # Test creating a model
        text_classifier = self.model_factory.create_model('text_classifier')
        self.assertIsNotNone(text_classifier)
        
        image_classifier = self.model_factory.create_model('image_classifier')
        self.assertIsNotNone(image_classifier)

if __name__ == '__main__':
    unittest.main() 