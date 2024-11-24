import os
from pathlib import Path
from typing import Optional, Dict, List, Union
from dataclasses import dataclass
from dotenv import load_dotenv
import google.generativeai as genai
import together
from pdf2image import convert_from_path
from PIL import Image
import io
import base64
import json
import pandas as pd
import logging

@dataclass
class ProcessingResult:
    """Data class to store processing results and metadata"""
    success: bool
    data: Optional[Dict]
    error_message: Optional[str] = None
    source_file: Optional[str] = None

class InvoiceProcessor:
    """Process invoices from PDF files or images"""
    
    SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png'}
    SUPPORTED_EXCEL_FORMATS = {'.xlsx', '.xls', '.csv'}
    
    def __init__(self, together_api_key: str = None, google_api_key: str = None):
        load_dotenv()
        self.together_api_key = os.getenv('TOGETHER_API_KEY') or together_api_key
        self.google_api_key = os.getenv('GOOGLE_API_KEY') or google_api_key
            
        if not all([self.together_api_key, self.google_api_key]):
            raise ValueError("Missing required API keys")
            
        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize API clients"""
        try:
            self.together_client = together.Together(api_key=self.together_api_key)
            genai.configure(api_key=self.google_api_key)
            self.genai_model = genai.GenerativeModel("gemini-1.5-pro")
        except Exception as e:
            raise

    def process_file(self, file_path: Union[str, Path]) -> ProcessingResult:
        """Main entry point for processing files"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return ProcessingResult(
                    success=False,
                    data=None,
                    error_message=f"File not found: {file_path}",
                    source_file=str(file_path)
                )

            if file_path.suffix.lower() in self.SUPPORTED_EXCEL_FORMATS:
                return self._process_excel(file_path)
            elif file_path.suffix.lower() == '.pdf':
                return self._process_pdf(file_path)
            elif file_path.suffix.lower() in self.SUPPORTED_IMAGE_FORMATS:
                return self._process_image(file_path)
            else:
                return ProcessingResult(
                    success=False,
                    data=None,
                    error_message=f"Unsupported file format: {file_path.suffix}",
                    source_file=str(file_path)
                )
            
        except Exception as e:
            return ProcessingResult(
                success=False,
                data=None,
                error_message=str(e),
                source_file=str(file_path)
            )

    def _process_pdf(self, pdf_path: Path) -> ProcessingResult:
        """Process PDF files by converting to images first"""
        try:
            if not pdf_path.exists():
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
                
            images = convert_from_path(
                pdf_path,
                dpi=300,
                fmt='jpeg',
                grayscale=False,
                size=(1800, None)
            )
            
            all_text = []
            for idx, image in enumerate(images, 1):
                enhanced_image = self._enhance_image_for_ocr(image)
                
                try:
                    text = self._extract_invoice_data(enhanced_image)
                    if text:
                        all_text.append(text)
                except Exception:
                    continue

            if not all_text:
                return ProcessingResult(
                    success=False,
                    data=None,
                    error_message="Failed to extract text from all PDF pages",
                    source_file=str(pdf_path)
                )

            combined_text = "\n---PAGE BREAK---\n".join(all_text)
            return self._process_extracted_text(combined_text, pdf_path)

        except Exception as e:
            return ProcessingResult(
                success=False,
                data=None,
                error_message=f"PDF processing error: {str(e)}",
                source_file=str(pdf_path)
            )

    def _enhance_image_for_ocr(self, image: Image.Image) -> Image.Image:
        """Enhance image quality for better OCR results"""
        try:
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            max_dimension = 2000
            if max(image.size) > max_dimension:
                ratio = max_dimension / max(image.size)
                new_size = tuple(int(dim * ratio) for dim in image.size)
                image = image.resize(new_size, Image.LANCZOS)
            
            return image
        except Exception:
            return image

    def _process_image(self, image_path: Path) -> ProcessingResult:
        """Process single image files"""
        try:
            with Image.open(image_path) as img:
                text = self._extract_invoice_data(img)

                if not text:
                    return ProcessingResult(
                        success=False,
                        data=None,
                        error_message="Failed to extract text from image",
                        source_file=str(image_path)
                    )
                return self._process_extracted_text(text, image_path)

        except Exception as e:
            return ProcessingResult(
                success=False,
                data=None,
                error_message=f"Image processing error: {str(e)}",
                source_file=str(image_path)
            )
        
    def _process_excel(self, excel_path: Path) -> ProcessingResult:
        """Process Excel files by converting to tabular text"""
        try:
            df = pd.read_excel(excel_path) if excel_path.suffix in {'.xlsx', '.xls'} else pd.read_csv(excel_path)
            tabular_text = df.to_string(index=False, header=True)
            return self._process_extracted_text(tabular_text, excel_path)

        except Exception as e:
            return ProcessingResult(
                success=False,
                data=None,
                error_message=f"Excel processing error: {str(e)}",
                source_file=str(excel_path)
            )

    def _extract_invoice_data(self, image: Image.Image) -> Optional[str]:
        """Extract text from image using Together AI"""
        try:
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            base64_image = base64.b64encode(img_byte_arr).decode('utf-8')
            logging.info("Requesting extraction from Together AI API.")
            response = self.together_client.chat.completions.create(
                model="meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Convert the provided image into Markdown format. Ensure that all content from the page is included, 
                                       such as headers, footers, subtexts, images (with alt text if possible), tables, and any other elements.
                                        
                                       Requirements:
                                        - Output Only Markdown: Return solely the Markdown content without any additional explanations or comments.
                                        - No Delimiters: Do not use code fences or delimiters like \`\`\`markdown.
                                        - Preserve Numerical Accuracy: Extract and represent numerical values exactly as provided (e.g., "1.000" should NOT be written as "1,000" and vice versa).
                                        - Complete Content: Do not omit any part of the page, including headers, footers, and subtext."""
                        },
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }],
                max_tokens=2048,
                temperature=0.3
            )
            return response.choices[0].message.content
            
        except Exception:
            return None

    def _process_invoice_text(self, text: str) -> str:
        """Process invoice text using Gemini with structured schema"""
        is_tabular = '\n' in text and any(char in text for char in [',', '\t', '|'])
        prompt = f"""
        Parse this {'tabular' if is_tabular else 'invoice'} text into a structured format with exact values and calculations.
        Include all products, customer details, and invoice information.
        
        {'Tabular' if is_tabular else 'Invoice'} Text:
        {text}

        Return the data in a JSON format matching this exact structure:
        {{
            "Invoice": {{
                "SerialNumber": "string",
                "CustomerName": "string",
                "Quantity": number,
                "TotalTax": number,
                "TotalAmount": number,
                "Date": "string"
            }},
            "Products": [
                {{
                    "Name": "string",
                    "Quantity": number,
                    "UnitPrice": number,
                    "Tax": number,
                    "PriceWithTax": number,
                    "Discount": number
                }}
            ],
            "Customer": {{
                "CustomerName": "string",
                "PhoneNumber": "string(10)",
                "TotalPurchaseAmount": number
            }}
        }}
        """
        
        try:
            logging.info("Requesting JSON request from Gemini.")
            response = self.genai_model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json"
                )
            )
            return response.text
        except Exception as e:
            raise

    def _clean_json_response(self, json_str: str) -> str:
        """Clean and validate JSON response"""
        json_str = json_str.replace('```json', '').replace('```', '').strip()
        
        try:
            parsed = json.loads(json_str)
            return json.dumps(parsed)
        except json.JSONDecodeError:
            return json_str

    def _process_extracted_text(self, text: str, source_path: Path) -> ProcessingResult:
        """Process extracted text into structured data"""
        try:
            result = self._process_invoice_text(text)
            clean_json = result
            
            try:
                data = json.loads(clean_json)
                return ProcessingResult(
                    success=True,
                    data=data,
                    source_file=str(source_path)
                )
            except json.JSONDecodeError as e:
                return ProcessingResult(
                    success=False,
                    data=None,
                    error_message=f"Invalid JSON format: {str(e)}",
                    source_file=str(source_path)
                )
            
        except Exception as e:
            return ProcessingResult(
                success=False,
                data=None,
                error_message=f"Text processing error: {str(e)}",
                source_file=str(source_path)
            )

def main():
    """Example usage of the InvoiceProcessor"""
    try:
        processor = InvoiceProcessor()
        
        # Process Excel file
        file_path = "/Users/manpatel/Desktop/automated-invoice/backend/pos_invoice.jpg"
        result = processor.process_file(file_path)
        
        print(result.data)

    except Exception as e:
        print(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()