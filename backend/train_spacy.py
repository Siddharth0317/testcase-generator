import random
import json
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding

def main(data_file="sample_tests_expanded.jsonl", output_dir="models/testgen_model", n_iter=10):
    texts, cats = [], []
    with open(data_file, "r", encoding="utf8") as f:
        for line in f:
            obj = json.loads(line)
            texts.append(obj["text"])
            cats.append(obj.get("labels", {}))

    nlp = spacy.blank("en")
    textcat = nlp.add_pipe("textcat", last=True)
    labels = set()
    for c in cats:
        labels.update(c.keys())
    for l in labels:
        textcat.add_label(l)

    optimizer = nlp.begin_training()
    train_data = list(zip(texts, [{"cats": c} for c in cats]))

    for i in range(n_iter):
        random.shuffle(train_data)
        losses = {}
        batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
            texts_batch, annotations = zip(*batch)
            nlp.update(texts_batch, annotations, sgd=optimizer, drop=0.2, losses=losses)
        print(f"Iter {i+1}/{n_iter} - Losses: {losses}")

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    nlp.to_disk(output_dir)
    print("✅ Saved model to", output_dir)

if __name__ == "__main__":
    main()
