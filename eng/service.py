import re

import requests
import fake_useragent
from bs4 import BeautifulSoup

from eng.models import Sentence, Word


DEFAULT_LINK = 'https://www.manythings.org/sentences/words/{}/2.html'
BACKUP_LINK = 'https://www.manythings.org/sentences/words/{}/1.html'


class GetSentencesError(Exception):
    """
    Ошибка получения предложений
    """
    pass


def parse_and_add_sentences(word: Word) -> None:
    if len(word.word.split()) == 1:
        parser = SentenceParser(word.word)
        sentences = parser.get_sentences()
        if sentences:
            objects = [Sentence(text=sentence, word=word)
                       for sentence in sentences]
            Sentence.objects.bulk_create(objects)


class SentenceParser:

    def __init__(self, word: str) -> None:
        self.user_agent = fake_useragent.UserAgent().random
        self.link = DEFAULT_LINK.format(word)
        self.backup_link = BACKUP_LINK.format(word)

    def get_sentences(self) -> list[str] | None:
        try:
            html_page = self._get_html_page_soup()
        except GetSentencesError:
            return None
        block_with_sentences = self._get_sentences_block_from_page(
            html_page)
        sentences_list = self._get_clean_sentences(block_with_sentences)

        return sentences_list

    def _get_html_page_soup(self) -> BeautifulSoup:
        response = requests.get(
            self.link, headers={'user-agent': self.user_agent})
        if response.status_code != 200:
            response = requests.get(
                self.backup_link, headers={'user-agent': self.user_agent})
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'lxml')
        raise GetSentencesError

    def _get_sentences_block_from_page(self, raw_html: BeautifulSoup) -> BeautifulSoup:
        pre = raw_html.find('pre')
        return pre

    def _get_clean_sentences(self, sentences_block: BeautifulSoup) -> list[str]:

        text_without_html = self.__remove_html_and_tabs(str(sentences_block))
        clean_text = self.__remove_digits_from_text(text_without_html)

        sentences = []
        for sentence in clean_text.split('\n'):
            sentence = self.__sentence_without_author(sentence)
            if sentence:
                sentences.append(sentence)

        return sentences

    def __remove_html_and_tabs(self, text: str) -> str:
        regex = re.compile('(<.*?>)|\t')
        res = re.sub(regex, '', text)

        return res

    def __remove_digits_from_text(self, text: str) -> str:
        text_without_digits = [i for i in text if not i.isdigit()]
        result = ''.join(text_without_digits)

        return result

    def __sentence_without_author(self, sentence: str | None) -> str | None:
        if sentence:
            for i in range(len(sentence)):
                if sentence[i] in ['.', '?', '!']:
                    end_index = i+1
                    break
            return sentence[:end_index]
        return None


if __name__ == '__main__':

    parser = SentenceParser('lot')
    print(parser.get_sentences())
