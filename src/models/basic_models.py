import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
import numpy as np
from typing import List, Dict, Any

class SimpleTextClassifier(nn.Module):
    """A simple text classification model using BERT."""
    def __init__(self, num_labels: int = 2):
        super().__init__()
        self.bert = AutoModel.from_pretrained('bert-base-uncased')
        self.classifier = nn.Linear(768, num_labels)
        
    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs.pooler_output
        return self.classifier(pooled_output)

class SimpleImageClassifier(nn.Module):
    """A simple CNN for image classification."""
    def __init__(self, num_classes: int = 10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.classifier = nn.Sequential(
            nn.Linear(128 * 8 * 8, 512),
            nn.ReLU(inplace=True),
            nn.Linear(512, num_classes)
        )
        
    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

class ModelFactory:
    """Factory class to create and manage different model implementations."""
    
    @staticmethod
    def create_model(model_type: str, **kwargs) -> Any:
        """Create a model instance based on the type."""
        if model_type == "text_classifier":
            return SimpleTextClassifier(**kwargs)
        elif model_type == "image_classifier":
            return SimpleImageClassifier(**kwargs)
        else:
            raise ValueError(f"Unknown model type: {model_type}")

    @staticmethod
    def get_available_models() -> List[Dict]:
        """Get list of available model implementations."""
        return [
            {
                "name": "SimpleTextClassifier",
                "type": "text_classifier",
                "description": "Basic text classification using BERT",
                "capabilities": ["text classification", "sentiment analysis"]
            },
            {
                "name": "SimpleImageClassifier",
                "type": "image_classifier",
                "description": "Basic CNN for image classification",
                "capabilities": ["image classification", "object detection"]
            }
        ]

if __name__ == "__main__":
    # Example usage
    factory = ModelFactory()
    print("Available models:")
    for model in factory.get_available_models():
        print(f"- {model['name']}: {model['description']}") 