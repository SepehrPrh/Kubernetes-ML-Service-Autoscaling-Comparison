import os
import numpy as np
import pandas as pd

STRATEGIES = {
    "Custom Autoscaler": "auto",
    "HPA 70%": "hpa70",
    "HPA 90%": "hpa90",
}


def load_csv(name):
    path = os.path.join(os.path.dirname(__file__), name)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Missing file: {path}\nPlease run run_experiment.py first."
        )
    return pd.read_csv(path)


def parse_cpu(series):
    def _parse(v):
        if isinstance(v, str) and v.endswith("m"):
            return float(v[:-1])
        return float(v)

    return series.apply(_parse)


def compute_metrics(label):
    slug = STRATEGIES[label]

    lat = load_csv(f"latency_{slug}.csv")
    cpu = load_csv(f"cpu_{slug}.csv")
    rep = load_csv(f"replicas_{slug}.csv")

    latencies = lat["latency"].dropna()
    cpu_vals = parse_cpu(cpu["cpu_millicores"].dropna())
    replicas = rep["replicas"].dropna()

    return {
        "Avg Latency (s)": round(latencies.mean(), 3),
        "P95 Latency (s)": round(np.percentile(latencies, 95), 3),
        "P99 Latency (s)": round(np.percentile(latencies, 99), 3),
        "Max Latency (s)": round(latencies.max(), 3),
        "Peak CPU (cores)": round(cpu_vals.max() / 1000, 3),
        "Avg CPU (cores)": round(cpu_vals.mean() / 1000, 3),
        "Max Replicas": int(replicas.max()),
    }


def main():
    print("=" * 62)
    print("  AUTOSCALING STRATEGY COMPARISON")
    print("=" * 62)

    rows = {}
    for label in STRATEGIES:
        try:
            rows[label] = compute_metrics(label)
        except FileNotFoundError as e:
            print(f"\n[ERROR] {e}")
            return

    metrics = list(next(iter(rows.values())).keys())
    col_w = 22

    header = f"{'Metric':<28}" + "".join(f"{s:>{col_w}}" for s in rows)
    print(f"\n{header}")
    print("-" * (28 + col_w * len(rows)))

    for m in metrics:
        line = f"{m:<28}" + "".join(f"{rows[s][m]:>{col_w}}" for s in rows)
        print(line)

    print("\n" + "=" * 62)
    print("  SUMMARY")
    print("=" * 62)

    best_p99 = min(rows, key=lambda s: rows[s]["P99 Latency (s)"])
    best_cpu = min(rows, key=lambda s: rows[s]["Peak CPU (cores)"])
    best_scale = min(rows, key=lambda s: rows[s]["Max Replicas"])

    print(
        f"  Lowest P99 latency : {best_p99} "
        f"({rows[best_p99]['P99 Latency (s)']} s)"
    )
    print(
        f"  Lowest peak CPU    : {best_cpu} "
        f"({rows[best_cpu]['Peak CPU (cores)']} cores)"
    )
    print(
        f"  Fewest max replicas: {best_scale} "
        f"({rows[best_scale]['Max Replicas']} replicas)"
    )
    print("=" * 62)


if __name__ == "__main__":
    main()