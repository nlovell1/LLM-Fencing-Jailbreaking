import json

def process_test_jsonl(file_path):
    parsed_data = []
    with open(file_path, 'r') as file:
        for line in file:
            entry = json.loads(line)
            mapped_entry = {
                "prompt": entry["prompt"],
                "type": entry["category"],
                "source": "BeaverTails",
                "jailbreak": ""
            }
            parsed_data.append(mapped_entry)
    return parsed_data

def process_red_team_jsonl(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    parsed_data = []
    for entry in data:
        # Skip entries without the required fields
        if "transcript" not in entry or "model_type" not in entry:
            continue
        mapped_entry = {
            "prompt": entry["transcript"],
            "type": entry.get("tags", ""),
            "source": "HH-RLHF",
            "jailbreak": entry["model_type"]
        }
        parsed_data.append(mapped_entry)
    return parsed_data

def process_chinese_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    parsed_data = []
    for category, entries in data.items():
        for entry in entries:
            mapped_entry = {
                "prompt": entry["prompt"],
                "type": entry["type"],
                "source": "Chinese-Safety-Prompts",
                "jailbreak": ""
            }
            parsed_data.append(mapped_entry)
    return parsed_data

def combine_data(test_path, red_team_path, chinese_path):
    combined_data = process_test_jsonl(test_path) + process_red_team_jsonl(red_team_path) + process_chinese_json(chinese_path)
    return combined_data

final_data = combine_data("test.jsonl", "red_team_attempts.jsonl", "typical_safety_scenarios.json")
with open("combined_data.json", "w") as outfile:
    json.dump(final_data, outfile, indent=4)
