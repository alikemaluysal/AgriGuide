import pandas as pd

co2_emissions = {
    "bugday": 0.20,
    "arpa": 0.18,
    "misir": 0.15,
    "pirinc": 0.30,
    "tutun": 0.25,
    "pamuk": 0.27,
    "cay": 0.22,
    "aycicegi": 0.17,
    "soya": 0.24,
    "yer_fistigi": 0.21,
    "nohut": 0.12,
    "bezelye": 0.14,
    "portakal": 0.10,
    "limon": 0.11,
    "greyfurt": 0.13
}

def sort_by_co2(recommended_crops):
    df = pd.DataFrame(recommended_crops, columns=['crop'])
    df['CO2_Emissions'] = df['crop'].map(co2_emissions)
    df = df.sort_values('CO2_Emissions', ascending=True)
    
    return df
