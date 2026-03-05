from Read import read_epr
import matplotlib.pyplot as plt

path = r"C:\Users\Santi\OneDrive - University of Cambridge\EPRdata\2026-01-08_Rui_pulsed-charged\00_as_packed\sm2974_Li-KBr_range-330-345mT_mod0.1mT_power0.1mW_01\sm2974_Li-KBr_range-330-345mT_mod0.1mT_power0.1mW_02/"
df = read_epr("20260108_191910053_sm2974_Li-KBr_range-330-345mT_mod0.1mT_power0.1mW_02_pow_1_0000mW.csv", path=path)



fig, ax = plt.subplots()
B = df["BField [mT]"]
spec = df["MW_Absorption []"]
ax.plot(B, spec)
ax.set_xlabel("B (mT)")
ax.set_ylabel("I (a.u.)")
