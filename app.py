from flask import Flask, jsonify, request, render_template
from werkzeug.utils import secure_filename
from yolo_detection_images import detect_objects

app = Flask(__name__)

# Configure a secret key to enable session storage
app.config['SECRET_KEY'] = 'objectdetection_1.1'

# Define the allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/myapp/detectobjects', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save('images/' + filename)
        img_path = 'images/' + filename
        results = detect_objects(img_path)
        
        # Extract labels and confidences from the results
        detections = results.get('detections', {}).get('labels', [])
        
        # Format labels and confidences as plain text with each pair on a separate line
        text_response = '\n'.join([f"{d['label']}: {d['confidence']}" for d in detections])
        
        return text_response
    else:
        return jsonify({'error': 'File type not allowed'})

if __name__ == '__main__':
    app.run(debug=True)
