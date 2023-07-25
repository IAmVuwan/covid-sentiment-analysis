from flair.data import Sentence
from flair.models import TextClassifier


class CsaFlair:
    def __init__(self) -> None:
        self.classifier = TextClassifier.load("en-sentiment")

    @staticmethod
    def label_to_score(label, score):
        if label == "positive":
            return 1 * score
        elif label == "negative":
            return -1 * score
        else:
            return 0

    def score(self, tweet_text):
        sentence = Sentence(tweet_text)
        self.classifier.predict(sentence)
        total_sentiment = sentence.labels[0].value
        total_sentiment_score = sentence.labels[0].score
        flair_score = CsaFlair.label_to_score(
            total_sentiment.lower(), total_sentiment_score
        )
        return round(flair_score, 5)
