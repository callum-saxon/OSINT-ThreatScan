import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from textblob import TextBlob

def analyze_text(content):

    tokens = word_tokenize(content)
    tagged = pos_tag(tokens)
    tree = ne_chunk(tagged, binary=False)

    named_entities = []
    for subtree in tree.subtrees():
        if subtree.label() in ["PERSON", "ORGANIZATION", "GPE", "FACILITY", "GSP"]:
            entity = " ".join(leaf[0] for leaf in subtree.leaves())
            named_entities.append((entity, subtree.label()))

    blob = TextBlob(content)
    polarity = blob.sentiment.polarity  # -1 to 1
    subjectivity = blob.sentiment.subjectivity  # 0 to 1

    return {
        "named_entities": named_entities,
        "sentiment": polarity,
        "subjectivity": subjectivity
    }
