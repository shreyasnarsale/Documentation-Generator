
from fastapi import APIRouter, HTTPException, Response
from models.api_models import ExportRequest

router = APIRouter()

@router.post("/export-markdown")
async def export_markdown(request: ExportRequest):
    try:
        headers = {
            "Content-Disposition": f"attachment; filename={request.filename}",
            "Content-Type": "text/markdown; charset=utf-8"
        }
        
        return Response(
            content=request.documentation,
            media_type="text/markdown",
            headers=headers
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")
