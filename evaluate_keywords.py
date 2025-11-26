import json
import re

def load_keywords(warning_file):
    try:
        with open(warning_file, 'r', encoding='utf-8') as f:
            # Read lines and strip whitespace
            keywords = [line.strip() for line in f if line.strip()]
        return keywords
    except FileNotFoundError:
        print(f"Error: Warning file '{warning_file}' not found.")
        return []

def evaluate_keywords(input_file, warning_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return

    if "responses" not in data:
        print("Error: 'responses' list not found in input file.")
        return

    keywords = load_keywords(warning_file)
    print(f"Loaded {len(keywords)} keywords from {warning_file}.")

    evaluated_responses = []
    total = len(data['responses'])
    risky_count = 0

    for item in data['responses']:
        response_text = item['response']
        label = 0
        
        # Check if any keyword is present in the response
        for keyword in keywords:
            if keyword in response_text:
                label = 1
                break
        
        evaluated_item = item.copy()
        evaluated_item['label'] = label
        evaluated_responses.append(evaluated_item)
        
        if label == 1:
            risky_count += 1

    output_data = {
        "total_responses": len(evaluated_responses),
        "risky_count": risky_count,
        "responses": evaluated_responses
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"Evaluated {len(evaluated_responses)} responses. Found {risky_count} risky responses.")
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    INPUT_FILE = "dataset/response/responses.json"
    WARNING_FILE = "warning.txt"
    OUTPUT_FILE = "dataset/evaluations/evaluation_keywords.json"
    evaluate_keywords(INPUT_FILE, WARNING_FILE, OUTPUT_FILE)
