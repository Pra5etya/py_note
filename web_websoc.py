from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk mengirimkan data dari desktop ke web
@app.route('/send_data', methods=['POST'])
def send_data():
    if request.method == 'POST':
        data_from_desktop = request.form['data']
        # Menampilkan data yang diterima dari desktop di konsol Flask
        print("Data yang diterima dari desktop:", data_from_desktop)
        return 'Data berhasil diterima di web'

# Route untuk mengirimkan data dari web ke desktop
@app.route('/get_data', methods=['GET'])
def get_data():
    if request.method == 'GET':
        data_to_desktop = "Data dari web"
        # Menampilkan data yang dikirim ke desktop di konsol Flask
        print("Data yang dikirim ke desktop:", data_to_desktop)
        return jsonify({'data': data_to_desktop})

if __name__ == '__main__':
    app.run(debug=True)
