from flask import Flask, jsonify

app = Flask(__name__)

# Data sederhana untuk contoh
data = {"message": "Halo dari aplikasi web!"}

# Route untuk menerima permintaan dari aplikasi desktop
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
