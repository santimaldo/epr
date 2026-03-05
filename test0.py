
from Read import read_epr
import matplotlib.pyplot as plt
import os
path = r"C:\Users\Santi\OneDrive - University of Cambridge\EPRdata\2026-01-08_Rui_pulsed-charged\01_next-day_beforeDNP/"
# df = read_epr("20260108_190256036_sm2974_Li-KBr_range-330-345mT_mod0.1mT_power0.1mW_01_pow_0_0519mW", path=path)
# fig, ax = plt.subplots()
# B = df["BField [mT]"]
# spec = df["MW_Absorption []"]
# ax.plot(B, spec)
# ax.set_xlabel("B (mT)")
# ax.set_ylabel("I (a.u.)")


#%%%

# def plot_all_spectra(folder_path="./"):
#     """
#     Reads all .csv EPR spectra in a folder, plots them together with labels,
#     and returns a list of spectrum names in plotting order.
    
#     Labels format: "0: <name>", "1: <name>", ...
#     """
# List all CSV files in folder

folder_path = path

all_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".csv")])

spectrum_names = []

plt.figure(figsize=(8,6))

for i, file in enumerate(all_files):
    # Remove extension for read_epr
    name_without_ext = os.path.splitext(file)[0]
    
    # Read spectrum
    df = read_epr(name_without_ext, path=folder_path)
    B = df[df.columns[0]]  # Assuming first column is BField
    spec = df[df.columns[1]]  # Assuming second column is MW Absorption
    # Plot
    plt.plot(B, spec, label=f"{i}: {name_without_ext}")
    
    # Save name in order
    spectrum_names.append(name_without_ext)

plt.xlabel("BField [mT]")
plt.ylabel("MW Absorption []")
plt.title("EPR Spectra")
plt.legend()
plt.tight_layout()
plt.show()
    
# return spectrum_names
# %%
