import json

def display_submenu_module_labels(modules_file):
    """
    Display all module labels for every parent module with InputType 'SubMenuInput'.

    Args:
        modules_file (str): Path to the modules JSON file.

    Returns:
        None
    """
    # Load the modules data from the JSON file
    with open(modules_file, 'r') as mf:
        modules_data = json.load(mf)
    
    # Create a mapping from module id to label
    id_to_label = {module['id']: module['meta']['label'] for module in modules_data}
    
    # Find all parent modules with InputType 'SubMenuInput'
    parent_modules = [module for module in modules_data if module['meta']['inputType'] == 'SubMenuInput']

    # Iterate over parent modules and display their child module labels
    for parent_module in parent_modules:
        parent_label = parent_module['meta']['label']
        print(f"Parent Module (SubMenuInput): {parent_label}")
        
        # Iterate over all modules and find children of the parent module
        for module in modules_data:
            if module['meta'].get('parentModuleId') == parent_module['id']:
                submodule_label = module['meta']['label']
                print(f"  Submodule Label: {submodule_label}")

# Example usage
if __name__ == "__main__":
    display_submenu_module_labels('modules.json')
