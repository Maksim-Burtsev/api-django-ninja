from typing import List

from django.shortcuts import get_object_or_404

from ninja import NinjaAPI

from eng.models import Word
from eng.services import parse_and_add_sentences
from eng.schemas import WordSchema, WordDetailSchema, Message


api = NinjaAPI(urls_namespace='eng_api')


@api.post('/add_word/', response={201: WordSchema, 200: Message})
def add_word(request, word: WordSchema):
    word_obj, created = Word.objects.get_or_create(word=word.word)
    if created:
        word_obj.transcription = word.transcription
        word_obj.save()
        parse_and_add_sentences(word=word_obj)
        return 201, word
    return 200, {'message': 'This word already exists.'}


@api.get('/words/', response=List[WordSchema])
def get_words(request):
    words = Word.objects.all()
    return words


@api.get('/words/{word}/', response=WordDetailSchema)
def get_word_detail(request, word: str):
    word = get_object_or_404(Word, word=word)
    return word


@api.delete('/words/{word}/')
def delete_word(request, word: str):
    word = get_object_or_404(Word, word=word)
    word.delete()

    return None
