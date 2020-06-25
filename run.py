from tia.routes import app
from nltk.stem import PorterStemmer
from nltk import word_tokenize


def stemming_tokenizer(text):
    # This is here for nlp models (will be relocated)
    stemmer = PorterStemmer()
    return [stemmer.stem(w) for w in word_tokenize(text)]


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
