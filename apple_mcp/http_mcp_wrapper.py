#!/usr/bin/env python3
"""
HTTP Wrapper for Tonnage Prediction MCP Server
This makes it easy to integrate with n8n using HTTP Request nodes
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import json
import sys
import os

# Add the current directory to path to import the MCP server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tonnage_mcp_server import MCPServer

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Create a single MCP server instance
mcp_server = MCPServer()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_trained": mcp_server.model_trained
    })

@app.route('/mcp', methods=['POST'])
def handle_mcp_request():
    """Handle MCP protocol requests"""
    try:
        request_data = request.get_json()
        
        # Run async function in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(mcp_server.handle_request(request_data))
        loop.close()
        
        return jsonify(response)
    except Exception as e:
        return jsonify({
            "jsonrpc": "2.0",
            "id": request_data.get("id") if request_data else None,
            "error": {
                "code": -32603,
                "message": str(e)
            }
        }), 500

@app.route('/train', methods=['POST'])
def train_model():
    """Simplified endpoint for training (easier for n8n)"""
    try:
        data = request.get_json()
        csv_path = data.get('csv_path')
        model_type = data.get('model_type', 'random_forest')
        
        # Call the MCP server's train_model
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "train_model",
                "arguments": {
                    "csv_path": csv_path,
                    "model_type": model_type
                }
            }
        }
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(mcp_server.handle_request(mcp_request))
        loop.close()
        
        if "error" in response:
            return jsonify(response["error"]), 400
        
        result = json.loads(response["result"]["content"][0]["text"])
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/predict', methods=['POST'])
def predict():
    """Simplified endpoint for prediction (easier for n8n)"""
    try:
        data = request.get_json()
        
        # Call the MCP server's predict_tonnage
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "predict_tonnage",
                "arguments": {
                    "city": data.get('city'),
                    "customer_id": data.get('customer_id'),
                    "apple_variety": data.get('apple_variety'),
                    "year": data.get('year'),
                    "month": data.get('month')
                }
            }
        }
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(mcp_server.handle_request(mcp_request))
        loop.close()
        
        if "error" in response:
            return jsonify(response["error"]), 400
        
        result = json.loads(response["result"]["content"][0]["text"])
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    """Simplified endpoint for batch prediction (easier for n8n)"""
    try:
        data = request.get_json()
        predictions = data.get('predictions', [])
        
        # Call the MCP server's batch_predict
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "batch_predict",
                "arguments": {
                    "predictions": predictions
                }
            }
        }
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(mcp_server.handle_request(mcp_request))
        loop.close()
        
        if "error" in response:
            return jsonify(response["error"]), 400
        
        result = json.loads(response["result"]["content"][0]["text"])
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/valid-values', methods=['GET'])
def get_valid_values():
    """Simplified endpoint for getting valid values (easier for n8n)"""
    try:
        # Call the MCP server's get_valid_values
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "get_valid_values",
                "arguments": {}
            }
        }
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(mcp_server.handle_request(mcp_request))
        loop.close()
        
        if "error" in response:
            return jsonify(response["error"]), 400
        
        result = json.loads(response["result"]["content"][0]["text"])
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/', methods=['GET'])
def index():
    """Show available endpoints"""
    return jsonify({
        "service": "Tonnage Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "This help page",
            "GET /health": "Health check",
            "POST /train": "Train the model (body: {csv_path, model_type})",
            "POST /predict": "Make a prediction (body: {city, customer_id, apple_variety, year, month})",
            "POST /batch-predict": "Batch predictions (body: {predictions: [...]})",
            "GET /valid-values": "Get valid categorical values",
            "POST /mcp": "Raw MCP protocol endpoint"
        },
        "model_trained": mcp_server.model_trained
    })

if __name__ == '__main__':
    print("="*60)
    print("Tonnage Prediction HTTP Server")
    print("="*60)
    print("\nStarting server on http://localhost:8000")
    print("\nAvailable endpoints:")
    print("  GET  /              - API documentation")
    print("  GET  /health        - Health check")
    print("  POST /train         - Train model")
    print("  POST /predict       - Make prediction")
    print("  POST /batch-predict - Batch predictions")
    print("  GET  /valid-values  - Get valid values")
    print("  POST /mcp           - MCP protocol")
    print("\n" + "="*60)
    
    # Install flask-cors if not already installed
    try:
        import flask_cors
    except ImportError:
        print("\nWARNING: flask-cors not installed. Installing now...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask-cors", "--break-system-packages"])
        print("✓ flask-cors installed\n")
    
    app.run(host='0.0.0.0', port=8000, debug=True)
