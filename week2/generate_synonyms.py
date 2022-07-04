import argparse
import csv
import fasttext
import pandas as pd

parser = argparse.ArgumentParser(description='Process some integers.')
general = parser.add_argument_group("general")
general.add_argument("--model_path", default="/workspace/datasets/fasttext/title_model.bin",  help="The path to the model")
general.add_argument("--top_words", default="/workspace/datasets/fasttext/top_words.txt",  help="The path to the text file containing the top words")
general.add_argument("--output", default="/workspace/datasets/fasttext/synonyms.csv", help="the file to output to")

args = parser.parse_args()
model_path = args.model_path
top_words_file = args.top_words
output_file = args.output

# Train model
model = fasttext.load_model(model_path)

threshold = 0.8
df = pd.read_csv(top_words_file, sep='\t', header=None, names=["token"])
tokens = df['token'].tolist()
synonyms_dict = []

# Get nearest neighbours
for token in tokens:
    synonyms_data = model.get_nearest_neighbors(token)
    nn = [token]
    for (similarity, synonym) in synonyms_data:
        if similarity > threshold:
            nn.append(synonym)
    if len(nn) > 1:
        synonyms_dict.append({"synonym": ', '.join(nn)})

synonym_df = pd.DataFrame(synonyms_dict)
synonym_df.to_csv(output_file, header=False, index=False, sep='\t', quoting = csv.QUOTE_NONE)