from Read import read_epr
import matplotlib.pyplot as plt
import os

def get_spec_names(folder_path="./", normalize=False, Brange=None):
    """
    Reads all .csv EPR spectra in a folder, plots them together with labels,
    and returns a list of spectrum names in plotting order.
    
    Labels format: "0: <name>", "1: <name>", ...
    """

    folder_path = path

    all_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".csv")])

    spec_names = []
    data = []

    fig, ax = plt.subplots(figsize=(8,6))

    for ii, file in enumerate(all_files):
        # Remove extension for read_epr
        name_without_ext = os.path.splitext(file)[0]
        
        # Read spectrum
        df = read_epr(name_without_ext, path=folder_path)
        B = df[df.columns[0]]  # Assuming first column is BField
        spec = df[df.columns[1]]  # Assuming second column is MW Absorption
        # Plot
        data.append((B, spec))
        # Save name in order
        spec_names.append(name_without_ext)
        if normalize:
            spec = spec / spec.max()  # Normalize to max value
        ax.plot(B, spec, label=f"{ii}")
    ax.set_xlabel("BField [mT]")
    ax.set_ylabel("MW Absorption []")
    ax.set_title("EPR Spectra")
    ax.legend()
    if Brange is not None:
        ax.set_xlim([min(Brange), max(Brange)])
    fig.tight_layout()
    plt.show()
    
    return spec_names


if __name__ == "__main__":

    # PC
    path = r"C:\Users\Santi\OneDrive - University of Cambridge\EPRdata\2026-01-08_Rui_pulsed-charged\01_next-day_beforeDNP"
    normalize = True
    Brange = [335, 337]

    # CC
    path = r"C:\Users\Santi\OneDrive - University of Cambridge\EPRdata\2025-11-13_Rui\01_CCsample_beforeDNP"
    normalize = False # True
    Brange = [335, 337]


    names = get_spec_names(folder_path=path, normalize=normalize, Brange=Brange)
    print(path)
    print("Spectrum names in plotting order:")    
    for i, name in enumerate(names):
        print(f"{i}: {name}")


    df = read_epr(names[0], path=path)