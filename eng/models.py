from django.db import models


class Word(models.Model):
    """
    Слово и его перевод
    """

    word = models.CharField(max_length=255)
    transcription = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.word

#TODO Sentence model with ForeignKey on Word + sentence auto add
