from django.db import models

class VideoAnalysis(models.Model):
    video_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    author_name = models.CharField(max_length=100, blank=True, null=True)
    total_comment_count = models.IntegerField(default=0)
    
    # Analysis Results
    sentiment_distribution = models.JSONField(default=dict) # e.g., {"positive": 60, "neutral": 30, "negative": 10}
    weighted_sentiment_score = models.FloatField(default=0.0)
    top_keywords = models.JSONField(default=list)
    topic_clusters = models.JSONField(default=list)
    detected_pain_points = models.JSONField(default=list)
    detected_questions = models.JSONField(default=list)
    creator_recommendations = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.video_id})"

class Comment(models.Model):
    video_analysis = models.ForeignKey(VideoAnalysis, related_name='comments', on_delete=models.CASCADE)
    comment_id = models.CharField(max_length=100, unique=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    text = models.TextField()
    cleaned_text = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=255)
    like_count = models.IntegerField(default=0)
    published_at = models.DateTimeField()
    
    # NLP results for individual comments
    sentiment = models.CharField(max_length=20, blank=True, null=True)
    sentiment_score = models.FloatField(default=0.0)
    language = models.CharField(max_length=10, default='en')
    translated_text = models.TextField(blank=True, null=True)
    cluster_id = models.IntegerField(blank=True, null=True)
    is_question = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Comment by {self.author} on {self.video_analysis.video_id}"
