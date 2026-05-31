import subprocess
import time

UP_THRESHOLD = 400
DOWN_THRESHOLD = 200

MAX_REPLICAS = 5
MIN_REPLICAS = 1

COOLDOWN = 8           # seconds between scaling actions
last_scale_time = 0


def get_cpu_millicores():
    try:
        out = subprocess.check_output("kubectl top pods", shell=True).decode()
        lines = out.strip().split("\n")[1:]

        total = 0
        for l in lines:
            parts = l.split()
            cpu = parts[1]

            if cpu.endswith("m"):
                total += int(cpu[:-1])

        return total
    except:
        return 0


def get_replicas():
    out = subprocess.check_output(
        "kubectl get deployment ml-deployment -o jsonpath='{.spec.replicas}'",
        shell=True
    )
    return int(out)


def set_replicas(n):
    subprocess.run(
        f"kubectl scale deployment ml-deployment --replicas={n}",
        shell=True
    )


while True:
    cpu = get_cpu_millicores()
    replicas = get_replicas()

    print(f"CPU={cpu}m replicas={replicas}")

    now = time.time()

    # SCALE UP (controlled)
    if cpu > UP_THRESHOLD and replicas < MAX_REPLICAS:
        if now - last_scale_time > COOLDOWN:
            new = replicas + 1
            print(f"Scale UP → {new}")
            set_replicas(new)
            last_scale_time = now

    # SCALE DOWN (slow)
    elif cpu < DOWN_THRESHOLD and replicas > MIN_REPLICAS:
        if now - last_scale_time > COOLDOWN:
            new = replicas - 1
            print(f"Scale DOWN → {new}")
            set_replicas(new)
            last_scale_time = now

    time.sleep(2)