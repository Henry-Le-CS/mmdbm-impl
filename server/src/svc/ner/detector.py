import spacy
import time
import pandas as pd
import logging

from .lm.albert import AlbertNER
from .extractors import *
from src.svc.ner.checker import Checker
from src.svc.ner.filter import Filter
from src.svc.ner.mapper import get_entity_name

from typing import List, Tuple
import string
import os

ACTOR = "actor"
DIRECTOR = "director"
CHARACETR = "character"
ASSETS_PATH = "./assets"

class Detector:
    def __init__(self):
        self.model = spacy.load("en_core_web_lg")
        self.ner = AlbertNER()

        # Check data with movie database
        df_movies = pd.read_csv(os.path.join(ASSETS_PATH, "movies.csv"), dtype={3: str})
        df_movies = df_movies.loc[df_movies.actors.notna()]
        self.df_movies = df_movies


        self.genre_extractor = GenreExtractor(df_movies)
        self.person_extractor = PersonExtractor(df_movies)
        self.rate_extractor = RateExtractor(df_movies)
        self.title_extractor = TitleExtractor(df_movies)
        self.year_extractor = YearExtractor(df_movies)
        self.extractors = [
            self.genre_extractor,
            self.person_extractor,
            self.rate_extractor,
            self.title_extractor,
            self.year_extractor
        ]

        self.filter = Filter()
        self.checker = Checker(self.filter, df_movies)
        logging.info("Detector initialized")

    def get_entities(self, **kwargs: dict) -> dict:
        doc = self.model(kwargs['text'])
        kwargs['entities_spacy'] = [(ent.text, ent.label_) for ent in doc.ents]
        kwargs['entities_albert'] = self.ner.extract(kwargs['text'])

        return kwargs

    def parse_entity(self, entity_text: str, label: str) -> List[str]:
        words = entity_text.split(" ")
        entities = [(words[0], f"B-{label}")]
        entities += [(w, f"I-{label}") for w in words[1:]]

        return entities

    def merge_entities(
        self, 
        entities: List[Tuple[str, str]],
        new_entities: List[Tuple[str, str]],
        ) -> List[Tuple[str, str]]:
        original_words = list(enumerate([ent_[0].strip().strip(string.punctuation) for ent_ in entities]))
        for ent in new_entities:
            words = [x[0] for x in ent]
            idxs = []
            for i, word in original_words:
                if word == words[0].strip().strip(string.punctuation):
                    val = True
                    for j in range(len(words)):
                        if entities[i + j][0] != words[j].strip().strip(string.punctuation):
                            val = False
                            break
                    if val:
                        idxs += list(zip(ent, range(i, i + len(words))))
                        
            for ent_, i in idxs:
                if ent_[1].startswith("I"):
                    if i != 0 and (entities[i - 1][1] == ent_[1].replace("I-", "B-") or entities[i - 1][1] == ent_[1]):
                        entities[i] = ent_
                else:
                    entities[i] = ent_

        return entities

    def parse_entities(self, **kwargs: dict):
        titles_parsed = []
        for title in kwargs['titles']:
            titles_parsed.append(self.parse_entity(title.strip(), "TITLE"))
            
        years_parsed = []
        for year in kwargs['years']:
            years_parsed.append(self.parse_entity(year.strip(), "YEAR"))
            
        ratings_avg_parsed = []
        for rating_average in kwargs['rate_avg']:
            ratings_avg_parsed.append(self.parse_entity(rating_average.strip(), "RATINGS_AVERAGE"))
            
        rate_parsed = []
        for rating in kwargs['rate']:
            rate_parsed.append(self.parse_entity(rating.strip(), "RATING"))
            
        genres_parsed = []
        for genre in kwargs['genres']:
            genres_parsed.append(self.parse_entity(genre.strip(), "GENRE"))
        
        actors_parsed = []
        for actor in kwargs['actors']:
            actors_parsed.append(self.parse_entity(actor.strip(), "ACTOR"))
            
        directors_parsed = []
        for director in kwargs['directors']:
            directors_parsed.append(self.parse_entity(director.strip(), "DIRECTOR"))
            
        characters_parsed = []
        for character in kwargs['characters']:
            characters_parsed.append(self.parse_entity(character.strip(), "CHARACTER"))
            
        new_entities = titles_parsed + years_parsed + ratings_avg_parsed + \
                       rate_parsed + genres_parsed + directors_parsed + actors_parsed + \
                       characters_parsed
        return new_entities

    def explore(self, text: str) -> List[Tuple[str, str]]:
        start_time = time.time()
        kwargs = {'text': text}
        words = text.split(" ")
        entities = [(w.strip().strip(string.punctuation), "O") for w in words]
        kwargs = self.get_entities(**kwargs)
        
        for extractor in self.extractors:
            kwargs = extractor.run(**kwargs)
        
        # filter again with data from movies 
        kwargs, _ = self.checker.run(**kwargs)

        new_entities = self.parse_entities(**kwargs)
        entities = self.merge_entities(entities, new_entities)
        ret = []
        for ent in entities:
            if ent[1] == "O":
                entities.remove(ent)
            
            n = get_entity_name(ent[1])
            if n is None:
                continue
            
            ret.append((ent[0], n))
        
        logging.info(f"Exploration took {time.time() - start_time} seconds")
        return ret