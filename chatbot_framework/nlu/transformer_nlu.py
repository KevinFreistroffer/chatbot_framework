from typing import Dict, Any, List
from .base import NLUEngine
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import numpy as np

class TransformerNLU(NLUEngine):
    """Implementation of NLU using transformer models."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Using a smaller, faster model by default
        self.model = SentenceTransformer(model_name)
        self.ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
        self.intent_examples = {}  # Intent name -> list of example embeddings
        self.intent_texts = {}     # Intent name -> list of example texts
        
    def train(self, training_data: List[Dict[str, Any]]) -> None:
        """
        Train the NLU model with provided training data.
        
        Args:
            training_data: List of dicts with 'text' and 'intent' keys
        """
        # Group examples by intent
        for example in training_data:
            intent = example['intent']
            text = example['text']
            if intent not in self.intent_texts:
                self.intent_texts[intent] = []
            self.intent_texts[intent].append(text)
        
        # Compute embeddings for each intent's examples
        for intent, texts in self.intent_texts.items():
            embeddings = self.model.encode(texts, convert_to_tensor=True)
            self.intent_examples[intent] = embeddings
    
    def parse(self, text: str) -> Dict[str, Any]:
        """Parse user input to extract intent and entities."""
        print(f"Parsing text: {text}")
        # Get text embedding
        text_embedding = self.model.encode(text, convert_to_tensor=True)
        # Find closest intent
        best_intent = None
        best_score = -1
        
        for intent, examples_embedding in self.intent_examples.items():
            # Compute cosine similarity with all examples
            similarities = util.pytorch_cos_sim(text_embedding, examples_embedding)[0]
            max_similarity = float(similarities.max())
            
            if max_similarity > best_score:
                best_score = max_similarity
                best_intent = intent
        
        # Extract entities
        entities = []
        try:
            ner_results = self.ner_pipeline(text)
            for ent in ner_results:
                entities.append({
                    'entity': ent['entity'],
                    'value': ent['word'],
                    'start': ent['start'],
                    'end': ent['end'],
                    'confidence': ent['score']
                })
        except Exception as e:
            print(f"Warning: NER processing failed: {e}")
        
        return {
            'intent': best_intent if best_intent else 'unknown',
            'confidence': best_score if best_score > 0 else 0.0,
            'entities': entities,
            'original_text': text
        }