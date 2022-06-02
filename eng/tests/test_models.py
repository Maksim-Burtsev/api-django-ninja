from telnetlib import SE
from django.test import TestCase

from eng.models import Sentence, Word


class EngModelsTestCase(TestCase):

    def test_word_model(self):

        word = Word.objects.create(word='Weather', transcription='Погода')

        self.assertTrue(Word.objects.all().count(), 1)

        word.refresh_from_db()
        self.assertEqual(word.word, 'weather')
        self.assertEqual(word.transcription, 'погода')

    def test_sentence(self):
        word = Word.objects.create(word='Weather', transcription='Погода')

        sentence = Sentence.objects.create(
            text='The weather is good.', word=word)

        self.assertEqual(Sentence.objects.all().count(), 1)

        sentence.refresh_from_db()
        self.assertEqual(sentence.word_id, 1)
        self.assertEqual(sentence.text, 'The weather is good.')
