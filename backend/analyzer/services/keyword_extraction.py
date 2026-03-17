from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

class KeywordExtractor:
    def __init__(self, top_n=10):
        self.top_n = top_n
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=1000,
            min_df=1
        )

    def extract_keywords(self, corpus):
        """Extracts top keywords/phrases from a collection of comments."""
        if not corpus or len(corpus) < 2:
            return []

        try:
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
            feature_names = self.vectorizer.get_feature_names_out()
            
            # Sum tf-idf scores for each word across all documents
            sums = tfidf_matrix.sum(axis=0)
            
            # Connecting feature names to their sum scores
            data = []
            for col, term in enumerate(feature_names):
                data.append((term, sums[0, col]))
            
            ranking = pd.DataFrame(data, columns=['term', 'score'])
            ranking = ranking.sort_values('score', ascending=False)
            
            return ranking.head(self.top_n)['term'].tolist()
        except Exception as e:
            print(f"Error in keyword extraction: {e}")
            return []
