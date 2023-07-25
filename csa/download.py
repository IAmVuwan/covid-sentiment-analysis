import glob
import json
import os
import zipfile
from pathlib import Path

import gdown
import pandas as pd
from twarc import Twarc2, expansions

from csa.utils import CsaUtils


class CsaDownloads:
    def __init__(self):
        self.utils = CsaUtils()

    def download_maps(self):
        zip_filepath = f"{self.utils.tmp_dir}/maps.zip"
        if not os.path.exists(zip_filepath):
            print(f"Downloading the data into [{zip_filepath}]")
            gdown.download(
                url="https://drive.google.com/uc?id=1Ppbw6LGurxHpdKmaP4Wz__ch-rd4x1GT",
                output=zip_filepath,
            )

            zips_dir = f"{self.utils.raw_dir}/maps"
            Path(zips_dir).mkdir(parents=True, exist_ok=True)

            print(f"Extracting the data zip file into [{zips_dir}]")
            with zipfile.ZipFile(zip_filepath, "r") as zf:
                zf.extractall(f"{zips_dir}")

        print("Data was downloaded.")

    def download_data(self):
        zip_filepath = f"{self.utils.tmp_dir}/data.zip"
        if not os.path.exists(zip_filepath):
            print(f"Downloading the data into [{zip_filepath}]")
            gdown.download(
                url="https://drive.google.com/uc?id=1xWEBpETBiECvAyBEnz2kQ1wO1WeY7mYs",
                output=zip_filepath,
            )

            zips_dir = f"{self.utils.tmp_dir}/zips"
            Path(zips_dir).mkdir(parents=True, exist_ok=True)

            print(f"Extracting the data zip file into [{zips_dir}]")
            with zipfile.ZipFile(zip_filepath, "r") as zf:
                zf.extractall(f"{zips_dir}")

            extract_dir = f"{self.utils.tmp_dir}/extract"
            Path(extract_dir).mkdir(parents=True, exist_ok=True)
            print(f"Extracting the raw zip files into [{extract_dir}]")
            zip_files = glob.glob(f"{zips_dir}/*.zip")
            for zip_file in zip_files:
                with zipfile.ZipFile(zip_file, "r") as zf:
                    zf.extractall(f"{extract_dir}")

            print(f"Aggregate twitter ids into file [{self.utils.raw_ids_csv}]")
            df_cols = ["tweet_id"]
            df1 = CsaUtils.read_df_from_csvs(df_cols, f"{extract_dir}/*/*.csv")
            df2 = CsaUtils.read_df_from_csvs(df_cols, f"{extract_dir}/*.csv")
            df = pd.concat([df1, df2])
            df = df.drop_duplicates(subset=["tweet_id"], keep=False)
            print(df.shape)
            df.to_csv(self.utils.raw_ids_csv, encoding="utf-8", index=False)
        print("Data was downloaded.")

    def download_tweets(self):
        consumer_key = ""
        consumer_key_secret = ""
        access_token = ""
        access_token_secret = ""
        bearer_token = ""
        twrc = Twarc2(
            consumer_key=consumer_key,
            consumer_secret=consumer_key_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            bearer_token=bearer_token,
            connection_errors=0,
            metadata=True,
        )

        tweets_dir = f"{self.utils.tmp_dir}/tweets"
        Path(tweets_dir).mkdir(parents=True, exist_ok=True)
        print(
            "-------------------------------------------------------------------------------\n"
        )
        tweet_ids = list(
            pd.read_csv(self.utils.raw_ids_csv, skiprows=1, header=None)[0]
        )
        tweets_count = len(tweet_ids)
        lookup = twrc.tweet_lookup(tweet_ids)
        print("No of Tweets: " + str(tweets_count))
        for page in lookup:
            result = expansions.flatten(page)
            for tweet in result:
                tweet_id = str(tweet["conversation_id"])
                tweet_json_filepath = f"{tweets_dir}/{tweet_id}.json"
                with open(tweet_json_filepath, "w", encoding="utf-8") as outfile:
                    json.dump(tweet, outfile, ensure_ascii=False, indent=2)
        print("Processed no of tweets: " + str((len(tweet_ids) - tweets_count)))
        print(
            "-------------------------------------------------------------------------------\n"
        )

    def extract_tweets(self):
        tweets_dir = f"{self.utils.tmp_dir}/tweets"
        records = []

        def get_text_from_tweet(tweet_json):
            if "extended_tweet" in tweet_json:
                status_json = tweet_json["extended_tweet"]["text"]
            elif (
                "retweeted_status" in tweet_json
                and "extended_tweet" in tweet_json["retweeted_status"]
            ):
                status_json = tweet_json["retweeted_status"]["extended_tweet"]["text"]
            elif "retweeted_status" in tweet_json:
                status_json = tweet_json["retweeted_status"]["text"]
            else:
                status_json = tweet_json["text"]
            return status_json

        def get_country(tweet_json):
            if "geo" in tweet_json:
                if "country" in tweet_json["geo"]:
                    return tweet_json["geo"]["country"]
            return None

        def get_coordinates(tweet_json):
            if "geo" in tweet_json:
                if "coordinates" in tweet_json["geo"]:
                    if "coordinates" in tweet_json["geo"]["coordinates"]:
                        _long = tweet_json["geo"]["coordinates"]["coordinates"][0]
                        _lat = tweet_json["geo"]["coordinates"]["coordinates"][1]
                        return _long, _lat
            return None, None

        for tweet_json_filepath in glob.glob(f"{tweets_dir}/*.json"):
            with open(tweet_json_filepath, encoding="utf-8") as fh:
                tweet = json.load(fh)
                tweet_id = tweet["conversation_id"]
                try:
                    long, lat = get_coordinates(tweet)
                    text = get_text_from_tweet(tweet)
                    country = get_country(tweet)
                    records.append(
                        {
                            "tweet_id": tweet_id,
                            "country": country,
                            "long": long,
                            "lat": lat,
                            "created_at": tweet["created_at"],
                            "raw_text": text,
                        }
                    )
                except Exception as e:
                    print(f"Missing information for tweet id: {tweet_id}")
                    raise e

        df = pd.DataFrame(records)

        print(
            "-------------------------------------------------------------------------------\n"
        )
        print("Raw Tweets shape: ", df.shape)
        df = df[df["country"] == "United States"]
        print("Raw Tweets shape for [United States]: ", df.shape)
        df.to_pickle(self.utils.raw_us_tweets_pkl)
        print(
            "-------------------------------------------------------------------------------\n"
        )

    def extract_datasets(self):
        with zipfile.ZipFile(
            os.path.join(Path(__file__).parent, "../datasets/nytimes-us-states.zip"),
            "r",
        ) as zf:
            zf.extractall(f"{self.utils.raw_dir}")
        with zipfile.ZipFile(
            os.path.join(Path(__file__).parent, "../datasets/maps.zip"),
            "r",
        ) as zf:
            zf.extractall(f"{self.utils.raw_dir}")
        with zipfile.ZipFile(
            os.path.join(Path(__file__).parent, "../datasets/keywords.zip"),
            "r",
        ) as zf:
            zf.extractall(f"{self.utils.raw_dir}")

    def extract_embedded_datasets(self):
        with zipfile.ZipFile(
                os.path.join(Path(__file__).parent, "../datasets/raw-us-tweets.zip"), "r"
        ) as zf:
            zf.extractall(f"{self.utils.raw_dir}")
        with zipfile.ZipFile(
                os.path.join(Path(__file__).parent, "../datasets/preprocess-us-tweets.zip"), "r"
        ) as zf:
            zf.extractall(f"{self.utils.preprocess_dir}")
