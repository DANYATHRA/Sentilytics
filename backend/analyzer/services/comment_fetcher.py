import os
import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class YouTubeFetcher:
    def __init__(self, api_key):
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    @staticmethod
    def extract_video_id(url):
        """Extracts the video ID from a YouTube URL."""
        pattern = r'(?:v=|\/|be\/|embed\/)([0-9A-Za-z_-]{11})'
        match = re.search(pattern, url)
        return match.group(1) if match else None

    def fetch_video_details(self, video_id):
        """Fetches video title, description, author, and statistics."""
        try:
            request = self.youtube.videos().list(
                part="snippet,statistics",
                id=video_id
            )
            response = request.execute()
            if not response['items']:
                return None
            
            item = response['items'][0]
            snippet = item['snippet']
            stats = item['statistics']
            return {
                'title': snippet['title'],
                'description': snippet['description'],
                'thumbnail_url': snippet['thumbnails']['high']['url'],
                'author_name': snippet['channelTitle'],
                'total_comment_count': int(stats.get('commentCount', 0))
            }
        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            return None

    def fetch_comments(self, video_id, max_results=2000):
        """Fetches up to max_results comments (including top-level and replies) with pagination."""
        comments = []
        next_page_token = None
        
        try:
            while len(comments) < max_results:
                request = self.youtube.commentThreads().list(
                    part="snippet,replies",
                    videoId=video_id,
                    maxResults=100, # Max allowed by API
                    pageToken=next_page_token,
                    textFormat="plainText"
                )
                response = request.execute()
                
                for item in response.get('items', []):
                    # Add top level comment
                    snippet = item['snippet']['topLevelComment']['snippet']
                    comments.append({
                        'comment_id': item['id'],
                        'text': snippet['textDisplay'],
                        'author': snippet['authorDisplayName'],
                        'like_count': snippet['likeCount'],
                        'published_at': snippet['publishedAt']
                    })
                    
                    # Add replies if they exist
                    if 'replies' in item:
                        for reply in item['replies']['comments']:
                            reply_snippet = reply['snippet']
                            comments.append({
                                'comment_id': reply['id'],
                                'parent_id': item['id'],
                                'text': reply_snippet['textDisplay'],
                                'author': reply_snippet['authorDisplayName'],
                                'like_count': reply_snippet['likeCount'],
                                'published_at': reply_snippet['publishedAt']
                            })
                            if len(comments) >= max_results:
                                break
                    
                    if len(comments) >= max_results:
                        break
                
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            
        return comments
