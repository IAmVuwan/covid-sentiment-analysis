from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    AutoConfig,
    TextClassificationPipeline,
)


class CsaHuggingFace:
    def __init__(
        self,
        num_labels: int = 2,
    ) -> None:
        name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
        self.tokenizer = AutoTokenizer.from_pretrained(name)
        self.config = AutoConfig.from_pretrained(name, num_labels=num_labels)
        self.model = AutoModelForSequenceClassification.from_pretrained(name)
        self._pipeline = TextClassificationPipeline(
            model=self.model, tokenizer=self.tokenizer
        )

    @staticmethod
    def label_to_score(label, score):
        if label == "positive":
            return 1 * score
        elif label == "negative":
            return -1 * score
        else:
            return 0

    def score(self, tweet_text):
        results = self._pipeline.__call__(tweet_text)
        first_result = results[0]
        total_sentiment = first_result["label"]
        total_sentiment_score = first_result["score"]
        huggingface_score = CsaHuggingFace.label_to_score(
            total_sentiment.lower(), total_sentiment_score
        )
        return round(huggingface_score, 5)
