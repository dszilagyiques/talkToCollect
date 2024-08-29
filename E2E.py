import time
import json
from createModuleCatalog import create_module_catalog
from createSchema import generate_json_schema
from processNaturalLanguage import talk_to_collect
from convertToQuantumFormat import convert_to_quantum_format
from updateCollectionData import update_collection_data
from transcribeAudioFile import get_transcript
from addSubmenuRow import format_child_modules

# Start total time timer
total_start_time = time.time()

# Step 1: Transcribe audio to text
start_time = time.time()
example_prompt = get_transcript(r'audioFiles\test.m4a')
end_time = time.time()
print(example_prompt)
print(f"Step 1: Transcribe audio took {end_time - start_time:.6f} seconds")

# Step 2: Create the module catalog
start_time = time.time()
create_module_catalog(input_json=r'docs/modules.json', output_json=r'docs/moduleCatalog.json')
end_time = time.time()
print(f"Step 2: Create module catalog took {end_time - start_time:.6f} seconds")

# Step 3: Load the module catalog from the JSON file
start_time = time.time()
with open(r'docs/moduleCatalog.json', 'r') as f:
    module_catalog = json.load(f)
end_time = time.time()
print(f"Step 3: Load module catalog took {end_time - start_time:.6f} seconds")

# Step 4: Generate the JSON schema
start_time = time.time()
json_schema = generate_json_schema(module_catalog)
end_time = time.time()
print(f"Step 4: Generate JSON schema took {end_time - start_time:.6f} seconds")

# Step 5: Save the generated JSON schema to a file
start_time = time.time()
with open(r'docs/promptSchema.json', 'w') as f:
    json.dump(json_schema, f, indent=4)
end_time = time.time()
print(f"Step 5: Save JSON schema took {end_time - start_time:.6f} seconds")

# Step 6: Use the JSON schema and user prompt to generate the response and save it to output.json
start_time = time.time()
talk_to_collect(json_schema=json_schema, user_prompt=example_prompt, output_file=r'docs/output.json')
end_time = time.time()
print(f"Step 6: Generate response with JSON schema took {end_time - start_time:.6f} seconds")

# Step 7: Load the output JSON data
start_time = time.time()
with open(r'docs/output.json', 'r') as f:
    output_data = json.load(f)
end_time = time.time()
print(f"Step 7: Load output JSON data took {end_time - start_time:.6f} seconds")

# Step 8: Convert values to Quantum collection data format
start_time = time.time()
converted_data = convert_to_quantum_format(output_data)
end_time = time.time()
print(f"Step 8: Converting values to Quantum format took {end_time - start_time:.6f} seconds")

# Step 9: Save the stringified data back to the output file
start_time = time.time()
with open(r'docs/output.json', 'w') as f:
    json.dump(converted_data, f, indent=4)
end_time = time.time()
print(f"Step 9: Saving converted data took {end_time - start_time:.6f} seconds")

# Step 10: Populate the collection data
start_time = time.time()
update_collection_data('docs/modules.json', 'docs/output.json', 'docs/collection.json', 'docs/updatedCollection.json')
end_time = time.time()
print(f"Step 10: Populate collection data took {end_time - start_time:.6f} seconds")

# Step 11: Format child modules
start_time = time.time()
format_child_modules()
end_time = time.time()
print(f"Step 11: Format child modules took {end_time - start_time:.6f} seconds")

# Print final output location
print("Final output has been saved to docs/updatedCollection.json.")

# End total time timer
total_end_time = time.time()
print(f"Total time taken for the entire process: {total_end_time - total_start_time:.6f} seconds")
