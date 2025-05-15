# Academic Content Generator

A web application that transforms academic documents into summaries, presentations, and podcasts. This tool helps users quickly digest academic content in multiple formats.

## Find the video demo link here: [Watch Demo Video](https://drive.google.com/file/d/1D_qVQ_WdoKHCwdlkgeAzyn-qHXZNnoHA/view?usp=sharing)

## Features

- **Document Processing**
  - Supports PDF, DOCX, and TXT files
  - Extracts text while maintaining document structure
  - Handles multiple file formats efficiently

- **Text Summarization**
  - AI-powered text summarization using BART model
  - Maintains key information while reducing length
  - Processes long documents in chunks for better results

- **Presentation Generation**
  - Two presentation styles:
    - Formal (professional, structured format)
    - Informal (casual, engaging format)
  - Automatic section classification
  - Clean, readable slides
  - Proper formatting and styling

- **Podcast Creation**
  - Convert summaries to audio
  - Multiple voice options (4 different voices)
  - High-quality text-to-speech conversion
  - Easy download and sharing

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
cd backend
python app.py
```

4. Open your web browser and navigate to:
[localhost](http://localhost:5000)


## Usage

1. **Upload Document**
   - Click "Choose File" to select your academic document
   - Supported formats: PDF, DOCX, TXT
   - Click "Upload" to process the document

2. **View Summary**
   - After upload, the AI-generated summary will appear
   - Review the summary for accuracy

3. **Generate Content**
   - Choose your desired output format:
     - **Presentation**: Select formal or informal style
     - **Podcast**: Choose from 4 different voices
   - Click "Generate" to create your content

4. **Download**
   - Click the download link to save your generated content
   - Presentations save as .pptx files
   - Podcasts save as .mp3 files




## Project Structure
```
project/
├── backend/
│ ├── app.py # Main Flask application
│ ├── text_extraction.py # Document text extraction
│ ├── text_summarisation.py # AI summarization
│ ├── podcast.py # Audio generation
│ └── presentation.py # PPT generation
├── frontend/
│ ├── index.html # User interface
│ └── styles.css # Styling
├── uploads/ # Temporary file storage
├── generated/ # Output file storage
└── requirements.txt # Project dependencies
```
## Technical Details

- **Frontend**: HTML5, CSS3
- **Backend**: Python, Flask
- **AI Models**: 
  - BART for text summarization
  - ElevenLabs for text-to-speech
- **Libraries**:
  - `transformers` for AI processing
  - `python-pptx` for presentation generation
  - `PyPDF2` and `python-docx` for document processing
  - `nltk` for text processing

## Requirements

- Python 3.8 or higher
- 2GB free disk space (for ML models)
- Internet connection (for first run and API calls)
- Modern web browser

## Error Handling

The application includes comprehensive error handling for:
- Invalid file formats
- Processing failures
- API connection issues
- File size limitations

## Future Improvements

Potential areas for enhancement:
- Additional presentation templates
- More voice options
- Conversion to video
- Batch processing
- Custom summarization lengths
- Export in more formats

