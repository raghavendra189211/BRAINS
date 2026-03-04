import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Config
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super-secret-key')
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

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
    if len(parts) >= 2:
        initials = (parts[0][0] + parts[-1][0]).upper()
    elif parts:
        initials = parts[0][:2].upper()
    else:
        initials = 'U'

    return render_template(
        'dashboard.html',
        user_name=name,
        user_initials=initials,
        is_new_user=is_new
    )


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    file.save(filepath)

    mock_result = {
        'success': True,
        'breed': 'Golden Retriever',
        'breed_confidence': 98.5,
        'disease_detected': 'None',
        'disease_confidence': 99.1,
        'image_url': f"/static/uploads/{filename}"
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


# ✅ Important for Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
