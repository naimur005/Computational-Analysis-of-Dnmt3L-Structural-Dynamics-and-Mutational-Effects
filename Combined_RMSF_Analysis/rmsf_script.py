import pandas as pd
import matplotlib.pyplot as plt


def per_ns_rmsf_xvg(xvg_file):
    """Process RMSF data from XVG, multiplying by 10."""
    data = []
    with open(xvg_file, "r") as f:
        for line in f:
            if line.startswith(("#", "@")):  
                continue
            parts = line.strip().split()
            if len(parts) == 2:
                try:
                    t, v = float(parts[0]), float(parts[1])
                    data.append((t, v * 10))  
                except ValueError:
                    continue
    df = pd.DataFrame(data, columns=["Time (ns)", "RMSF (Å)"])
    return df


def per_ns_rmsf_csv(csv_file):
    """Process RMSF data from CSV without multiplying values."""
    df = pd.read_csv(csv_file)
    df.rename(columns={"Residue Number": "Time (ns)"}, inplace=True)  
    return df


wt_rmsf = per_ns_rmsf_xvg("rmsf_500_wt.xvg")
ace238_rmsf = per_ns_rmsf_xvg("rmsf_500_238.xvg")
bothace_rmsf = per_ns_rmsf_xvg("rmsf_500_bothace.xvg")
ace412_rmsf = per_ns_rmsf_xvg("rmsf_500_412ace.xvg")

amp_238R_rmsf = per_ns_rmsf_csv("K238R_rmsf-2.csv")
amp_412R_rmsf = per_ns_rmsf_csv("K412R_rmsf-2.csv")


plt.figure(figsize=(12, 3.5))


plt.plot(bothace_rmsf["Time (ns)"], bothace_rmsf["RMSF (Å)"], label="WT ac", color="red", linestyle="-")
plt.plot(ace238_rmsf["Time (ns)"], ace238_rmsf["RMSF (Å)"], label="K238ac", color="blue", linestyle="-")

plt.plot(ace412_rmsf["Time (ns)"], ace412_rmsf["RMSF (Å)"], label="K412ac", color="green", linestyle="-")

plt.plot(wt_rmsf["Time (ns)"], wt_rmsf["RMSF (Å)"], label="WT", color="red", linestyle=":")

plt.plot(amp_238R_rmsf["Time (ns)"], amp_238R_rmsf["Value (Å)"], label="K238R", color="blue", linestyle=":")
plt.plot(amp_412R_rmsf["Time (ns)"], amp_412R_rmsf["Value (Å)"], label="K412R", color="green", linestyle=":")


plt.axvline(238, ymin=0, ymax=1, ls="--", color="black", linewidth=0.5)
plt.axvline(412, ymin=0, ymax=1, ls="--", color="black", linewidth=0.5)


plt.xlabel("Residue Number", fontsize=20)
plt.ylabel("RMSF (Å)", fontsize=20)


plt.xticks([100, 150, 200, 250, 300, 350, 400], fontsize=16)
plt.yticks([0, 2, 4, 6, 8], fontsize=16)

plt.ylim(0, 7.5)


plt.legend(loc="upper left", bbox_to_anchor=(1, 1), fontsize=13)


plt.tight_layout()


plt.savefig("fig-all-RMSF_noLegend.png", dpi=600, transparent=True)
plt.show()

