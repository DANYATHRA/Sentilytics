from analyzer.services.insight_generator import InsightGenerator

def test_intent_classification():
    ig = InsightGenerator()
    test_cases = [
        # Questions (True Intent)
        ("Why is this happening", True),
        ("எப்படி இது வேலை செய்கிறது", True),
        ("Can you explain this", True),
        
        # Statements with interrogative words (Should NOT be categorized as questions)
        ("This is why India hates Pakistan", False),
        ("I know how this works", False),
        ("That’s why this method failed", False),
        ("i see what you did there", False),
        
        # Plain Statements
        ("I completed the task yesterday", False),
        ("The video was very helpful", False)
    ]
    
    print("Verifying Intent-Based Question Detection...\n")
    failed_cases = []
    passed = 0
    for text, expected in test_cases:
        result = ig.detect_questions(text)
        if result == expected:
            passed += 1
            status = "PASS"
        else:
            status = "FAIL"
            failed_cases.append((text, expected, result))
        print(f"[{status}] Text: '{text}'")
    
    if failed_cases:
        print("\n--- FAILED CASES ---")
        for text, exp, got in failed_cases:
            print(f"Input: '{text}' | Expected: {exp} | Got: {got}")

    print(f"\nResults: {passed}/{len(test_cases)} Passed.")

if __name__ == "__main__":
    test_intent_classification()
