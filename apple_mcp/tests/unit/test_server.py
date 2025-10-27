#!/usr/bin/env python3
"""
Unit tests for the MCP Server
"""

import pytest
import json
import asyncio
import tempfile
import os
import pandas as pd
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from tonnage_mcp.server import MCPServer


@pytest.fixture
def server():
    """Create a fresh server instance for each test"""
    return MCPServer()


@pytest.fixture
def sample_csv():
    """Create a temporary CSV file with sample data"""
    data = {
        'city': ['Riyadh', 'Riyadh', 'Jeddah', 'Jeddah', 'Dammam'],
        'customer_id': ['Lulu', 'Carrefour', 'Lulu', 'Carrefour', 'Lulu'],
        'apple_variety': ['fuji', 'gala', 'fuji', 'gala', 'fuji'],
        'year': [2024, 2024, 2024, 2024, 2024],
        'month': ['jan', 'feb', 'jan', 'feb', 'jan'],
        'tonnage': [100.5, 85.2, 120.8, 95.3, 110.6]
    }
    df = pd.DataFrame(data)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df.to_csv(f.name, index=False)
        yield f.name

    # Cleanup
    os.unlink(f.name)


class TestMCPServerInitialization:
    """Test server initialization"""

    @pytest.mark.asyncio
    async def test_initialize(self, server):
        """Test the initialize method"""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }

        response = await server.handle_request(request)

        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert "result" in response
        assert response["result"]["protocolVersion"] == "2024-11-05"
        assert response["result"]["serverInfo"]["name"] == "tonnage-predictor"
        assert response["result"]["serverInfo"]["version"] == "1.0.0"

    @pytest.mark.asyncio
    async def test_list_tools(self, server):
        """Test the list_tools method"""
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }

        response = await server.handle_request(request)

        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 2
        assert "result" in response
        assert "tools" in response["result"]

        tools = response["result"]["tools"]
        assert len(tools) == 4

        tool_names = [tool["name"] for tool in tools]
        assert "train_model" in tool_names
        assert "predict_tonnage" in tool_names
        assert "get_valid_values" in tool_names
        assert "batch_predict" in tool_names


class TestModelTraining:
    """Test model training functionality"""

    @pytest.mark.asyncio
    async def test_train_model_success(self, server, sample_csv):
        """Test successful model training"""
        request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "train_model",
                "arguments": {
                    "csv_path": sample_csv,
                    "model_type": "random_forest"
                }
            }
        }

        response = await server.handle_request(request)

        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 3
        assert "result" in response

        result = json.loads(response["result"]["content"][0]["text"])
        assert result["status"] == "success"
        assert result["model_type"] == "random_forest"
        assert result["training_samples"] == 5
        assert "metrics" in result
        assert "mae" in result["metrics"]
        assert "r2_score" in result["metrics"]
        assert "valid_values" in result

        # Verify model is trained
        assert server.model_trained is True
        assert server.model is not None
        assert len(server.encoders) == 4

    @pytest.mark.asyncio
    async def test_train_model_invalid_path(self, server):
        """Test training with invalid CSV path"""
        request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "train_model",
                "arguments": {
                    "csv_path": "/invalid/path/to/file.csv",
                    "model_type": "random_forest"
                }
            }
        }

        response = await server.handle_request(request)

        assert response["jsonrpc"] == "2.0"
        assert "result" in response
        result = json.loads(response["result"]["content"][0]["text"])
        assert result["status"] == "error"
        assert "isError" in response["result"]


class TestPrediction:
    """Test prediction functionality"""

    @pytest.mark.asyncio
    async def test_predict_without_training(self, server):
        """Test prediction before training model"""
        request = {
            "jsonrpc": "2.0",
            "id": 5,
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
        }

        response = await server.handle_request(request)

        assert "result" in response
        result = json.loads(response["result"]["content"][0]["text"])
        assert result["status"] == "error"
        assert "not trained" in result["message"].lower()

    @pytest.mark.asyncio
    async def test_predict_after_training(self, server, sample_csv):
        """Test prediction after training model"""
        # First train the model
        train_request = {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "tools/call",
            "params": {
                "name": "train_model",
                "arguments": {
                    "csv_path": sample_csv,
                    "model_type": "random_forest"
                }
            }
        }

        await server.handle_request(train_request)

        # Now make a prediction
        predict_request = {
            "jsonrpc": "2.0",
            "id": 7,
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
        }

        response = await server.handle_request(predict_request)

        assert "result" in response
        result = json.loads(response["result"]["content"][0]["text"])
        assert result["status"] == "success"
        assert "prediction" in result
        assert isinstance(result["prediction"], (int, float))
        assert result["prediction"] > 0
        assert result["inputs"]["city"] == "Riyadh"

    @pytest.mark.asyncio
    async def test_predict_invalid_value(self, server, sample_csv):
        """Test prediction with invalid categorical value"""
        # First train the model
        train_request = {
            "jsonrpc": "2.0",
            "id": 8,
            "method": "tools/call",
            "params": {
                "name": "train_model",
                "arguments": {
                    "csv_path": sample_csv,
                    "model_type": "random_forest"
                }
            }
        }

        await server.handle_request(train_request)

        # Try prediction with invalid city
        predict_request = {
            "jsonrpc": "2.0",
            "id": 9,
            "method": "tools/call",
            "params": {
                "name": "predict_tonnage",
                "arguments": {
                    "city": "InvalidCity",
                    "customer_id": "Lulu",
                    "apple_variety": "fuji",
                    "year": 2024,
                    "month": "jan"
                }
            }
        }

        response = await server.handle_request(predict_request)

        assert "result" in response
        result = json.loads(response["result"]["content"][0]["text"])
        assert result["status"] == "error"
        assert "isError" in response["result"]


