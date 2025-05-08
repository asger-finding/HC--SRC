import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import locale

# Indstil for dansk numerisk format
locale.setlocale(locale.LC_NUMERIC, 'da_DK.UTF-8')
plt.rcParams['axes.formatter.use_locale'] = True

def hypothetical(t):
    return 1.1724395+(37-1.1724395)*np.exp(-0.0019307*t)

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

def add_hypothermia_stages():
    stage_1 = 35
    stage_2 = 32
    stage_3 = 28
    stage_4 = 24
    plt.axhline(y=stage_1, color='#9e9e9e', linestyle=':', label='Stadie 1 (35-32°C)')
    plt.axhline(y=stage_2, color='#8b8b8b', linestyle=':', label='Stadie 2 (<32-28°C)')
    plt.axhline(y=stage_3, color='#777777', linestyle=':', label='Stadie 3 (<28-24°C)')
    plt.axhline(y=stage_4, color='#646464', linestyle=':', label='Stadie 4 (<24°C)')

# Indlæs dataen for kyllingebryst
t = np.arange(0, 1801, 10)
T = hypothetical(t)

# Opret diagrammet
plt.figure(figsize=(12, 6))

# Tilføj hypotermi faser
add_hypothermia_stages()

# --- Funktionplots ---
# Plot menneskelig model
plt.plot(t, hypothetical(t),
        color='#0000ff',
        linestyle='-',
        linewidth=1.5,
        alpha=1.0)
# Tilføj annotering
idx = len(t) // 3
text = (r'$\mathrm{Hypotetisk\;model\;for\;menneske:}$' + '\n' +
        r'$T(t)=1,1724395+(37-1,1724395)\cdot e^{-0,0019307\cdot t}$' + '\n')
add_function_annotation(plt.gca(), t[idx], T[idx], text, 
                      line_pos='right', color='#0000ff',
                      fontsize=9, focus=True)
# --- Funktionsplots slut ---

# Tilpas og vis
plt.title('Nedkølingshastighed menneske (70 kg) i 0,8°C vand', fontsize=14)
plt.xlabel('Tid (s)', fontsize=12)
plt.ylabel('Temperatur (°C)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
