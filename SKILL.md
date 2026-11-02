---
name: genpark-personal-agent-muscle-oxygenation-nirs-smo2-skill
description: Deterministic Near-Infrared Spectroscopy (NIRS) muscle oxygen saturation (SmO2) modeling, peripheral extraction capacity, and hyperemic reperfusion kinetics.
version: 1.0.0
author: GenPark Autonomous Agents Ecosystem
license: MIT
tags:
  - personal-agent
  - ai-agent
  - openclaw
  - genpark
  - mcp
  - mcp-server
  - model-context-protocol
  - python
  - zero-dependency
  - wellness
  - productivity
  - production-ready
---

# Muscle Oxygenation (SmO2) & NIRS Reperfusion Kinetics Skill

## Overview
The `genpark-personal-agent-muscle-oxygenation-nirs-smo2-skill` brings non-invasive peripheral muscle metabolic analytics to sovereign personal agents. Using continuous-wave near-infrared spectroscopy (NIRS), this skill monitors local muscle oxygen saturation ($SmO_2$ in %) and total hemoglobin ($tHb$). Unlike systemic heart rate or pulse oximetry ($SpO_2$), localized $SmO_2$ directly measures the balance between local capillary oxygen delivery and mitochondrial oxygen consumption in active skeletal muscle. It evaluates the muscle oxygenation breakpoint (MOB) under load and tracks hyperemic reperfusion recovery rates post-effort.

## Physiological Model & Mathematics
1. **Muscle Oxygen Saturation ($SmO_2$)**:
   $$SmO_2 = \frac{[HbO_2]}{[HbO_2] + [HHb]} \times 100\%$$
2. **Local Peripheral Extraction Ratio**:
   $$\text{Extraction \%} = \frac{SmO_{2,\text{baseline}} - SmO_{2,\text{nadir}}}{SmO_{2,\text{baseline}}} \times 100\%$$
   - Elite endurance athletes can drive quadriceps or deltoid $SmO_2$ down to $10 - 20\%$ at maximal exertion.
3. **10-Second Hyperemic Reperfusion Velocity**:
   $$\text{Reperfusion Slope} = \frac{\Delta SmO_{2,10\text{s}}}{10} \quad (\%/\text{second})$$
   - Normative recovery velocity: $> 1.5 - 2.5\%/\text{s}$ denotes rich capillarization and brisk arteriolar dilation.
4. **Half-Recovery Horizon ($t_{1/2}$)**:
   Time in seconds to achieve $50\%$ recovery from nadir back toward resting baseline.

## Tools & Endpoints
- `evaluate_muscle_desaturation_profile`: Calculates desaturation drop, peripheral extraction percentage, and oxidative capacity tier.
- `calculate_reperfusion_kinetics`: Computes 10-second reperfusion slope, $t_{1/2}$ recovery horizon, and Muscle Oxygenation Index.
