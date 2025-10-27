#!/usr/bin/env python3
"""
Integration tests for the Tonnage MCP Server
Tests the complete workflow from training to prediction
"""

import pytest
import json
import tempfile
import os
import pandas as pd
import subprocess
import time
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


@pytest.fixture
def sample_csv():
    """Create a temporary CSV file with realistic sample data"""
    data = {
        'city': ['Riyadh', 'Riyadh', 'Jeddah', 'Jeddah', 'Dammam', 'Riyadh', 'Jeddah', 'Dammam',
                 'Riyadh', 'Jeddah'],
        'customer_id': ['Lulu', 'Carrefour', 'Lulu', 'Carrefour', 'Lulu', 'Lulu', 'Carrefour',
                        'Carrefour', 'Lulu', 'Lulu'],
        'apple_variety': ['fuji', 'gala', 'fuji', 'gala', 'fuji', 'gala', 'fuji', 'gala',
                          'fuji', 'gala'],
        'year': [2024, 2024, 2024, 2024, 2024, 2024, 2024, 2024, 2024, 2024],
        'month': ['jan', 'feb', 'jan', 'feb', 'jan', 'mar', 'mar', 'apr', 'apr', 'may'],
        'tonnage': [100.5, 85.2, 120.8, 95.3, 110.6, 92.1, 115.4, 88.7, 105.2, 118.9]
    }
    df = pd.DataFrame(data)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df.to_csv(f.name, index=False)
        yield f.name

    # Cleanup
    try:
        os.unlink(f.name)
    except:
        pass


