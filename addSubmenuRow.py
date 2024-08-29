import json, os


def add_submenu_row(output_file, combined_output_file, submenu_folder):
    """
    Reads output data and combined output data, creates new submenu rows for matching modules
    with parentModuleId, and updates the combined output JSON with the submenu data.

    Args:
        output_file (str): Path to the input output JSON file.
        combined_output_file (str): Path to the input combined output JSON file.
        submenu_folder (str): Path to the folder where submenu JSON files are saved.

    Returns:
        None
    """
    
    # Load the output data from the JSON file
    with open(output_file, 'r') as of:
        output_data = json.load(of)
    
    # Load the combined output data from the JSON file if it exists
    if os.path.exists(combined_output_file):
        with open(combined_output_file, 'r') as cf:
            combined_data = json.load(cf)
    else:
        combined_data = {'attachmentProperties': []}  # Initialize an empty dict if the file does not exist

    # Dictionary to store all submenu rows by parentModuleId
    submenu_data = {}

    # Iterate over the combined data to find modules with parentModuleId
    for module in combined_data['attachmentProperties']:
        label = module.get('Label')
        parent_id = module.get('parentModuleId')

        # If the module has a parentModuleId and a corresponding value in output data
        if parent_id is not None and label in output_data:
            value = output_data[label]
            api_id = module['apiId']

            # Initialize a new submenu list if the parent_id is not yet in the submenu_data
            if parent_id not in submenu_data:
                submenu_data[parent_id] = []

            # Create a new submenu row entry
            submenu_row_entry = {
                "id": 0,  # Placeholder for the submenu row ID
                "apiId": api_id,
                "moduleId": api_id,
                "value": value,
                "inputType": module["InputType"]
            }

            # Append the submenu entry to the corresponding parent id's list
            submenu_data[parent_id].append(submenu_row_entry)

    # Save each submenu list as a separate JSON file named by the parent id
    if not os.path.exists(submenu_folder):
        os.makedirs(submenu_folder)

    for parent_id, submenu_entries in submenu_data.items():
        # Check if all values are empty for the current parent id
        all_empty = all(entry['value'] == "" for entry in submenu_entries)
        
        if all_empty:
            print(f"Skipped adding submenu rows for parent id {parent_id} because all child modules are empty.")
            continue

        # Load existing submenu data from the collection.json if it exists
        existing_submenu_json_str = next((mod['value'] for mod in combined_data['attachmentProperties'] if mod['apiId'] == parent_id), "[]")
        
        try:
            existing_submenu_json = json.loads(existing_submenu_json_str)
        except json.JSONDecodeError:
            existing_submenu_json = []
        
        # Determine the new row ID for this submenu based on existing data
        new_row_id = len(existing_submenu_json) + 1  # Start at 1 for the first row
        
        submenu_row = {
            "id": new_row_id,  # Set the id for the new submenu row
            "values": submenu_entries
        }

        submenu_filename = os.path.join(submenu_folder, f"{parent_id}_submenus.json")

        # Append the new submenu row to the existing data
        existing_submenu_json.append(submenu_row)

        # Write updated submenu data to the JSON file
        with open(submenu_filename, 'w') as sf:
            json.dump(existing_submenu_json, sf, indent=4)
        
        print(f"Submenu rows for parent id {parent_id} have been written to {submenu_filename}")

        # Update the collection.json with the stringified value of the submenu
        for module in combined_data['attachmentProperties']:
            if module['apiId'] == parent_id:
                module['value'] = json.dumps(existing_submenu_json)
                print(f"Updated module {parent_id} with submenu data")

    # Save the updated combined data back to collection.json
    with open(combined_output_file, 'w') as cf:
        json.dump(combined_data, cf, indent=4)

    print(f"Combined data has been updated in {combined_output_file}")

def clear_submenu_folder(submenu_folder):
    """
    Clears all files in the submenu folder.

    Args:
        submenu_folder (str): Path to the folder where submenu JSON files are saved.

    Returns:
        None
    """
    for filename in os.listdir(submenu_folder):
        file_path = os.path.join(submenu_folder, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print(f"All files in {submenu_folder} have been cleared.")

def format_child_modules():
    """
    Reads the 'updatedCollection.json' file, formats child modules based on their parentModuleId,
    and writes the formatted data back to the same JSON file.

    Returns:
        None
    """
    input_file = 'docs/updatedCollection.json'

    # Load the data from the input JSON file
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    # Iterate over each module in the data
    for module in data.get('attachmentProperties', []):
        parent_id = module.get('parentModuleId')
        input_type = module.get('InputType')

        # If the module has a parentModuleId, set its value based on its type
        if parent_id is not None:
            if input_type == 'ToggleInput':
                module['value'] = 'false'
            else:
                module['value'] = ""

    # Save the formatted data to the output JSON file
    with open(input_file, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    print(f"Formatted data has been written to {input_file}")


