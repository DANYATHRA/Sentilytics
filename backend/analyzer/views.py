from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import VideoAnalysis, Comment
from .services.comment_fetcher import YouTubeFetcher
from .services.preprocessing import TextPreprocessor
from .services.sentiment_analysis import SentimentAnalyzer
from .services.keyword_extraction import KeywordExtractor
from .services.topic_clustering import TopicClusterting
from .services.insight_generator import InsightGenerator
from django.db import transaction
import os

# Using the provided API key directly for immediate functionality
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', 'AIzaSyCvn5iyyrCyn6GlCv2acbpJMhS3QiOCeb4')

def index(request):
    return render(request, 'analyzer/index.html')

def analyze_video(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        if not video_url:
            messages.error(request, "Please provide a YouTube URL.")
            return redirect('index')

        fetcher = YouTubeFetcher(YOUTUBE_API_KEY)
        video_id = fetcher.extract_video_id(video_url)
        
        if not video_id:
            messages.error(request, "Invalid YouTube URL.")
            return redirect('index')

        # Check if already analyzed (optional: add refresh logic)
        # existing_analysis = VideoAnalysis.objects.filter(video_id=video_id).first()
        # if existing_analysis:
        #     return redirect('dashboard', video_id=video_id)

        # 1. Fetch Data
        try:
            details = fetcher.fetch_video_details(video_id)
            if not details:
                messages.error(request, "Could not fetch video details. Check your API key or connection.")
                return redirect('index')
                
            raw_comments = fetcher.fetch_comments(video_id)
            if not raw_comments:
                messages.error(request, "No comments found or API error. Ensure the video is public.")
                return redirect('index')
        except Exception as e:
            messages.error(request, f"Data collection failed (likely network/SSL issue): {str(e)}")
            return redirect('index')

        # 2. Process Data
        try:
            preprocessor = TextPreprocessor()
            sentiment_analyzer = SentimentAnalyzer()
            
            processed_comments = []
            intent_counts = {'positive': 0, 'neutral': 0, 'negative': 0, 'question': 0}
            total_weighted_sentiment = 0
            
            insight_gen = InsightGenerator() 
            sentiment_analyzer = SentimentAnalyzer()
            preprocessor = TextPreprocessor()
            
            for rc in raw_comments:
                cleaned = preprocessor.clean_text(rc['text'])
                lang = preprocessor.detect_language(cleaned)
                
                # Rule 1: Detect Question (Intent-Based) - This takes priority
                is_q = insight_gen.detect_questions(rc['text'])
                
                if is_q:
                    label = 'neutral' # Question itself is sentiment-neutral in our storage
                    score = 0.5
                    intent_counts['question'] += 1
                else:
                    # Rule 2: Video-Based Sentiment Classification (if NOT a question)
                    label, score = sentiment_analyzer.analyze(cleaned)
                    intent_counts[label] += 1
                
                weighted_score = sentiment_analyzer.calculate_weighted_sentiment(score, rc['like_count'], label)
                total_weighted_sentiment += weighted_score
                
                processed_comments.append({
                    'raw': rc,
                    'cleaned': cleaned,
                    'lang': lang,
                    'sentiment': label,
                    'score': score,
                    'is_question': is_q
                })
        except Exception as e:
            messages.error(request, f"Analysis service failure: {str(e)}")
            return redirect('index')

        # 3. Aggregated Analysis
        try:
            all_text = [c['cleaned'] for c in processed_comments if c['cleaned']]
            
            kw_extractor = KeywordExtractor()
            keywords = kw_extractor.extract_keywords(all_text)
            
            clustering = TopicClusterting()
            cluster_ids, cluster_themes = clustering.cluster_comments(all_text)
            
            insight_gen = InsightGenerator()
            pain_points = insight_gen.detect_pain_points([c['cleaned'] for c in processed_comments])
            
            question_count = intent_counts['question']
            
            # Use all 4 categories for the distribution (Rule: Exactly One)
            sentiment_dist = {k: (v / len(processed_comments)) * 100 for k, v in intent_counts.items() if len(processed_comments) > 0}
            recommendations = insight_gen.generate_recommendations(sentiment_dist, pain_points, question_count)

            # 4. Save to Database
            with transaction.atomic():
                # Delete old analysis if exists to refresh
                VideoAnalysis.objects.filter(video_id=video_id).delete()
                
                analysis = VideoAnalysis.objects.create(
                    video_id=video_id,
                    title=details['title'],
                    description=details['description'],
                    thumbnail_url=details['thumbnail_url'],
                    author_name=details['author_name'],
                    total_comment_count=details.get('total_comment_count', 0),
                    sentiment_distribution=sentiment_dist,
                    weighted_sentiment_score=total_weighted_sentiment / len(processed_comments) if processed_comments else 0,
                    top_keywords=keywords,
                    topic_clusters=cluster_themes,
                    detected_pain_points=pain_points,
                    detected_questions=[c['raw']['text'] for c in processed_comments if c['is_question']][:20], 
                    creator_recommendations=recommendations
                )
                
                # Save comments in two passes: 
                # 1. Create all comment objects
                # 2. Link replies to parents
                comment_map = {} # Maps youtube comment_id to our model instance
                
                # First pass: Create all objects
                seen_ids = set()
                for pc in processed_comments:
                    if pc['raw']['comment_id'] in seen_ids:
                        continue
                    seen_ids.add(pc['raw']['comment_id'])
                    
                    # Map cluster ID
                    c_id = None
                    if pc['cleaned'] in all_text:
                        try:
                            text_index = all_text.index(pc['cleaned'])
                            c_id = cluster_ids[text_index]
                        except: pass
                            
                    comment_obj = Comment.objects.create(
                        video_analysis=analysis,
                        comment_id=pc['raw']['comment_id'],
                        text=pc['raw']['text'],
                        cleaned_text=pc['cleaned'],
                        author=pc['raw']['author'],
                        like_count=pc['raw']['like_count'],
                        published_at=pc['raw']['published_at'],
                        sentiment=pc['sentiment'],
                        sentiment_score=pc['score'],
                        language=pc['lang'],
                        cluster_id=c_id,
                        is_question=pc['is_question']
                    )
                    comment_map[pc['raw']['comment_id']] = comment_obj

                # Second pass: Associate parents
                for pc in processed_comments:
                    parent_id = pc['raw'].get('parent_id')
                    if parent_id and parent_id in comment_map:
                        comment_obj = comment_map[pc['raw']['comment_id']]
                        comment_obj.parent_comment = comment_map[parent_id]
                        comment_obj.save()

            return redirect('dashboard', video_id=video_id)

        except Exception as e:
            messages.error(request, f"Analysis failed: {str(e)}")
            return redirect('index')

    return redirect('index')

def dashboard(request, video_id):
    analysis = get_object_or_404(VideoAnalysis, video_id=video_id)
    # Fetch top-level comments for primary cards (ordered by likes)
    top_comments = analysis.comments.filter(parent_comment__isnull=True).order_by('-like_count')
    
    context = {
        'analysis': analysis,
        'top_comments': top_comments,
    }
    return render(request, 'analyzer/dashboard.html', context)
