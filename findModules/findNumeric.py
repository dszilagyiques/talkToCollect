def find_numeric_modules(modules):
    """
    Finds all NumericInput modules within the given list of modules, including parent submenu labels if applicable.
    
    Args:
        modules (list): A list of modules from which to find NumericInput modules.

    Returns:
        list: A list of dictionaries representing the NumericInput modules found, including parent submenu labels if present.
    """
    numeric_modules = []
    submenu_map = {}

    # First, create a map of submenu labels using their ID
    for module in modules:
        if module.get('type') == "SubMenu":
            submenu_map[module['id']] = module['meta']['label']

    # Then, find all numeric modules and append submenu labels if applicable
    for module in modules:
        if module.get('type') == "Numeric":
            parent_label = submenu_map.get(module['meta'].get('parentModuleId'), None)
            # Extract relevant details for the module catalog
            numeric_module_entry = {
                "label": module['meta']['label'],
                "type": module['type'],
                "inputs": ["number"],
                "parentModule": parent_label if parent_label else None
            }
            numeric_modules.append(numeric_module_entry)
    
    return numeric_modules
