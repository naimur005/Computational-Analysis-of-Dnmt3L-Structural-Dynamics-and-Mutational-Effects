import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

file_paths = {
    "WT ac": "both_ace_2.xvg",
    "K238ac": "238ace_1.xvg",
    "K412ac": "412ace_2.xvg",

    "WT": "wt_3.xvg",
    "K238R": "K238R_pullf.xvg",
    "K412R": "K412R_pullf-R2.xvg"
}

colors = {
    "WT ac": "red",
    "K238ac": "blue",
    "K412ac": "green",
    "WT": "red",
    "K238R": "blue",
    "K412R": "green"
}

linestyles = {
    "WT ac": "-",  
    "K238ac": "-",  
    "K412ac": "-",  
    "WT": ":",     
    "K238R": ":",   
    "K412R": ":"    
}

plt.figure(figsize=(12, 6))

peak_forces = {}

for label, file_path in file_paths.items():
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data_lines = [line for line in lines if not line.startswith(('#', '@'))]
    data_str = ''.join(data_lines)
    data = pd.read_csv(StringIO(data_str), delim_whitespace=True, header=None)

    time = data[0]
    force = data[1]

    peak_force = force.max()
    peak_time = time[force.idxmax()]
    peak_forces[label] = (peak_force, peak_time)

    plt.plot(time, force, label=f'{label}', color=colors[label], linestyle=linestyles[label], alpha=0.7)


plt.xlabel('Time (ps)', fontsize=30)
plt.ylabel('Force (kJmol⁻¹nm⁻¹)', fontsize=30)

#plt.legend(fontsize=12)

plt.xticks(fontsize=22)
plt.yticks(fontsize=22)

plt.tight_layout()
plt.show()

for label, (peak_force, peak_time) in peak_forces.items():
    print(f"{label} - Peak Force: {peak_force:.2f} kJ/mol/nm at {peak_time:.2f} ps")

plt.savefig("fig-pull-all-mutants_noLegend.png", dpi=600, transparent=True)
plt.show()

