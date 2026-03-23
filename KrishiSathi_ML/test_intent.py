import requests

url = "http://127.0.0.1:5000/classify_intent"  # ✅ CORRECT

# Test queries in 3 languages
test_queries = [
    {"query": "How much water does rice need?"},  # English
    {"query": "चावल के लिए कितना पानी चाहिए?"},  # Hindi
    {"query": "ধান কতটুকু পানি চায়?"},  # Bengali
    {"query": "What is the capital of India?"},  # OUT_OF_SCOPE
    {"query": "When should I spray pesticides?"},  # SPRAY_DECISION
    {"query": "Tell me a joke"}  # OUT_OF_SCOPE
]

print("Testing Intent Classification Module\n")
print("=" * 60)

for test in test_queries:
    print(f"\nQuery: {test['query']}")
    
    try:
        response = requests.post(url, json=test)
        result = response.json()
        
        print(f"Intent: {result.get('intent', 'N/A')}")
        print(f"Confidence: {result.get('confidence', 'N/A')}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    print("-" * 60)

print("\n✅ Testing Complete!")