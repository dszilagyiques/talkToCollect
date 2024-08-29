def find_textarea_modules(modules):
    """
    Finds all TextareaInput modules within the given list of modules, including parent submenu labels if applicable.
    
    Args:
        modules (list): A list of modules from which to find TextareaInput modules.

    Returns:
        list: A list of dictionaries representing the TextareaInput modules found, including parent submenu labels if present.
    """
    textarea_modules = []
    submenu_map = {}

    # First, create a map of submenu labels using their ID
    for module in modules:
        if module.get('type') == "SubMenu":
            submenu_map[module['id']] = module['meta']['label']

    # Then, find all textarea modules and append submenu labels if applicable
    for module in modules:
        if module.get('type') == "Textarea":
            parent_label = submenu_map.get(module['meta'].get('parentModuleId'), None)
            # Extract relevant details for the module catalog
            textarea_module_entry = {
                "label": module['meta']['label'],
                "type": module['type'],
                "inputs": ["string"],
                "parentModule": parent_label if parent_label else None
            }
            textarea_modules.append(textarea_module_entry)
    
    return textarea_modules
