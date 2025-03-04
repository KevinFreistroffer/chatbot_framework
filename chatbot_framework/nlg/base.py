from abc import ABC, abstractmethod
from typing import Dict, Any

class NLGEngine(ABC):
    """Base class for Natural Language Generation (NLG) components."""
    
    @abstractmethod
    def generate_response(self, intent: str, entities: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        Generate a natural language response based on the intent and entities.
        
        Args:
            intent (str): The intent to respond to
            entities (Dict[str, Any]): Extracted entities to use in response
            context (Dict[str, Any]): Current conversation context
            
        Returns:
            str: Generated response text
        """
        pass
    
    @abstractmethod
    def load_templates(self, templates: Dict[str, Any]) -> None:
        """
        Load response templates for different intents.
        
        Args:
            templates: Dictionary mapping intents to response templates
        """
        pass 