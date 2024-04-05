import pandas as pd
from saf_loader import load_saf, rename_saf
from mohler_loader import load_mohler, rename_mohler
from cunlp_loader import load_cunlp, rename_cunlp
from beetle_loader import load_beetle, rename_beetle

def combine_datasets(datasets: list[pd.DataFrame]):
    return pd.concat(datasets)

def normalize_grade(df: pd.DataFrame) -> pd.DataFrame:
    """
    Expects the data frame to contain a grade column
    """
    df['normalized_grade'] = (df['grade'] - df['grade'].min()) / (df['grade'].max() - df['grade'].min())
    return df

def load_datasets():
    beetle = load_beetle()
    beetle = rename_beetle(beetle)
    beetle['data_source'] = 'Beetle'

    saf = load_saf()
    saf = rename_saf(saf)
    saf['data_source'] = 'SAF'


    cunlp = load_cunlp()
    cunlp = rename_cunlp(cunlp)
    cunlp['data_source'] = 'CU-NLP'


    mohler = load_mohler()
    mohler = rename_mohler(mohler)
    mohler['data_source'] = 'Mohler'
    
    return [beetle, saf, mohler, cunlp]