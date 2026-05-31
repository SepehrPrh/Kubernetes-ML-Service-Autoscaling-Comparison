import time
import csv
import subprocess

OUTPUT = "replicas.csv"

data = []

start = time.time()

for _ in range(120):  # run ~120 seconds
    t = time.time() - start

    result = subprocess.check_output(
        "kubectl get deployment ml-deployment -o jsonpath='{.status.replicas}'",
        shell=True
    ).decode().strip()

    try:
        replicas = int(result)
    except:
        replicas = 0
    print(f"time={t:.1f}s replicas={replicas}")
    data.append((t, replicas))

    time.sleep(1)

# save
with open(OUTPUT, "w") as f:
    writer = csv.writer(f)
    writer.writerow(["time", "replicas"])
    writer.writerows(data)