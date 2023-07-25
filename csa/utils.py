import glob
import os.path
from os import path
from pathlib import Path

import pandas as pd


class CsaUtils:
    def __init__(self):
        self.work_dir = os.path.join(path.expanduser("~"), ".csa")
        self.data_dir = os.path.join(self.work_dir, "data")
        self.model_dir = os.path.join(self.work_dir, "models")
        self.tmp_dir = f"{self.data_dir}/tmp"
        self.raw_dir = f"{self.data_dir}/raw"
        self.keywords_dir = f"{self.raw_dir}/keywords"
        self.preprocess_dir = f"{self.data_dir}/preprocess"
        Path(self.raw_dir).mkdir(parents=True, exist_ok=True)
        Path(self.preprocess_dir).mkdir(parents=True, exist_ok=True)
        Path(self.tmp_dir).mkdir(parents=True, exist_ok=True)
        self.raw_ids_csv = f"{self.raw_dir}/ids.csv"
        self.raw_us_tweets_pkl = f"{self.raw_dir}/us-tweets.pkl"
        self.raw_nytimes_us_states_pkl = f"{self.raw_dir}/nytimes-us-states.pkl"
        self.preprocess_tweets_pkl = f"{self.preprocess_dir}/us-tweets.pkl"

    def get_raw_nytimes_us_states(self) -> pd.DataFrame:
        return pd.read_pickle(self.raw_nytimes_us_states_pkl)

    def get_raw_us_based_tweets(self) -> pd.DataFrame:
        return pd.read_pickle(self.raw_us_tweets_pkl)

    @staticmethod
    def read_df_from_csvs(df_cols, glob_dir):
        pd_df = None
        for filename in glob.glob(glob_dir):
            file_df = pd.read_csv(filename, header=None, index_col=False, names=df_cols)
            if pd_df is None:
                pd_df = file_df
            else:
                pd_df = pd.concat([pd_df, file_df])
        return pd_df
