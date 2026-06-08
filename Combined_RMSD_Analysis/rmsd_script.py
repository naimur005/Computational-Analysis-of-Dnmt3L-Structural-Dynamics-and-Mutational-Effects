import pandas as pd
import matplotlib.pyplot as plt

df_wt = pd.read_csv("RMSD_WT_per_ns.csv")
df_bothace = pd.read_csv("RMSD_BothACE_per_ns.csv")
df_238ace = pd.read_csv("RMSD_238ACE_per_ns.csv")
df_238r = pd.read_csv("K238R_rmsd_per-ns.csv")
df_412r = pd.read_csv("K412R_rmsd_per-ns.csv")
df_412ace = pd.read_csv("RMSD_412ACE_per_ns.csv")  

plt.figure(figsize=(12, 6))

plt.plot(df_bothace["Time (ns)"], df_bothace["RMSD (Å)"],
         label="WT ac", color="red", linestyle="-", alpha=0.7, linewidth=1.8)

plt.plot(df_238ace["Time (ns)"], df_238ace["RMSD (Å)"],
         label="K238ac", color="blue", linestyle="-", alpha=0.7, linewidth=1.8)

plt.plot(df_412ace["Time (ns)"], df_412ace["RMSD (Å)"],
         label="K412ac", color="green", linestyle="-", alpha=0.7, linewidth=1.8)

plt.plot(df_wt["Time (ns)"], df_wt["RMSD (Å)"],
         label="WT", color="red", linestyle=":", alpha=0.7, linewidth=1.8)

plt.plot(df_238r["Time (ns)"], df_238r["RMSD (Å)"],
         label="K238R", color="blue", linestyle=":", alpha=0.7, linewidth=1.8)

plt.plot(df_412r["Time (ns)"], df_412r["RMSD (Å)"],
         label="K412R", color="green", linestyle=":", alpha=0.7, linewidth=1.8)

plt.xlabel("Time (ns)", fontsize=30)
plt.ylabel("RMSD (Å)", fontsize=30)

plt.xticks(fontsize=22)
plt.yticks(fontsize=22)

plt.ylim(0, 7)

#legend = plt.legend(loc="upper left", fontsize=14, frameon=False)

plt.tight_layout()

plt.savefig("fig-all-RMSD.png", dpi=300, transparent=True)

plt.show()

