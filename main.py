from fastapi import FastAPI, File, UploadFile
import os
import json
from createModuleCatalog import create_module_catalog
from createSchema import generate_json_schema
from processNaturalLanguage import talk_to_collect
from convertToQuantumFormat import convert_to_quantum_format
from updateCollectionData import update_collection_data
from transcribeAudioFile import get_transcript

app = FastAPI()

@app.post("/talk_to_collect_2d/")
async def update_collection(
    audio_file: UploadFile = File(...),
    modules_file: UploadFile = File(...),
    collection_file: UploadFile = None
):
    # Step 1: Save the uploaded files
    audio_path = f"temp/{audio_file.filename}"
    modules_path = f"temp/{modules_file.filename}"
    collection_path = f"temp/{collection_file.filename}" if collection_file else None
    
    os.makedirs("temp", exist_ok=True)
    
    with open(audio_path, "wb") as f:
        f.write(audio_file.file.read())
    with open(modules_path, "wb") as f:
        f.write(modules_file.file.read())
    if collection_file:
        with open(collection_path, "wb") as f:
            f.write(collection_file.file.read())
    else:
        collection_path = 'collection.json'
    
    # Step 2: Process the audio file
    example_prompt = get_transcript(audio_path)

    # Step 3: Create the module catalog
    create_module_catalog(input_json=modules_path, output_json='docs/moduleCatalog.json')
    
    # Step 4: Load the module catalog
    with open('docs/moduleCatalog.json', 'r') as f:
        module_catalog = json.load(f)
    
    # Step 5: Generate the JSON schema
    json_schema = generate_json_schema(module_catalog)
    
    # Step 6: Generate the response using the JSON schema and user prompt
    talk_to_collect(json_schema=json_schema, user_prompt=example_prompt, output_file='docs/output.json')
    
    # Step 7: Load the output JSON data
    with open('docs/output.json', 'r') as f:
        output_data = json.load(f)
    
    # Step 8: Convert values to Quantum collection data format
    converted_data = convert_to_quantum_format(output_data)
    
    # Step 9: Save the converted data
    with open('docs/output.json', 'w') as f:
        json.dump(converted_data, f, indent=4)
    
    # Step 10: Update the collection data
    update_collection_data(modules_path, 'docs/output.json', collection_path, 'updatedCollection.json')
    
    # Step 11: Return the updated collection JSON
    with open('updatedCollection.json', 'r') as f:
        updated_collection = json.load(f)
    
    return updated_collection

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
