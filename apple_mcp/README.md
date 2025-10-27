# Apple Tonnage Prediction MCP Server

A Model Context Protocol (MCP) server for predicting apple tonnage based on historical data. This server provides machine learning capabilities for predicting apple shipment volumes based on city, customer, variety, and time period.

## Features

- MCP protocol compliant server for integration with various AI assistants
- HTTP REST API wrapper for easy integration with tools like n8n
- Random Forest and Linear Regression models
- Batch prediction support
- Comprehensive test coverage

## Project Structure

```
apple_mcp/
├── src/
│   └── tonnage_mcp/
│       ├── __init__.py
│       ├── server.py          # Main MCP server
│       └── http_wrapper.py    # HTTP REST API wrapper
├── tests/
│   ├── unit/                  # Unit tests
│   │   ├── test_server.py
│   │   └── test_http_wrapper.py
│   └── integration/           # Integration tests
│       └── test_integration.py
├── examples/
│   └── client_example.py      # Example client usage
├── docs/
│   ├── QUICK_START.md
│   └── N8N_INTEGRATION_GUIDE.md
├── config/
│   └── mcp_config.json        # MCP configuration
├── requirements.txt
├── setup.py
└── pytest.ini
```

## Installation

### From Source

1. Clone the repository:
```bash
git clone <repository-url>
cd apple_mcp
```

2. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### For Development

Install with development dependencies:
```bash
pip install -e ".[dev]"
```

## Quick Start

### Using the MCP Server

1. Prepare your training data in CSV format with columns:
   - city
   - customer_id
   - apple_variety
   - year
   - month
   - tonnage

2. Run the MCP server:
```bash
python3 src/tonnage_mcp/server.py
```

3. Use the example client:
```bash
python3 examples/client_example.py
```

### Using the HTTP API

1. Start the HTTP server:
```bash
python3 src/tonnage_mcp/http_wrapper.py
```

2. The server will be available at `http://localhost:8000`

#### Available HTTP Endpoints

- `GET /` - API documentation
- `GET /health` - Health check
- `POST /train` - Train the model
  ```json
  {
    "csv_path": "/path/to/data.csv",
    "model_type": "random_forest"
  }
  ```
- `POST /predict` - Make a prediction
  ```json
  {
    "city": "Riyadh",
    "customer_id": "Lulu",
    "apple_variety": "fuji",
    "year": 2024,
    "month": "jan"
  }
  ```
- `POST /batch-predict` - Batch predictions
- `GET /valid-values` - Get valid categorical values

## Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test Types

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Run with coverage report
pytest --cov=src/tonnage_mcp --cov-report=html
```

### Test Coverage

The project includes comprehensive test coverage:
- Unit tests for server functionality
- Unit tests for HTTP wrapper
- Integration tests for complete workflows
- Error handling and recovery tests

## Development

### Code Style

The project uses:
- `black` for code formatting
- `flake8` for linting
- `mypy` for type checking

Run formatting:
```bash
black src/ tests/
flake8 src/ tests/
mypy src/
```

### Adding New Features

1. Write tests first (TDD approach)
2. Implement the feature
3. Ensure all tests pass
4. Update documentation

## MCP Tools

The server provides the following MCP tools:

### train_model
Train the tonnage prediction model with CSV data.

**Parameters:**
- `csv_path` (required): Path to the CSV file
- `model_type` (optional): "linear", "ridge", or "random_forest" (default: "random_forest")

### predict_tonnage
Predict tonnage for a single record.

**Parameters:**
- `city` (required): City name
- `customer_id` (required): Customer ID
- `apple_variety` (required): Apple variety
- `year` (required): Year
- `month` (required): Month

### batch_predict
Predict tonnage for multiple records at once.

**Parameters:**
- `predictions` (required): Array of prediction objects

### get_valid_values
Get list of valid values for categorical fields.

## Configuration

### MCP Configuration

Edit `config/mcp_config.json` to configure the MCP server for your environment:

```json
{
  "mcpServers": {
    "tonnage-predictor": {
      "command": "python3",
      "args": ["${PROJECT_ROOT}/src/tonnage_mcp/server.py"],
      "env": {},
      "description": "Tonnage prediction model server"
    }
  }
}
```

Replace `${PROJECT_ROOT}` with your actual project path.

## Documentation

- [Quick Start Guide](docs/QUICK_START.md)
- [n8n Integration Guide](docs/N8N_INTEGRATION_GUIDE.md)

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. **CSV file not found**: Use absolute paths for CSV files

3. **Port already in use**: Change the port in `http_wrapper.py` or kill the process using the port

### Getting Help

If you encounter issues:
1. Check the documentation in the `docs/` folder
2. Review the example client in `examples/`
3. Open an issue on GitHub

## License

[Your License Here]

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## Authors

[Your Name/Organization]

## Acknowledgments

Built using the Model Context Protocol (MCP) specification.
