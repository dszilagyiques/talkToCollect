def find_date_modules(modules):
    """
    Finds all DateInput modules within the given list of modules, including parent submenu labels if applicable.
    
    Args:
        modules (list): A list of modules from which to find DateInput modules.

    Returns:
        list: A list of dictionaries representing the DateInput modules found, including parent submenu labels if present.
    """
    date_modules = []
    submenu_map = {}

    # First, create a map of submenu labels using their ID
    for module in modules:
        if module.get('type') == "SubMenu":
            submenu_map[module['id']] = module['meta']['label']

    # Then, find all date modules and append submenu labels if applicable
    for module in modules:
        if module.get('type') == "Date":
            parent_label = submenu_map.get(module['meta'].get('parentModuleId'), None)
            # Extract relevant details for the module catalog
            date_module_entry = {
                "label": module['meta']['label'],
                "type": module['type'],
                "inputs": ["YYYY-MM-DD"],
                "parentModule": parent_label if parent_label else None
            }
            date_modules.append(date_module_entry)
    
    return date_modules