import re
import nltk
import spacy
import unicodedata

from utils.contractions import CONTRACTION_MAP
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.stem.porter import PorterStemmer
from sklearn.base import BaseEstimator, TransformerMixin

nltk.download('stopwords')
tokenizer = ToktokTokenizer()
stemmer = PorterStemmer()
stopword_list = nltk.corpus.stopwords.words('english')
#nlp = spacy.load('en_core_web_sm')


def remove_html_tags(text):
    # Put your code
    remove_html = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    text = re.sub(remove_html, '', text)
    return text


def stem_text(text):
    # Put your code
    tokens = tokenizer.tokenize(text)
    stems = [stemmer.stem(token) for token in tokens]
    text = " ".join(stems)
    return text


def lemmatize_text(text):
    # Put your code
    tokens = nlp(text)
    lemmas = [token.lemma_ for token in tokens]
    text = " ".join(lemmas)
    return text


def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
    # Put your code
    for word, replacement in contraction_mapping.items():
        text = text.replace(word, replacement)     
    return text


def remove_accented_chars(text):
    # Put your code
    nfkd = unicodedata.normalize('NFKD', text)
    ascii = nfkd.encode('ASCII', 'ignore')
    text = ascii.decode('UTF-8')
    return text


def remove_special_chars(text, remove_digits=False):
    # Put your code
    chars= r"[^a-zA-Z0-9 ]+"
    text = re.sub(chars, '', text)
    if remove_digits:
        numbers = r"[\d]"
        text = re.sub(numbers, '', text)
    return text


def remove_stopwords(text, is_lower_case=False, stopwords=stopword_list):
    # Put your code
    if is_lower_case:
        text = text.lower()
    tokens = tokenizer.tokenize(text)
    no_stop = [w for w in tokens if not w in stopword_list]
    text = " ".join(no_stop)
    return text


def remove_extra_new_lines(text):
    # Put your code
    text = re.sub('\n', ' ', text.strip())
    return text


def remove_extra_whitespace(text):
    # Put your code
    text = re.sub(' +', ' ', text.strip())
    return text
    

def normalize_corpus(
    corpus,
    html_stripping=True,
    contraction_expansion=True,
    accented_char_removal=True,
    text_lower_case=True,
    text_stemming=False,
    text_lemmatization=False,
    special_char_removal=True,
    remove_digits=True,
    stopword_removal=True,
    stopwords=stopword_list
):
    
    normalized_corpus = []

    # Normalize each doc in the corpus
    for doc in corpus:
        # Remove HTML
        if html_stripping:
            doc = remove_html_tags(doc)
            
        # Remove extra newlines
        doc = remove_extra_new_lines(doc)
        
        # Remove accented chars
        if accented_char_removal:
            doc = remove_accented_chars(doc)
            
        # Expand contractions    
        if contraction_expansion:
            doc = expand_contractions(doc)
            
        # Lemmatize text
        if text_lemmatization:
            doc = lemmatize_text(doc)
            
        # Stemming text
        if text_stemming and not text_lemmatization:
            doc = stem_text(doc)
            
        # Remove special chars and\or digits    
        if special_char_removal:
            doc = remove_special_chars(
                doc,
                remove_digits=remove_digits
            )  

        # Remove extra whitespace
        doc = remove_extra_whitespace(doc)

         # Lowercase the text    
        if text_lower_case:
            doc = doc.lower()

        # Remove stopwords
        if stopword_removal:
            doc = remove_stopwords(
                doc,
                is_lower_case=text_lower_case,
                stopwords=stopwords
            )

        # Remove extra whitespace
        doc = remove_extra_whitespace(doc)
        doc = doc.strip()
            
        normalized_corpus.append(doc)
        
    return normalized_corpus


class Normalizer(BaseEstimator, TransformerMixin):
    
    def fit(self, X, y=None):
        return self
        
    def transform(self, X, y=None):
        normalized_desc = normalize_corpus(
        X,
        html_stripping=True,
        contraction_expansion=True,
        accented_char_removal=True,
        text_lower_case=True,
        text_stemming=True,
        text_lemmatization=False,
        special_char_removal=True,
        remove_digits=False,
        stopword_removal=True,
        stopwords=stopword_list,
    )
        return normalized_desc