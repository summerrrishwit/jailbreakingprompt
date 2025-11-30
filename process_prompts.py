import json
import concurrent.futures
from pathlib import Path
from deep_translator import GoogleTranslator

def translate_one(text):
    """
    Translates a single text string to Chinese.
    """
    if not text or not text.strip():
        return None
        
    try:
        # Translate to Chinese
        # deep_translator creates a new instance easily or we can instantiate here
        translator = GoogleTranslator(source='en', target='zh-CN')
        translation = translator.translate(text)
        return {
            "query": translation,
            "language": "zh"
        }
    except Exception as e:
        print(f"Error translating: {text[:30]}... Error: {e}")
        return {
            "query": text,
            "language": "en_translation_failed"
        }

def process_prompts():
    prompt_txt_path = Path("dataset/prompt/prompt.txt")
    prompts_json_path = Path("dataset/prompt/prompts.json")
    output_file = Path("dataset/queries/queries.json")
    
    all_prompts = []
    
    # Read prompt.txt
    if prompt_txt_path.exists():
        with open(prompt_txt_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
            print(f"Read {len(lines)} prompts from {prompt_txt_path}")
            all_prompts.extend(lines)
    else:
        print(f"Warning: {prompt_txt_path} not found.")
        
    # Read prompts.json
    if prompts_json_path.exists():
        try:
            with open(prompts_json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                # Assuming json_data is a list of dicts with "prompt" key
                json_prompts = [item.get('prompt', '').strip() for item in json_data if item.get('prompt')]
                print(f"Read {len(json_prompts)} prompts from {prompts_json_path}")
                all_prompts.extend(json_prompts)
        except json.JSONDecodeError:
            print(f"Error decoding {prompts_json_path}")
    else:
        print(f"Warning: {prompts_json_path} not found.")
    
    total = len(all_prompts)
    print(f"Total prompts to process: {total}")
    
    translated_queries = []
    
    # Use ThreadPoolExecutor for parallel translation
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Submit all tasks
        future_to_prompt = {executor.submit(translate_one, prompt): prompt for prompt in all_prompts}
        
        for i, future in enumerate(concurrent.futures.as_completed(future_to_prompt)):
            result = future.result()
            if result:
                translated_queries.append(result)
            
            if (i + 1) % 50 == 0:
                print(f"[{i+1}/{total}] Processed...")

    output_data = {
        "total_queries": len(translated_queries),
        "queries": translated_queries
    }
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"Processing complete. Saved to {output_file}")

if __name__ == "__main__":
    process_prompts()
