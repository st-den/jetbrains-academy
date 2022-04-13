from string import punctuation

from lxml import etree
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

if __name__ == "__main__":
    lemmatizer = WordNetLemmatizer()
    vectorizer = TfidfVectorizer()
    stoplist = stopwords.words("english") + list(punctuation)

    corpus = etree.parse("news.xml").getroot().find("corpus")  # type: ignore
    headlines = []
    documents = []

    for news in corpus:
        headlines.append(news.find("value[@name='head']").text)
        tokens = word_tokenize(news.find("value[@name='text']").text.lower())
        normalized_tokens = [token for token in tokens if token not in stoplist]
        lemmas = [lemmatizer.lemmatize(token) for token in normalized_tokens]
        word_pos = [pos_tag([word]) for word in lemmas]
        nouns = [word[0][0] for word in word_pos if word[0][1] == "NN"]
        documents.append(" ".join(nouns))

    tfidf_arr = vectorizer.fit_transform(documents).toarray()
    terms = vectorizer.get_feature_names_out()

    for i, head in enumerate(headlines):
        freqs = dict(
            sorted(zip(terms, tfidf_arr[i]), key=lambda x: (x[1], x[0]), reverse=True)
        )
        print(head, ":\n", " ".join(list(freqs)[:5]), sep="", end="\n\n")
