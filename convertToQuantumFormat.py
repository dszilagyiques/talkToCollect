import json
import re

def convert_to_quantum_format(data):
    """
    Convert the values in a JSON object according to specific rules:
    - Booleans and numbers are converted to strings.
    - null values are converted to empty strings "".
    - Lists are converted to a stringified JSON array.
    - 'SeparatedFeetAndInches' is converted to a double, then stringified.

    Args:
        data (dict): The JSON object with original values.

    Returns:
        dict: A new JSON object with all values stringified.
    """
    
    def convert_feet_inches_to_double(feet_inches_str):
        # Match the pattern for feet and inches
        match = re.match(r"(\d+)'(\d+)?(?:[ ]?(\d+/\d+))?\"", feet_inches_str)
        if match:
            feet = int(match.group(1))
            inches = int(match.group(2)) if match.group(2) else 0
            fractional_inches = match.group(3)
            if fractional_inches:
                # Convert the fractional part to a decimal
                numerator, denominator = map(int, fractional_inches.split('/'))
                inches += numerator / denominator
            # Convert everything to feet as a float
            return feet + inches / 12
        return None

    def stringify_value(value):
        if isinstance(value, bool):
            return json.dumps(value)  # Converts booleans to "true" or "false"
        elif isinstance(value, (int, float)):
            return str(value)
        elif value is None:
            return ""
        elif isinstance(value, list):
            return json.dumps(value)  # Converts list to a JSON array string
        elif isinstance(value, str) and re.match(r"^\d+'\d*\"$", value):
            # Convert SeparatedFeetAndInches string to a double and then stringify it
            double_value = convert_feet_inches_to_double(value)
            return str(double_value) if double_value is not None else ""
        else:
            return value

    # Apply the function to all items in the JSON
    stringified_data = {k: stringify_value(v) for k, v in data.items()}

    return stringified_data

