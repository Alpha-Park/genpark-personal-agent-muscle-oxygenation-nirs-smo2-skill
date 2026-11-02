"""
Muscle Oxygenation (SmO2) & NIRS Microvascular Reperfusion Engine.
Provides deterministic, zero-dependency modeling of continuous-wave NIRS muscle oxygen saturation (SmO2),
deoxygenation rate, local breakpoint inflection, and hyperemic reperfusion slope.
"""

from typing import Dict, Any, List, Optional


class MuscleOxygenationClient:
    """
    Deterministic client for analyzing Near-Infrared Spectroscopy (NIRS) muscle oxygenation data.
    Pure Python standard library implementation based on exercise physiology NIRS standards.
    """

    def __init__(self):
        pass

    def evaluate_muscle_desaturation_profile(
        self,
        baseline_smo2_pct: float,
        nadir_smo2_pct: float,
        thb_arbitrary_units: float = 12.0,
        workload_watts: float = 250.0
    ) -> Dict[str, Any]:
        """
        Evaluates muscle oxygenation desaturation during high-intensity or threshold exercise.
        SmO2: muscle oxygen saturation percentage (0 - 100%).
        """
        if baseline_smo2_pct <= 0 or baseline_smo2_pct > 100 or nadir_smo2_pct < 0 or nadir_smo2_pct > 100:
            return {"error": "SmO2 values must be valid percentages between 0 and 100"}

        delta_smo2 = max(0.0, baseline_smo2_pct - nadir_smo2_pct)
        extraction_ratio = round((delta_smo2 / max(0.1, baseline_smo2_pct)) * 100.0, 1)

        # Extraction capability classification:
        # High athletic extraction: SmO2 drops to 10-25% at VO2max
        # Sedentary / poor extraction: SmO2 rarely drops below 50-60%
        if nadir_smo2_pct <= 20.0:
            extraction_tier = "ELITE_MITOCHONDRIAL_EXTRACTION"
            interpretation = "Exceptional local peripheral oxygen extraction capacity; mitochondria deoxygenating capillary bed fully."
        elif nadir_smo2_pct <= 40.0:
            extraction_tier = "WELL_TRAINED_OXIDATIVE_CAPACITY"
            interpretation = "Robust muscular oxygen extraction consistent with dedicated aerobic conditioning."
        elif nadir_smo2_pct <= 60.0:
            extraction_tier = "MODERATE_EXTRACTION_RESERVE"
            interpretation = "Moderate desaturation; local peripheral muscle is not the primary limiting factor."
        else:
            extraction_tier = "ATTENUATED_PERIPHERAL_DESATURATION"
            interpretation = "Minimal muscle desaturation under load; central circulatory delivery or neuromuscular recruitment may be limiting."

        return {
            "baseline_smo2_pct": baseline_smo2_pct,
            "nadir_smo2_pct": nadir_smo2_pct,
            "delta_desaturation_pct": round(delta_smo2, 1),
            "muscle_o2_extraction_pct": extraction_ratio,
            "thb_index": thb_arbitrary_units,
            "workload_watts": workload_watts,
            "extraction_tier": extraction_tier,
            "physiological_interpretation": interpretation
        }

    def calculate_reperfusion_kinetics(
        self,
        nadir_smo2_pct: float,
        post_recovery_samples_pct: List[float],
        sample_interval_sec: float = 1.0
    ) -> Dict[str, Any]:
        """
        Calculates hyperemic reperfusion slope (%/sec) and time to half recovery (t1/2)
        following exercise cessation or arterial occlusion release.
        """
        if not post_recovery_samples_pct:
            return {"error": "Recovery samples must not be empty"}

        peak_recovery = max(post_recovery_samples_pct)
        peak_idx = post_recovery_samples_pct.index(peak_recovery)
        time_to_peak_sec = (peak_idx + 1) * sample_interval_sec

        delta_rebound = max(0.0, peak_recovery - nadir_smo2_pct)
        half_rebound_target = nadir_smo2_pct + (delta_rebound / 2.0)

        # Estimate t1/2 (seconds to achieve 50% recovery)
        t_half_sec = None
        for i, val in enumerate(post_recovery_samples_pct):
            if val >= half_rebound_target:
                t_half_sec = round((i + 1) * sample_interval_sec, 1)
                break
        if t_half_sec is None:
            t_half_sec = round(len(post_recovery_samples_pct) * sample_interval_sec, 1)

        # Initial 10-second reperfusion slope (%/sec)
        ten_sec_idx = min(len(post_recovery_samples_pct) - 1, int(10.0 / sample_interval_sec))
        if ten_sec_idx > 0:
            slope_10s = round((post_recovery_samples_pct[ten_sec_idx] - nadir_smo2_pct) / (ten_sec_idx * sample_interval_sec), 2)
        else:
            slope_10s = round(delta_rebound / max(1.0, time_to_peak_sec), 2)

        # Muscle Oxygenation Health Score (0 - 100)
        # Normal athletic reperfusion slope > 1.8 %/sec, t1/2 < 12 sec
        slope_score = min(50.0, (slope_10s / 2.5) * 50.0)
        thalf_score = max(5.0, min(50.0, 50.0 - (t_half_sec - 5.0) * 3.0))
        moi_score = round(min(100.0, max(5.0, slope_score + thalf_score)), 1)

        if slope_10s >= 2.0 and t_half_sec <= 10.0:
            status = "RAPID_HYPEREMIC_MICROVASCULAR_REBOUND"
            recommendation = "Rapid arterial inflow and microvascular capillary recruitment; excellent interval recovery readiness."
        elif slope_10s >= 1.0:
            status = "NORMAL_AEROBIC_REPERFUSION"
            recommendation = "Standard oxygen resaturation velocity; allow standard work-to-rest ratio."
        else:
            status = "SLUGGISH_MICROVASCULAR_REPERFUSION"
            recommendation = "Delayed oxygen replenishment; extend recovery interval before subsequent high-intensity intervals."

        return {
            "nadir_smo2_pct": nadir_smo2_pct,
            "peak_recovery_smo2_pct": peak_recovery,
            "delta_rebound_pct": round(delta_rebound, 1),
            "reperfusion_slope_10s_pct_sec": slope_10s,
            "time_to_half_recovery_sec": t_half_sec,
            "time_to_peak_recovery_sec": round(time_to_peak_sec, 1),
            "muscle_oxygenation_index": moi_score,
            "status": status,
            "actionable_guidance": recommendation
        }
