#!/usr/bin/env python3
"""
Unit tests for the HTTP Wrapper
"""

import pytest
import json
import tempfile
import os
import pandas as pd
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from tonnage_mcp.http_wrapper import app, mcp_server


@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


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


@pytest.fixture(autouse=True)
def reset_server():
    """Reset the MCP server state before each test"""
    mcp_server.model = None
    mcp_server.encoders = {}
    mcp_server.model_trained = False
    yield


class TestHealthEndpoint:
    """Test the health check endpoint"""

    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200

        data = response.get_json()
        assert data['status'] == 'healthy'
        assert 'model_trained' in data
        assert data['model_trained'] is False


class TestIndexEndpoint:
    """Test the index endpoint"""

    def test_index(self, client):
        """Test index endpoint"""
        response = client.get('/')
        assert response.status_code == 200

        data = response.get_json()
        assert data['service'] == 'Tonnage Prediction API'
        assert data['version'] == '1.0.0'
        assert 'endpoints' in data
        assert 'model_trained' in data


class TestTrainEndpoint:
    """Test the train endpoint"""

    def test_train_success(self, client, sample_csv):
        """Test successful training via HTTP endpoint"""
        response = client.post('/train',
                               json={
                                   'csv_path': sample_csv,
                                   'model_type': 'random_forest'
                               })
        assert response.status_code == 200

        data = response.get_json()
        assert data['status'] == 'success'
        assert data['model_type'] == 'random_forest'
        assert data['training_samples'] == 5
        assert 'metrics' in data

    def test_train_invalid_path(self, client):
        """Test training with invalid CSV path"""
        response = client.post('/train',
                               json={
                                   'csv_path': '/invalid/path.csv',
                                   'model_type': 'random_forest'
                               })

        data = response.get_json()
        # Check for error in response (may be 200 with error status or 400/500)
        assert response.status_code in [200, 400, 500]
        assert data['status'] == 'error'


class TestPredictEndpoint:
    """Test the predict endpoint"""

    def test_predict_without_training(self, client):
        """Test prediction without training"""
        response = client.post('/predict',
                               json={
                                   'city': 'Riyadh',
                                   'customer_id': 'Lulu',
                                   'apple_variety': 'fuji',
                                   'year': 2024,
                                   'month': 'jan'
                               })

        data = response.get_json()
        # Check for error in response (may be 200 with error status or 400/500)
        assert response.status_code in [200, 400, 500]
        assert data['status'] == 'error'

    def test_predict_after_training(self, client, sample_csv):
        """Test prediction after training"""
        # First train
        client.post('/train',
                    json={
                        'csv_path': sample_csv,
                        'model_type': 'random_forest'
                    })

        # Now predict
        response = client.post('/predict',
                               json={
                                   'city': 'Riyadh',
                                   'customer_id': 'Lulu',
                                   'apple_variety': 'fuji',
                                   'year': 2024,
                                   'month': 'jan'
                               })
        assert response.status_code == 200

        data = response.get_json()
        assert data['status'] == 'success'
        assert 'prediction' in data
        assert isinstance(data['prediction'], (int, float))
        assert data['prediction'] > 0


class TestBatchPredictEndpoint:
    """Test the batch predict endpoint"""

    def test_batch_predict_without_training(self, client):
        """Test batch prediction without training"""
        response = client.post('/batch-predict',
                               json={
                                   'predictions': [
                                       {
                                           'city': 'Riyadh',
                                           'customer_id': 'Lulu',
                                           'apple_variety': 'fuji',
                                           'year': 2024,
                                           'month': 'jan'
                                       }
                                   ]
                               })

        data = response.get_json()
        # Check for error in response (may be 200 with error status or 400/500)
        assert response.status_code in [200, 400, 500]
        assert data['status'] == 'error'

    def test_batch_predict_after_training(self, client, sample_csv):
        """Test batch prediction after training"""
        # First train
        client.post('/train',
                    json={
                        'csv_path': sample_csv,
                        'model_type': 'random_forest'
                    })

        # Now batch predict
        response = client.post('/batch-predict',
                               json={
                                   'predictions': [
                                       {
                                           'city': 'Riyadh',
                                           'customer_id': 'Lulu',
                                           'apple_variety': 'fuji',
                                           'year': 2024,
                                           'month': 'jan'
                                       },
                                       {
                                           'city': 'Jeddah',
                                           'customer_id': 'Carrefour',
                                           'apple_variety': 'gala',
                                           'year': 2024,
                                           'month': 'feb'
                                       }
                                   ]
                               })
        assert response.status_code == 200

        data = response.get_json()
        assert data['status'] == 'success'
        assert 'predictions' in data
        assert data['total'] == 2
        assert data['successful'] == 2


class TestValidValuesEndpoint:
    """Test the valid values endpoint"""

    def test_valid_values_without_training(self, client):
        """Test getting valid values without training"""
        response = client.get('/valid-values')

        data = response.get_json()
        # Check for error in response (may be 200 with error status or 400/500)
        assert response.status_code in [200, 400, 500]
        assert data['status'] == 'error'

    def test_valid_values_after_training(self, client, sample_csv):
        """Test getting valid values after training"""
        # First train
        client.post('/train',
                    json={
                        'csv_path': sample_csv,
                        'model_type': 'random_forest'
                    })

        # Get valid values
        response = client.get('/valid-values')
        assert response.status_code == 200

        data = response.get_json()
        assert data['status'] == 'success'
        assert 'valid_values' in data
        assert 'cities' in data['valid_values']
        assert 'customers' in data['valid_values']
        assert 'varieties' in data['valid_values']
        assert 'months' in data['valid_values']


class TestMCPEndpoint:
    """Test the raw MCP protocol endpoint"""

    def test_mcp_initialize(self, client):
        """Test MCP initialize via HTTP"""
        response = client.post('/mcp',
                               json={
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
                               })
        assert response.status_code == 200

        data = response.get_json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 1
        assert "result" in data

    def test_mcp_list_tools(self, client):
        """Test MCP list tools via HTTP"""
        response = client.post('/mcp',
                               json={
                                   "jsonrpc": "2.0",
                                   "id": 2,
                                   "method": "tools/list",
                                   "params": {}
                               })
        assert response.status_code == 200

        data = response.get_json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 2
        assert "result" in data
        assert "tools" in data["result"]
