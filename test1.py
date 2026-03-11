
from EPR import *
import matplotlib.pyplot as plt
import numpy as np


# path = r"C:\Users\Santi\OneDrive - University of Cambridge\EPRdata\2026-01-08_Rui_pulsed-charged\01_next-day_beforeDNP"
# file = "20260109_132404483_sm2974_Li-KBr_range-330-345mT_mod0.001mT_power0.1mW"
# df1 = read_epr(file, path=path)

# path = r"C:\Users\Santi\OneDrive - University of Cambridge\EPRdata\2025-11-13_Rui\01_CCsample_beforeDNP"
# file = "20251114_104936669_sm2974_Rui_330-345mT_mod-0.001mT"
# df2 = read_epr(file, path=path)


path = r"C:\Users\Santi\OneDrive - University of Cambridge\Projects\LiMetal\Rui\analysis\epr"
name1 = "CC"
name2 = "PC"

df1 = read_epr(name1, path=path)
df2 = read_epr(name2, path=path)



# path = r"C:\Users\Santi\OneDrive - University of Cambridge\EPRdata\2026-01-08_Rui_pulsed-charged\03_tuesday-13-01_beforeDNP"
# name1 ="20260113_120141723_sm2974_Li-KBr_range-330-345mT_mod0.1mT_power0.1mW"
# name2 = "20260113_120427493_sm2974_Li-KBr_range-330-345mT_mod0.1mT_power0.1mW_01"
# df1 = read_epr(name1, path=path)
# df2 = read_epr(name2, path=path)

reportes = []
names = [name1, name2]
for ii, df in enumerate([df1, df2]):
    fig, ax = plt.subplots()
    B = df["BField [mT]"]    
    spec = df["MW_Absorption []"]
    spec/= -spec.min()
    ax.plot(B, spec, label=names[ii])
    report = report_spectrum(df)
    reportes.append(report)

    ax.axhline(0, color='k', ls='--')
    ax.set_xlabel("B (mT)")
    ax.set_ylabel("I (a.u.)")
    ax.set_xlim([335.5, 336.5])
    ax.legend()

for key in reportes[0].keys():
    print(f"{key}: {reportes[0][key]}\t{reportes[1][key]}") 


# df_comp = compare_params([df1,df2])
