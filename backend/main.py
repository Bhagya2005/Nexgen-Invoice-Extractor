from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path
import tempfile
import uvicorn
import shutil
import os
from typing import Optional

from invoice_processor import InvoiceProcessor 

app = FastAPI(
    title="Invoice Processing API",
    description="API for processing invoices from various file formats",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the invoice processor
processor = None

@app.on_event("startup")
async def startup_event():
    global processor
    try:
        processor = InvoiceProcessor()
    except ValueError as e:
        print(f"Error initializing InvoiceProcessor: {e}")
        

@app.get("/")
async def root():
    return {"message": "Invoice Processing API is running"}

@app.post("/process-invoice/")
async def process_invoice(file: UploadFile = File(...)):
    """
    Process an invoice file and return structured data
    """
    if not processor:
        raise HTTPException(
            status_code=500,
            detail="Invoice processor not initialized. Check API keys configuration."
        )
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = Path(temp_dir) / file.filename
        
        try:
            # Save uploaded file
            with temp_file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Process the file
            result = processor.process_file(temp_file_path)
            
            if not result.success:
                raise HTTPException(
                    status_code=400,
                    detail=result.error_message or "Failed to process invoice"
                )
            
            return JSONResponse(content=result.data)
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing file: {str(e)}"
            )
        finally:
            file.file.close()

@app.get("/health")
async def health_check():
    """
    Check API health and configuration status
    """
    return {
        "status": "healthy",
        "processor_initialized": processor is not None
    }

def start_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Start the FastAPI server"""
    uvicorn.run("main:app", host=host, port=port, reload=reload)

if __name__ == "__main__":
    start_server(reload=True)