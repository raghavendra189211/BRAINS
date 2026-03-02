import os
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change for production
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action')
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        name = fullname or (email.split('@')[0].title() if email else 'User')
        is_new = 'true' if action == 'register' else 'false'
        return redirect(url_for('dashboard', name=name, is_new=is_new))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    name = request.args.get('name', 'User')
    is_new_str = request.args.get('is_new', 'false')
    is_new = is_new_str.lower() == 'true'
    parts = [p.strip() for p in name.split() if p.strip()]
    initials = (parts[0][0] + parts[-1][0]).upper() if len(parts) >= 2 else (parts[0][:2].upper() if parts else 'U')
    return render_template('dashboard.html', user_name=name, user_initials=initials, is_new_user=is_new)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Here we would call the ML service
        # classification_result = predict_breed_and_disease(filepath)
        
        # Mock result for now
        mock_result = {
            'success': True,
            'breed': 'Golden Retriever',
            'breed_confidence': 98.5,
            'disease_detected': 'None',
            'disease_confidence': 99.1,
            'image_url': f"/static/uploads/{file.filename}"
        }
        
        return jsonify(mock_result)

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/pet/<pet_name>')
def pet_dashboard(pet_name):
    return render_template('pet_dashboard.html', pet_name=pet_name.title())

@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
