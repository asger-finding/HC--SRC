import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import locale

# Indstil for dansk numerisk format
locale.setlocale(locale.LC_NUMERIC, 'da_DK.UTF-8')
plt.rcParams['axes.formatter.use_locale'] = True

def hypothetical(t):
    return 15/16+(37-15/16)*np.exp(-1/488*t)

def expLoose(t):
    return -0.06618+36.69*np.exp(-0.001866*t)

def expStrict(t):
    return 0.8+37.0*np.exp(-0.002033*t)

def get_R2(func, t, T):
    values = func(t)
    residuals = T - values
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((T - np.mean(T))**2)
    r_squared = 1 - (ss_res / ss_tot)
    return r_squared

def add_function_annotation(ax, x, y, text, line_pos='right', color='#0000ff', 
                          linewidth=1, fontsize=10, focus=False):
    """
    Annoteringsfunktion
    
    Parametre:
    ax - matplotlib axes objekt
    x - x-position i sekunder (numerisk)
    y - y-position
    text - annoteringstekst
    line_pos - tekstplacering ('right', 'left', 'top', 'bottom')
    color - farve
    linewidth - linjetykkelse
    fontsize - tekststørrelse
    """
    x_range = ax.get_xlim()[1] - ax.get_xlim()[0]
    y_range = ax.get_ylim()[1] - ax.get_ylim()[0]
    
    # Offset i datarange
    offset_factor = 0.05  # 5% af akselængden
    x_offset = x_range * offset_factor
    y_offset = y_range * offset_factor
    
    if line_pos == 'right':
        xytext = (x_offset, 0)
        ha = 'left'
        va = 'center'
    elif line_pos == 'left':
        xytext = (-x_offset, 0)
        ha = 'right'
        va = 'center'
    elif line_pos == 'top':
        xytext = (0, y_offset)
        ha = 'center'
        va = 'bottom'
    else:  # bottom
        xytext = (0, -y_offset)
        ha = 'center'
        va = 'top'
    
    ann = ax.annotate(
        text, 
        xy=(x, y),
        xytext=xytext,
        textcoords='offset points',
        ha=ha,
        va=va,
        fontsize=fontsize,
        color=color,
        alpha=1.0 if focus else 0.3,
        arrowprops=dict(
            alpha=1.0 if focus else 0.3,
            arrowstyle="->",
            color=color,
            linewidth=linewidth,
            shrinkA=5,
            shrinkB=5,
            connectionstyle="arc3,rad=0.2"
        ),
        bbox=dict(
            boxstyle='round,pad=0.5',
            fc='white',
            alpha=0.9,
            edgecolor='lightgray'
        )
    )

    if focus == False:
        ann.set_zorder(1)

    ax.figure.canvas.draw()
    return ann

def add_minmax():
    max_temp = statistics['Maksimum']
    min_temp = statistics['Minimum']
    plt.axhline(y=max_temp, color='#fa7a55', linestyle=':', label='Maksimum (' + f"{statistics['Maksimum']:.2f}".replace('.', ',') + '°C)')
    plt.axhline(y=min_temp, color='#d11d05', linestyle=':', label='Minimum (' + f"{statistics['Minimum']:.2f}".replace('.', ',') + '°C)')

def add_hypothermia_stages():
    stage_1 = 35
    stage_2 = 32
    stage_3 = 28
    stage_4 = 24
    plt.axhline(y=stage_1, color='#9e9e9e', linestyle=':', label='Stadie 1 (35-32°C)')
    plt.axhline(y=stage_2, color='#8b8b8b', linestyle=':', label='Stadie 2 (<32-28°C)')
    plt.axhline(y=stage_3, color='#777777', linestyle=':', label='Stadie 3 (<28-24°C)')
    plt.axhline(y=stage_4, color='#646464', linestyle=':', label='Stadie 4 (<24°C)')

def print_statistics(stats):
    print("Temperaturstatistics:")
    for key, value in stats.items():
        print(f"{key}: {value:.2f}" if isinstance(value, (float, np.floating)) else f"{key}: {value}")

# Indlæs dataen for kyllingebryst
df = pd.read_csv('Simulering_Kyllingebryst.csv')
df.columns = ['tid', 'temperatur']

