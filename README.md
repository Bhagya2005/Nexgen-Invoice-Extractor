# Nexgen Invoice Extractor - Automated Invoice Extraction

This project is an Invoice Management System that allows users to upload and process invoices in various formats (PDF, images, Excel). The system extracts structured data from the invoices and displays it in a user-friendly interface. The project consists of a frontend built with React and a backend built with FastAPI.

![Image Description](https://github.com/Bhagya2005/Nexgen-Invoice-Extractor/blob/main/Screenshot%20(1376).png)
![Image Description](https://github.com/Bhagya2005/Nexgen-Invoice-Extractor/blob/main/Screenshot%20(1377).png)
![Image Description](https://github.com/Bhagya2005/Nexgen-Invoice-Extractor/blob/main/Screenshot%20(1378).png)
![Image Description](https://github.com/Bhagya2005/Nexgen-Invoice-Extractor/blob/main/Screenshot%20(1379).png)
![Image Description](https://github.com/Bhagya2005/Nexgen-Invoice-Extractor/blob/main/Screenshot%20(1380).png)


## Prerequisites

Before you begin, ensure you have the following installed:
- Node.js 
- Python 
- npm 
- git

## Project Structure
```
SWIPE 2/
├── backend/              # Python FastAPI backend
├── invoice-management/   # React frontend
```

## Installation

### Backend Setup
1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
# For Unix/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file: with 2 api's TogetherAI and Gemini API

### Frontend Setup
1. Navigate to the frontend directory:
```bash
cd invoice-management
```

2. Install dependencies:
```bash
npm install
```

## Running the Application


### Start Backend Server
```bash
cd backend
source venv/bin/activate  # If not already activated
venv\Scripts\activate

uvicorn main:app --reload
```
The backend server will start at `http://localhost:8000`

### Start Frontend Development Server
```bash
cd invoice-management
npm start
```
The frontend development server will start at `http://localhost:3000`

## Tech Stack

### Frontend
- React
- Redux Toolkit
- Tailwind CSS
- @tailwindcss/forms

### Backend
- Python
- FastAPI
- Other dependencies listed in requirements.txt


## Backend Architecture

### FastAPI Backend Components

#### InvoiceProcessor
The core component responsible for processing invoice files in various formats:
- Supports PDF, image, and Excel formats
- Utilizes Together AI and Google API for OCR and text extraction
- Implements file type detection and appropriate processing strategies

#### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/process-invoice/` | POST | Processes invoice files and returns structured data |

#### File Processing Pipeline

1. **File Type Detection & Processing**
   - `process_file` method determines file type
   - Specialized handling for each format:
     - PDF → Image conversion
     - Image enhancement for OCR
     - Excel → Tabular text conversion

2. **Text Extraction Flow**
   - OCR processing using Together AI api with Llama-3.2-90B-Vision model
   - Structured data extraction using json MIME of gemini API
   - JSON response formatting

## Frontend Architecture

```
src/
├── components/
│   ├── InvoiceTab.js      # Invoice details view
│   ├── ProductsTab.js     # Product management
│   └── CustomerTab.js     # Customer information
├── store/
│   ├── actions.js         # Redux actions
│   └── reducer.js         # State management logic
├── App.js                 # Main application component
```

## Data Flow

1. User uploads invoice file
2. File sent to backend API
3. Backend processes file:
   - OCR extraction
   - Data structuring
   - JSON response
4. Frontend receives structured data
5. Redux store updates
6. UI components re-render with new data


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
