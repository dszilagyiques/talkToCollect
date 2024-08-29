def find_multiselect_modules(modules):
    """
    Finds all MultiSelectInput modules within the given list of modules, including parent submenu labels if applicable.
    
    Args:
        modules (list): A list of modules from which to find MultiSelectInput modules.

    Returns:
        list: A list of dictionaries representing the MultiSelectInput modules found, including parent submenu labels if present.
    """
    multiselect_modules = []
    submenu_map = {}

    # First, create a map of submenu labels using their ID
    for module in modules:
        if module.get('type') == "SubMenu":
            submenu_map[module['id']] = module['meta']['label']

    # Then, find all multiselect modules and append submenu labels if applicable
    for module in modules:
        if module.get('type') == "MultiSelect":
            parent_label = submenu_map.get(module['meta'].get('parentModuleId'), None)
            # Extract relevant details for the module catalog
            multiselect_module_entry = {
                "label": module['meta']['label'],
                "type": module['type'],
                "inputs": module['meta'].get('options', []),
                "parentModule": parent_label if parent_label else None
            }
            multiselect_modules.append(multiselect_module_entry)
    
    return multiselect_modules
