import csv
import json


def csv_to_json(input_csv_path, output_json_path):
    with open(input_csv_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        result = []
        
        for row in reader:
            first_col = list(row.keys())[0]  # First column title
            first_col_value = row[first_col]
            
            # Create a dictionary for the remaining columns
            remaining_data = {key: value for key, value in row.items() if key != first_col}
            
            # Construct the desired structure
            result.append({first_col_value: remaining_data})
        
        # Write the JSON to a file
        with open(output_json_path, mode='w', encoding='utf-8') as json_file:
            json.dump(result, json_file, indent=4, ensure_ascii=False)

# Example usage
csv_to_json('Operators/data/csv/char_names.csv', 'Operators/data/json/char_names.json')