# Beregn og print statistics
R2_hypothetical = get_R2(hypothetical, df['tid'], df['temperatur'])
R2_expLoose = get_R2(expLoose, df['tid'], df['temperatur'])
R2_expStrict = get_R2(expStrict, df['tid'], df['temperatur'])
statistics = {
    'Antal målinger': len(df),
    'Gennemsnit': df['temperatur'].mean(),
    'Median': df['temperatur'].median(),
    'Minimum': df['temperatur'].min(),
    'Maksimum': df['temperatur'].max(),
    'Standardafvigelse': df['temperatur'].std(),
    '25. percentil': df['temperatur'].quantile(0.25),
    '75. percentil': df['temperatur'].quantile(0.75),
    'R²-værdi for hypotetisk model': R2_hypothetical,
    'R²-værdi for løst kurvefit': R2_expLoose,
    'R²-værdi for stramt kurvefit': R2_expStrict
}
print_statistics(statistics)

# Opret diagrammet
plt.figure(figsize=(12, 6))

# Tilføj hypotermi faser
# add_hypothermia_stages()

# Tilføj min-max linjer
add_minmax()

# --- Funktionplots ---
focus = 0

# Plot temperaturdataen
plt.plot(df['tid'], df['temperatur'], 
         label='Nedkølingstemperatur', 
         color='#ff0000', 
         linewidth=2.0,
         alpha=1.0 if focus == 0 else 0.3,
         )

mid_idx = len(df) // 2

# Plot hypotetisk model
plt.plot(df['tid'], hypothetical(df['tid']),
        color='#0000ff',
        linestyle='-' if focus == 1 else '--',
        linewidth=1.5 if focus == 1 else 1.0,
        alpha=1.0 if focus == 1 else 0.3)
# Tilføj annotering
R2_hypotheticalFormatted = f"{R2_hypothetical:.4f}".replace('.', ',')
text = (r'$\mathrm{Hypotetisk\;model:}$' + '\n' +
        r'$T(t)=\frac{15}{16}+(37-\frac{15}{16})\cdot e^{-1/488\cdot t}$' + '\n' +
        f'$R^{{2}}={R2_hypotheticalFormatted}$')
x_pos = df['tid'].iloc[mid_idx - 240]
y_pos = hypothetical(df['tid']).iloc[mid_idx - 240]
add_function_annotation(plt.gca(), x_pos, y_pos, text, 
                      line_pos='right', color='#0000ff',
                      fontsize=9, focus=focus==1)

# Plot løst fit
plt.plot(df['tid'], expLoose(df['tid']),
        color='#00ff00',
        linestyle='-' if focus == 2 else '--',
        linewidth=1.5 if focus == 2 else 1.0,
        alpha=1.0 if focus == 2 else 0.3)
# Tilføj annotering
R2_expLooseFormatted = f"{R2_expLoose:.4f}".replace('.', ',')
text = (r'$\mathrm{Løst\;kurvefit:}$' + '\n' +
        r'$T(t)=-0,06618+36,69\cdot e^{-0,001866\cdot t}$' + '\n' +
        f'$R^{{2}}={R2_expLooseFormatted}$')
x_pos = df['tid'].iloc[mid_idx - 120]
y_pos = hypothetical(df['tid']).iloc[mid_idx - 120]
add_function_annotation(plt.gca(), x_pos, y_pos, text, 
                      line_pos='right', color='#00bb00',
                      fontsize=9, focus=focus==2)

# Plot stramt fit
plt.plot(df['tid'], expStrict(df['tid']),
        color='#c633ff',
        linestyle='-' if focus == 3 else '--',
        linewidth=1.5 if focus == 3 else 1.0,
        alpha=1.0 if focus == 3 else 0.3)
# Tilføj annotering
R2_expStrictFormatted = f"{R2_expStrict:.4f}".replace('.', ',')
text = (r'$\mathrm{Stramt\;kurvefit:}$' + '\n' +
        r'$T(t)=0,8+37,0\cdot e^{-0,002033\cdot t}$' + '\n' +
        f'$R^{{2}}={R2_expStrictFormatted}$')
x_pos = df['tid'].iloc[mid_idx + 40]
y_pos = hypothetical(df['tid']).iloc[mid_idx + 40]
add_function_annotation(plt.gca(), x_pos, y_pos, text, 
                      line_pos='right', color='#c633ff',
                      fontsize=9, focus=focus==3)
# --- Funktionsplots slut ---

# Tilpas og vis
plt.title('Nedkølingshastighed af 37°C kyllingebryst i 0,8°C vand', fontsize=14)
plt.xlabel('Tid (s)', fontsize=12)
plt.ylabel('Temperatur (°C)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
