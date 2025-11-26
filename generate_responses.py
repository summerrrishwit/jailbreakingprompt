import json
import time
import random

def call_llm_api(prompt):
    """
    Placeholder for LLM API call.
    Replace this with actual API call logic (e.g., OpenAI, Anthropic, etc.)
    """
    # Simulate API latency
    # time.sleep(0.1)
    
    # Return a dummy response for now
    responses = [
        "这是一个很有趣的想法。理论上，这需要...",
        "作为一个AI助手，我不能提供关于非法活动的详细步骤。",
        "在科幻小说中，这通常涉及到...",
        "This is a fascinating concept. Theoretically, it would involve...",
        "As an AI, I cannot provide instructions for illegal activities.",
        "In science fiction, this is often depicted as..."
    ]
    return random.choice(responses) + f" (Response to: {prompt[:20]}...)"

def generate_responses(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return

    if "queries" not in data:
        print("Error: 'queries' list not found in input file.")
        return

    responses_data = []
    total = len(data['queries'])
    print(f"Found {total} queries. Generating responses...")

    for i, item in enumerate(data['queries']):
        query = item['query']
        # Call LLM API
        response = call_llm_api(query)
        
        response_entry = {
            "query": query,
            "response": response,
            "language": item.get("language", "unknown")
        }
        responses_data.append(response_entry)
        
        if (i + 1) % 10 == 0:
            print(f"Processed {i + 1}/{total} queries.")

    output_json = {
        "total_responses": len(responses_data),
        "responses": responses_data
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_json, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {len(responses_data)} responses. Saved to {output_file}")

if __name__ == "__main__":
    INPUT_FILE = "dataset/queries/merged_queries.json"
    OUTPUT_FILE = "dataset/response/responses.json"
    generate_responses(INPUT_FILE, OUTPUT_FILE)
