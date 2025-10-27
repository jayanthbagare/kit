#!/usr/bin/env python3
"""
MCP Server for Tonnage Prediction
This server exposes the tonnage prediction model via MCP protocol
"""

import json
import sys
import asyncio
from typing import Any, Sequence
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

# MCP Protocol Implementation
class MCPServer:
    def __init__(self):
        self.model = None
        self.encoders = {}
        self.model_trained = False
        
    async def handle_request(self, request: dict) -> dict:
        """Handle incoming MCP requests"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "initialize":
                result = await self.initialize(params)
            elif method == "tools/list":
                result = await self.list_tools()
            elif method == "tools/call":
                result = await self.call_tool(params)
            else:
                raise ValueError(f"Unknown method: {method}")
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
    
    async def initialize(self, params: dict) -> dict:
        """Initialize the MCP server"""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "tonnage-predictor",
                "version": "1.0.0"
            }
        }
    
    async def list_tools(self) -> dict:
        """List available tools"""
        return {
            "tools": [
                {
                    "name": "train_model",
                    "description": "Train the tonnage prediction model with CSV data",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "csv_path": {
                                "type": "string",
                                "description": "Path to the CSV file with training data"
                            },
                            "model_type": {
                                "type": "string",
                                "description": "Type of model to train (linear, ridge, or random_forest)",
                                "enum": ["linear", "ridge", "random_forest"],
                                "default": "random_forest"
                            }
                        },
                        "required": ["csv_path"]
                    }
                },
                {
                    "name": "predict_tonnage",
                    "description": "Predict tonnage based on input parameters",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "City name (e.g., Riyadh)"
                            },
                            "customer_id": {
                                "type": "string",
                                "description": "Customer ID (e.g., Lulu)"
                            },
                            "apple_variety": {
                                "type": "string",
                                "description": "Apple variety (e.g., fuji)"
                            },
                            "year": {
                                "type": "integer",
                                "description": "Year (e.g., 2024)"
                            },
                            "month": {
                                "type": "string",
                                "description": "Month (e.g., jan)"
                            }
                        },
                        "required": ["city", "customer_id", "apple_variety", "year", "month"]
                    }
                },
                {
                    "name": "get_valid_values",
                    "description": "Get list of valid values for categorical fields",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                },
                {
                    "name": "batch_predict",
                    "description": "Predict tonnage for multiple records at once",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "predictions": {
                                "type": "array",
                                "description": "Array of prediction requests",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "city": {"type": "string"},
                                        "customer_id": {"type": "string"},
                                        "apple_variety": {"type": "string"},
                                        "year": {"type": "integer"},
                                        "month": {"type": "string"}
                                    },
                                    "required": ["city", "customer_id", "apple_variety", "year", "month"]
                                }
                            }
                        },
                        "required": ["predictions"]
                    }
                }
            ]
        }
    
    async def call_tool(self, params: dict) -> dict:
        """Call a specific tool"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "train_model":
            return await self.train_model(arguments)
        elif tool_name == "predict_tonnage":
            return await self.predict_tonnage(arguments)
        elif tool_name == "get_valid_values":
            return await self.get_valid_values()
        elif tool_name == "batch_predict":
            return await self.batch_predict(arguments)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
    
    async def train_model(self, args: dict) -> dict:
        """Train the tonnage prediction model"""
        csv_path = args.get("csv_path")
        model_type = args.get("model_type", "random_forest")
        
        try:
            # Load data
            df = pd.read_csv(csv_path)
            
            # Encode categorical features
            le_city = LabelEncoder()
            le_customer = LabelEncoder()
            le_variety = LabelEncoder()
            le_month = LabelEncoder()
            
            df['city_encoded'] = le_city.fit_transform(df['city'])
            df['customer_encoded'] = le_customer.fit_transform(df['customer_id'])
            df['variety_encoded'] = le_variety.fit_transform(df['apple_variety'])
            df['month_encoded'] = le_month.fit_transform(df['month'])
            
            # Prepare features and target
            feature_columns = ['city_encoded', 'customer_encoded', 'variety_encoded', 'year', 'month_encoded']
            X = df[feature_columns]
            y = df['tonnage']
            
            # Train model
            if model_type == "random_forest":
                model = RandomForestRegressor(
                    n_estimators=100,
                    max_depth=10,
                    min_samples_split=5,
                    min_samples_leaf=2,
                    random_state=42,
                    n_jobs=-1
                )
            else:  # linear or ridge
                model = LinearRegression()
            
            model.fit(X, y)
            
            # Store model and encoders
            self.model = model
            self.encoders = {
                'city': le_city,
                'customer': le_customer,
                'variety': le_variety,
                'month': le_month
            }
            self.model_trained = True
            
            # Calculate training metrics
            from sklearn.metrics import mean_absolute_error, r2_score
            y_pred = model.predict(X)
            mae = mean_absolute_error(y, y_pred)
            r2 = r2_score(y, y_pred)
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "status": "success",
                            "message": "Model trained successfully",
                            "model_type": model_type,
                            "training_samples": len(df),
                            "metrics": {
                                "mae": float(mae),
                                "r2_score": float(r2)
                            },
                            "valid_values": {
                                "cities": list(le_city.classes_),
                                "customers": list(le_customer.classes_),
                                "varieties": list(le_variety.classes_),
                                "months": list(le_month.classes_)
                            }
                        }, indent=2)
                    }
                ]
            }
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "status": "error",
                            "message": str(e)
                        })
                    }
                ],
                "isError": True
            }
    
    async def predict_tonnage(self, args: dict) -> dict:
        """Predict tonnage for given inputs"""
        if not self.model_trained:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "status": "error",
                            "message": "Model not trained. Please train the model first using train_model tool."
                        })
                    }
                ],
                "isError": True
            }
        
        try:
            city = args.get("city")
            customer_id = args.get("customer_id")
            apple_variety = args.get("apple_variety")
            year = args.get("year")
            month = args.get("month")
            
            # Encode inputs
            city_encoded = self.encoders['city'].transform([city])[0]
            customer_encoded = self.encoders['customer'].transform([customer_id])[0]
            variety_encoded = self.encoders['variety'].transform([apple_variety])[0]
            month_encoded = self.encoders['month'].transform([month])[0]
            
            # Create feature array
            features = np.array([[city_encoded, customer_encoded, variety_encoded, year, month_encoded]])
            
            # Make prediction
            prediction = self.model.predict(features)[0]
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "status": "success",
                            "prediction": float(prediction),
                            "inputs": {
                                "city": city,
                                "customer_id": customer_id,
                                "apple_variety": apple_variety,
                                "year": year,
                                "month": month
                            }
                        }, indent=2)
                    }
                ]
            }
        except ValueError as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "status": "error",
                            "message": f"Invalid input value: {str(e)}",
                            "valid_values": {
                                "cities": list(self.encoders['city'].classes_),
                                "customers": list(self.encoders['customer'].classes_),
                                "varieties": list(self.encoders['variety'].classes_),
                                "months": list(self.encoders['month'].classes_)
                            }
                        }, indent=2)
                    }
                ],
                "isError": True
            }
    
    async def get_valid_values(self) -> dict:
        """Get valid values for categorical fields"""
        if not self.model_trained:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "status": "error",
                            "message": "Model not trained yet"
                        })
                    }
                ],
                "isError": True
            }
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "status": "success",
                        "valid_values": {
                            "cities": list(self.encoders['city'].classes_),
                            "customers": list(self.encoders['customer'].classes_),
                            "varieties": list(self.encoders['variety'].classes_),
                            "months": list(self.encoders['month'].classes_)
                        }
                    }, indent=2)
                }
            ]
        }
    
    async def batch_predict(self, args: dict) -> dict:
        """Batch prediction for multiple records"""
        if not self.model_trained:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "status": "error",
                            "message": "Model not trained"
                        })
                    }
                ],
                "isError": True
            }
        
        predictions_input = args.get("predictions", [])
        results = []
        
        for item in predictions_input:
            try:
                city_encoded = self.encoders['city'].transform([item['city']])[0]
                customer_encoded = self.encoders['customer'].transform([item['customer_id']])[0]
                variety_encoded = self.encoders['variety'].transform([item['apple_variety']])[0]
                month_encoded = self.encoders['month'].transform([item['month']])[0]
                
                features = np.array([[city_encoded, customer_encoded, variety_encoded, item['year'], month_encoded]])
                prediction = self.model.predict(features)[0]
                
                results.append({
                    "status": "success",
                    "inputs": item,
                    "prediction": float(prediction)
                })
            except Exception as e:
                results.append({
                    "status": "error",
                    "inputs": item,
                    "error": str(e)
                })
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "status": "success",
                        "predictions": results,
                        "total": len(results),
                        "successful": sum(1 for r in results if r["status"] == "success")
                    }, indent=2)
                }
            ]
        }


async def main():
    """Main server loop"""
    server = MCPServer()
    
    # Read from stdin and write to stdout (MCP protocol)
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            request = json.loads(line)
            response = await server.handle_request(request)
            
            # Write response to stdout
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
            
        except json.JSONDecodeError:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                }
            }
            sys.stdout.write(json.dumps(error_response) + "\n")
            sys.stdout.flush()
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
            sys.stdout.write(json.dumps(error_response) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    asyncio.run(main())
