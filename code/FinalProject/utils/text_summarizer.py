from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import bs4 as BeautifulSoup
import urllib.request


class TextSummarizer:
    def __call__(self, raw_text):
        word_dict, sentence_dict, sentences = \
            self.word_sentence_dictionary(raw_text)

        # threshold based on sentence frequencies
        threshold = self.generate_threhsold(sentence_dict)

        article_summary = self.generate_summary(
            sentences, sentence_dict, 1.1 * threshold)

        return article_summary

    def word_sentence_dictionary(self, text: dict):
        # word frequencies
        words = word_tokenize(text)
        stem = PorterStemmer()
        stop_words = set(stopwords.words("english"))
        word_dict = dict()
        for wd in words:
            wd = stem.stem(wd)
            if wd in stop_words:
                continue
            if wd in word_dict:
                word_dict[wd] += 1
            else:
                word_dict[wd] = 1

        # sentence frequencies
        sentences = sent_tokenize(text)
        sentence_dict = dict()
        for sentence in sentences:
            # sentence length without stop words
            sentence_length_updated = 0
            for word in word_dict:
                if word in sentence.lower():
                    sentence_length_updated += 1
                    if sentence in sentence_dict:
                        sentence_dict[sentence] += word_dict[word]
                    else:
                        sentence_dict[sentence] = word_dict[word]

            sentence_dict[sentence] = \
                sentence_dict[sentence] / sentence_length_updated

        return word_dict, sentence_dict, sentences

    def generate_threhsold(self, sentence_dict) -> int:
        sum_values = 0
        for entry in sentence_dict:
            sum_values += sentence_dict[entry]
        average_score = (sum_values / len(sentence_dict))
        return average_score

    def generate_summary(self, sentences, sentence_dict, threshold):
        counter = 0
        summary = ''

        for sentence in sentences:
            if sentence in sentence_dict and \
                    sentence_dict[sentence] >= (threshold):
                summary += " " + sentence
                counter += 1
        return summary
