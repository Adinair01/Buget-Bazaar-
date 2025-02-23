from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['sell_your_treasures']
collection = db['items']

# Configure file upload settings
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/submit', methods=['POST'])
def submit_form():
    if 'product-photo' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['product-photo']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    data = request.form
    product_name = data.get('product-name')
    product_type = data.get('product-type')
    phone_number = data.get('phone-number')
    hostel_room = data.get('email')
    
    document = {
        "product_name": product_name,
        "product_type": product_type,
        "phone_number": phone_number,
        "hostel_room": hostel_room,
        "product_photo": filename  # Store the filename or URL if you want to use it later
    }
    
    result = collection.insert_one(document)
    return jsonify({"id": str(result.inserted_id)}), 201

if __name__ == '__main__':
    app.run(debug=True)
