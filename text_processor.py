import spacy_udpipe


class TextProcessor:
    def __init__(self):
        spacy_udpipe.download("ru")
        self.nlp = spacy_udpipe.load("ru")

    # Этого синглтона пока не надо от детей просить. Просто для демо: иначе будет долго грузиться
    __instance = None

    @classmethod
    def get_instance(cls): #
        if not cls.__instance:
            cls.__instance = TextProcessor()
        return cls.__instance
    ###########

    def extract_lemmatized_tokens(self, text):
        text = text
        processed_text = self.nlp(text)
        return [_t.lemma_ for _t in processed_text]


if __name__ == '__main__':
    text = 'Дай мне парочку бигмаков'
    processor = TextProcessor()
    lemmas = processor.extract_lemmatized_tokens(text)
    print(lemmas)