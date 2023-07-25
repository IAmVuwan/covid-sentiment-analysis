from labMTsimple.storyLab import *


class CsaLabMT:
    def __init__(self) -> None:
        self.lang = "english"
        self.lab_mt, self.lab_mt_vector, self.lab_mt_list = emotionFileReader(
            stopval=0.0, lang=self.lang, returnVector=True
        )

    def score(self, tweet_text):
        valence, f_vec = emotion(
            tweet_text, self.lab_mt, shift=True, happsList=self.lab_mt_vector
        )
        stopped_vec = stopper(f_vec, self.lab_mt_vector, self.lab_mt_list, stopVal=1.0)
        happiness_score = emotionV(stopped_vec, self.lab_mt_vector)
        return round(happiness_score, 5)
