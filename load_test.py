import requests
import time
import os
import statistics
import csv
import random

URL = "http://192.168.49.2:30512/predict"
IMG_DIR = "imagenet-sample-images"

latencies_over_time = []
latencies = []
start_global = time.time()
files = [
    os.path.join(IMG_DIR, f)
    for f in os.listdir(IMG_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

qps = 100

delay = 1 / qps

# for i in range(200):
img_path = random.choice(files)
start = time.time()
with open(img_path, "rb") as f:
    res = requests.post(URL, files={"file": f})
latency = time.time() - start

timestamp = time.time() - start_global
# ✅ FIX 1
latencies.append(latency)

latencies_over_time.append((timestamp, latency))

print(f" {res.status_code}, latency={latency:.3f}s")

    # time.sleep(delay)

# ---- results ----
print("\n--- RESULTS ---")
print(f"avg latency: {statistics.mean(latencies):.3f}s")
print(f"p95 latency: {sorted(latencies)[int(0.95*len(latencies))]:.3f}s")
print(f"max latency: {max(latencies):.3f}s")

# ---- save for plotting ----
with open("latency.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["time", "latency"])
    writer.writerows(latencies_over_time)