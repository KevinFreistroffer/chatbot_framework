from typing import Dict, Any, Optional
from chatbot_framework.nlu.base import NLUEngine
from chatbot_framework.nlg.base import NLGEngine

class DialogManager:
    """Manages the conversation flow between user and chatbot."""
    
    def __init__(self, nlu_engine: NLUEngine, nlg_engine: NLGEngine):
        self.nlu_engine = nlu_engine
        self.nlg_engine = nlg_engine
        self.context: Dict[str, Any] = {}
        self.conversation_history = []
        
    def process_message(self, message: str) -> str:
        """
        Process an incoming message and generate a response.
        
        Args:
            message (str): The incoming user message
            
        Returns:
            str: The generated response
        """
        print(f"Processing message: {message}")
        # Parse the user input
        nlu_result = self.nlu_engine.parse(message)
        
        # Update conversation context
        self._update_context(nlu_result)
        
        # Generate response
        response = self.nlg_engine.generate_response(
            intent=nlu_result['intent'],
            entities=nlu_result.get('entities', {}),
            context=self.context
        )
        
        # Store in conversation history
        self.conversation_history.append({
            'user': message,
            'bot': response,
            'nlu_result': nlu_result
        })
        
        return response
    
    def _update_context(self, nlu_result: Dict[str, Any]) -> None:
        """Update the conversation context with new information."""
        self.context.update({
            'last_intent': nlu_result['intent'],
            'last_entities': nlu_result.get('entities', {}),
            'turn_count': len(self.conversation_history) + 1
        })
    
    def get_context(self) -> Dict[str, Any]:
        """Get the current conversation context."""
        return self.context
    
    def reset_context(self) -> None:
        """Reset the conversation context."""
        self.context = {}
        self.conversation_history = [] 