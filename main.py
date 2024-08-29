from fastapi import FastAPI, File, UploadFile, HTTPException
import os
import json
import logging
from createModuleCatalog import create_module_catalog
from createSchema import generate_json_schema
from processNaturalLanguage import talk_to_collect
from convertToQuantumFormat import convert_to_quantum_format
from updateCollectionData import update_collection_data
from transcribeAudioFile import get_transcript
from addSubmenuRow import format_child_modules

# Initialize FastAPI
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.post("/talk_to_collect_2d/")
async def update_collection(
    audio_file: UploadFile = File(...),
    modules_file: UploadFile = File(...),
    collection_file: UploadFile = File(...)
):
    logger.info("Endpoint '/talk_to_collect_2d/' called")

    # Ensure all files are provided
    if not audio_file:
        logger.error("Audio file is not provided")
        raise HTTPException(status_code=400, detail="Audio file must be provided")
    if not modules_file:
        logger.error("Modules file is not provided")
        raise HTTPException(status_code=400, detail="Modules file must be provided")
    if not collection_file:
        logger.error("Collection file is not provided")
        raise HTTPException(status_code=400, detail="Collection file must be provided")

    # Step 2: Save the uploaded files
    try:
        os.makedirs("temp", exist_ok=True)
        audio_path = f"temp/{audio_file.filename}"
        modules_path = f"temp/{modules_file.filename}"
        collection_path = f"temp/{collection_file.filename}"
        
        with open(audio_path, "wb") as f:
            f.write(audio_file.file.read())
        logger.info(f"Audio file saved to {audio_path}")

        with open(modules_path, "wb") as f:
            f.write(modules_file.file.read())
        logger.info(f"Modules file saved to {modules_path}")

        with open(collection_path, "wb") as f:
            f.write(collection_file.file.read())
        logger.info(f"Collection file saved to {collection_path}")

    except Exception as e:
        logger.error(f"Error saving uploaded files: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving uploaded files: {e}")

    # Step 3: Process the audio file
    try:
        example_prompt = get_transcript(audio_path)
        logger.info(f"Audio transcription completed: {example_prompt}")
    except Exception as e:
        logger.error(f"Error processing audio file: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing audio file: {e}")

    # Step 4: Create the module catalog
    try:
        create_module_catalog(input_json=modules_path, output_json='docs/moduleCatalog.json')
        logger.info("Module catalog created successfully")
    except Exception as e:
        logger.error(f"Error creating module catalog: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating module catalog: {e}")

    # Step 5: Load the module catalog
    try:
        with open('docs/moduleCatalog.json', 'r') as f:
            module_catalog = json.load(f)
        logger.info("Module catalog loaded successfully")
    except Exception as e:
        logger.error(f"Error loading module catalog: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading module catalog: {e}")

    # Step 6: Generate the JSON schema
    try:
        json_schema = generate_json_schema(module_catalog)
        logger.info("JSON schema generated successfully")
    except Exception as e:
        logger.error(f"Error generating JSON schema: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating JSON schema: {e}")

    # Step 7: Generate the response using the JSON schema and user prompt
    try:
        talk_to_collect(json_schema=json_schema, user_prompt=example_prompt, output_file='docs/output.json')
        logger.info("Response generated and saved to 'docs/output.json'")
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating response: {e}")

    # Step 8: Load the output JSON data
    try:
        with open('docs/output.json', 'r') as f:
            output_data = json.load(f)
        logger.info("Output JSON data loaded successfully")
    except Exception as e:
        logger.error(f"Error loading output JSON data: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading output JSON data: {e}")

    # Step 9: Convert values to Quantum collection data format
    try:
        converted_data = convert_to_quantum_format(output_data)
        logger.info("Data converted to Quantum format successfully")
    except Exception as e:
        logger.error(f"Error converting to Quantum format: {e}")
        raise HTTPException(status_code=500, detail=f"Error converting to Quantum format: {e}")

    # Step 10: Save the converted data
    try:
        with open('docs/output.json', 'w') as f:
            json.dump(converted_data, f, indent=4)
        logger.info("Converted data saved to 'docs/output.json'")
    except Exception as e:
        logger.error(f"Error saving converted data: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving converted data: {e}")

    # Step 11: Update the collection data
    try:
        update_collection_data(modules_path, 'docs/output.json', collection_path, 'docs/updatedCollection.json')
        logger.info("Collection data updated successfully")
    except Exception as e:
        logger.error(f"Error updating collection data: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating collection data: {e}")

    # Step 12: Format child modules before returning the JSON
    try:
        format_child_modules()
        logger.info("Child modules formatted successfully")
    except Exception as e:
        logger.error(f"Error formatting child modules: {e}")
        raise HTTPException(status_code=500, detail=f"Error formatting child modules: {e}")

    # Step 13: Return the updated collection JSON
    try:
        with open('docs/updatedCollection.json', 'r') as f:
            updated_collection = json.load(f)
        logger.info("Updated collection loaded successfully")
        return updated_collection
    except Exception as e:
        logger.error(f"Error loading updated collection: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading updated collection: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
