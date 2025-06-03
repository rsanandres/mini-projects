from fastapi import APIRouter, HTTPException
from typing import List, Dict
from pydantic import BaseModel
from ..scraper.trend_scraper import TrendScraper
from ..analyzer.trend_analyzer import TrendAnalyzer
from ..models.basic_models import ModelFactory

router = APIRouter()

class TrendResponse(BaseModel):
    trends: List[Dict]
    summary: Dict
    recommendations: List[str]

class ModelResponse(BaseModel):
    name: str
    type: str
    description: str
    capabilities: List[str]

@router.get("/trends", response_model=TrendResponse)
async def get_trends():
    """Get current AI trends and analysis."""
    try:
        scraper = TrendScraper()
        analyzer = TrendAnalyzer()
        
        # Get trends
        trends = scraper.get_all_trends()
        
        # Analyze trends
        analysis = analyzer.get_trend_summary(trends)
        
        return {
            "trends": trends,
            "summary": analysis['summary'],
            "recommendations": analysis['recommendations']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models", response_model=List[ModelResponse])
async def get_models():
    """Get available model implementations."""
    try:
        factory = ModelFactory()
        return factory.get_available_models()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/{model_type}")
async def get_model_details(model_type: str):
    """Get details about a specific model type."""
    try:
        factory = ModelFactory()
        models = factory.get_available_models()
        
        for model in models:
            if model['type'] == model_type:
                return model
                
        raise HTTPException(status_code=404, detail=f"Model type {model_type} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Example usage
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router, prefix="/api/v1") 