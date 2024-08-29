from openai import OpenAI
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
MODEL = "gpt-4o-2024-08-06"
client = OpenAI(api_key=api_key)

def talk_to_collect(json_schema, user_prompt, output_file=r'docs\output.json'):
    """
    Generates a response based on the provided JSON schema and user prompt.

    Args:
        json_schema (json): The JSON schema to be used for structured output.
        user_prompt (str): The user input prompt to guide the AI.
        output_file (str): The file path where the output will be saved.

    Returns:
        None
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant filling out form data."},
                {"role": "user", "content": user_prompt}
            ],
            response_format={
                "type": "json_schema",
                "json_schema": json_schema
            }
        )

        # Check if the response content is not empty
        if response.choices and response.choices[0].message.content:
            response_content_str = response.choices[0].message.content

            # Replace any invalid JSON parts
            response_content_str = response_content_str.replace(":,", ":null,")  # Handle missing values like "DropDown":,
            response_content_str = response_content_str.replace(":[],", ":null,")  # Handle missing values like "DropDown":,


            try:
                # Parse the stringified JSON response back into a dictionary
                response_content = json.loads(response_content_str)
                
                # Save the parsed response content to the output file
                with open(output_file, 'w') as f:
                    json.dump(response_content, f, indent=4)

            except json.JSONDecodeError as e:
                print(f"JSON decoding failed: {e}")
                print("Response content was:", response_content_str)

        else:
            print("The response content is empty or not in the expected format.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
# talk_to_collect(json_schema, example_prompt)
