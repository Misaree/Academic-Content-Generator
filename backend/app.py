from flask import Flask, request, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from text_extraction import extract_text
from text_summarisation import summarize_text
from podcast import generate_podcast
from presentation import create_presentation
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure folders
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "generated"
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            # Extract text from the document
            extracted_text = extract_text(filepath)
            
            # Generate summary
            summary = summarize_text(extracted_text)
            
            # Save summary to a file
            summary_path = os.path.join(OUTPUT_FOLDER, f"{filename}_summary.txt")
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(summary)
            
            return jsonify({
                'message': 'File processed successfully',
                'summary': summary,
                'filename': filename
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/generate', methods=['POST'])
def generate_content():
    data = request.json
    output_type = data.get('type')  # 'podcast' or 'presentation'
    style = data.get('style')  # 'formal' or 'informal' for presentations
    text = data.get('text')
    filename = data.get('filename', 'output')
    
    try:
        if output_type == 'podcast':
            voice_id = data.get('voice_id', "1")  # Default to voice 1
            output_path = os.path.join(OUTPUT_FOLDER, f"{filename}_podcast.mp3")
            success = generate_podcast(text, voice_id)
            if success:
                # Move the generated file to our output path
                os.rename("elevenlabs_output.mp3", output_path)
                return jsonify({
                    'message': 'Podcast generated successfully',
                    'download_url': f'/api/download/{os.path.basename(output_path)}'
                })
            else:
                return jsonify({'error': 'Failed to generate podcast'}), 500
            
        elif output_type == 'presentation':
            output_path = os.path.join(OUTPUT_FOLDER, f"{filename}_presentation.pptx")
            create_presentation(text, output_path, style == 'formal')
            return jsonify({
                'message': 'Presentation generated successfully',
                'download_url': f'/api/download/{os.path.basename(output_path)}'
            })
        else:
            return jsonify({'error': 'Invalid output type'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

@app.route('/')
def serve_frontend():
    return send_file('../frontend/index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_file(f'../frontend/{path}')

if __name__ == '__main__':
    app.run(debug=True, port=5000)