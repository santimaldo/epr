
from Read import read_epr
import matplotlib.pyplot as plt
import numpy as np


path = r"C:\Users\Santi\OneDrive - University of Cambridge\EPRdata\2026-01-08_Rui_pulsed-charged\01_next-day_beforeDNP"
file = "20260109_132404483_sm2974_Li-KBr_range-330-345mT_mod0.001mT_power0.1mW"
df1 = read_epr(file, path=path)

path = r"C:\Users\Santi\OneDrive - University of Cambridge\EPRdata\2025-11-13_Rui\01_CCsample_beforeDNP"
file = "20251114_104936669_sm2974_Rui_330-345mT_mod-0.001mT"
df2 = read_epr(file, path=path)

fig, ax = plt.subplots()
for df in [df1, df2]:
    B = df["BField [mT]"]    
    spec = df["MW_Absorption []"]
    spec/= -spec.min()
    ax.plot(B, spec)
    
ax.set_xlabel("B (mT)")
ax.set_ylabel("I (a.u.)")
ax.set_xlim([335, 337])
