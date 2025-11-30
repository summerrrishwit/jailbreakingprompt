import json
import time
from pathlib import Path
import concurrent.futures
from deep_translator import GoogleTranslator

def translate_one(item, translator=None):
    """
    Translates a single item. 
    """
    original_query = item['query']
    try:
        # Translate to English
        # deep_translator creates a new instance easily
        translator = GoogleTranslator(source='zh-CN', target='en')
        translation = translator.translate(original_query)
        translated_query = {
            "query": translation,
            "language": "en"
        }
        return translated_query
    except Exception as e:
        print(f"Error translating query: {original_query[:30]}... Error: {e}")
        return {
            "query": original_query,
            "language": "zh_translation_failed"
        }

def translate_queries(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return

    translated_queries = []
    queries = data['queries']
    total = len(queries)
    print(f"Found {total} queries to translate.")

    # Use ThreadPoolExecutor for parallel translation
    # Adjust max_workers as needed. Too many might trigger rate limits.
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Submit all tasks
        future_to_query = {executor.submit(translate_one, item): item for item in queries}
        
        for i, future in enumerate(concurrent.futures.as_completed(future_to_query)):
            result = future.result()
            translated_queries.append(result)
            if (i + 1) % 10 == 0:
                print(f"[{i+1}/{total}] Processed...")

    output_data = {
        "total_queries": len(translated_queries),
        "queries": translated_queries
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"Translation complete. Saved to {output_file}")

if __name__ == "__main__":
    INPUT_FILE = "dataset/queries/all_ai_queries.json"
    OUTPUT_FILE = "dataset/queries/all_ai_queries_en.json"
    translate_queries(INPUT_FILE, OUTPUT_FILE)
