import json
import time
from pathlib import Path
try:
    from googletrans import Translator
except ImportError:
    print("Please install googletrans: pip install googletrans==4.0.0-rc1")
    exit(1)

def translate_queries(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return

    translator = Translator()
    translated_queries = []
    
    total = len(data['queries'])
    print(f"Found {total} queries to translate.")

    for i, item in enumerate(data['queries']):
        original_query = item['query']
        try:
            # Translate to English
            translation = translator.translate(original_query, src='zh-cn', dest='en')
            translated_query = {
                "query": translation.text,
                "language": "en"
            }
            translated_queries.append(translated_query)
            print(f"[{i+1}/{total}] Translated: {translation.text[:30]}...")
            
            # Sleep briefly to avoid hitting rate limits too fast
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error translating query {i+1}: {e}")
            # Keep original if translation fails, or handle as needed
            translated_queries.append({
                "query": original_query,
                "language": "zh_translation_failed"
            })

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
