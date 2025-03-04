from typing import Dict, Any, Optional
from chatbot_framework.nlu.transformer_nlu import TransformerNLU
from chatbot_framework.nlg.template_nlg import TemplateNLG
from chatbot_framework.dialog.manager import DialogManager

class Chatbot:
    """Main chatbot class that can be integrated into any front-end."""
    
    def __init__(self, training_data: Optional[list] = None, templates: Optional[dict] = None):
        """
        Initialize the chatbot with optional training data and templates.
        
        Args:
            training_data: List of dicts with 'text' and 'intent' keys
            templates: Dictionary mapping intents to response templates
        """
        # Initialize components
        self.nlu = TransformerNLU()
        self.nlg = TemplateNLG()
        self.dialog_manager = DialogManager(self.nlu, self.nlg)
        
        # Train and configure if data is provided
        if training_data:
            self.nlu.train(training_data)
        if templates:
            self.nlg.load_templates(templates)
    
    async def process_message(self, message: str) -> Dict[str, Any]:
        """
        Process a user message and return the response.
        
        Args:
            message: The user's input message
            
        Returns:
            Dict containing:
                - response: The chatbot's response
                - intent: The detected intent
                - confidence: Confidence score
                - entities: Extracted entities
        """
        # Process the message
        nlu_result = self.nlu.parse(message)
        
        # Generate response
        response = self.nlg.generate_response(
            intent=nlu_result['intent'],
            entities=nlu_result.get('entities', {}),
            context=self.dialog_manager.get_context()
        )
        
        # Update dialog context
        self.dialog_manager.process_message(message)
        
        return {
            'response': response,
            'intent': nlu_result['intent'],
            'confidence': nlu_result['confidence'],
            'entities': nlu_result['entities']
        }
    
    def reset_conversation(self) -> None:
        """Reset the conversation context."""
        self.dialog_manager.reset_context()

# Example usage:
"""
from chatbot_framework import Chatbot

# Initialize with training data and templates
chatbot = Chatbot(
    training_data=[
        {"text": "Hello", "intent": "greeting"},
        {"text": "Hi there", "intent": "greeting"},
        # ... more training data
    ],
    templates={
        "greeting": [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?"
        ],
        # ... more templates
    }
)

# In an async context:
async def handle_message(message):
    result = await chatbot.process_message(message)
    return result['response']
""" 

print(Chatbot.__init__)