class TestValidValues:
    """Test get_valid_values functionality"""

    @pytest.mark.asyncio
    async def test_get_valid_values_without_training(self, server):
        """Test getting valid values before training"""
        request = {
            "jsonrpc": "2.0",
            "id": 10,
            "method": "tools/call",
            "params": {
                "name": "get_valid_values",
                "arguments": {}
            }
        }

        response = await server.handle_request(request)

        assert "result" in response
        result = json.loads(response["result"]["content"][0]["text"])
        assert result["status"] == "error"

    @pytest.mark.asyncio
    async def test_get_valid_values_after_training(self, server, sample_csv):
        """Test getting valid values after training"""
        # First train the model
        train_request = {
            "jsonrpc": "2.0",
            "id": 11,
            "method": "tools/call",
            "params": {
                "name": "train_model",
                "arguments": {
                    "csv_path": sample_csv,
                    "model_type": "random_forest"
                }
            }
        }

        await server.handle_request(train_request)

        # Get valid values
        valid_request = {
            "jsonrpc": "2.0",
            "id": 12,
            "method": "tools/call",
            "params": {
                "name": "get_valid_values",
                "arguments": {}
            }
        }

        response = await server.handle_request(valid_request)

        assert "result" in response
        result = json.loads(response["result"]["content"][0]["text"])
        assert result["status"] == "success"
        assert "valid_values" in result
        assert "cities" in result["valid_values"]
        assert "customers" in result["valid_values"]
        assert "varieties" in result["valid_values"]
        assert "months" in result["valid_values"]
        assert "Riyadh" in result["valid_values"]["cities"]
        assert "Lulu" in result["valid_values"]["customers"]


class TestBatchPredict:
    """Test batch prediction functionality"""

    @pytest.mark.asyncio
    async def test_batch_predict_without_training(self, server):
        """Test batch prediction before training"""
        request = {
            "jsonrpc": "2.0",
            "id": 13,
            "method": "tools/call",
            "params": {
                "name": "batch_predict",
                "arguments": {
                    "predictions": [
                        {
                            "city": "Riyadh",
                            "customer_id": "Lulu",
                            "apple_variety": "fuji",
                            "year": 2024,
                            "month": "jan"
                        }
                    ]
                }
            }
        }

        response = await server.handle_request(request)

        assert "result" in response
        result = json.loads(response["result"]["content"][0]["text"])
        assert result["status"] == "error"

    @pytest.mark.asyncio
    async def test_batch_predict_after_training(self, server, sample_csv):
        """Test batch prediction after training"""
        # First train the model
        train_request = {
            "jsonrpc": "2.0",
            "id": 14,
            "method": "tools/call",
            "params": {
                "name": "train_model",
                "arguments": {
                    "csv_path": sample_csv,
                    "model_type": "random_forest"
                }
            }
        }

        await server.handle_request(train_request)

        # Batch predict
        batch_request = {
            "jsonrpc": "2.0",
            "id": 15,
            "method": "tools/call",
            "params": {
                "name": "batch_predict",
                "arguments": {
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
            }
        }

        response = await server.handle_request(batch_request)

        assert "result" in response
        result = json.loads(response["result"]["content"][0]["text"])
        assert result["status"] == "success"
        assert "predictions" in result
        assert len(result["predictions"]) == 2
        assert result["total"] == 2
        assert result["successful"] == 2

        for pred in result["predictions"]:
            assert pred["status"] == "success"
            assert "prediction" in pred
            assert isinstance(pred["prediction"], (int, float))


class TestErrorHandling:
    """Test error handling"""

    @pytest.mark.asyncio
    async def test_unknown_method(self, server):
        """Test handling of unknown method"""
        request = {
            "jsonrpc": "2.0",
            "id": 16,
            "method": "unknown_method",
            "params": {}
        }

        response = await server.handle_request(request)

        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 16
        assert "error" in response
        assert response["error"]["code"] == -32603

    @pytest.mark.asyncio
    async def test_unknown_tool(self, server):
        """Test calling unknown tool"""
        request = {
            "jsonrpc": "2.0",
            "id": 17,
            "method": "tools/call",
            "params": {
                "name": "unknown_tool",
                "arguments": {}
            }
        }

        response = await server.handle_request(request)

        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 17
        assert "error" in response
