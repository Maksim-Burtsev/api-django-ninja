from typing import List

from django.shortcuts import get_object_or_404

from ninja import NinjaAPI

from eng.models import Word, Sentence
from eng.service import SentenceParser
from eng.schemas import WordSchema, WordDetailSchema


api = NinjaAPI(urls_namespace='eng_api')


@api.post('/add_word/', response={201: WordSchema})
def add_word(request, word: WordSchema):
    word = Word.objects.create(**word.dict())

    parser = SentenceParser(word.word)
    sentences = parser.get_sentences()

    objects = [Sentence(text=sentence, word=word) for sentence in sentences]
    Sentence.objects.bulk_create(objects)

    return 201, word


@api.get('/words/', response=List[WordSchema])
def get_words(request):
    words = Word.objects.all()
    return words


@api.get('/word/{word}/', response=WordDetailSchema)
def get_word_detail(request, word: str):
    word = get_object_or_404(Word, word=word)
    return word