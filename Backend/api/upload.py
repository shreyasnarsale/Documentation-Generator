
import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from services import file_processing, llm_service
from models.api_models import UploadResponse, ErrorResponse

router = APIRouter()

@router.post("/upload-and-generate", response_model=UploadResponse, responses={400: {"model": ErrorResponse}})
async def upload_and_generate(zipFile: UploadFile = File(...)):
    if not zipFile.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only ZIP files are allowed")

    try:
        # Save uploaded file
        temp_zip_path = file_processing.save_upload_file(zipFile, zipFile.filename)
        
        # Create extraction directory
        session_id = os.path.splitext(zipFile.filename)[0] + "_" + str(os.urandom(4).hex())
        extract_to = os.path.join(file_processing.TEMP_DIR, session_id)
        
        # Extract ZIP
        file_processing.extract_zip(temp_zip_path, extract_to)
        
        # Analyze file structure
        file_structure = file_processing.get_file_structure(extract_to)
        
        if not file_structure['files']:
             raise HTTPException(status_code=400, detail="ZIP file is empty or contains no readable files")

        # Generate Documentation using LLM
        generation_result = llm_service.generate_documentation(file_structure)
        
        # Cleanup temp files (optional: could be background task)
        file_processing.cleanup_temp_files(extract_to)
        os.remove(temp_zip_path)

        return UploadResponse(
            sessionId=session_id,
            documentation=generation_result['documentation'],
            fileStructure=file_structure,
            metadata=generation_result['metadata']
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
