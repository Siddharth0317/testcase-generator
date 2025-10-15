# backend/test_spacy.py
import spacy

MODEL_PATH = "models/testgen_model"
nlp = spacy.load(MODEL_PATH)

test_sentences = [
    "Users should be able to log in using Google account.",
    "The system must respond within 1 second.",
    "The uploaded file size should not exceed 10MB."
]

for sent in test_sentences:
    doc = nlp(sent)
    # Print predicted labels with probabilities
    print(f"Sentence: {sent}")
    print("Predicted labels:")
    for label, score in doc.cats.items():
        print(f"  {label}: {score:.3f}")
    print("------")
