from sumy.utils import get_stop_words
from sumy.nlp.stemmers import Stemmer
from sumy.summarizers.lex_rank import LexRankSummarizer as summ
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
import nltk
nltk.data.path.append("nltk_data")
# from sumy.summarizers.lsa import LsaSummarizer as summ
# from sumy.summarizers.luhn import LuhnSummarizer as summ
# from sumy.summarizers.text_rank import TextRankSummarizer as summ


def sum_urls(urls):
    text = " "
    for url in urls:
        try:
            parser = HtmlParser.from_url(url, Tokenizer("english"))
            stemmer = Stemmer("english")
            summarizer = summ(stemmer)
            summarizer.stop_words = get_stop_words("english")
            text += " ".join(str(sentence)
                            for sentence in summarizer(parser.document, 3))
        except:
            pass

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    stemmer = Stemmer("english")
    summarizer = summ(stemmer)
    summarizer.stop_words = get_stop_words("english")

    return " ".join(str(sentence) for sentence in summarizer(parser.document, 2))
