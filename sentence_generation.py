import pandas as pd
from typing import List

class SentenceGenerator():

    @staticmethod
    def generate_sentences(df: pd.DataFrame) -> List[str]:
        sentences = []
        for _, row in df.iterrows():
            sentences.append(row['source'] + " " + row['edge'] + " " + row['target'] + ".")
        return sentences

    @staticmethod
    def generate_text(df: pd.DataFrame) -> str:
        text = ""
        for _, row in df.iterrows():
            text = text + (row['source'] + " " + row['edge'] + " " + row['target'] + ". ")
        return text
        
