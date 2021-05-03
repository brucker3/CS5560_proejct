from nltk import tokenize
from operator import itemgetter
import math
import spacy
from nltk.corpus import stopwords
nlp = spacy.load('en')


class ExtractKeywords:
    def __init__(self, nnumberofkeywords=5):
        self.keywordsstopwords = set(stopwords.words('english'))
        self.nnumberofkeywords = nnumberofkeywords

    def __call__(self, summaryResult):
        allTotalWords = summaryResult.split()
        allTotalWordLength = len(allTotalWords)
        # print(allTotalWordLength)
        allTotalSentences = tokenize.sent_tokenize(summaryResult)
        allTotalSenLength = len(allTotalSentences)
        # print(allTotalSenLength)

        defineTFScore = {}
        for eachSingleWords in allTotalWords:
            eachSingleWords = eachSingleWords.replace('.', '')
            if eachSingleWords not in self.keywordsstopwords:
                if eachSingleWords in defineTFScore:
                    defineTFScore[eachSingleWords] += 1
                else:
                    defineTFScore[eachSingleWords] = 1

        # Dividing by allTotalWordLength for each dictionary element
        defineTFScore.update((x, y/int(allTotalWordLength))
                             for x, y in defineTFScore.items())
        # print(defineTFScore)
        defineTDFScore = {}
        for eachSingleWords in allTotalWords:
            eachSingleWords = eachSingleWords.replace('.', '')
            if eachSingleWords not in self.keywordsstopwords:
                if eachSingleWords in defineTDFScore:
                    defineTDFScore[eachSingleWords] = self.checkSentence(
                        eachSingleWords, allTotalSentences)
                else:
                    defineTDFScore[eachSingleWords] = 1

        defineTDFScore.update((x, math.log(int(allTotalSenLength)/y))
                              for x, y in defineTDFScore.items())

        TFIDFScore = {key: defineTFScore[key] * defineTDFScore.get(key, 0)
                      for key in defineTFScore.keys()}
        return list(self.getTopNValues(TFIDFScore, self.nnumberofkeywords).
                    keys())

    def checkSentence(self, eachWord, summary):
        finalkey = [all([w in x for w in eachWord]) for x in summary]
        sentLength = [summary[i] for i in range(0, len(finalkey))
                      if finalkey[i]]
        return int(len(sentLength))

    def getTopNValues(self, listItems, n):
        result = dict(sorted(listItems.items(),
                      key=itemgetter(1), reverse=True)[:n])
        return result
