# ============================================================
# GIPI: Power sweep – lectura, análisis y ploteo usando read_epr
# ============================================================

import os
import numpy as np
import matplotlib.pyplot as plt
from EPR import *

# ------------------------------------------------------------
# Parameters
# ------------------------------------------------------------
# data_folder = r"C:\Users\Santi\OneDrive - University of Cambridge\EPRdata\2025-12-23_LiLisym_LP57\04_2026-01-07_Before-DNP\01_power_sweep_mod0.1mT_more-points\sm2974_Li-KBr_range-330-345mT_mod0.1mT_powerSweep_01"

# # # Li on Cu - sweep TIme 60 s  - mod 0.001 mT
# data_folder = r"C:\Users\Santi\OneDrive - University of Cambridge\EPRdata\2026-02_InSitu\00_Li-Cu_edge\00_PwerSweep_60s\sm2974_Li-Cu_330-345mT_60s_mod0.001mT_01"

# # Li on Cu - sweep TIme 300 s - mod 0.001 mT
# data_folder = r"C:\Users\Santi\OneDrive - University of Cambridge\EPRdata\2026-02_InSitu\00_Li-Cu_edge\01_PowerSweep_300s\sm2974_Li-Cu_330-345mT_180s_mod0\sm2974_Li-Cu_330-345mT_180s_mod0.001mT_01"

# Li on Cu - sweep TIme 300 s - mod 0.1 mT
data_folder = r"C:\Users\Santi\OneDrive - University of Cambridge\EPRdata\2026-02_InSitu\00_Li-Cu_edge\01_PowerSweep_300s\sm2974_Li-Cu_330-345mT_60s_mod0.001mT_01\sm2974_Li-Cu_330-345mT_180s_mod0.001mT"





# ------------------------------------------------------------
# List CSV files
# ------------------------------------------------------------
files = sorted([f for f in os.listdir(data_folder) if f.endswith('.csv')])

if len(files) == 0:
    raise RuntimeError('No CSV files found in the folder.')

# ------------------------------------------------------------
# Containers for results
# ------------------------------------------------------------
powers = []
Amp = []
AtoB = []
DeltaBpp = []
dfs = []
# ------------------------------------------------------------
# Plot spectra
# ------------------------------------------------------------
fig_spec, ax_spec = plt.subplots()

for fname in files:

    # Remove extension for read_epr
    name_without_ext = os.path.splitext(fname)[0]

    # Read spectrum using optimized function
    df = read_epr(name_without_ext, path=data_folder)
    dfs.append(df)
    x = df["BField [mT]"].values
    y = df["MW_Absorption []"].values

    # Extract MicrowavePower directly from attrs
    power_mW = float(df.attrs["params"]["MicrowavePower"])

    # -----------------------------
    # Peak analysis
    # -----------------------------
    idx_max = np.argmax(y)
    idx_min = np.argmin(y)

    y_max = y[idx_max]
    y_min = y[idx_min]

    x_max = x[idx_max]
    x_min = x[idx_min]

    Amp.append(y_max)
    AtoB.append(abs(y_max / y_min))
    DeltaBpp.append(abs(x_max - x_min))
    powers.append(power_mW)

    ax_spec.plot(x, y, label=f'{power_mW:.4f} mW')

ax_spec.set_xlabel('B [mT]')
ax_spec.set_ylabel('Amplitude [a.u.]')
ax_spec.set_xlim([335, 337])
fig_spec.tight_layout()

# ------------------------------------------------------------
# Convert to arrays and sort by power
# ------------------------------------------------------------
powers = np.array(powers)
Amp = np.array(Amp)
AtoB = np.array(AtoB)
DeltaBpp = np.array(DeltaBpp)

order = np.argsort(powers)

powers = powers[order]
Amp = Amp[order]
AtoB = AtoB[order]
DeltaBpp = DeltaBpp[order]

# ------------------------------------------------------------
# Amp vs Power
# ------------------------------------------------------------
fig, ax = plt.subplots()
ax.plot(np.sqrt(powers), Amp, 'o-')
ax.set_xlabel(r'Power$^{1/2}$ [mW$^{1/2}$]')
ax.set_ylabel('Amp (max)')
fig.tight_layout()

# ------------------------------------------------------------
# AtoB vs Power
# ------------------------------------------------------------
fig, ax = plt.subplots()
ax.plot(np.sqrt(powers), AtoB, 'o-')
ax.set_xlabel(r'Power$^{1/2}$ [mW$^{1/2}$]')
ax.set_ylabel('A / B')
fig.tight_layout()

# ------------------------------------------------------------
# DeltaBpp vs Power
# ------------------------------------------------------------
fig, ax = plt.subplots()
ax.plot(np.sqrt(powers), DeltaBpp, 'o-')
ax.set_xlabel(r'Power$^{1/2}$ [mW$^{1/2}$]')
ax.set_ylabel(r"$\Delta$B$_{pp}$ [mT]")
fig.tight_layout()

#%%------------------------------------------------------------
# T2 vs Swep time
# ------------------------------------------------------------
fig, ax = plt.subplots()
T2 =calculate_T2(DeltaBpp)
ax.plot(np.sqrt(powers), T2/1e-9, 'o-')
ax.set_xlabel(r'Power$^{1/2}$ [mW$^{1/2}$]')
ax.set_ylabel("T2 [ns]")
fig.tight_layout()



#%% Fist and last spectra

fig, ax = plt.subplots()
colors = ['navy', 'firebrick']
ax.set_prop_cycle(color=colors)
for ii, df in enumerate([dfs[0], dfs[-1]]):
    B = df["BField [mT]"]
    spec = df["MW_Absorption []"]
    spec /= -spec.min()
    ax.plot(B, spec, color=colors[ii], label=df.attrs["params"]["MicrowavePower"])
ax.set_xlabel("B (mT)")
ax.set_ylabel("I (a.u.)")
ax.set_xlim([335, 337])
ax.legend(title="Power (mW)")
# %%
plt.show()