from django.contrib import admin

from eng.models import Word, Sentence


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    pass


@admin.register(Sentence)
class SentenceAdmin(admin.ModelAdmin):
    pass
