# Import modul yang diperlukan
import cv2  # OpenCV untuk pemrosesan video
from flask import Flask, render_template, Response
from flask_socketio import SocketIO

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Inisialisasi SocketIO untuk komunikasi real-time
socketio = SocketIO(app)

# Inisialisasi kamera menggunakan OpenCV
camera = cv2.VideoCapture(0)  # Gunakan kamera default (0)

# Fungsi untuk menghasilkan frame dari kamera
def generate_frames():
    while True:
        # Baca frame dari kamera
        success, frame = camera.read()
        
        # Jika pembacaan frame gagal, keluar dari loop
        if not success:
            break
        else:
            # Konversi frame menjadi format JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            # Menghasilkan frame sebagai response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route untuk halaman utama yang menggunakan template 'video_index.html'
@app.route('/')
def index():
    return render_template('video_index.html')

# Event handler untuk koneksi dari client menggunakan SocketIO
@socketio.on('connect')
def handle_connect():
    # Emit pesan respons kepada client bahwa koneksi berhasil
    emit('response', {'data': 'Connected'})

# Main block untuk menjalankan aplikasi saat script dijalankan
if __name__ == '__main__':
    # Menjalankan aplikasi dengan SocketIO, dengan mode debug aktif
    socketio.run(app, debug=True)
