# orchestrator.py
import json, subprocess, time, os, datetime

CONFIGS = [
    "configs/C0_low_coherence.json",
    "configs/C1_filtered.json",
    "configs/C2_synced.json",
    "configs/C3_ultra_coherent.json"
]

def run_test(config_path):
    with open(config_path) as f:
        config = json.load(f)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = f"runs/run_{config['run_id']}_{ts}"
    os.makedirs(run_dir, exist_ok=True)

    with open(f"{run_dir}/config.json", "w") as f:
        json.dump(config, f, indent=2)

    print(f"\n🧪 RUNNING {config['run_id']}")

    # start server
    server = subprocess.Popen(["python", "server.py"])
    time.sleep(1)

    # start observers
    obsA = subprocess.Popen(
        ["python", "observer.py", "A", config_path, f"{run_dir}/obsA.csv"]
    )
    obsB = subprocess.Popen(
        ["python", "observer.py", "B", config_path, f"{run_dir}/obsB.csv"]
    )

    obsA.wait()
    obsB.wait()

    server.terminate()

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
