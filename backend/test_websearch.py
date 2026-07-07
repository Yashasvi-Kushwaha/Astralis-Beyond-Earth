from services.web_search import WebSearch

search = WebSearch()

results = search.search("What is a Dyson Sphere?")

for i, result in enumerate(results, start=1):
    print("=" * 50)
    print(f"Result {i}")
    print("Title:", result["title"])
    print("URL:", result["url"])
    print("Content:")
    print(result["content"])