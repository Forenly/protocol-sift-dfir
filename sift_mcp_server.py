#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protocol SIFT MCP Server - Cyber-Physical Forensics Core (STDIO)
Implements standard Model Context Protocol over STDIO for SIFT Workstation forensics.
"""

import sys
import json
import traceback
from evidence_store import CASES

# Log to stderr since stdout is reserved for JSON-RPC
def log(msg):
    sys.stderr.write(f"[SIFT-MCP-SERVER] {msg}\n")
    sys.stderr.flush()

# Define the schemas of the SIFT forensic tools
TOOLS = [
    {
        "name": "volatility3",
        "description": "Examine Linux volatile memory (RAM) dumps to extract active processes, open sockets, and malicious code injections.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "case_id": {
                    "type": "string",
                    "description": "The unique case identifier (e.g. 'case_ros2_node_hijack', 'case_slam_map_tampering', 'case_dji_mirai_botnet')",
                    "enum": ["case_ros2_node_hijack", "case_slam_map_tampering", "case_dji_mirai_botnet"]
                },
                "command": {
                    "type": "string",
                    "description": "The Volatility plugin command to run",
                    "enum": ["linux_pslist", "linux_netstat", "linux_malfind"]
                }
            },
            "required": ["case_id", "command"]
        }
    },
    {
        "name": "plaso",
        "description": "Perform super-timeline logs analysis (log2timeline) to correlate system events, udev attachments, execution records, and sensor logs.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "case_id": {
                    "type": "string",
                    "description": "The unique case identifier",
                    "enum": ["case_ros2_node_hijack", "case_slam_map_tampering", "case_dji_mirai_botnet"]
                },
                "query": {
                    "type": "string",
                    "description": "Optional keyword or grep query to filter the parsed super-timeline"
                }
            },
            "required": ["case_id"]
        }
    },
    {
        "name": "sleuthkit",
        "description": "Explore the robot's physical disk image, list directories (fls), and carve/view configuration and shell files (icat).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "case_id": {
                    "type": "string",
                    "description": "The unique case identifier",
                    "enum": ["case_ros2_node_hijack", "case_slam_map_tampering", "case_dji_mirai_botnet"]
                },
                "command": {
                    "type": "string",
                    "description": "The TSK tool command to run",
                    "enum": ["fls", "icat_setup_bash", "icat_patch_bash", "icat_mapslayer", "icat_crontab"]
                }
            },
            "required": ["case_id", "command"]
        }
    },
    {
        "name": "yara",
        "description": "Run pattern matching signatures on filesystems or extracted process memory regions to find known IoT malware families.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "case_id": {
                    "type": "string",
                    "description": "The unique case identifier",
                    "enum": ["case_ros2_node_hijack", "case_slam_map_tampering", "case_dji_mirai_botnet"]
                },
                "rule_name": {
                    "type": "string",
                    "description": "The signature rule identifier (e.g. 'Linux_Backdoor_Pnscan', 'Linux_Tool_MapSlayer', 'IoT_Malware_Mirai')"
                }
            },
            "required": ["case_id", "rule_name"]
        }
    }
]

def handle_volatility3(arguments):
    case_id = arguments.get("case_id")
    command = arguments.get("command")
    
    if case_id not in CASES:
        return f"Error: Case '{case_id}' not found."
    
    case = CASES[case_id]
    vol_data = case.get("volatility3", {})
    
    if command in vol_data:
        return vol_data[command]
    else:
        return f"Volatility command '{command}' has no data recorded for this case."

def handle_plaso(arguments):
    case_id = arguments.get("case_id")
    query = arguments.get("query", "").lower()
    
    if case_id not in CASES:
        return f"Error: Case '{case_id}' not found."
    
    timeline_data = CASES[case_id].get("plaso", {}).get("timeline", "")
    
    if not query:
        return timeline_data
    
    # Filter the super-timeline by the query keyword
    lines = timeline_data.split("\n")
    matching_lines = [line for line in lines if query in line.lower()]
    
    if not matching_lines:
        return f"No timeline events matched the filter query: '{query}'"
    
    return "\n".join(matching_lines)

def handle_sleuthkit(arguments):
    case_id = arguments.get("case_id")
    command = arguments.get("command")
    
    if case_id not in CASES:
        return f"Error: Case '{case_id}' not found."
    
    case = CASES[case_id]
    tsk_data = case.get("sleuthkit", {})
    
    if command in tsk_data:
        return tsk_data[command]
    else:
        return f"Sleuth Kit command '{command}' is not available for this case. Available commands: {', '.join(tsk_data.keys())}"

def handle_yara(arguments):
    case_id = arguments.get("case_id")
    rule_name = arguments.get("rule_name")
    
    if case_id not in CASES:
        return f"Error: Case '{case_id}' not found."
    
    yara_data = CASES[case_id].get("yara", {}).get("scan", "")
    
    if rule_name.lower() in yara_data.lower() or rule_name == "*":
        return yara_data
    else:
        return f"YARA rule '{rule_name}' ran with no hits on the evidence set."

def run_tool(name, arguments):
    log(f"Executing tool '{name}' with arguments: {arguments}")
    if name == "volatility3":
        return handle_volatility3(arguments)
    elif name == "plaso":
        return handle_plaso(arguments)
    elif name == "sleuthkit":
        return handle_sleuthkit(arguments)
    elif name == "yara":
        return handle_yara(arguments)
    else:
        raise ValueError(f"Unknown tool: '{name}'")

def main():
    log("SIFT MCP Server Started. Monitoring stdin for JSON-RPC requests...")
    
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            
            # 1. Handle Tools Listing (discovery)
            if method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": TOOLS}
                }
                sys.stdout.write(json.dumps(res) + "\n")
                sys.stdout.flush()
                
            # 2. Handle Tools Execution (call)
            elif method == "tools/call":
                params = req.get("params", {})
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                try:
                    text_output = run_tool(tool_name, arguments)
                    res = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": text_output
                                }
                            ]
                        }
                    }
                except Exception as ex:
                    log(f"Error executing tool {tool_name}: {ex}")
                    res = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {
                            "code": -32603,
                            "message": f"Internal Tool Execution Error: {ex}",
                            "data": traceback.format_exc()
                        }
                    }
                sys.stdout.write(json.dumps(res) + "\n")
                sys.stdout.flush()
                
            # 3. Handle Other standard/lifecycle methods
            else:
                # Unsupported method, send empty or mock result to satisfy protocol handshake
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {}
                }
                sys.stdout.write(json.dumps(res) + "\n")
                sys.stdout.flush()
                
        except Exception as e:
            log(f"Critical error in main loop: {e}")
            sys.stderr.write(traceback.format_exc())
            sys.stderr.flush()

if __name__ == "__main__":
    main()
