from earningscall import get_company
from textblob import TextBlob


# Initialize the Earnings Call API
company = get_company("AAPL")

# Fetch the transcript of a specific earnings call
transcript = company.get_transcript(quarter=1, year=2024)

# Perform sentiment analysis on the transcript
blob = TextBlob(transcript.text)
sentiment = blob.sentiment

# Print the results
print(sentiment)
print(f"Sentiment Polarity: {sentiment.polarity}")
print(f"Sentiment Subjectivity: {sentiment.subjectivity}")


# from flair.data import Sentence
# from flair.nn import Classifier

# # make a sentence
# sentence = Sentence('I love Berlin .')

# # load the NER tagger
# tagger = Classifier.load('sentiment')

# # run NER over sentence
# tagger.predict(sentence)

# # print the sentence with all annotations
# print(sentence)

