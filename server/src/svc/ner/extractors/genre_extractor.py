import re
import os
import logging
from typing import List
from src.svc.ner.extractors.base_extractor import BaseExtractor
from src.svc.ner.extractors.config import ASSETS_PATH

with open(os.path.join(ASSETS_PATH, "genres.list"), "r") as f:
    GENRES = f.read().split("\n")


class GenreExtractor(BaseExtractor):
    def get_genre(self, **kwargs: dict) -> List[str]:
        genres_tmp = []
        for genre in GENRES:
            if genre in kwargs['text']:
                genres_tmp.append(genre)
                
        return genres_tmp

    def get_genres_from_df(self, text: str, genre: str) -> List[str]:
        genres = genre.split(",")
        pat = fr"\b(?:{'|'.join(genres)})\b"
        genres = re.findall(pat, text, re.IGNORECASE)

        print("GENRES", genres)
        return genres

    def run(self, **kwargs: dict) -> dict:
        kwargs['genres'] = self.get_genre(**kwargs)
        return kwargs
