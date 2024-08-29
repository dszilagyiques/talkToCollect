import time
import json
from createModuleCatalog import create_module_catalog
from createSchema import generate_json_schema
from processNaturalLanguage import talk_to_collect
from convertToQuantumFormat import convert_to_quantum_format
from updateCollectionData import update_collection_data
from transcribeAudioFile import get_transcript


example_prompt = get_transcript(r'audioFiles\test.m4a')
print(example_prompt)

# Step 1: Create the module catalog
start_time = time.time()
create_module_catalog(input_json=r'modules.json', output_json=r'docs/moduleCatalog.json')
end_time = time.time()
print(f"Step 1: Create module catalog took {end_time - start_time:.6f} seconds")

# Step 2: Load the module catalog from the JSON file
start_time = time.time()
with open(r'docs/moduleCatalog.json', 'r') as f:
    module_catalog = json.load(f)
end_time = time.time()
print(f"Step 2: Load module catalog took {end_time - start_time:.6f} seconds")

# Step 3: Generate the JSON schema
start_time = time.time()
json_schema = generate_json_schema(module_catalog)
end_time = time.time()
print(f"Step 3: Generate JSON schema took {end_time - start_time:.6f} seconds")

# Step 4: Save the generated JSON schema to a file
start_time = time.time()
with open(r'docs/promptSchema.json', 'w') as f:
    json.dump(json_schema, f, indent=4)
end_time = time.time()
print(f"Step 4: Save JSON schema took {end_time - start_time:.6f} seconds")

# Step 5: Use the JSON schema and user prompt to generate the response and save it to output.json
start_time = time.time()
talk_to_collect(json_schema=json_schema, user_prompt=example_prompt, output_file=r'docs/output.json')
end_time = time.time()
print(f"Step 5: Generate response with JSON schema took {end_time - start_time:.6f} seconds")

# Step 6: Load the output JSON data
start_time = time.time()
with open(r'docs/output.json', 'r') as f:
    output_data = json.load(f)
end_time = time.time()
print(f"Step 6: Load output JSON data took {end_time - start_time:.6f} seconds")

# Step 7: Convert values to Quantum collection data format
start_time = time.time()
converted_data = convert_to_quantum_format(output_data)
end_time = time.time()
print(f"Step 7: Converting values to Quantum format took {end_time - start_time:.6f} seconds")

# Step 8: Save the stringified data back to the output file
start_time = time.time()
with open(r'docs/output.json', 'w') as f:
    json.dump(converted_data, f, indent=4)
end_time = time.time()
print(f"Step 8: Saving converted data took {end_time - start_time:.6f} seconds")

# Step 9: Populate the collection data
start_time = time.time()
update_collection_data('modules.json', 'docs/output.json', 'collection.json','updatedCollection.json')

end_time = time.time()
print(f"Step 9: Populate collection data took {end_time - start_time:.6f} seconds")

print("Final output has been saved to updatedCollection.json.")
