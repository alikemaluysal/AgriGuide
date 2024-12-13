import pandas as pd

def lookup_table(temp, rainfall, soil_type):
    df = pd.read_excel('data/lookup.xlsx')

    df = df[(df['soil-type'] == soil_type) | (df['soil-type-2'] == soil_type)]
    df = df[(df['temp-opt-min'] <= temp) & (df['temp-opt-max'] >= temp)]
    df = df[(df['rainfall-opt-min'] <= rainfall) & (df['rainfall-opt-max'] >= rainfall)]

    df['temp-score'] = abs(df['temp-opt-min'] + df['temp-opt-max'] / 2 - temp)
    df['rainfall-score'] = abs(df['rainfall-opt-min'] + df['rainfall-opt-max'] / 2 - rainfall)

    df['total-score'] = df['temp-score'] + df['rainfall-score']

    df = df.sort_values('total-score', ascending=True)

    return df['crop'].head(3).tolist()
