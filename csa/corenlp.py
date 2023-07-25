from stanza.server import CoreNLPClient, StartServer


class CsaCorenlp:
    def __init__(self) -> None:
        self.client = CoreNLPClient(
            start_server=StartServer.DONT_START,
            annotators=[
                "sentiment",
            ],
            timeout=9999999999,
            outputFormat="json",
            memory="3G",
            be_quiet=True,
        )

    @staticmethod
    def label_to_score(label):
        if label == "Positive":
            return 1
        elif label == "Negative":
            return -1
        elif label == "Very Positive":
            return 2
        elif label == "Very Negative":
            return -2
        else:
            return 0

    def score(self, tweet_text):
        scores = []
        ann = self.client.annotate(str(tweet_text))
        for sentence in ann.sentence:
            scores.append(CsaCorenlp.label_to_score(sentence.sentiment))
        if len(scores) == 0:
            return 0
        return round(sum(scores) / len(scores), 5)
