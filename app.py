"""
File Compressor - Enhanced version with batch processing, video support, and more
"""
import os
import io
import json
import uuid
import hashlib
from datetime import datetime
from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify, session
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path
from PIL import Image
import img2pdf
import tempfile
import shutil
import zipfile
import subprocess
import threading
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB for videos
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'mp4', 'avi', 'mov', 'mkv', 'zip'}

# In-memory storage for demo (use database in production)
users = {}  # username: {password_hash, history: []}
compression_tasks = {}  # task_id: {status, progress, result}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_size_mb(filepath):
    """Get file size in MB"""
    return os.path.getsize(filepath) / (1024 * 1024)

def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def compress_pdf(input_path, output_path, target_size_mb=None, quality=85, dpi=250, task_id=None):
    """Compress a PDF file"""
    if task_id:
        compression_tasks[task_id]['progress'] = 10
    
    images = convert_from_path(input_path, dpi=dpi)
    
    if task_id:
        compression_tasks[task_id]['progress'] = 30
    
    temp_images = []
    temp_dir = tempfile.mkdtemp()
    
    try:
        for i, img in enumerate(images):
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            temp_path = os.path.join(temp_dir, f'page_{i}.jpg')
            img.save(temp_path, 'JPEG', quality=quality, optimize=True)
            temp_images.append(temp_path)
            
            if task_id:
                compression_tasks[task_id]['progress'] = 30 + (40 * (i + 1) / len(images))
        
        with open(output_path, 'wb') as f:
            f.write(img2pdf.convert(temp_images))
        
        if task_id:
            compression_tasks[task_id]['progress'] = 80
        
        # If target size specified, adjust quality
        if target_size_mb:
            current_size = get_file_size_mb(output_path)
            if current_size > target_size_mb and quality > 50:
                new_quality = int(quality * 0.9)
                new_dpi = int(dpi * 0.95)
                return compress_pdf(input_path, output_path, target_size_mb, new_quality, new_dpi, task_id)
    
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    if task_id:
        compression_tasks[task_id]['progress'] = 100
    
    return get_file_size_mb(output_path)

def compress_image(input_path, output_path, target_size_mb=None, quality=85, task_id=None):
    """Compress an image file"""
    if task_id:
        compression_tasks[task_id]['progress'] = 20
    
    img = Image.open(input_path)
    
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
        img = background
    
    if task_id:
        compression_tasks[task_id]['progress'] = 60
    
    img.save(output_path, 'JPEG', quality=quality, optimize=True)
    
    if target_size_mb:
        current_size = get_file_size_mb(output_path)
        if current_size > target_size_mb and quality > 30:
            new_quality = int(quality * 0.85)
            return compress_image(input_path, output_path, target_size_mb, new_quality, task_id)
    
    if task_id:
        compression_tasks[task_id]['progress'] = 100
    
    return get_file_size_mb(output_path)

def compress_video(input_path, output_path, target_size_mb=None, quality='medium', task_id=None):
    """Compress a video file using ffmpeg"""
    if task_id:
        compression_tasks[task_id]['progress'] = 10
    
    # Quality presets
    crf_values = {
        'low': 32,      # More compression
        'medium': 28,   # Balanced
        'high': 23,     # Less compression, better quality
        'maximum': 18   # Minimal compression
    }
    
    crf = crf_values.get(quality, 28)
    
    try:
        # Build ffmpeg command
        cmd = [
            'ffmpeg', '-i', input_path,
            '-c:v', 'libx264',  # Video codec
            '-crf', str(crf),   # Quality level
            '-preset', 'medium', # Encoding speed
            '-c:a', 'aac',      # Audio codec
            '-b:a', '128k',     # Audio bitrate
            '-y',               # Overwrite output
            output_path
        ]
        
        # Run compression
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Monitor progress
        for line in process.stderr:
            if task_id and 'time=' in line:
                compression_tasks[task_id]['progress'] = min(90, compression_tasks[task_id]['progress'] + 1)
        
        process.wait()
        
        if process.returncode != 0:
            raise Exception("Video compression failed")
        
        # If target size specified and file too large, compress more
        if target_size_mb:
            current_size = get_file_size_mb(output_path)
            if current_size > target_size_mb and crf < 35:
                new_crf = crf + 3
                return compress_video(input_path, output_path, target_size_mb, new_crf, task_id)
        
        if task_id:
            compression_tasks[task_id]['progress'] = 100
        
        return get_file_size_mb(output_path)
    
    except Exception as e:
        if task_id:
            compression_tasks[task_id]['status'] = 'failed'
            compression_tasks[task_id]['error'] = str(e)
        raise

def compress_zip(input_path, output_path, task_id=None):
    """Compress a ZIP file by re-compressing with maximum compression"""
    if task_id:
        compression_tasks[task_id]['progress'] = 10
    
    with zipfile.ZipFile(input_path, 'r') as zip_in:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zip_out:
            files = zip_in.namelist()
            for i, file in enumerate(files):
                zip_out.writestr(file, zip_in.read(file))
                
                if task_id:
                    compression_tasks[task_id]['progress'] = 10 + (80 * (i + 1) / len(files))
    
    if task_id:
        compression_tasks[task_id]['progress'] = 100
    
    return get_file_size_mb(output_path)

def determine_optimal_size(file_path, file_type):
    """Automatically determine optimal compression size"""
    original_size = get_file_size_mb(file_path)
    
    # Aim for 50-70% reduction for most files
    if file_type == 'pdf':
        return original_size * 0.4  # 60% reduction
    elif file_type in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp']:
        return original_size * 0.5  # 50% reduction
    elif file_type in ['mp4', 'avi', 'mov', 'mkv']:
        return original_size * 0.6  # 40% reduction
    elif file_type == 'zip':
        return original_size * 0.8  # 20% reduction
    
    return original_size * 0.5  # Default 50%

