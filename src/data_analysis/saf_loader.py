from datasets import load_dataset
import pandas as pd

def transform_dataset_to_dataframe_with_split_name(split_dataset, split_name):
    df = split_dataset.to_pandas()
    df['split'] = split_name
    return df

def load_saf_huggingface_splits():
    return load_dataset("Short-Answer-Feedback/saf_communication_networks_english")


def load_saf():
    saf_datasets = load_saf_huggingface_splits()
    splits = [
        transform_dataset_to_dataframe_with_split_name(saf_datasets[key], key) 
        for key in saf_datasets
    ]
    return pd.concat(splits)


def rename_saf(saf: pd.DataFrame) -> pd.DataFrame:
    return saf.rename(columns={
        "score": "grade",
    })