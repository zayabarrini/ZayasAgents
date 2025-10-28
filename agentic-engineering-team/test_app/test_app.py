from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hello from Agentic Engineering Team!</h1><p>Your application is running successfully!</p>"

@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Test Flask App",
        "version": "1.0.0"
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)