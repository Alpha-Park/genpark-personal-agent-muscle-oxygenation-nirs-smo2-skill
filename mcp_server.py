"""
MCP Server for Muscle Oxygenation (SmO2) & NIRS Microvascular Reperfusion.
Exposes JSON-RPC endpoints for evaluating muscle oxygen saturation dynamics and reperfusion slopes.
"""

import json
import sys
from client import MuscleOxygenationClient

client = MuscleOxygenationClient()


def handle_request(request: dict) -> dict:
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "evaluate_muscle_desaturation_profile",
                        "description": "Evaluates muscle oxygen saturation (SmO2) desaturation magnitude, extraction percentage, and peripheral oxidative capacity.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "baseline_smo2_pct": {"type": "number", "description": "Baseline resting SmO2 percentage (e.g. 70.0)"},
                                "nadir_smo2_pct": {"type": "number", "description": "Minimum SmO2 percentage reached during exertion (e.g. 18.5)"},
                                "thb_arbitrary_units": {"type": "number", "default": 12.0, "description": "Total hemoglobin (tHb) index"},
                                "workload_watts": {"type": "number", "default": 250.0, "description": "Workload in Watts during measurement"}
                            },
                            "required": ["baseline_smo2_pct", "nadir_smo2_pct"]
                        }
                    },
                    {
                        "name": "calculate_reperfusion_kinetics",
                        "description": "Calculates hyperemic reperfusion slope (%/s), half-recovery time (t1/2), and Muscle Oxygenation Index from recovery SmO2 series.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "nadir_smo2_pct": {"type": "number", "description": "SmO2 percentage at the end of exercise / occlusion"},
                                "post_recovery_samples_pct": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Sequential post-exercise SmO2 values in % during recovery"
                                },
                                "sample_interval_sec": {"type": "number", "default": 1.0, "description": "Time interval between samples in seconds"}
                            },
                            "required": ["nadir_smo2_pct", "post_recovery_samples_pct"]
                        }
                    }
                ]
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "evaluate_muscle_desaturation_profile":
            res = client.evaluate_muscle_desaturation_profile(
                baseline_smo2_pct=args.get("baseline_smo2_pct", 70.0),
                nadir_smo2_pct=args.get("nadir_smo2_pct", 22.0),
                thb_arbitrary_units=args.get("thb_arbitrary_units", 12.0),
                workload_watts=args.get("workload_watts", 250.0)
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }

        elif tool_name == "calculate_reperfusion_kinetics":
            res = client.calculate_reperfusion_kinetics(
                nadir_smo2_pct=args.get("nadir_smo2_pct", 20.0),
                post_recovery_samples_pct=args.get("post_recovery_samples_pct", []),
                sample_interval_sec=args.get("sample_interval_sec", 1.0)
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method {tool_name} not found"}
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32600, "message": "Invalid Request"}
    }


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
