import pandas as pd
import os
import numpy as np
import scipy.constants as const

def read_epr(filename, path="./"):
    """
    Reads an EPR spectrum from Magnettech-MS5000 file and returns 
    df_meas with attrs:
    - df.attrs["name"]: name of the spectrum
    - df.attrs["params"]: dictionary containing all parameters
    - df.attrs["param_blocks"]: dictionary indicating the block of each parameter
    """
    
    # Helper function to convert a value to int or float if possible
    def parse_value(val):
        try:
            return int(val)
        except:
            try:
                return float(val)
            except:
                return val

    # Build the full file path
    filepath = os.path.join(path, filename + ".csv")
    
    # Read all lines
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # Initialize dictionaries and storage
    params = {}
    param_blocks = {}
    df_meas = None
    block = None
    meas_rows = []  # store Meas rows temporarily
    meas_header = None
    
    for line in lines:
        # Detect block changes
        if line in ["Recipe", "Additional", "Meas"]:
            block = line
            continue
        
        # Read parameter blocks
        if block in ["Recipe", "Additional"]:
            parts = line.split(";")
            if len(parts) >= 2:
                key = parts[0]
                value = parse_value(parts[1])
                params[key] = value
                param_blocks[key] = block
                
        # Read experimental data
        elif block == "Meas":
            if meas_header is None:
                meas_header = line.split(";")
            else:
                values = [float(v) for v in line.split(";")]
                meas_rows.append(values)
    
    # Create DataFrame from accumulated Meas rows
    df_meas = pd.DataFrame(meas_rows, columns=meas_header)
    
    # Add attributes to the dataframe
    df_meas.attrs["name"] = filename
    df_meas.attrs["params"] = params
    df_meas.attrs["param_blocks"] = param_blocks
    
    return df_meas



###############################################################################
###############################################################################
###############################################################################

def calculate_T2(DeltaBpp_mT, model="Lorentzian"):
    if model.lower() != "lorentzian":
        raise ValueError("Currently only 'Lorentzian' model is supported.")
    elif model.lower() == "lorentzian":
        """
        Calculate T2 (s) from DeltaBpp (mT) assuming Lorentzian line (first derivative).
        """
        gamma_e = const.physical_constants["electron gyromag. ratio"][0]  # rad s^-1 T^-1
        DeltaBpp_T = np.array(DeltaBpp_mT) * 1e-3  # mT to T
        T2 = 2 / (np.sqrt(3) * gamma_e * DeltaBpp_T)  # seconds
    return T2

def report_spectrum(df):
    """
    Generate a report dictionary for a single EPR spectrum.
    """
    # Extract experimental parameters
    params = df.attrs["params"]
    report = {
        "name": df.attrs["name"],
        "MicrowavePower_mW": params.get("MicrowavePower"),
        "AmplitudeModulation_mT": params.get("Modulation"),
        "ModulationFreq_Hz": params.get("ModulationFreq"),
        "SweepTime_s": params.get("SweepTime"),
        "B_range_mT": (params.get("Bfrom"), params.get("Bto"))        
    }
    
    # Extract spectrum
    y = df["MW_Absorption []"].values
    x = df["BField [mT]"].values

    # B_FreqNorm likelyness:
    if abs(x[0] - params.get("Bfrom")) > 1e-12:
        report["B_FreqNorm_used"] = "Likely"
    else:
        report["B_FreqNorm_used"] = "Unlikely"
    
    # A/B
    y_max = y.max()
    y_min = y.min()
    report["AtoB"] = abs(y_max / y_min)
    
    # DeltaBpp
    idx_max = np.argmax(y)
    idx_min = np.argmin(y)
    B_max = x[idx_max]
    B_min = x[idx_min]
    DeltaBpp = abs(B_max - B_min)
    report["DeltaBpp_mT"] = DeltaBpp
    
    # T2
    report["T2_ns"] = calculate_T2([DeltaBpp])[0] / 1e-9  # Convert to ns
    
    return report

def compare_params(dfs):
    """
    Build a dataframe containing the params of several EPR dataframes.

    Columns correspond to individual spectra.
    Rows correspond to parameter names.
    """

    params_dict = {}

    for i, df in enumerate(dfs):
        name = df.attrs["name"]
        params_dict[name] = df.attrs["params"]

    df_params = pd.DataFrame(params_dict)
    print("Parameter comparison:")
    # The scope of these changes made to
    # pandas settings are local to with statement.
    with pd.option_context('display.max_rows', None,
                        'display.max_columns', None,
                        ):
        print(df_params)

    return df_params