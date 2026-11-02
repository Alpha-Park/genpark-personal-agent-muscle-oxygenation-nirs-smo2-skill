# Muscle Oxygenation (SmO2) & NIRS Reperfusion Kinetics Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](https://github.com/alphaparkinc/genpark-personal-agent-muscle-oxygenation-nirs-smo2-skill)
[![OpenClaw Ready](https://img.shields.io/badge/OpenClaw-Compatible-purple.svg)](https://github.com/alphaparkinc/genpark-personal-agent-muscle-oxygenation-nirs-smo2-skill)
[![MCP Protocol](https://img.shields.io/badge/MCP-Standard-orange.svg)](https://modelcontextprotocol.io/)

A sovereign personal agent capability for computational Near-Infrared Spectroscopy (NIRS) muscle oxygenation modeling, evaluating peripheral $SmO_2$ extraction capacity, and post-effort hyperemic reperfusion.

## Architecture

```mermaid
flowchart TD
    NIRSSensor["NIRS Dual-Wavelength Photons (760nm & 850nm)"] --> SmO2Calc["SmO2 Saturation: [HbO2] / ([HbO2] + [HHb]) * 100%"]
    SmO2Calc --> Desaturation["Muscle Desaturation Profile (Nadir & Extraction %)"]
    Desaturation --> Reperfusion["Hyperemic Reperfusion Engine (Rebound Slope & t_1/2)"]
    Reperfusion --> HealthScore["Muscle Oxygenation Index (MOI: 0 - 100)"]
    HealthScore --> IntervalPacing["OpenClaw / Hermes Rest-to-Work Ratio & Pacing Recommendations"]
```

## Quickstart

```python
from client import MuscleOxygenationClient

client = MuscleOxygenationClient()

# Assess muscle desaturation profile during effort
res = client.evaluate_muscle_desaturation_profile(
    baseline_smo2_pct=72.0,
    nadir_smo2_pct=18.5,
    thb_arbitrary_units=13.2,
    workload_watts=320.0
)

print("Extraction Ratio:", res["muscle_o2_extraction_pct"], "%")
print("Extraction Tier:", res["extraction_tier"])
print("Interpretation:", res["physiological_interpretation"])
```

## MCP Server Integration

Add to your `claude_desktop_config.json` or OpenClaw tool registry:

```json
{
  "mcpServers": {
    "muscle-oxygenation": {
      "command": "python",
      "args": ["/path/to/genpark-personal-agent-muscle-oxygenation-nirs-smo2-skill/mcp_server.py"]
    }
  }
}
```

## License
MIT License.
