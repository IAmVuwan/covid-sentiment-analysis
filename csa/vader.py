import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")


class CsaVader:
    def __init__(self) -> None:
        self.analyzer = SentimentIntensityAnalyzer()

    def score(self, tweet_text):
        compound = self.analyzer.polarity_scores(tweet_text)["compound"]
        return round(compound, 5)
