from django.db import models


class Word(models.Model):
    """
    Word with transcription
    """
    word = models.CharField(max_length=255)
    transcription = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.word

    def save(self, *args, **kwargs):
        self.word = self.word.lower()
        self.transcription = self.transcription.lower()
        
        return super().save(*args, **kwargs)


class Sentence(models.Model):
    """
    Word sentences
    """
    text = models.CharField(max_length=255)
    word = models.ForeignKey(Word,
                             on_delete=models.CASCADE, related_name='sentences')

    def __str__(self) -> str:
        return self.text
