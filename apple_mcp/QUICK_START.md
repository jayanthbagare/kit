# Quick Start Guide - Tonnage Prediction MCP Server

## 🚀 Getting Started

### Prerequisites
```bash
pip install pandas numpy scikit-learn flask flask-cors --break-system-packages
```

## Option 1: HTTP Server (Recommended for n8n)

### Start the Server
```bash
python3 http_mcp_wrapper.py
```

The server will start on `http://localhost:8000`

### Test with curl

1. **Train the model:**
```bash
curl -X POST http://localhost:8000/train \
  -H "Content-Type: application/json" \
  -d '{
    "csv_path": "/path/to/your/data.csv",
    "model_type": "random_forest"
  }'
```

2. **Make a prediction:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Riyadh",
    "customer_id": "Lulu",
    "apple_variety": "fuji",
    "year": 2024,
    "month": "jan"
  }'
```

3. **Get valid values:**
```bash
curl http://localhost:8000/valid-values
```

## Option 2: Pure MCP Server (stdio)

### Test with the test client:
```bash
python3 test_mcp_client.py
```

## 📱 n8n Integration

### Simple n8n Workflow

1. **HTTP Request Node - Train Model (Run Once)**
   - Method: POST
   - URL: `http://localhost:8000/train`
   - Body:
   ```json
   {
     "csv_path": "/absolute/path/to/your/data.csv",
     "model_type": "random_forest"
   }
   ```

2. **HTTP Request Node - Make Prediction**
   - Method: POST
   - URL: `http://localhost:8000/predict`
   - Body:
   ```json
   {
     "city": "{{ $json.city }}",
     "customer_id": "{{ $json.customer_id }}",
     "apple_variety": "{{ $json.apple_variety }}",
     "year": {{ $json.year }},
     "month": "{{ $json.month }}"
   }
   ```

3. **Process Response**
   - The prediction will be in: `{{ $json.prediction }}`

### Example n8n Workflow JSON

```json
{
  "nodes": [
    {
      "parameters": {
        "method": "POST",
        "url": "http://localhost:8000/train",
        "options": {},
        "bodyParametersJson": "{\n  \"csv_path\": \"/path/to/data.csv\",\n  \"model_type\": \"random_forest\"\n}"
      },
      "name": "Train Model",
      "type": "n8n-nodes-base.httpRequest",
      "position": [250, 300]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "http://localhost:8000/predict",
        "options": {},
        "bodyParametersJson": "={\n  \"city\": \"{{ $json.city }}\",\n  \"customer_id\": \"{{ $json.customer_id }}\",\n  \"apple_variety\": \"{{ $json.apple_variety }}\",\n  \"year\": {{ $json.year }},\n  \"month\": \"{{ $json.month }}\"\n}"
      },
      "name": "Predict Tonnage",
      "type": "n8n-nodes-base.httpRequest",
      "position": [450, 300]
    }
  ]
}
```

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API documentation |
| `/health` | GET | Check if server is running |
| `/train` | POST | Train the model |
| `/predict` | POST | Single prediction |
| `/batch-predict` | POST | Multiple predictions |
| `/valid-values` | GET | Get valid categorical values |
| `/mcp` | POST | Raw MCP protocol (advanced) |

## 📝 Example Responses

### Train Model Response
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
    "months": ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
  }
}
```

### Predict Response
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

### Batch Predict Response
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

## 🐛 Troubleshooting

### Error: "Model not trained"
**Solution:** Call the `/train` endpoint first before making predictions

### Error: "Invalid input value"
**Solution:** Use `/valid-values` to see acceptable values. Values must match exactly what's in the training data.

### Error: "Connection refused"
**Solution:** Make sure the server is running:
```bash
python3 http_mcp_wrapper.py
```

### Error: "Module not found"
**Solution:** Install dependencies:
```bash
pip install pandas numpy scikit-learn flask flask-cors --break-system-packages
```

## 💡 Tips

1. **Train once per session** - The model stays in memory until the server restarts
2. **Use batch predict** - More efficient for multiple predictions
3. **Check valid values** - Always verify your inputs against valid values
4. **Health check** - Use `/health` to verify the server and model status
5. **Case sensitive** - All inputs are case-sensitive (e.g., "Riyadh" not "riyadh")

## 🔐 Production Considerations

For production use, consider:
1. Adding authentication (API keys)
2. Implementing rate limiting
3. Using HTTPS
4. Persisting the trained model to disk
5. Adding logging and monitoring
6. Running behind a reverse proxy (nginx)
7. Using environment variables for configuration

## 📚 Files Overview

- `tonnage_mcp_server.py` - Core MCP server (stdio)
- `http_mcp_wrapper.py` - HTTP wrapper for easy integration
- `test_mcp_client.py` - Test client for validation
- `N8N_INTEGRATION_GUIDE.md` - Detailed n8n integration guide
- `mcp_config.json` - MCP configuration file

## Need Help?

Check the detailed guide: `N8N_INTEGRATION_GUIDE.md`
