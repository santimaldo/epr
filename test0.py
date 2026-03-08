
from Read import read_epr
import matplotlib.pyplot as plt
import numpy as np
# from scipy.constants import physical_constants


path = r"C:\Users\Santi\OneDrive - University of Cambridge\EPRdata\2026-01-08_Rui_pulsed-charged\01_next-day_beforeDNP"
file = "20260109_132404483_sm2974_Li-KBr_range-330-345mT_mod0.001mT_power0.1mW"
df1 = read_epr(file, path=path)

path = r"C:\Users\Santi\OneDrive - University of Cambridge\EPRdata\2025-11-13_Rui\01_CCsample_beforeDNP"
file = "20251114_104936669_sm2974_Rui_330-345mT_mod-0.001mT"
df2 = read_epr(file, path=path)

# para convertir frequencia a campo magnetico: B0 = h*F0/(g*mu_B)
# gamma_e = physical_constants["electron gyromag. ratio"][0] # in rad/s/T

fig, ax = plt.subplots()
for df in [df1, df2]:
    B = df["BField [mT]"]
    # F0 = df.attrs["params"]["Frequency"] * 1e9
    # B0 = 2*np.pi*F0/gamma_e / 1e-3 # en mT
    spec = df["MW_Absorption []"]
    spec/= -spec.min()
    ax.plot(B, spec)
    
ax.set_xlabel("B (mT)")
ax.set_ylabel("I (a.u.)")
ax.set_xlim([335, 337])


