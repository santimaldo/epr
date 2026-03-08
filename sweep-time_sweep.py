# ============================================================
# GIPI: Sweep time analysis – lectura, filtrado y ploteo
# ============================================================

import os
import numpy as np
import matplotlib.pyplot as plt
from EPR import calculate_T2, read_epr

# ------------------------------------------------------------
# Parameters
# ------------------------------------------------------------
data_folder = r"C:\Users\Santi\OneDrive - University of Cambridge\EPRdata\2026-02_InSitu\00_Li-Cu_edge"

target_modulation = 0.001  # mT

# ------------------------------------------------------------
# List CSV files
# ------------------------------------------------------------
files = sorted([f for f in os.listdir(data_folder) if f.endswith('.csv')])

if len(files) == 0:
    raise RuntimeError("No CSV files found in the folder.")

# ------------------------------------------------------------
# Containers for results
# ------------------------------------------------------------
sweep_times = []
Amp = []
AtoB = []
DeltaBpp = []

# ------------------------------------------------------------
# Plot spectra
# ------------------------------------------------------------
fig_spec, ax_spec = plt.subplots()

for fname in files:

    name_without_ext = os.path.splitext(fname)[0]

    df = read_epr(name_without_ext, path=data_folder)

    params = df.attrs["params"]

    modulation = float(params["Modulation"])

    # --------------------------------------------------------
    # Filter by modulation amplitude
    # --------------------------------------------------------
    if abs(modulation-target_modulation) > 1e-4:
        continue

    sweep_time = float(params["SweepTime"])

    x = df["BField [mT]"].values
    y = df["MW_Absorption []"].values

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
    sweep_times.append(sweep_time)

    ax_spec.plot(x, y, label=f"{sweep_time:.1f} s")

ax_spec.set_xlabel("B [mT]")
ax_spec.set_ylabel("Amplitude [a.u.]")
ax_spec.set_xlim([335, 337])
ax_spec.legend(title="Sweep time")
fig_spec.tight_layout()

# ------------------------------------------------------------
# Convert to arrays and sort by sweep time
# ------------------------------------------------------------
sweep_times = np.array(sweep_times)
Amp = np.array(Amp)
AtoB = np.array(AtoB)
DeltaBpp = np.array(DeltaBpp)

order = np.argsort(sweep_times)

sweep_times = sweep_times[order]
Amp = Amp[order]
AtoB = AtoB[order]
DeltaBpp = DeltaBpp[order]

# ------------------------------------------------------------
# Amp vs Sweep time
# ------------------------------------------------------------
fig, ax = plt.subplots()
ax.plot(sweep_times, Amp, "o-")
ax.set_xlabel("Sweep time [s]")
ax.set_ylabel("Amp (max)")
fig.tight_layout()

# ------------------------------------------------------------
# A/B vs Sweep time
# ------------------------------------------------------------
fig, ax = plt.subplots()
ax.plot(sweep_times, AtoB, "o-")
ax.set_xlabel("Sweep time [s]")
ax.set_ylabel("A / B")
fig.tight_layout()

#%%------------------------------------------------------------
# DeltaBpp vs Sweep time
# ------------------------------------------------------------
fig, ax = plt.subplots()
ax.plot(sweep_times, DeltaBpp, "o-")
ax.set_xlabel("Sweep time [s]")
ax.set_ylabel(r"$\Delta$B$_{pp}$ [mT]")
fig.tight_layout()

#%%------------------------------------------------------------
# T2 vs Swep time
# ------------------------------------------------------------
fig, ax = plt.subplots()
T2 =calculate_T2(DeltaBpp)
ax.plot(sweep_times, T2/1e-9, "o-")
ax.set_xlabel("Sweep time [s]")
ax.set_ylabel("T2 [ns]")
fig.tight_layout()

plt.show()
# %%
