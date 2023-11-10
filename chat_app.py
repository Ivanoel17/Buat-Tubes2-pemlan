from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Inisialisasi objek SocketIO yang terkait dengan aplikasi Flask
socketio = SocketIO(app)

# Route untuk halaman utama yang menggunakan template 'index.html'
@app.route('/')
def index():
    return render_template('index.html')

# Event handler untuk event 'message' dari client
@socketio.on('message')
def handle_message(msg):
    # Mencetak pesan ke konsol server
    print('Message:', msg)
    
    # Mengirim kembali pesan ke semua klien yang terhubung (broadcast=True)
    emit('message', msg, broadcast=True)

# Blok utama untuk menjalankan aplikasi saat script dijalankan
if __name__ == '__main__':
    # Menjalankan aplikasi dengan SocketIO, dengan mode debug aktif
    socketio.run(app, debug=True)
