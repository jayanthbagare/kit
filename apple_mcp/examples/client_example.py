#!/usr/bin/env python3
"""
Test client for the Tonnage Prediction MCP Server
"""

import json
import subprocess
import sys
import os

class MCPClient:
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
        self.process.stdin.close()
        self.process.terminate()
        self.process.wait()


def main():
    print("="*60)
    print("Testing Tonnage Prediction MCP Server")
    print("="*60)
    
    # Start the MCP client
    # Get the project root directory and construct path to server
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    server_path = os.path.join(project_root, 'src', 'tonnage_mcp', 'server.py')
    client = MCPClient(server_path)
    
    try:
        # Step 1: Initialize
        print("\n1. Initializing server...")
        response = client.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        })
        print(f"✓ Initialized: {response['result']['serverInfo']['name']}")
        
        # Step 2: List tools
        print("\n2. Listing available tools...")
        response = client.send_request("tools/list")
        tools = response['result']['tools']
        print(f"✓ Available tools: {len(tools)}")
        for tool in tools:
            print(f"   - {tool['name']}: {tool['description']}")
        
        # Step 3: Train model
        print("\n3. Training model...")
        csv_path = input("Enter path to CSV file (or press Enter to skip): ").strip()
        
        if csv_path:
            response = client.send_request("tools/call", {
                "name": "train_model",
                "arguments": {
                    "csv_path": csv_path,
                    "model_type": "random_forest"
                }
            })
            
            result = json.loads(response['result']['content'][0]['text'])
            if result['status'] == 'success':
                print(f"✓ Model trained successfully!")
                print(f"   Training samples: {result['training_samples']}")
                print(f"   MAE: {result['metrics']['mae']:.4f}")
                print(f"   R² Score: {result['metrics']['r2_score']:.4f}")
                
                # Step 4: Get valid values
                print("\n4. Getting valid values...")
                response = client.send_request("tools/call", {
                    "name": "get_valid_values",
                    "arguments": {}
                })
                
                result = json.loads(response['result']['content'][0]['text'])
                valid_values = result['valid_values']
                print(f"✓ Valid values:")
                print(f"   Cities: {valid_values['cities']}")
                print(f"   Customers: {valid_values['customers']}")
                print(f"   Varieties: {valid_values['varieties']}")
                print(f"   Months: {valid_values['months']}")
                
                # Step 5: Make a prediction
                print("\n5. Making a prediction...")
                print("Enter prediction details:")
                city = input(f"City {valid_values['cities']}: ").strip()
                customer = input(f"Customer {valid_values['customers']}: ").strip()
                variety = input(f"Variety {valid_values['varieties']}: ").strip()
                year = int(input("Year (e.g., 2024): ").strip())
                month = input(f"Month {valid_values['months']}: ").strip()
                
                response = client.send_request("tools/call", {
                    "name": "predict_tonnage",
                    "arguments": {
                        "city": city,
                        "customer_id": customer,
                        "apple_variety": variety,
                        "year": year,
                        "month": month
                    }
                })
                
                result = json.loads(response['result']['content'][0]['text'])
                if result['status'] == 'success':
                    print(f"\n✓ Prediction: {result['prediction']:.2f} tonnes")
                else:
                    print(f"\n✗ Error: {result['message']}")
                
                # Step 6: Batch prediction
                print("\n6. Testing batch prediction...")
                response = client.send_request("tools/call", {
                    "name": "batch_predict",
                    "arguments": {
                        "predictions": [
                            {
                                "city": city,
                                "customer_id": customer,
                                "apple_variety": variety,
                                "year": year,
                                "month": month
                            },
                            {
                                "city": valid_values['cities'][0],
                                "customer_id": valid_values['customers'][0],
                                "apple_variety": valid_values['varieties'][0],
                                "year": 2024,
                                "month": valid_values['months'][0]
                            }
                        ]
                    }
                })
                
                result = json.loads(response['result']['content'][0]['text'])
                print(f"✓ Batch prediction completed:")
                print(f"   Total: {result['total']}")
                print(f"   Successful: {result['successful']}")
                for i, pred in enumerate(result['predictions']):
                    if pred['status'] == 'success':
                        print(f"   Prediction {i+1}: {pred['prediction']:.2f} tonnes")
        else:
            print("Skipping training - no CSV path provided")
        
        print("\n" + "="*60)
        print("✓ All tests completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()


if __name__ == "__main__":
    main()
