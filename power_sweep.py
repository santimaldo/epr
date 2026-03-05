# ============================================================
# GIPI: Power sweep – lectura, análisis y ploteo usando read_epr
# ============================================================

import os
import numpy as np
import matplotlib.pyplot as plt
from Read import read_epr  # tu función optimizada

# ------------------------------------------------------------
# Parameters
# ------------------------------------------------------------
data_folder = r"C:\Users\Santi\OneDrive - University of Cambridge\EPRdata\2025-12-23_LiLisym_LP57\04_2026-01-07_Before-DNP\01_power_sweep_mod0.1mT_more-points\sm2974_Li-KBr_range-330-345mT_mod0.1mT_powerSweep_01"

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

# ------------------------------------------------------------
# Plot spectra
# ------------------------------------------------------------
fig_spec, ax_spec = plt.subplots()

for fname in files:

    # Remove extension for read_epr
    name_without_ext = os.path.splitext(fname)[0]

    # Read spectrum using optimized function
    df = read_epr(name_without_ext, path=data_folder)

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
ax.plot(powers, Amp, 'o-')
ax.set_xscale('log')
ax.set_xlabel('Power [mW]')
ax.set_ylabel('Amp (max)')
fig.tight_layout()

# ------------------------------------------------------------
# AtoB vs Power
# ------------------------------------------------------------
fig, ax = plt.subplots()
ax.plot(powers, AtoB, 'o-')
ax.set_xscale('log')
ax.set_xlabel('Power [mW]')
ax.set_ylabel('A / B')
fig.tight_layout()

# ------------------------------------------------------------
# DeltaBpp vs Power
# ------------------------------------------------------------
fig, ax = plt.subplots()
ax.plot(powers, DeltaBpp, 'o-')
ax.set_xscale('log')
ax.set_xlabel('Power [mW]')
ax.set_ylabel('DeltaBpp [mT]')
fig.tight_layout()

plt.show()