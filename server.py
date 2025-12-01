from flask import Flask, request, jsonify
from flask_cors import CORS
import app

flask_app = Flask(__name__)
CORS(flask_app)


@flask_app.route('/api/json/search', methods=['POST'])
def handle_search():
    print("processing request")
    data = request.json
    collection = data.get("collection", [])
    sort_by = data.get("sort_by", "")
    target_value = data.get("target_value", "")
    
    result = app.call(collection, sort_by, target_value)
    
    
    if result is None:
        return jsonify({
            "error": "Unauthorized"
        }), 401
        
    return jsonify({
        "result": result
    }), 200

if __name__ == '__main__':
    flask_app.run(debug=True, host='0.0.0.0', port=5000)