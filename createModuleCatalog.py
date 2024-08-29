import json
from findModules.findToggle import find_toggle_modules
from findModules.findDate import find_date_modules
from findModules.findDropdown import find_dropdown_modules
from findModules.findText import find_text_modules
from findModules.findMultiselect import find_multiselect_modules
from findModules.findTextarea import find_textarea_modules
from findModules.findNumeric import find_numeric_modules
from findModules.findFeetAndInches import find_feet_and_inches_modules

def create_module_catalog(input_json, output_json):
    """
    Creates a module catalog JSON file based on the input JSON data.
    
    Args:
        input_json (str): Path to the input JSON file.
        output_json (str): Path to the output JSON file.
    """
    # Load the input JSON file
    with open(input_json, 'r') as infile:
        modules = json.load(infile)
    
    # Initialize the module catalog list
    module_catalog = []

    # Create a map of module IDs to their labels for parent lookup
    module_map = {module['id']: module['meta']['label'] for module in modules}

    # Iterate through the modules and filter based on parentModuleId
    for module in modules:
        catalog_entry = None
        if module['meta']['parentModuleId'] is None:
            # Apply find functions to extract relevant modules
            if module['type'] == "Toggle":
                catalog_entry = find_toggle_modules([module])
            elif module['type'] == "Date":
                catalog_entry = find_date_modules([module])
            elif module['type'] == "DropDown":
                catalog_entry = find_dropdown_modules([module])
            elif module['type'] == "Text":
                catalog_entry = find_text_modules([module])
            elif module['type'] == "MultiSelect":
                catalog_entry = find_multiselect_modules([module])
            elif module['type'] == "Textarea":
                catalog_entry = find_textarea_modules([module])
            elif module['type'] == "Numeric":
                catalog_entry = find_numeric_modules([module])
            elif module['type'] == "SeparatedFeetAndInches":
                catalog_entry = find_feet_and_inches_modules([module])
        elif module['meta']['parentModuleId'] in module_map:
            # If there's a parent module, include its label in the parentModule field
            parent_label = module_map[module['meta']['parentModuleId']]
            if module['type'] == "Toggle":
                catalog_entry = find_toggle_modules([module])
            elif module['type'] == "Date":
                catalog_entry = find_date_modules([module])
            elif module['type'] == "DropDown":
                catalog_entry = find_dropdown_modules([module])
            elif module['type'] == "Text":
                catalog_entry = find_text_modules([module])
            elif module['type'] == "MultiSelect":
                catalog_entry = find_multiselect_modules([module])
            elif module['type'] == "Textarea":
                catalog_entry = find_textarea_modules([module])
            elif module['type'] == "Numeric":
                catalog_entry = find_numeric_modules([module])
            elif module['type'] == "SeparatedFeetAndInches":
                catalog_entry = find_feet_and_inches_modules([module])
            
            # Update the parentModule field in the catalog entry
            for entry in catalog_entry:
                entry['parentModule'] = parent_label

        if catalog_entry:
            module_catalog.extend(catalog_entry)
        
    # Save the filtered module catalog to the output JSON file
    with open(output_json, 'w') as outfile:
        json.dump(module_catalog, outfile, indent=4)


# Example usage
# create_module_catalog('path_to_modules.json', 'path_to_output.json')
