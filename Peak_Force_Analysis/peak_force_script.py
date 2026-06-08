import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

order  = [ 'WT ac','K238ac',  'K412ac','WT', 'K238R', 'K412R']
colors = {
    'WT ac': 'red',
    'K238ac': 'blue',
    'K412ac': 'green',
    'WT': 'red',
    'K238R': 'blue',
    'K412R': 'green'
}

data = (pd.DataFrame({
                'Variant': ['WT ac', 'K238ac', 'K412ac','WT', 'K238R', 'K412R'],
                'PeakForce': [702.93, 836.89,  772.02, 734.16, 774.71, 809.76]})
          .set_index('Variant')
          .loc[order]               
          .reset_index())

fig, ax = plt.subplots(figsize=(8, 6), dpi=600)

sns.barplot(data=data, x='Variant', y='PeakForce',
            order=order,
            palette=[colors[v] for v in order],
            width=0.4, ax=ax)       

edge_styles = {
    "K238R": {'color': 'black', 'linewidth': 2, 'linestyle': ':'}, 
    "K412R": {'color': 'black', 'linewidth': 2, 'linestyle': ':'},  
    "WT": {'color': 'black', 'linewidth': 2, 'linestyle': ':'},     
}

for i, variant in enumerate(data['Variant']):
    if variant in edge_styles:
        ax.patches[i].set_edgecolor(edge_styles[variant]['color'])
        ax.patches[i].set_linewidth(edge_styles[variant]['linewidth'])
        ax.patches[i].set_linestyle(edge_styles[variant]['linestyle'])

for i, v in enumerate(data['PeakForce']):
    ax.text(i, v + 10, f'{v:.2f}', ha='center', va='bottom', fontsize=20)

ax.set_xlabel('')                                
ax.set_ylabel('Peak Force (kJmol⁻¹nm⁻¹)', fontsize=26)
ax.set_ylim(0, 900)
ax.set_yticks([0, 200, 400, 600, 800])
ax.tick_params(axis='x', labelsize=18)
ax.tick_params(axis='y', labelsize=20)

sns.despine(ax=ax)


separator_x_pos = 2.5 
ax.axvline(x=separator_x_pos, color='black', linestyle='-', linewidth=2)


fig.tight_layout()

fig.savefig('Peak_force_high_res.png', dpi=300, bbox_inches='tight')

plt.show()

