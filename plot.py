import pandas as pd
import matplotlib.pyplot as plt

def plot_file(file, label, ycol):
    df = pd.read_csv(file)
    plt.plot(df["time"], df[ycol], label=label)

# ---- latency ----
plt.figure()
plot_file("latency_auto.csv", "auto", "latency")
plot_file("latency_hpa70.csv", "hpa70", "latency")
plot_file("latency_hpa90.csv", "hpa90", "latency")

plt.xlabel("time")
plt.ylabel("latency (s)")
plt.legend()
plt.title("Latency over time")
plt.savefig("latency.png")

# ---- cpu ----
plt.figure()
plot_file("cpu_auto.csv", "auto", "cpu_millicores")
plot_file("cpu_hpa70.csv", "hpa70", "cpu_millicores")
plot_file("cpu_hpa90.csv", "hpa90", "cpu_millicores")

plt.xlabel("time")
plt.ylabel("CPU (millicores)")
plt.legend()
plt.title("CPU usage over time")
plt.savefig("cpu.png")


# ---- replicas ----
plt.figure()
plot_file("replicas_auto.csv", "auto", "replicas")
plot_file("replicas_hpa70.csv", "hpa70", "replicas")
plot_file("replicas_hpa90.csv", "hpa90", "replicas")

plt.xlabel("time")
plt.ylabel("replicas")
plt.legend()
plt.title("Replicas over time")
plt.savefig("replicas.png")