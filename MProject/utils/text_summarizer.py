import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from heapq import nlargest
import nltk
import heapq


class TextSummarizer:
    def __init__(self, mode: str):
        assert mode in ('spacy', 'nltk'), \
            'Choose correct summarizer: spacy/nltk'
        self.mode = mode
        self.mode_selection = {'spacy': self.spacy_summarizer,
                               'nltk': self.nltk_summarizer}
        self.summarizer = self.mode_selection[self.mode]

    def __call__(self, raw_text):
        return self.summarizer(raw_text)

    def spacy_summarizer(self, raw_text):
        nlp = spacy.load("en_core_web_sm")
        raw_text = raw_text
        docx = nlp(raw_text)
        stopwords = list(STOP_WORDS)

        # Build Word Frequency # word.text is tokenization in spacy
        word_frequencies = {}
        for word in docx:
            if word.text not in stopwords:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

        maximum_frequncy = max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

        # Sentence Tokens
        sentence_list = [sentence for sentence in docx.sents]

        # Sentence Scores
        sentence_scores = {}
        for sent in sentence_list:
            for word in sent:
                if word.text.lower() in word_frequencies.keys():
                    if len(sent.text.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[
                                word.text.lower()]
                        else:
                            sentence_scores[sent] += word_frequencies[
                                word.text.lower()]

        summarized_sentences = nlargest(7, sentence_scores,
                                        key=sentence_scores.get)
        final_sentences = [w.text for w in summarized_sentences]
        summary = ' '.join(final_sentences)
        return summary

    def nltk_summarizer(self, raw_text):
        nltk.download('stopwords')
        nltk.download('punkt')
        from nltk.corpus import stopwords
        stopWords = set(stopwords.words("english"))
        word_frequencies = {}
        for word in nltk.word_tokenize(raw_text):
            if word not in stopWords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

        maximum_frequncy = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

        sentence_list = nltk.sent_tokenize(raw_text)
        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]

        summary_sentences = heapq.nlargest(7, sentence_scores,
                                           key=sentence_scores.get)

        summary = ' '.join(summary_sentences)
        return summary
