import json
import glob
import os

def merge_jsons(output_file):
    merged_queries = []
    
    # Find all JSON files in the dataset/queries/ directory
    json_files = glob.glob("dataset/queries/*.json")
    
    print(f"Found {len(json_files)} JSON files.")
    
    for file_path in json_files:
        # Skip the output file itself if it exists
        if os.path.basename(file_path) == os.path.basename(output_file):
            continue
            
        # Skip other potential output files to avoid processing them if re-run
        if os.path.basename(file_path) in ["responses.json", "evaluation_keywords.json", "evaluation_llm.json"]:
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Check if it has the expected structure
                if "queries" in data and isinstance(data["queries"], list):
                    print(f"Merging {len(data['queries'])} queries from {file_path}")
                    merged_queries.extend(data["queries"])
                else:
                    print(f"Skipping {file_path}: 'queries' list not found.")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    output_data = {
        "total_queries": len(merged_queries),
        "queries": merged_queries
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"Merged {len(merged_queries)} queries into {output_file}")

if __name__ == "__main__":
    OUTPUT_FILE = "dataset/queries/merged_queries.json"
    merge_jsons(OUTPUT_FILE)