class MCPTestClient:
    """Test client for MCP server integration tests"""

    def __init__(self, server_script):
        self.process = subprocess.Popen(
            ['python3', server_script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        self.request_id = 0
        # Give server time to start
        time.sleep(0.5)

    def send_request(self, method, params=None):
        """Send a request to the MCP server"""
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }

        self.process.stdin.write(json.dumps(request) + "\n")
        self.process.stdin.flush()

        response_line = self.process.stdout.readline()
        return json.loads(response_line)

    def close(self):
        """Close the connection"""
        try:
            self.process.stdin.close()
            self.process.terminate()
            self.process.wait(timeout=2)
        except:
            self.process.kill()


@pytest.fixture
def mcp_client():
    """Create an MCP test client"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    server_path = os.path.join(project_root, 'src', 'tonnage_mcp', 'server.py')

    client = MCPTestClient(server_path)
    yield client
    client.close()


class TestCompleteWorkflow:
    """Test complete workflow from initialization to prediction"""

    def test_full_workflow(self, mcp_client, sample_csv):
        """Test the complete workflow: initialize -> list tools -> train -> predict"""

        # Step 1: Initialize
        response = mcp_client.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "integration-test",
                "version": "1.0.0"
            }
        })

        assert response["jsonrpc"] == "2.0"
        assert "result" in response
        assert response["result"]["serverInfo"]["name"] == "tonnage-predictor"

        # Step 2: List tools
        response = mcp_client.send_request("tools/list")

        assert "result" in response
        assert len(response["result"]["tools"]) == 4

        # Step 3: Train model
        response = mcp_client.send_request("tools/call", {
            "name": "train_model",
            "arguments": {
                "csv_path": sample_csv,
                "model_type": "random_forest"
            }
        })

        assert "result" in response
        result = json.loads(response["result"]["content"][0]["text"])
        assert result["status"] == "success"
        assert result["training_samples"] == 10

        # Save valid values for predictions
        valid_values = result["valid_values"]

        # Step 4: Get valid values
        response = mcp_client.send_request("tools/call", {
            "name": "get_valid_values",
            "arguments": {}
        })

        assert "result" in response
        result = json.loads(response["result"]["content"][0]["text"])
        assert result["status"] == "success"
        assert len(result["valid_values"]["cities"]) == 3  # Riyadh, Jeddah, Dammam

        # Step 5: Make single prediction
        response = mcp_client.send_request("tools/call", {
            "name": "predict_tonnage",
            "arguments": {
                "city": valid_values["cities"][0],
                "customer_id": valid_values["customers"][0],
                "apple_variety": valid_values["varieties"][0],
                "year": 2024,
                "month": valid_values["months"][0]
            }
        })

        assert "result" in response
        result = json.loads(response["result"]["content"][0]["text"])
        assert result["status"] == "success"
        assert "prediction" in result
        assert result["prediction"] > 0

        # Step 6: Batch prediction
        response = mcp_client.send_request("tools/call", {
            "name": "batch_predict",
            "arguments": {
                "predictions": [
                    {
                        "city": valid_values["cities"][0],
                        "customer_id": valid_values["customers"][0],
                        "apple_variety": valid_values["varieties"][0],
                        "year": 2024,
                        "month": valid_values["months"][0]
                    },
                    {
                        "city": valid_values["cities"][1] if len(valid_values["cities"]) > 1 else valid_values["cities"][0],
                        "customer_id": valid_values["customers"][1] if len(valid_values["customers"]) > 1 else valid_values["customers"][0],
                        "apple_variety": valid_values["varieties"][1] if len(valid_values["varieties"]) > 1 else valid_values["varieties"][0],
                        "year": 2024,
                        "month": valid_values["months"][1] if len(valid_values["months"]) > 1 else valid_values["months"][0]
                    }
                ]
            }
        })

        assert "result" in response
        result = json.loads(response["result"]["content"][0]["text"])
        assert result["status"] == "success"
        assert result["total"] == 2
        assert result["successful"] == 2


class TestErrorRecovery:
    """Test error handling and recovery"""

    def test_invalid_then_valid_prediction(self, mcp_client, sample_csv):
        """Test that server recovers from invalid input"""

        # Initialize and train
        mcp_client.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0.0"}
        })

        response = mcp_client.send_request("tools/call", {
            "name": "train_model",
            "arguments": {
                "csv_path": sample_csv,
                "model_type": "random_forest"
            }
        })

        result = json.loads(response["result"]["content"][0]["text"])
        valid_values = result["valid_values"]

        # Try invalid prediction
        response = mcp_client.send_request("tools/call", {
            "name": "predict_tonnage",
            "arguments": {
                "city": "InvalidCity",
                "customer_id": "InvalidCustomer",
                "apple_variety": "InvalidVariety",
                "year": 2024,
                "month": "InvalidMonth"
            }
        })

        result = json.loads(response["result"]["content"][0]["text"])
        assert result["status"] == "error"

        # Now try valid prediction - server should still work
        response = mcp_client.send_request("tools/call", {
            "name": "predict_tonnage",
            "arguments": {
                "city": valid_values["cities"][0],
                "customer_id": valid_values["customers"][0],
                "apple_variety": valid_values["varieties"][0],
                "year": 2024,
                "month": valid_values["months"][0]
            }
        })

        result = json.loads(response["result"]["content"][0]["text"])
        assert result["status"] == "success"
        assert "prediction" in result


class TestModelTypes:
    """Test different model types"""

    def test_linear_model(self, mcp_client, sample_csv):
        """Test training with linear model"""

        mcp_client.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0.0"}
        })

        response = mcp_client.send_request("tools/call", {
            "name": "train_model",
            "arguments": {
                "csv_path": sample_csv,
                "model_type": "linear"
            }
        })

        result = json.loads(response["result"]["content"][0]["text"])
        assert result["status"] == "success"
        assert result["model_type"] == "linear"

        # Verify prediction works with linear model
        valid_values = result["valid_values"]
        response = mcp_client.send_request("tools/call", {
            "name": "predict_tonnage",
            "arguments": {
                "city": valid_values["cities"][0],
                "customer_id": valid_values["customers"][0],
                "apple_variety": valid_values["varieties"][0],
                "year": 2024,
                "month": valid_values["months"][0]
            }
        })

        result = json.loads(response["result"]["content"][0]["text"])
        assert result["status"] == "success"
