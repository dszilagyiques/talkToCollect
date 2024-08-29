import json
import os
from addSubmenuRow import add_submenu_row, clear_submenu_folder, format_child_modules

def update_collection_data(modules_file, output_file, collection_data, updated_collection_data):
    """
    Reads module data and output data, then writes formatted data to a new updated JSON file,
    updating existing modules or adding new ones as necessary.

    Args:
        modules_file (str): Path to the input modules JSON file.
        output_file (str): Path to the input output JSON file.
        collection_data (str): Path to the input combined JSON file.
        updated_collection_data (str): Path to the output updated JSON file.

    Returns:
        None
    """
    # Load the modules data from the JSON file
    with open(modules_file, 'r') as mf:
        modules_data = json.load(mf)

    # Extract 'attachmentProperties'
    if 'attachmentProperties' in modules_data:
        modules_data = modules_data['attachmentProperties']

    # Load the output data from the JSON file
    with open(output_file, 'r') as of:
        output_data = json.load(of)
    
    # Load existing collection data or initialize an empty dict with 'attachmentProperties'
    if os.path.exists(collection_data):
        with open(collection_data, 'r') as cf:
            try:
                existing_data = json.load(cf)
                if 'attachmentProperties' not in existing_data:
                    existing_data = {'attachmentProperties': existing_data}
            except json.JSONDecodeError:
                existing_data = {'attachmentProperties': []}
    else:
        existing_data = {'attachmentProperties': []}

    # Helper function to format a module based on its type
    def format_module(module, value):
        return {
            "ActionName": module['meta'].get('actionName'),
            "CategoryId": module.get('categoryId'),
            "Id": module['meta'].get('id', 0),
            "InputType": module['meta'].get('inputType'),
            "Label": module['meta'].get('label'),
            "TypeId": module.get('typeId'),
            "apiId": module.get('id'),
            "attachmentPropertyIds": module['meta'].get('attachmentPropertyIds', []),
            "isEditable": module['meta'].get('isEditable', True),
            "isVisible": module['meta'].get('isVisible', True),
            "locationId": module.get('locationId'),
            "ordinal": module.get('ordinal', 0),
            "subMenuId": module.get('subMenuModuleId'),
            "value": str(value) if value not in [None, ""] else "",
            "isDefault": module.get('isDefault', False),
            "parentModuleId": module['meta'].get('parentModuleId')
        }

    # Function to find and update or add a module in the existing data
    def update_or_add_module(existing_data, new_module):
        for existing_module in existing_data['attachmentProperties']:
            if existing_module['apiId'] == new_module['apiId']:
                # Check if there are any changes, avoiding 'value' updates for submenu parents
                changes = {}
                for key in new_module:
                    if key == 'value':
                        # Skip updating 'value' if the new value is None or empty
                        if new_module[key] in [None, ""]:
                            continue
                        # Skip adding child row to 'value' for submenu parents unless new value is not empty
                        if new_module['InputType'] == 'SubMenuInput' and existing_module[key] != new_module[key] and new_module[key] != "":
                            changes[key] = new_module[key]
                        elif existing_module[key] != new_module[key]:
                            changes[key] = new_module[key]
                    elif existing_module[key] != new_module[key]:
                        changes[key] = new_module[key]

                if changes:
                    print(f"Updated module {existing_module.get('apiId')} with changes: {changes}")
                    existing_module.update(changes)
                    return True
                return False

        # If not found, add the new module
        print(f"Added new module: {new_module.get('apiId')}")
        existing_data['attachmentProperties'].append(new_module)
        return True

    # Iterate over the modules data to find and format all modules
    changes_made = False
    for module in modules_data:
        label = module['meta'].get('label')
        module_value = output_data.get(label)

        # Format the module
        formatted_module = format_module(module, module_value)

        # Update or add the formatted module to the existing data
        if update_or_add_module(existing_data, formatted_module):
            changes_made = True

    # Save the combined formatted data to a new JSON file if changes were made
    if changes_made:
        with open(updated_collection_data, 'w') as ucf:
            json.dump(existing_data, ucf, indent=4)
        print(f"Changes have been written to {updated_collection_data}")

        # Adding submenu rows after updating the collection data
        add_submenu_row('docs/output.json', updated_collection_data, 'submenus')
        print("Submenu rows have been added.")

        # Clear the submenu folder after processing
        clear_submenu_folder('submenus')
        print("Submenu folder has been cleared.")
    else:
        print("No changes detected.")
    format_child_modules
# # Example usage:
# if __name__ == "__main__":
#     update_collection_data('modules.json', 'docs/output.json', 'collection.json', 'updatedCollection.json')
