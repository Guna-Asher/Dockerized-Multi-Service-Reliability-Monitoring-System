from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({'status': 'OK'})

@app.route('/')
def home():
    return jsonify({'message': 'Flask App for Reliability Monitoring Demo'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

