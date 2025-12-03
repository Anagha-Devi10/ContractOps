
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MemoryBank:
    def __init__(self):
        self.df = pd.DataFrame(columns=["contract_id", "title", "summary"])
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf = None

    def add_contract(self, c):
        self.df.loc[len(self.df)] = [c.contract_id, c.title, c.summary]
        self.reindex()

    def reindex(self):
        corpus = (self.df["title"] + " " + self.df["summary"]).tolist()
        if corpus:
            self.tfidf = self.vectorizer.fit_transform(corpus)

    def query(self, q, top_k=1):
        qv = self.vectorizer.transform([q])
        sims = cosine_similarity(qv, self.tfidf).flatten()
        idx = sims.argsort()[::-1][:top_k]
        res = []
        for i in idx:
            res.append({"contract_id": self.df.iloc[i]["contract_id"], "score": float(sims[i])})
        return res
