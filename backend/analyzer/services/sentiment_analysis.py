import torch
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import numpy as np

class SentimentAnalyzer:
    def __init__(self):
        # Switching to a more lightweight and multilingual model
        self.model_name = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
        self.labels = ['negative', 'neutral', 'positive']
        
        # Check if we should force fallback to avoid long loading times
        self.force_fallback = os.environ.get('USE_FAST_SENTIMENT', 'True') == 'True'
        
        if self.force_fallback:
            print("Fast Sentiment mode enabled. Using rule-based analyzer.")
            self.use_transformer = False
            return

        try:
            # Try to load, but ONLY if files are already local to avoid hangs
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, local_files_only=True)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name, local_files_only=True)
            self.use_transformer = True
        except Exception:
            print("Transformer files not found locally. Using rule-based fallback.")
            self.use_transformer = False

    def analyze(self, text):
        """Performs sentiment analysis on the text."""
        if not text or text.strip() == "":
            return 'neutral', 0.0

        if not self.use_transformer:
            return self._fallback_analyze(text)

        try:
            # Prepare inputs
            encoded_input = self.tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
            
            # Forward pass
            with torch.no_grad():
                output = self.model(**encoded_input)
            
            # Extract scores
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)
            
            # Get index of highest score
            ranking = np.argsort(scores)
            ranking = ranking[::-1]
            
            top_label = self.labels[ranking[0]]
            top_score = float(scores[ranking[0]])
            
            return top_label, top_score
            
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return self._fallback_analyze(text)

    def _fallback_analyze(self, text):
        """Rule-based sentiment fallback with multilingual support."""
        # Positive: supports, appreciates, agrees, useful
        positive_words = {
            'great', 'awesome', 'love', 'good', 'thanks', 'helpful', 'excellent', 'clear', 'best', 'nice', 'useful', 'agree', 'supported',
            'நல்லது', 'நன்று', 'அருமை', 'நன்றி', 'பயனுள்ளது', # Tamil
            'अच्छा', 'बढ़िया', 'धन्यवाद', 'शुक्रिया', 'मज़ा' # Hindi
        }
        # Negative: criticizes, disagrees, unhelpful
        negative_words = {
            'bad', 'worst', 'poor', 'confusing', 'fast', 'slow', 'boring', 'hate', 'waste', 'unhelpful', 'disagree', 'criticize', 'fail',
            'மோசம்', 'பிடிக்கவில்லை', 'தவறு', 'குறை', # Tamil
            'बुरा', 'खराब', 'गलत', 'बोर' # Hindi
        }
        
        words = set(text.lower().split())
        pos_count = len(words.intersection(positive_words))
        neg_count = len(words.intersection(negative_words))
        
        if pos_count > neg_count:
            return 'positive', 0.6
        elif neg_count > pos_count:
            return 'negative', 0.6
        else:
            return 'neutral', 0.5

    def calculate_weighted_sentiment(self, score, like_count, label):
        """
        weighted_sentiment = sentiment_score * log(like_count + 1)
        Positive: +score, Negative: -score, Neutral: 0
        """
        multiplier = 0
        if label == 'positive':
            multiplier = 1
        elif label == 'negative':
            multiplier = -1
            
        contribution = (multiplier * score) * np.log1p(like_count)
        return float(contribution)
