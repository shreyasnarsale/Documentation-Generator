
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class DocumentationMetadata(BaseModel):
    totalFiles: int
    languages: List[str]
    processingTime: float
    tokensUsed: int

class FileStructure(BaseModel):
    root: str
    files: List[str]
    tree: str

class UploadResponse(BaseModel):
    sessionId: str
    documentation: str
    fileStructure: FileStructure
    metadata: DocumentationMetadata

class ErrorResponse(BaseModel):
    detail: str

class ExportRequest(BaseModel):
    documentation: str
    filename: Optional[str] = "documentation.md"

class ChatInitRequest(BaseModel):
    documentation: str

class ChatInitResponse(BaseModel):
    sessionId: str
    status: str

class ChatMessageRequest(BaseModel):
    sessionId: str
    message: str
    history: List[Dict[str, str]] = [] # List of {"role": "user"|"model", "content": "..."}

class ChatMessageResponse(BaseModel):
    response: str
    sources: List[str] = []
