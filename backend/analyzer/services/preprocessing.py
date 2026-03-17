import re
import emoji
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# For consistent language detection results
DetectorFactory.seed = 0

class TextPreprocessor:
    def __init__(self):
        # Basic emoji to sentiment word mapping as requested
        self.emoji_mapping = {
            '🔥': ' awesome ',
            '😍': ' love ',
            '👍': ' good ',
            '😡': ' angry ',
            '❤️': ' love ',
            '😂': ' funny ',
            '🙌': ' great ',
            '⭐': ' excellent ',
            '👏': ' bravo ',
            '✨': ' beautiful ',
            '✅': ' correct ',
            '❌': ' wrong ',
            '🤔': ' questionable ',
            '👎': ' bad ',
            '🙏': ' thankful ',
        }

    def clean_text(self, text):
        """Standardizes text: removes URLs, HTML, and normalizes emojis."""
        if not text:
            return ""

        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Convert specific emojis to sentiment words based on requirement
        for char, replacement in self.emoji_mapping.items():
            text = text.replace(char, replacement)
            
        # Convert remaining emojis to their textual descriptions
        text = emoji.demojize(text, delimiters=(" ", " "))
        text = text.replace("_", " ").replace(":", "")

        # Remove special characters except common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)
        
        # Lowercase and whitespace normalization
        text = text.lower().strip()
        text = re.sub(r'\s+', ' ', text)
        
        return text

    def detect_language(self, text):
        """Detects the language of the text."""
        try:
            if not text or len(text) < 3:
                return 'en'
            return detect(text)
        except LangDetectException:
            return 'en'

    def translate_to_english(self, text, source_lang):
        """
        Placeholder for translation using LibreTranslate or similar.
        In a real scenario, this would call an API or use a local model.
        For this implementation, we'll return the text as is if already English,
        or provide a 'placeholder' for where the translation logic would go.
        """
        if source_lang == 'en':
            return text
        
        # In a production environment with LibreTranslate:
        # url = "http://localhost:5000/translate"
        # res = requests.post(url, data={"q": text, "source": source_lang, "target": "en"})
        # return res.json()['translatedText']
        
        return text # Defaulting to original text for this demo implementation
