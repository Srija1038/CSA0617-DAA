"""Generates all graphs of the report from results/*.json (python make_graphs.py)."""
import json, math, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import NAME, REG

R = os.path.join(os.path.dirname(__file__), "..", "results"); F = os.path.join(os.path.dirname(__file__), "..", "figures")
NS = [1000, 10000, 100000, 1000000]
B = {n: json.load(open(f"{R}/bench_{n}.json")) for n in NS}
T12 = json.load(open(f"{R}/task12.json"))
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#555", "axes.titleweight": "bold", "axes.grid": True, "grid.color": "#e2e2e2", "grid.linewidth": 0.6})
ST = {"linear": ("#D62728", "o", "Linear search"), "binary": ("#1F77B4", "s", "Binary search (recursive)"), "hash": ("#2CA02C", "^", "Hash table (linear probing)")}
STAMP = f"Reg No: {REG} | {NAME}"


def stamp(fig):
    fig.text(0.995, 0.005, STAMP, ha="right", va="bottom", fontsize=6.5, color="#666")


def line(ax, ys, key):
    c, m, lab = ST[key]
    ax.plot(NS, ys, color=c, marker=m, lw=1.6, ms=5.5, label=lab)


def new(w=6.4, h=3.5):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200); return fig, ax


def finish(fig, ax, title, xl, yl, name, legend=True):
    ax.set_title(title, fontsize=10); ax.set_xlabel(xl); ax.set_ylabel(yl)
    ax.set_xscale("log"); ax.set_xticks(NS); ax.set_xticklabels([f"10$^{{{int(math.log10(n))}}}$" for n in NS])
    if legend: ax.legend(frameon=True, fontsize=8, loc="upper left")
    stamp(fig); fig.tight_layout(rect=(0, 0.02, 1, 1)); fig.savefig(f"{F}/{name}.png"); plt.close(fig)


# 9.5 time per found search
fig, ax = new()
for a in ST: line(ax, [B[n][a]["t_found"] for n in NS], a)
ax.set_yscale("log"); finish(fig, ax, "Average search time vs input size (log-log)", "Number of records n", "Average time per successful search (microseconds)", "fig9_5_time")
# 9.6 comparisons
fig, ax = new()
for a in ST: line(ax, [B[n][a]["c_found"] for n in NS], a)
ax.set_yscale("log"); finish(fig, ax, "Average number of comparisons vs input size (log-log)", "Number of records n", "Average key comparisons per successful search", "fig9_6_comps")
# 9.7 preprocessing
fig, ax = new()
c, m, lab = ST["binary"]; ax.plot(NS, [B[n]["sort_ms"] for n in NS], color=c, marker=m, lw=1.6, ms=5.5, label="Binary search - sort")
c, m, lab = ST["hash"]; ax.plot(NS, [B[n]["hash_build_ms"] for n in NS], color=c, marker=m, lw=1.6, ms=5.5, label="Hash table - build")
ax.set_yscale("log"); finish(fig, ax, "Preprocessing cost vs input size (linear search needs none)", "Number of records n", "Preprocessing time (milliseconds)", "fig9_7_prep")

# 10.1 theory vs measurement (three panels)
fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.9), dpi=200)
th_lin = [(n + 1) / 2 for n in NS]; th_bin = [math.log2(n + 1) - 1 for n in NS]
th_hash = [0.5 * (1 + 1 / (1 - B[n]["hash_load"])) for n in NS]
for ax, key, th, ttl in zip(axs, ("linear", "binary", "hash"), (th_lin, th_bin, th_hash), ("Linear: (n+1)/2", "Binary: log$_2$(n+1) - 1", "Hash: (1 + 1/(1-α))/2")):
    c, m, lab = ST[key]
    ax.plot(NS, th, "--", color="#333", lw=1.2, label="theory")
    ex = [B[n][key].get("exact_c_found", B[n][key]["c_found"]) for n in NS]
    ax.plot(NS, ex, color=c, marker=m, lw=0, ms=6, label="measured")
    ax.set_xscale("log"); ax.set_xticks(NS); ax.set_xticklabels(["10$^3$", "10$^4$", "10$^5$", "10$^6$"])
    ax.set_title(ttl, fontsize=8.5); ax.legend(fontsize=7, frameon=True)
    if key == "linear": ax.set_yscale("log")
    elif key == "binary": ax.set_ylim(8, 20)
    else: ax.set_ylim(1.3, 1.7)
axs[0].set_ylabel("comparisons per successful search"); axs[1].set_xlabel("Number of records n")
stamp(fig); fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(f"{F}/fig10_1_theory.png"); plt.close(fig)

# 10.2 normalised time
fig, ax = new(6.4, 3.3)
g = {"linear": lambda n: n, "binary": lambda n: math.log2(n), "hash": lambda n: 1.0}
for a in ST:
    v = [B[n][a]["t_found"] / g[a](n) for n in NS]; line(ax, [x / v[0] for x in v], a)
ax.axhline(1, color="#555", ls=":", lw=1); ax.set_yscale("log")
from matplotlib.ticker import ScalarFormatter, NullFormatter
ax.yaxis.set_major_formatter(ScalarFormatter()); ax.yaxis.set_minor_formatter(NullFormatter()); ax.set_yticks([0.5, 1, 2, 3, 4])
finish(fig, ax, "Measured time divided by predicted growth (normalised to n = 1,000)", "Number of records n", "ratio (1 = exact agreement)", "fig10_2_norm")

# 12.2 total cost of one day
fig, ax = plt.subplots(figsize=(6.4, 3.1), dpi=200)
labels = ["Linear\n(projected)", "Binary search\n(original)", "Hash table\n(linear probing)"]
vals = [T12["day_lin"], T12["day_bin"], T12["day_hash"]]
bars = ax.bar(labels, vals, color=[ST["linear"][0], ST["binary"][0], ST["hash"][0]], width=0.5)
ax.set_yscale("log"); ax.set_ylabel("CPU seconds per day (log scale)")
for b, v in zip(bars, vals): ax.text(b.get_x() + b.get_width() / 2, v * 1.15, f"{v:,.1f} s", ha="center", fontsize=8.5)
ax.axhline(86400, color="#333", ls="--", lw=1); ax.text(2.45, 86400 * 1.15, "24 h = 86,400 s", ha="right", fontsize=8)
ax.set_ylim(1, 1e6); ax.set_title("Cost of one day: daily preprocessing + 1,200,000 searches", fontsize=10)
stamp(fig); fig.tight_layout(rect=(0, 0.02, 1, 1)); fig.savefig(f"{F}/fig12_2_day.png"); plt.close(fig)
print("graphs ok")
