from abc import ABC, abstractmethod
from typing import Dict, Any, List

class NLUEngine(ABC):
    """Base class for Natural Language Understanding (NLU) components."""
    
    @abstractmethod
    def parse(self, text: str) -> Dict[str, Any]:
        """
        Parse user input to extract intent and entities.
        
        Args:
            text (str): The input text to parse
            
        Returns:
            Dict containing:
                - intent: The identified intent
                - confidence: Confidence score
                - entities: List of extracted entities
                - original_text: The original input text
        """
        pass
    
    @abstractmethod
    def train(self, training_data: List[Dict[str, Any]]) -> None:
        """
        Train the NLU model with provided training data.
        
        Args:
            training_data: List of training examples with intents and entities
        """
        pass 