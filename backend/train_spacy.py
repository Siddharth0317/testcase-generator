import spacy
from spacy.util import minibatch, compounding
import random
import json
from pathlib import Path
from spacy.training.example import Example

# Parameters
DATA_FILE = "data/sample_tests.jsonl"
OUTPUT_DIR = "models/testgen_model"
N_ITER = 10

# Load training data
texts, labels = [], []
with open(DATA_FILE, "r", encoding="utf8") as f:
    for line in f:
        obj = json.loads(line)
        texts.append(obj["text"])
        labels.append(obj["labels"])

# Create blank NLP model
nlp = spacy.blank("en")

# Add text classifier
textcat = nlp.add_pipe("textcat", last=True)
for label_name in set(k for d in labels for k in d.keys()):
    textcat.add_label(label_name)

# Prepare training data
train_data = list(zip(texts, [{"cats": l} for l in labels]))

# --- Training loop ---
optimizer = nlp.begin_training()

for i in range(N_ITER):
    random.shuffle(train_data)
    losses = {}
    batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
    for batch in batches:
        examples = []
        for text, annotation in batch:
            doc = nlp.make_doc(text)
            examples.append(Example.from_dict(doc, annotation))
        nlp.update(examples, sgd=optimizer, drop=0.2, losses=losses)
    print(f"Iteration {i+1}/{N_ITER} - Losses: {losses}")

# Save model
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
nlp.to_disk(OUTPUT_DIR)
print(f"✅ Model saved to {OUTPUT_DIR}")
