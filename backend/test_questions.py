from analyzer.services.insight_generator import InsightGenerator

def test_question_detection():
    ig = InsightGenerator()
    test_cases = [
        ("What is your name", True),
        ("எப்படி இந்த பிரச்சினையை தீர்ப்பது", True),
        ("I completed the task yesterday", False),
        ("आपका नाम क्या है", True),
        ("Can you help me?", True),
        ("This is a statement.", False),
        ("ஏன் தாமதம்?", True),
        ("How are you", True)
    ]
    
    print("Running Multilingual Question Detection Tests...\n")
    failed = 0
    for text, expected in test_cases:
        result = ig.detect_questions(text)
        status = "PASS" if result == expected else "FAIL"
        if result != expected:
            failed += 1
        print(f"[{status}] Input: '{text}' | Expected: {expected} | Got: {result}")
    
    print(f"\nTests completed. {len(test_cases) - failed}/{len(test_cases)} passed.")

if __name__ == "__main__":
    test_question_detection()
