from django.contrib import admin

from eng.models import Word, Sentence


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'transcription')


@admin.register(Sentence)
class SentenceAdmin(admin.ModelAdmin):
    list_display = ['text', 'get_transcription']

    @admin.display(description='transcription')
    def get_transcription(self, obj):
        return obj.word.transcription
