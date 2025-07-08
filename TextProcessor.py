from Processing import Processing
from transformers import pipeline
from transformers import BertTokenizer, BertModel

class TextProcessor(Processing) :
    def __init__(self):
        super(Processing, self).__init__()

    def translate_to_french(self, english_text):
        # Here you would implement the translation logic
        traduction = pipeline("translation_en_to_fr")
        french_text = traduction(english_text)

        return f'Le texte traduit en français : {french_text}'
    
    def extract_entities(self, text):
        # Here you would implement the entity extraction logic
        nlp = pipeline("ner", aggregation_strategy="simple")
        entities = nlp(text)
        
        return f'Les entités extraites : {entities}'
    
    def analyze_sentiment(self, text):
        # Here you would implement the sentiment analysis logic
        sentiment_analyzer = pipeline("sentiment-analysis")
        sentiment = sentiment_analyzer(text)
        
        return f'Analyse de sentiment : {sentiment}'
    
    #Extraction d'Embeddings : Ajoutez une méthode extract_embeddings qui prend un texte comme argument et renvoie ses embeddings. Pour cela, utilisez le BertTokenizer.from_pretrained('bert-base-uncased') pour tokenizer le texte, puis utilisez un modèle BERT pour obtenir les embeddings. Pensez à gérer la conversion entre les tokens et les embeddings en utilisant le modèle BERT approprié.
    def extract_embeddings (self, text):
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        model = BertModel.from_pretrained('bert-base-uncased')
        inputs = tokenizer(text, return_tensors='pt')
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()
        return f'Les embeddings extraits : {embeddings}'
    
    #Génération de Texte : Ajoutez une méthode generate_text qui utilise pipeline("text-generation", model="gpt2") pour générer du texte à partir d'une prompt donnée.
    def generate_text(self, prompt):
        text_generator = pipeline("text-generation", model="gpt2")
        generated_text = text_generator(prompt)
        return f'Texte généré : {generated_text}'

#Test
test = TextProcessor()
print(test.translate_to_french("This day I feel good"))
print(test.extract_entities("Barack Obama was the 44th president of the United States."))
print(test.analyze_sentiment("I love programming!"))
print(test.extract_embeddings("Hello, my dog is cute"))
print(test.generate_text("Once upon a time, a lord lived in a castle."))