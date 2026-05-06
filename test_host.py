from host.host import chat

history = []

queries = [
    "What is the weather in Mumbai?",
    "Convert 100 USD to INR",
    "Get me the latest news on cricket",
    "Analyze this: I am so happy today, everything is going great!"
]

for query in queries:
    print(f"\nUser: {query}")
    response = chat(query, history)
    print(f"Claude: {response}")
    print("-" * 50)