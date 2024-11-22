_PREDICTED_ENTITY_TO_STRING = {
    'B-REVIEW': 'review',
    'B-AWARD': 'award',
    'B-DIRECTOR': 'director',
    'B-RATING': 'rating',
    'B-RATINGS_AVERAGE': 'ratings_average',
    'B-GENRE': 'genre',
    'B-CHARACTER': 'character',
    'B-QUOTE': 'quote',
    'B-ORIGIN': 'origin',
    'B-SONG': 'song',
    'B-ACTOR': 'actor',
    'B-TITLE': 'title',
    'B-PLOT': 'plot',
    'B-RELATIONSHIP': 'relationship',
    'B-YEAR': 'year',
    'B-TRAILER': 'trailer',
    'I-REVIEW': 'review',
    'I-AWARD': 'award',
    'I-DIRECTOR': 'director',
    'I-RATING': 'rating',
    'I-RATINGS_AVERAGE': 'ratings_average',
}

def get_entity_name(entity: str) -> str | None:
    return _PREDICTED_ENTITY_TO_STRING.get(entity)