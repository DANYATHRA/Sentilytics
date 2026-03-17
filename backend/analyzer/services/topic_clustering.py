from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class TopicClusterting:
    def __init__(self, n_clusters=4):
        self.n_clusters = n_clusters
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
        self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)

    def cluster_comments(self, comments):
        """Groups comments into themes and returns cluster assignments and theme names."""
        if not comments or len(comments) < self.n_clusters:
            return [0] * len(comments), ["General Feedback"]

        try:
            # Transform comments to TF-IDF vectors
            X = self.vectorizer.fit_transform(comments)
            
            # Fit K-Means
            self.model.fit(X)
            cluster_assignments = self.model.labels_.tolist()
            
            # Identify top words for each cluster to name the themes
            order_centroids = self.model.cluster_centers_.argsort()[:, ::-1]
            terms = self.vectorizer.get_feature_names_out()
            
            cluster_themes = []
            for i in range(self.n_clusters):
                # Take top 3 words to describe the cluster
                top_words = [terms[ind] for ind in order_centroids[i, :3]]
                cluster_themes.append(" ".join(top_words).title())
                
            return cluster_assignments, cluster_themes
            
        except Exception as e:
            print(f"Error in topic clustering: {e}")
            return [0] * len(comments), ["General Discussion"]

    def map_to_predefined_themes(self, cluster_words):
        """
        Attempts to map arbitrary clusters to human-readable themes 
        like 'Concept Clarity' or 'Pacing Issues'.
        """
        theme_map = {
            'clarity': ['explain', 'clear', 'understand', 'confusion', 'concept'],
            'pacing': ['fast', 'slow', 'speed', 'quick', 'pacing'],
            'appreciation': ['great', 'awesome', 'thanks', 'love', 'helpful'],
            'request': ['please', 'could', 'can', 'next', 'video', 'tutorial'],
        }
        
        # Simple heuristic mapping
        for theme, keywords in theme_map.items():
            if any(word in " ".join(cluster_words).lower() for word in keywords):
                return theme.replace('_', ' ').title()
        
        return "General Feedback"
