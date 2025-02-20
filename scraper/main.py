import json
import sys
from scraper.rmp_scraper import fetch_all_uc_merced_professors

def main():
    try:
        professors = fetch_all_uc_merced_professors()
        print(f"Found {len(professors)} UC Merced professors.")
        
        # Save to a JSON file
        output_file = "output.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(professors, f, ensure_ascii=False, indent=2)
        
        print(f"Saved results to {output_file}")

    except Exception as e:
        print("Error occurred:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
