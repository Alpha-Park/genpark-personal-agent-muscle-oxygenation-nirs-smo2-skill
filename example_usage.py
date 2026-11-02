"""
Example usage for Muscle Oxygenation (SmO2) & NIRS Reperfusion Skill.
Demonstrates analyzing muscle desaturation profile and hyperemic reperfusion slope.
"""

from client import MuscleOxygenationClient


def main():
    client = MuscleOxygenationClient()

    print("=== 1. Evaluating Muscle SmO2 Desaturation Profile (Sprint Interval) ===")
    desat_res = client.evaluate_muscle_desaturation_profile(
        baseline_smo2_pct=72.0,
        nadir_smo2_pct=18.5,
        thb_arbitrary_units=13.2,
        workload_watts=320.0
    )
    print(f"Baseline SmO2: {desat_res['baseline_smo2_pct']}% | Nadir SmO2: {desat_res['nadir_smo2_pct']}%")
    print(f"Delta Desaturation: -{desat_res['delta_desaturation_pct']}% (Extraction: {desat_res['muscle_o2_extraction_pct']}%)")
    print(f"Extraction Tier: {desat_res['extraction_tier']}")
    print(f"Interpretation: {desat_res['physiological_interpretation']}")

    print("\n=== 2. Calculating Hyperemic Reperfusion Kinetics (Post-Effort Rebound) ===")
    # 20 seconds of sequential recovery SmO2 readings (1 Hz)
    recovery_stream = [22.0, 28.5, 36.0, 45.0, 53.0, 60.0, 66.0, 71.0, 74.5, 77.0, 78.5, 79.5, 80.0, 80.5, 80.5]
    reperf_res = client.calculate_reperfusion_kinetics(
        nadir_smo2_pct=18.5,
        post_recovery_samples_pct=recovery_stream,
        sample_interval_sec=1.0
    )
    print(f"Peak Rebound: {reperf_res['peak_recovery_smo2_pct']}% (Delta: +{reperf_res['delta_rebound_pct']}%)")
    print(f"10-Second Reperfusion Slope: {reperf_res['reperfusion_slope_10s_pct_sec']} %/s")
    print(f"Half-Recovery Time (t1/2): {reperf_res['time_to_half_recovery_sec']} s")
    print(f"Muscle Oxygenation Index: {reperf_res['muscle_oxygenation_index']} / 100")
    print(f"Status: {reperf_res['status']}")
    print(f"Guidance: {reperf_res['actionable_guidance']}")


if __name__ == "__main__":
    main()
