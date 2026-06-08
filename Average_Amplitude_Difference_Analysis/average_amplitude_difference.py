import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def per_ns_amplitude_xvg(xvg_file):
    """Calculate local RMSD amplitude (max-min) within each ns window from XVG."""
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
    df = pd.DataFrame(data, columns=["Time (ns)", "RMSD (Å)"])
    df["ns_bin"] = df["Time (ns)"].astype(int)
    grouped = df.groupby("ns_bin")["RMSD (Å)"].agg(lambda x: x.max() - x.min()).reset_index()
    grouped.rename(columns={"RMSD (Å)": "Amplitude_per_ns"}, inplace=True)
    return grouped

def per_ns_amplitude_csv(csv_file):
    """Calculate amplitude per ns from CSV with 'Time(ns)' and 'Value (Å)'."""
    df = pd.read_csv(csv_file)
    df["ns_bin"] = df["Time(ns)"].astype(int)
    grouped = df.groupby("ns_bin")["Value (Å)"].agg(lambda x: x.max() - x.min()).reset_index()
    grouped.rename(columns={"Value (Å)": "Amplitude_per_ns"}, inplace=True)
    return grouped


wt_amp = per_ns_amplitude_xvg("rmsd_wt_500ns.xvg")
ace238_amp = per_ns_amplitude_xvg("rmsd_238ac_500ns.xvg")
bothace_amp = per_ns_amplitude_xvg("rmsd_bothace_500ns.xvg")
new_amp = per_ns_amplitude_xvg("rmsd_412ac_500ns.xvg")

amp_238R = per_ns_amplitude_csv("K238R_rmsd_500ns.csv")
amp_412R = per_ns_amplitude_csv("K412R_rmsd_500ns.csv")


avg_amp = {
     "WT ac": bothace_amp["Amplitude_per_ns"].mean(),
     "K238ac": ace238_amp["Amplitude_per_ns"].mean(),
     "K412ac": new_amp["Amplitude_per_ns"].mean(),  
     "WT": wt_amp["Amplitude_per_ns"].mean(),
     "K238R": amp_238R["Amplitude_per_ns"].mean(),
     "K412R": amp_412R["Amplitude_per_ns"].mean()
}

df_avg_amp = pd.DataFrame(list(avg_amp.items()), columns=["Variant", "AvgAmplitude_per_ns"])


fig, ax = plt.subplots(figsize=(8, 6), dpi=600)

colors = {
    "WT ac": "red", "K238ac": "blue", "K412ac": "green", "WT": "red",
     "K238R": "blue", "K412R": "green"
}

edge_styles = {
    "WT": {'color': 'black', 'linewidth': 2, 'linestyle': ':'},
    "K238R": {'color': 'black', 'linewidth': 2, 'linestyle': ':'},
    "K412R": {'color': 'black', 'linewidth': 2, 'linestyle': ':'},

}

sns.barplot(data=df_avg_amp,
            x='Variant', y='AvgAmplitude_per_ns',
            palette=[colors[v] for v in df_avg_amp['Variant']],
            width=0.4, ax=ax)

for i, v in enumerate(df_avg_amp['AvgAmplitude_per_ns']):
    ax.text(i, v + 0.02, f'{v:.2f}', ha='center', va='bottom', fontsize=20)

for i, variant in enumerate(df_avg_amp['Variant']):
    if variant in edge_styles:
        ax.patches[i].set_edgecolor(edge_styles[variant]['color'])
        ax.patches[i].set_linewidth(edge_styles[variant]['linewidth'])
        ax.patches[i].set_linestyle(edge_styles[variant]['linestyle'])

ax.set_xlabel('')  
ax.set_ylabel('Mean Amplitude Difference (Å)', fontsize=26)
ax.set_ylim(0, 0.70)
ax.tick_params(axis='x', labelsize=18)
ax.set_yticks([0, 0.2, 0.4, 0.6])
ax.tick_params(axis='y', labelsize=20)

sns.despine(ax=ax)


separator_x_pos = 2.5  
ax.axvline(x=separator_x_pos, color='black', linestyle='-', linewidth=2)

fig.tight_layout()
fig.savefig('Average_Amplitude_Differences_Bar_Plot.png', dpi=300)
plt.show()

