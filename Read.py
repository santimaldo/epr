import pandas as pd
import os

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
    
    # Read the file lines, skipping empty lines
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # Initialize dictionaries and dataframe
    params = {}
    param_blocks = {}
    df_meas = None
    block = None
    
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
            # The first line in Meas is the header
            if df_meas is None:
                df_meas = pd.DataFrame(columns=line.split(";"))
            else:
                values = [parse_value(v) for v in line.split(";")]
                df_meas.loc[len(df_meas)] = values

    # Add attributes to the dataframe
    df_meas.attrs["name"] = filename
    df_meas.attrs["params"] = params
    df_meas.attrs["param_blocks"] = param_blocks
    
    return df_meas