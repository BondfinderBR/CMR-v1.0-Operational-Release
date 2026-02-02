import json, subprocess, time, os, datetime, signal, sys

CONFIGS = [
    "configs/C3_shared_M0.json",
    "configs/C3_shared_M25.json",
    "configs/C3_shared_mixed.json"
]

def run_test(config_path):
    with open(config_path) as f:
        cfg = json.load(f)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = f"runs/run_{cfg['run_id']}_{ts}"
    os.makedirs(run_dir, exist_ok=True)

    with open(f"{run_dir}/config.json", "w") as f:
        json.dump(cfg, f, indent=2)

    print(f"\n🧪 RUNNING {cfg['run_id']}")

    # start medium
    medium = subprocess.Popen(["python", "medium.py"])
    time.sleep(0.5)

    # start observers
    obsA = subprocess.Popen(
        ["python", "observer_shared.py",
         "A",
         str(cfg["observer"]["memory_A"]),
         str(cfg["observer"]["samples"]),
         str(cfg["observer"]["interval_ms"]),
         f"{run_dir}/obsA.csv"]
    )

    obsB = subprocess.Popen(
        ["python", "observer_shared.py",
         "B",
         str(cfg["observer"]["memory_B"]),
         str(cfg["observer"]["samples"]),
         str(cfg["observer"]["interval_ms"]),
         f"{run_dir}/obsB.csv"]
    )

    obsA.wait()
    obsB.wait()

    # stop medium
    medium.terminate()
    medium.wait()

    # analyze
    subprocess.run(
        ["python", "analyzer.py",
         f"{run_dir}/obsA.csv",
         f"{run_dir}/obsB.csv",
         f"{run_dir}/result.json"]
    )

if __name__ == "__main__":
    for cfg in CONFIGS:
        run_test(cfg)
