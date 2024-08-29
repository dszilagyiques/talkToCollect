import json

def generate_json_schema(module_catalog):
    schema = {
        "name": "fill_form",
        "description": "Fills the form data based on the user description.",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
            "required": []  # This will dynamically include all keys
        }
    }
    
    for module in module_catalog:
        label = module['label']
        field_type = module['type']
        inputs = module.get('inputs', [])
        parent_module = module.get('parentModule')

        # Build description prefix based on parentModule presence
        description_prefix = f"In a submenu called: '{parent_module}'. " if parent_module else ""
        
        # Map module types to JSON schema types and make them nullable
        if field_type == "Toggle":
            schema_type = ["boolean", "null"]
            description = f"{description_prefix}true or false."
        elif field_type == "Date":
            schema_type = ["string", "null"]
            description = f"{description_prefix}The date formatted as YYYY-MM-DD"
        elif field_type == "DropDown":
            schema_type = ["string", "null"]
            description = f"{description_prefix}Select a singular option from the enum"
            enum_values = inputs
        elif field_type == "Text":
            schema_type = ["string", "null"]
            description = f"{description_prefix}A string of text"
        elif field_type == "MultiSelect":
            schema_type = ["array", "null"]
            description = f"{description_prefix}Select one or multiple options"
            enum_values = inputs
        elif field_type == "Textarea":
            schema_type = ["string", "null"]
            description = f"{description_prefix}A string of text"
        elif field_type == "Numeric":
            schema_type = ["number", "null"]
            description = f"{description_prefix}A numeric value"
        elif field_type == "SeparatedFeetAndInches":
            schema_type = ["string", "null"]
            description = f"{description_prefix}Represents feet and inches as X'X\" (examples: 12'6\", 4'3\", 45'0\", 13'1/4\", 67'1/2\"))"
        else:
            raise ValueError(f"Unsupported field type: {field_type}")

        # Build the field schema
        field_schema = {
            "type": schema_type,
            "description": description
        }
        
        if field_type == "DropDown":
            field_schema["enum"] = enum_values

        if field_type == "MultiSelect":
            field_schema["items"] = {"type": "string", "enum": enum_values}

        # Add the field to the properties
        schema["schema"]["properties"][label.replace(" ", " ")] = field_schema
        schema["schema"]["required"].append(label.replace(" ", " "))  # Ensure the label is included in required

    return schema

# Load module catalog from file
with open(r'docs\moduleCatalog.json', 'r') as file:
    module_catalog = json.load(file)

# Generate the JSON schema
schema = generate_json_schema(module_catalog)

# Save the JSON schema to a file
with open(r'docs\promptSchema.json', 'w') as schema_file:
    json.dump(schema, schema_file, indent=4)
