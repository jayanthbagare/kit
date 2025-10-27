# Tonnage Prediction MCP Server - n8n Integration Guide

## Overview
This MCP server exposes a tonnage prediction model that can be integrated with n8n workflows.

## Files Created
1. `tonnage_mcp_server.py` - The MCP server implementation
2. `mcp_config.json` - Configuration file for MCP clients
3. `test_mcp_client.py` - Test client to verify functionality

## Available Tools

### 1. train_model
Train the prediction model with your CSV data.

**Input:**
```json
{
  "csv_path": "/path/to/your/data.csv",
  "model_type": "random_forest"  // Options: "linear", "ridge", "random_forest"
}
```

**Output:**
```json
{
  "status": "success",
  "model_type": "random_forest",
  "training_samples": 1800,
  "metrics": {
    "mae": 12.34,
    "r2_score": 0.85
  },
  "valid_values": {
    "cities": ["Riyadh", "Jeddah", "Dammam"],
    "customers": ["Lulu", "Carrefour", "Panda"],
    "varieties": ["fuji", "gala", "granny_smith"],
    "months": ["jan", "feb", "mar", ...]
  }
}
```

### 2. predict_tonnage
Make a single tonnage prediction.

**Input:**
```json
{
  "city": "Riyadh",
  "customer_id": "Lulu",
  "apple_variety": "fuji",
  "year": 2024,
  "month": "jan"
}
```

**Output:**
```json
{
  "status": "success",
  "prediction": 74.23,
  "inputs": {
    "city": "Riyadh",
    "customer_id": "Lulu",
    "apple_variety": "fuji",
    "year": 2024,
    "month": "jan"
  }
}
```

### 3. get_valid_values
Get lists of valid categorical values.

**Input:** (none required)

**Output:**
```json
{
  "status": "success",
  "valid_values": {
    "cities": ["Riyadh", "Jeddah", "Dammam"],
    "customers": ["Lulu", "Carrefour", "Panda"],
    "varieties": ["fuji", "gala", "granny_smith"],
    "months": ["jan", "feb", "mar", ...]
  }
}
```

### 4. batch_predict
Make multiple predictions at once.

**Input:**
```json
{
  "predictions": [
    {
      "city": "Riyadh",
      "customer_id": "Lulu",
      "apple_variety": "fuji",
      "year": 2024,
      "month": "jan"
    },
    {
      "city": "Jeddah",
      "customer_id": "Carrefour",
      "apple_variety": "gala",
      "year": 2024,
      "month": "feb"
    }
  ]
}
```

**Output:**
```json
{
  "status": "success",
  "predictions": [
    {
      "status": "success",
      "inputs": {...},
      "prediction": 74.23
    },
    {
      "status": "success",
      "inputs": {...},
      "prediction": 82.45
    }
  ],
  "total": 2,
  "successful": 2
}
```

## Testing the Server

### 1. Test locally with the test client:
```bash
python3 test_mcp_client.py
```

### 2. Manual testing with curl (if you expose via HTTP):
```bash
# Initialize
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {}
  }'

# Train model
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "train_model",
      "arguments": {
        "csv_path": "/path/to/data.csv",
        "model_type": "random_forest"
      }
    }
  }'

# Make prediction
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "predict_tonnage",
      "arguments": {
        "city": "Riyadh",
        "customer_id": "Lulu",
        "apple_variety": "fuji",
        "year": 2024,
        "month": "jan"
      }
    }
  }'
```

## Integrating with n8n

### Option 1: Using n8n's Execute Command Node

1. **Add Execute Command Node** in your n8n workflow
2. **Configure the node:**
   - Command: `python3`
   - Arguments: `/path/to/tonnage_mcp_server.py`
   - Input Mode: `JSON`
3. **Send MCP requests** as JSON input

### Option 2: Using n8n's HTTP Request Node (Recommended)

To use HTTP Request node, you'll need to wrap the MCP server in an HTTP server:

```python
# Add this wrapper (create http_mcp_wrapper.py):
from flask import Flask, request, jsonify
import asyncio
from tonnage_mcp_server import MCPServer

app = Flask(__name__)
server = MCPServer()

@app.route('/mcp', methods=['POST'])
async def handle_mcp():
    request_data = request.get_json()
    response = await server.handle_request(request_data)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

Then in n8n:
1. **Add HTTP Request Node**
2. **Configure:**
   - Method: POST
   - URL: `http://localhost:8000/mcp`
   - Body Content Type: JSON
   - Body:
   ```json
   {
     "jsonrpc": "2.0",
     "id": 1,
     "method": "tools/call",
     "params": {
       "name": "predict_tonnage",
       "arguments": {
         "city": "{{ $json.city }}",
         "customer_id": "{{ $json.customer_id }}",
         "apple_variety": "{{ $json.apple_variety }}",
         "year": {{ $json.year }},
         "month": "{{ $json.month }}"
       }
     }
   }
   ```

### Option 3: Using MCP Client in n8n (if n8n supports MCP natively)

1. Install the MCP server configuration
2. Configure n8n to use the MCP server:
   ```json
   {
     "mcpServers": {
       "tonnage-predictor": {
         "command": "python3",
         "args": ["/path/to/tonnage_mcp_server.py"]
       }
     }
   }
   ```
3. Use the MCP tools directly in your n8n workflow

## Example n8n Workflow

```
[Webhook/Trigger] 
    ↓
[HTTP Request: Train Model] (run once)
    ↓
[Set Variables: Extract valid values]
    ↓
[HTTP Request: Predict Tonnage] (for each input)
    ↓
[Process Results]
    ↓
[Output/Send Response]
```

## Running the Server

### Development (stdio mode):
```bash
python3 tonnage_mcp_server.py
```

### Production (HTTP mode - requires wrapper):
```bash
python3 http_mcp_wrapper.py
```

## Requirements
```
pandas
numpy
scikit-learn
flask (for HTTP wrapper)
```

Install with:
```bash
pip install pandas numpy scikit-learn flask
```

## Troubleshooting

### Model not trained error
- Make sure to call `train_model` before making predictions
- The model training is session-based and doesn't persist

### Invalid input values
- Use `get_valid_values` to see what values are acceptable
- Values must exactly match what's in the training data

### Connection issues with n8n
- Make sure the server is running and accessible
- Check firewall settings if using HTTP mode
- Verify the correct port and URL in n8n configuration

## Security Considerations

1. **Authentication**: Add API key authentication for production
2. **Rate Limiting**: Implement rate limiting to prevent abuse
3. **Input Validation**: Server validates inputs but add extra validation in n8n
4. **HTTPS**: Use HTTPS in production environments
5. **Model Persistence**: Consider saving trained models to disk for persistence

## Next Steps

1. Test the MCP server locally using `test_mcp_client.py`
2. Create the HTTP wrapper if using n8n's HTTP Request node
3. Set up your n8n workflow with the appropriate nodes
4. Train the model once at workflow startup
5. Use predict_tonnage for individual predictions
6. Use batch_predict for bulk operations
