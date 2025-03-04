from typing import Dict, Any
from .base import NLGEngine
import random
import re

class TemplateNLG(NLGEngine):
    """Template-based Natural Language Generation engine."""
    
    def __init__(self):
        self.templates: Dict[str, list] = {}
        self.fallback_responses = [
            "I'm not sure how to respond to that.",
            "Could you rephrase that?",
            "I don't have a response template for this scenario."
        ]
    
    def load_templates(self, templates: Dict[str, Any]) -> None:
        """
        Load response templates for different intents.
        
        Args:
            templates: Dictionary mapping intents to lists of response templates
        """
        self.templates = templates
    
    def generate_response(self, intent: str, entities: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate a response based on intent and entities."""
        print("_generate_response intent: ", intent)
        print("_generate_response entities: ", entities)
        print("_generate_response context: ", context)
        if intent not in self.templates:
            return random.choice(self.fallback_responses)
        
        # Get a random template for this intent
        template = random.choice(self.templates[intent])
        
        # Replace entity placeholders
        response = self._fill_template(template, entities, context)
        
        return response
    
    def _fill_template(self, template: str, entities: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Fill in a template with entity values and context information."""
        print("_fill_template entities: ", entities)
        # Replace entity placeholders
        for entity_name, entity_info in entities.items():
            if isinstance(entity_info, dict) and 'value' in entity_info:
                value = entity_info['value']
            else:
                value = str(entity_info)
            template = template.replace(f"{{{entity_name}}}", value)
        
        # Replace context variables
        for context_key, context_value in context.items():
            template = template.replace(f"{{context.{context_key}}}", str(context_value))
        
        # Remove any unfilled placeholders
        template = re.sub(r'\{[^}]+\}', '', template)
        
        return template.strip() 