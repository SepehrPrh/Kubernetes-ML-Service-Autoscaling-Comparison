import subprocess
import time
import shutil
import os

EXPERIMENTS = [
    ("auto", None),      # your autoscaler already running
    ("hpa70", 70),
    ("hpa90", 90),
]

DURATION = 150  # seconds


def run_cmd(cmd):
    return subprocess.Popen(cmd, shell=True)

def safe_move(src, dst):
    if os.path.exists(src):
        shutil.move(src, dst)
    else:
        print(f"WARNING: {src} not found")

def setup_hpa(cpu):
    if cpu is None:
        return
    print(f"Setting HPA to {cpu}%")
    subprocess.run(
        f"kubectl autoscale deployment ml-deployment --cpu-percent={cpu} --min=1 --max=10",
        shell=True
    )
    time.sleep(5)

def cleanup_hpa():
    subprocess.run(
        "kubectl delete hpa ml-deployment --ignore-not-found",
        shell=True
    )

def run_experiment(name, cpu_target):
    print(f"\n=== RUNNING {name} ===")

    autoscaler = None

    cleanup_hpa()

    # 👉 START autoscaler ONLY for "auto"
    if name == "auto":
        print("Starting autoscaler...")
        autoscaler = run_cmd("python autoscaler.py")
    else:
        setup_hpa(cpu_target)

    # start load + loggers
    load = run_cmd("python load_test.py")
    cpu = run_cmd("python cpu_logger.py")
    replicas = run_cmd("python replicas_logger.py")

    time.sleep(DURATION)

    # stop processes
    load.wait()
    cpu.wait()
    replicas.wait()

    # 👉 STOP autoscaler after auto experiment
    if autoscaler:
        print("Stopping autoscaler...")
        autoscaler.terminate()

    time.sleep(2)

    shutil.move("latency.csv", f"latency_{name}.csv")
    safe_move("cpu.csv", f"cpu_{name}.csv")
    shutil.move("replicas.csv", f"replicas_{name}.csv")

    print(f"Saved results for {name}")

    print("Resetting system...")

    subprocess.run(
        "kubectl scale deployment ml-deployment --replicas=1",
        shell=True
    )

    cleanup_hpa()

    # optional but good
    subprocess.run(
        "kubectl delete pod -l app=ml",
        shell=True
    )

    print("Waiting 60s for stabilization...")
    time.sleep(60)

if __name__ == "__main__":
    for name, cpu in EXPERIMENTS:
        run_experiment(name, cpu)

    print("\n✅ ALL EXPERIMENTS DONE")