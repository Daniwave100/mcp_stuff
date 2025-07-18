# mcp_server.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, Optional, Union
import uvicorn
import sys
import json

app = FastAPI()

from typing import Union

class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[Union[str, int]] = None  # Accept both string and int
    method: str
    params: Optional[Dict[str, Any]] = None

# Store your mom's name here!
MOMS_NAME = "YourActualMomsName"  # Replace with your actual mom's name

@app.post("/")
def handle_request(request: MCPRequest):
    # Ensure id is a string
    request_id = str(request.id) if request.id is not None else "1"
    
    if request.method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "Mom's Name Server", "version": "1.0.0"}
            }
        }
    
    elif request.method == "tools/list":
        return {
            "jsonrpc": "2.0", 
            "id": request_id,
            "result": {
                "tools": [{
                    "name": "get_moms_name",
                    "description": "Get the user's mother's name",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }]
            }
        }
    
    elif request.method == "tools/call":
        tool_name = request.params.get("name") if request.params else None
        if tool_name == "get_moms_name":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": f"Your mom's name is {MOMS_NAME}! 💕"}]
                }
            }
    
    return {
        "jsonrpc": "2.0", 
        "id": request_id, 
        "error": {"code": -32601, "message": "Method not found"}
    }

# For stdio communication (required for Claude Desktop)
async def handle_stdio():
    while True:
        try:
            line = input()
            if not line:
                break
            
            request_data = json.loads(line)
            request = MCPRequest(**request_data)
            
            # Ensure id is a string if it exists, otherwise use a default
            request_id = str(request.id) if request.id is not None else "1"
            
            # Process the request using the same logic
            if request.method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "Mom's Name Server", "version": "1.0.0"}
                    }
                }
            elif request.method == "tools/list":
                response = {
                    "jsonrpc": "2.0", 
                    "id": request_id,
                    "result": {
                        "tools": [{
                            "name": "get_moms_name",
                            "description": "Get the user's mother's name",
                            "inputSchema": {
                                "type": "object",
                                "properties": {},
                                "required": []
                            }
                        }]
                    }
                }
            elif request.method == "tools/call":
                tool_name = request.params.get("name") if request.params else None
                if tool_name == "get_moms_name":
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": f"Your mom's name is {MOMS_NAME}! 💕"}]
                        }
                    }
                else:
                    response = {
                        "jsonrpc": "2.0", 
                        "id": request_id, 
                        "error": {"code": -32601, "message": "Method not found"}
                    }
            else:
                response = {
                    "jsonrpc": "2.0", 
                    "id": request_id, 
                    "error": {"code": -32601, "message": "Method not found"}
                }
            
            print(json.dumps(response))
            sys.stdout.flush()
            
        except EOFError:
            break
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": "error",
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        import asyncio
        asyncio.run(handle_stdio())
    else:
        uvicorn.run(app, host="localhost", port=8000)