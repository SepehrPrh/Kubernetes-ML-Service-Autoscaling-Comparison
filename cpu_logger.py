import time
import csv
import subprocess

OUTPUT = "cpu.csv"

data = []

start = time.time()

for _ in range(120):
    t = time.time() - start

    try:
        result = subprocess.check_output(
            "kubectl top pods --no-headers | grep ml-deployment",
        shell=True
        ).decode().strip().split("\n")

        total_cpu = 0

        for line in result:
            parts = line.split()
            cpu = parts[1]  # e.g. "50m"
            if cpu.endswith("m"):
                total_cpu += int(cpu[:-1])

        print(f"time={t:.1f}s cpu={total_cpu}m")
        data.append((t, total_cpu))

    except:
        print("cpu read error")

    time.sleep(1)

# save
with open(OUTPUT, "w") as f:
    writer = csv.writer(f)
    writer.writerow(["time", "cpu_millicores"])
    writer.writerows(data)