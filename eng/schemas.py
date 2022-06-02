from typing import List

from ninja import Schema, ModelSchema

from eng.models import Word


class WordSchema(ModelSchema):
    class Config:
        model = Word
        model_fields = ['word', 'transcription']


class SentenceSchema(Schema):
    text: str


class WordDetailSchema(Schema):
    word: str
    transcription: str
    sentences: List[SentenceSchema] = None
