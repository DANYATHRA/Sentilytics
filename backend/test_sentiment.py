import os
import sys

# Add the project directory to sys.path to import our services
sys.path.append(os.getcwd())

try:
    from analyzer.services.sentiment_analysis import SentimentAnalyzer
    print("Initializing SentimentAnalyzer...")
    analyzer = SentimentAnalyzer()
    
    test_text = "I love this tutorial, it was so helpful!"
    print(f"Analyzing: {test_text}")
    label, score = analyzer.analyze(test_text)
    print(f"Result: {label} (Score: {score:.4f})")
    
except Exception as e:
    print(f"FAILURE: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
