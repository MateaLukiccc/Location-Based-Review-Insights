from fastopic import FASTopic
from topmost.preprocess import Preprocess
from functools import lru_cache
from transformers import pipeline


@lru_cache
def get_fastopic_model(num_topics: int):
    preprocess = Preprocess()
    return FASTopic(num_topics, preprocess)

@lru_cache
def get_distilbert_sentiment():
    return pipeline("sentiment-analysis")