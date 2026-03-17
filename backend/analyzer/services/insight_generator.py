import re

class InsightGenerator:
    def __init__(self):
        self.question_patterns = [
            r'\?',
            # English Interrogatives
            r'\bwhat\b', r'\bwhy\b', r'\bwhen\b', r'\bwhere\b', r'\bwho\b', r'\bhow\b', r'\bwhich\b',
            # Tamil Interrogatives
            r'எது', r'எந்த', r'எப்படி', r'ஏன்', r'எப்போது', r'எங்கே', r'யார்',
            # Hindi Interrogatives (Devenagari)
            r'क्या', r'क्यों', r'कब', r'कहाँ', r'कौन', r'कैसे',
            # Question Patterns
            r'\bcan you\b', r'\bcould you\b', r'\bdo you\b', r'\bis it\b', r'\bare they\b', r'\bshall we\b', r'\bwould you\b'
        ]
        
        self.pain_point_patterns = {
            'too_fast': [r'too fast', r'fast', r'slow down', r'speed', r'hard to follow'],
            'confused': [r'confused', r'confusing', r'don\'t understand', r'hard to understand', r'not clear', r'explanation'],
            'audio_visual': [r'sound', r'audio', r'low', r'loud', r'mic', r'screen', r'blurry', r'cannot see'],
            'missing_info': [r'missing', r'showed', r'forgot', r'link', r'resource', r'github'],
            'long_intro': [r'get to the point', r'too long', r'intro', r'skip'],
        }

    def detect_questions(self, comment_text):
        """Returns True if the comment is likely a question based on intent."""
        text = comment_text.lower().strip()
        
        # 1. Direct Question Mark
        if '?' in text:
            return True
            
        # 2. Exclude common statement patterns (Rule: Not a question just because word is present)
        statement_patterns = [
            r"this is (why|how|what|where|when)",
            r"that['’]s (why|how|what|where|when)",
            r"that is (why|how|what|where|when)",
            r"i (know|understand|see) (how|why|what)",
            r"i (wonder|was wondering) (if|how|why)",
            r"reason (why|how|what)",
            r"the way (how|it)",
            r"explains (why|how|what)"
        ]
        
        for sp in statement_patterns:
            if re.search(sp, text):
                return False

        # 3. Check for Interrogative start or strong patterns
        # English start-of-sentence questions
        if re.match(r'^(what|why|when|where|who|how|which|can|could|do|does|is|are|shall|would|should|may|will)\b', text):
            return True
            
        # 4. Check all patterns (fallback for mid-sentence or other languages)
        for pattern in self.question_patterns:
            if re.search(pattern, text):
                return True
                
        return False

    def detect_pain_points(self, comments_list):
        """Analyzes a list of comments for recurring pain points."""
        detected_points = []
        counts = {key: 0 for key in self.pain_point_patterns.keys()}
        
        for comment in comments_list:
            text = comment.lower()
            for point, patterns in self.pain_point_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, text):
                        counts[point] += 1
                        break
        
        # Threshold for reporting a pain point (e.g., mention by > 2% of commenters or at least 3 people)
        threshold = max(3, len(comments_list) * 0.02)
        
        if counts['too_fast'] >= threshold:
            detected_points.append("Several viewers mentioned that the explanation was too fast.")
        if counts['confused'] >= threshold:
            detected_points.append("Some viewers expressed confusion about specific concepts.")
        if counts['audio_visual'] >= threshold:
            detected_points.append("A few viewers pointed out audio or visual quality issues.")
        if counts['missing_info'] >= threshold:
            detected_points.append("Viewers are asking for missing links or resources mentioned.")
            
        return detected_points

    def generate_recommendations(self, sentiment_dist, pain_points, question_count):
        """Generates high-level recommendations for the creator."""
        recommendations = []
        
        # Sentiment-based
        if sentiment_dist.get('positive', 0) > 70:
            recommendations.append("The audience loves this content! Consider making a follow-up or a 'Part 2'.")
        elif sentiment_dist.get('negative', 0) > 30:
            recommendations.append("There's significant negative sentiment. Address the core concerns in the comments or a pinned comment.")
            
        # Pain point-based
        for pt in pain_points:
            if "too fast" in pt:
                recommendations.append("Try slowing down your pacing or using more visual marks/captions in your next video.")
            if "confusion" in pt:
                recommendations.append("Consider creating a deep-dive short or pinned comment clarifying the complex parts.")
            if "audio" in pt or "visual" in pt:
                recommendations.append("Check your recording setup; multiple viewers noticed quality issues.")
                
        # Question-based
        if question_count > 10:
            recommendations.append(f"You have {question_count} unanswered questions. A Q&A session or community post would highly engage your audience.")
            
        # Default if nothing specific
        if not recommendations:
            recommendations.append("Keep up the great work! Monitor the 'Viewer Questions' section for future video ideas.")
            
        return recommendations
