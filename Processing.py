# Importons les librairies pour faire les transformations stemming et lemmatization et le tokenizer de nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Téléchargement des dépendance NLTP
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

text = 'Text preprocessing helps improve the quality and reliability of NLP'

# Correction
class Processing:
    def __init__ (self):
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = stopwords.words('english')


    def tokenization(self, text:str, stem : bool = False, lem : bool = False) -> list:
        tokens =  [x.lower() for x in word_tokenize(text) if x.lower() not in self.stop_words]


        if stem:
            tokens = [self.stemmer.stem(token) for token in tokens]

        if lem:
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        return tokens

process = Processing()
result = process.tokenization(text, True, True)
print(result)

# Pour le CSV 
import pandas as pd
import string 

df = pd.read_csv('QA_bot.csv')
text = df.values[0][0]

process = Processing()
result = process.tokenization(text, True, True)

for elem in result: # On retire les tokens avec uniquement la ponctuation
  if elem not in string.punctuation:
    print(elem)