from nltk import tokenize
from operator import itemgetter
import math
import spacy
from nltk.corpus import stopwords
nlp = spacy.load('en')


class ExtractKeywords:
    def __init__(self, n_keywords=5):
        self.stop_words = set(stopwords.words('english'))
        self.n_keywords = n_keywords

    def __call__(self, doc):
        total_words = doc.split()
        total_word_length = len(total_words)
        # print(total_word_length)
        total_sentences = tokenize.sent_tokenize(doc)
        total_sent_len = len(total_sentences)
        # print(total_sent_len)

        tf_score = {}
        for each_word in total_words:
            each_word = each_word.replace('.', '')
            if each_word not in self.stop_words:
                if each_word in tf_score:
                    tf_score[each_word] += 1
                else:
                    tf_score[each_word] = 1

        # Dividing by total_word_length for each dictionary element
        tf_score.update((x, y/int(total_word_length))
                        for x, y in tf_score.items())
        # print(tf_score)
        idf_score = {}
        for each_word in total_words:
            each_word = each_word.replace('.', '')
            if each_word not in self.stop_words:
                if each_word in idf_score:
                    idf_score[each_word] = self.check_sent(
                        each_word, total_sentences)
                else:
                    idf_score[each_word] = 1
        # Performing a log and divide
        idf_score.update((x, math.log(int(total_sent_len)/y))
                         for x, y in idf_score.items())

        tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0)
                        for key in tf_score.keys()}
        return list(self.get_top_n(tf_idf_score, self.n_keywords).keys())

    def check_sent(self, word, sentences):
        final = [all([w in x for w in word]) for x in sentences]
        sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
        return int(len(sent_len))

    def get_top_n(self, dict_elem, n):
        result = dict(sorted(dict_elem.items(),
                      key=itemgetter(1), reverse=True)[:n])
        return result