def process_compression(file_info, task_id):
    """Background task to process compression"""
    try:
        compression_tasks[task_id]['status'] = 'processing'
        compression_tasks[task_id]['progress'] = 0
        
        input_path = file_info['input_path']
        output_path = file_info['output_path']
        file_type = file_info['file_type']
        target_size = file_info.get('target_size')
        quality = file_info.get('quality', 85)
        mode = file_info.get('mode', 'auto')
        
        # Determine target size if auto mode
        if mode == 'auto' and not target_size:
            target_size = determine_optimal_size(input_path, file_type)
        
        # Compress based on type
        if file_type == 'pdf':
            final_size = compress_pdf(input_path, output_path, target_size, quality, task_id=task_id)
        elif file_type in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp']:
            final_size = compress_image(input_path, output_path, target_size, quality, task_id=task_id)
        elif file_type in ['mp4', 'avi', 'mov', 'mkv']:
            quality_level = 'medium' if quality >= 70 else 'low' if quality >= 50 else 'high'
            final_size = compress_video(input_path, output_path, target_size, quality_level, task_id=task_id)
        elif file_type == 'zip':
            final_size = compress_zip(input_path, output_path, task_id=task_id)
        
        compression_tasks[task_id]['status'] = 'completed'
        compression_tasks[task_id]['final_size'] = final_size
        compression_tasks[task_id]['original_size'] = file_info['original_size']
        compression_tasks[task_id]['output_path'] = output_path
        
        # Save to history if user is logged in
        if 'username' in file_info and file_info['username'] in users:
            users[file_info['username']]['history'].append({
                'filename': file_info['filename'],
                'original_size': file_info['original_size'],
                'final_size': final_size,
                'compression_ratio': ((file_info['original_size'] - final_size) / file_info['original_size'] * 100),
                'timestamp': datetime.now().isoformat()
            })
    
    except Exception as e:
        compression_tasks[task_id]['status'] = 'failed'
        compression_tasks[task_id]['error'] = str(e)
    
    finally:
        # Clean up input file
        try:
            if os.path.exists(input_path):
                os.remove(input_path)
        except:
            pass

@app.route('/')
def index():
    history = []
    if 'username' in session and session['username'] in users:
        history = users[session['username']]['history'][-10:]  # Last 10 compressions
    return render_template('index_enhanced.html', history=history)

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    if username in users:
        return jsonify({'error': 'Username already exists'}), 400
    
    users[username] = {
        'password_hash': hash_password(password),
        'history': []
    }
    
    session['username'] = username
    return jsonify({'success': True})

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username not in users:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if users[username]['password_hash'] != hash_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    session['username'] = username
    return jsonify({'success': True})

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/compress', methods=['POST'])
def compress():
    if 'files' not in request.files:
        return jsonify({'error': 'No files selected'}), 400
    
    files = request.files.getlist('files')
    mode = request.form.get('mode', 'auto')  # 'auto' or 'manual'
    target_size = request.form.get('target_size', type=float) if mode == 'manual' else None
    quality = request.form.get('quality', type=int, default=85)
    
    # Handle batch processing
    task_ids = []
    
    for file in files:
        if file.filename == '' or not allowed_file(file.filename):
            continue
        
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        file_type = ext[1:].lower()
        
        # Save uploaded file
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}_{filename}")
        file.save(input_path)
        
        original_size = get_file_size_mb(input_path)
        
        # Create output filename
        output_filename = f"{name}_compressed{ext if file_type in ['pdf', 'zip'] else '.mp4' if file_type in ['mp4', 'avi', 'mov', 'mkv'] else '.jpg'}"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}_{output_filename}")
        
        # Create task
        task_id = str(uuid.uuid4())
        compression_tasks[task_id] = {
            'status': 'queued',
            'progress': 0,
            'filename': filename,
            'output_filename': output_filename
        }
        
        # Start compression in background
        file_info = {
            'input_path': input_path,
            'output_path': output_path,
            'file_type': file_type,
            'target_size': target_size,
            'quality': quality,
            'mode': mode,
            'original_size': original_size,
            'filename': filename,
            'username': session.get('username')
        }
        
        thread = threading.Thread(target=process_compression, args=(file_info, task_id))
        thread.daemon = True
        thread.start()
        
        task_ids.append(task_id)
    
    return jsonify({'task_ids': task_ids})

@app.route('/status/<task_id>')
def get_status(task_id):
    if task_id not in compression_tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    task = compression_tasks[task_id]
    return jsonify({
        'status': task['status'],
        'progress': task.get('progress', 0),
        'filename': task.get('filename'),
        'original_size': task.get('original_size'),
        'final_size': task.get('final_size'),
        'error': task.get('error')
    })

@app.route('/download/<task_id>')
def download(task_id):
    if task_id not in compression_tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    task = compression_tasks[task_id]
    
    if task['status'] != 'completed':
        return jsonify({'error': 'Task not completed'}), 400
    
    output_path = task['output_path']
    output_filename = task['output_filename']
    
    return send_file(
        output_path,
        as_attachment=True,
        download_name=output_filename
    )

@app.route('/history')
@login_required
def get_history():
    username = session['username']
    history = users[username]['history']
    return jsonify({'history': history})

@app.route('/preview/<task_id>')
def preview(task_id):
    """Generate preview comparison"""
    if task_id not in compression_tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    task = compression_tasks[task_id]
    
    return jsonify({
        'original_size': task.get('original_size', 0),
        'final_size': task.get('final_size', 0),
        'reduction': ((task.get('original_size', 1) - task.get('final_size', 0)) / task.get('original_size', 1) * 100) if task.get('original_size') else 0
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
