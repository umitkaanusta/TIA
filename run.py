from tia.routes import app

from tia.stalk.util import stemming_tokenizer

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
