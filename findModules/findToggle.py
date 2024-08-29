def find_toggle_modules(modules):
    """
    Finds all Toggle modules within the given list of modules, including parent submenu labels if applicable.
    
    Args:
        modules (list): A list of modules from which to find Toggle modules.

    Returns:
        list: A list of dictionaries representing the Toggle modules found, including parent submenu labels if present.
    """
    toggle_modules = []
    submenu_map = {}

    # First, create a map of submenu labels using their ID
    for module in modules:
        if module.get('type') == "SubMenu":
            submenu_map[module['id']] = module['meta']['label']

    # Then, find all toggle modules and append submenu labels if applicable
    for module in modules:
        if module.get('type') == "Toggle":
            parent_label = submenu_map.get(module['meta'].get('parentModuleId'), None)
            # Extract relevant details for the module catalog
            toggle_module_entry = {
                "label": module['meta']['label'],
                "type": module['type'],
                "inputs": ["true", "false"],
                "parentModule": parent_label if parent_label else None
            }
            toggle_modules.append(toggle_module_entry)
    
    return toggle_modules
