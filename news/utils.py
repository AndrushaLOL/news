import nltk
import re
import pymorphy2

from nltk.corpus import stopwords
nltk.download('stopwords')


class CleanText():

    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()
        self.stop = stopwords.words('russian')

    def clean_text(self, text):
        """
        Функция очистки текста
        """

        text = re.sub(r'[^\w\s]', '', text)  # удаление всех символов кроме букв и цифр
        text = re.sub(r'\d', '', text)  # удаление цифр
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)  # '    ' -> ' '
        text = text.lower()
        text = [w for w in text.split() if w not in self.stop]
        normals = [self.morph.parse(w)[0].normal_form for w in text]  # лемматизация
        return ' '.join(normals)
