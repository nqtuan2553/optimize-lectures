from flask import Flask, request, jsonify
from flask_cors import CORS
from services import generate_lecture_content

app = Flask(__name__)
CORS(app)

@app.route('/api/generate-lecture', methods=['POST'])
def generate_lecture():
    try:
        data = request.json
        print(" [INFO] Data received from Frontend:", data) 
        
        if not data:
            return jsonify({"error": "No data provided"}), 400

        result_text = generate_lecture_content(data)
        
        return jsonify({"result": result_text})

    except Exception as e:
        print(f" [ERROR] Server error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Server Backend is running on port 5000...")
    app.run(debug=True, port=5000)