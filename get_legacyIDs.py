import json

def create_name_id_json(input_file, output_file):
    """
    Reads professors from `input_file` (JSON array of dicts),
    and writes a new JSON file `output_file` containing
    [{ "FirstName LastName": "LegacyID" }, ...].
    """
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f) 

    new_data = []
    for prof in data:

        first_name = prof.get("firstName", "")
        last_name = prof.get("lastName", "")
        legacy_id = prof.get("legacyId", "")

        full_name = f"{first_name} {last_name}"
        new_data.append({ full_name: str(legacy_id) })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # Example usage
    input_file = "output.json"     
    output_file = "legacyIds.json"
    create_name_id_json(input_file, output_file)
    print(f"Created {output_file}")
