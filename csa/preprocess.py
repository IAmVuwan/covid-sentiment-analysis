import os
import re
import string
import time
from datetime import datetime
import pandas as pd
from emoji import replace_emoji
from timezonefinder import TimezoneFinder
from csa.corenlp import CsaCorenlp
from csa.flair import CsaFlair
from csa.huggingface import CsaHuggingFace
from csa.labMT import CsaLabMT
from csa.utils import CsaUtils
from csa.vader import CsaVader

from tqdm import tqdm

tqdm.pandas()

from pandarallel import pandarallel

pandarallel.initialize(progress_bar=True)


class CsaPreProcess:
    def __init__(self):
        self.utils = CsaUtils()
        covid19_keywords = os.path.join(self.utils.keywords_dir, "covid19.csv")
        anxiety_keywords = os.path.join(self.utils.keywords_dir, "anxiety.csv")
        self.anxiety_keywords = set(pd.read_csv(covid19_keywords).iloc[:, 0])
        self.covid_keywords = set(pd.read_csv(anxiety_keywords).iloc[:, 0])
        self.word_analyzer = re.compile(r"\w+")
        self.huggingface = CsaHuggingFace()
        self.vader = CsaVader()
        self.lab_mt = CsaLabMT()
        self.corenlp = CsaCorenlp()
        self.flair = CsaFlair()
        self.text_col = "clean_text"

    @staticmethod
    def to_local_date(dtime):
        utc_date_time = datetime.strptime(dtime, "%Y-%m-%dT%H:%M:%S.000Z")
        return utc_date_time.strftime("%Y-%m-%d")

    def clean_tweet(self, tweet):
        # Clean emojis from text
        def strip_emoji(text):
            return replace_emoji(text, "")  # remove emoji

        # Remove punctuations, links, mentions and \r\n new line characters
        def strip_all_entities(text):
            text = (
                text.replace("\r", "").replace("\n", " ").replace("\n", " ").lower()
            )  # remove \n and \r and lowercase
            text = re.sub(
                r"(?:\@|https?\://)\S+", "", text
            )  # remove links and mentions
            text = re.sub(
                r"[^\x00-\x7f]", r"", text
            )  # remove non utf8/ascii characters such as '\x9a\x91\x97\x9a\x97'
            banned_list = string.punctuation + "Ã" + "±" + "ã" + "¼" + "â" + "»" + "§"
            table = str.maketrans("", "", banned_list)
            text = text.translate(table)
            return text

        # clean hashtags at the end of the sentence, and keep those in the middle of
        # the sentence by removing just the # symbol
        def clean_hashtags(tweet):
            new_tweet = " ".join(
                word.strip()
                for word in re.split(
                    "#(?!(?:hashtag)\b)[\w-]+(?=(?:\s+#[\w-]+)*\s*$)", tweet
                )
            )  # remove last hashtags
            new_tweet2 = " ".join(
                word.strip() for word in re.split("#|_", new_tweet)
            )  # remove hashtags symbol from words in the middle of the sentence
            return new_tweet2

        # Filter special characters such as & and $ present in some words
        def filter_chars(a):
            sent = []
            for word in a.split(" "):
                if ("$" in word) | ("&" in word):
                    sent.append("")
                else:
                    sent.append(word)
            return " ".join(sent)

        def remove_mult_spaces(text):  # remove multiple spaces
            return re.sub("\s\s+", " ", text)

        return remove_mult_spaces(
            filter_chars(clean_hashtags(strip_all_entities(strip_emoji(tweet))))
        )

    def preprocess_tweets(self):
        df = self.utils.get_raw_us_based_tweets()
        begin = time.time()

        print("Cleaning Tweets....")
        df[self.text_col] = df["raw_text"].progress_apply(lambda x: self.clean_tweet(x))
        print("Extracting localDate....")
        df["localDate"] = df.progress_apply(
            lambda x: CsaPreProcess.to_local_date(x["created_at"]), axis=1
        )
        # ----------------------------- scores ---------------------------------------------
        self.compute_scores(df)
        # ----------------------------------------------------------------------------------
        df.rename(columns={"tweet_id": "tid"}, inplace=True)
        df.drop("raw_text", axis=1, inplace=True)
        df.drop("created_at", axis=1, inplace=True)
        df.drop("country", axis=1, inplace=True)
        df.to_pickle(f"{self.utils.preprocess_tweets_pkl}")
        print("Columns of the dataset", list(df.columns))
        print("Total records of the dataset", len(df))
        print(f"Total time taken to preprocessed: {time.time() - begin}")

    def compute_scores(self, df):
        self.parallel(df=df, func=self.corenlp.score, col="cnlpScore")
        self.serial(df=df, func=self.huggingface.score, col="huggingfaceScore")
        self.serial(df=df, func=self.flair.score, col="flairScore")
        self.serial(df=df, func=self.vader.score, col="vaderScore")
        self.serial(df=df, func=self.lab_mt.score, col="happinessScore")
        self.serial(
            df=df, func=self.anxiety_keyword_density, col="anxietyKeywordDensity"
        )
        self.serial(df=df, func=self.covid_keyword_density, col="covid19KeywordDensity")

    def anxiety_keyword_density(self, tweet_text):
        word_count = len(self.word_analyzer.findall(tweet_text))
        keyword_count = len(self.anxiety_keywords.intersection(tweet_text.split()))
        return round(keyword_count / word_count, 5)

    def covid_keyword_density(self, tweet_text):
        word_count = len(self.word_analyzer.findall(tweet_text))
        keyword_count = len(self.covid_keywords.intersection(tweet_text.split()))
        return round(keyword_count / word_count, 5)

    def parallel(self, df, func, col):
        """Function that executes the function using parallel_apply."""
        print(f"Computing {col}....")
        df[col] = df[self.text_col].parallel_apply(lambda x: func(x))

    def serial(self, df, func, col):
        """Function that executes the function using progress_apply."""
        print(f"Computing {col}....")
        df[col] = df[self.text_col].progress_apply(lambda x: func(x))
