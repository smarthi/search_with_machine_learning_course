import argparse
import multiprocessing
import glob
from tqdm import tqdm
import os
import random
import xml.etree.ElementTree as ET
from pathlib import Path
from tqdm import tqdm
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
import re


def transform_name(product_name):
    # IMPLEMENT
    stemmer = SnowballStemmer("english")
    if args.normalize:
        # Remove all non-alphanumeric characters other than underscore
        product_name = re.sub(r'[^\w_ ]', ' ', product_name)
        # Convert all chars to lowercase
        product_name = product_name.lower().strip()
        # Stemmer
        product_name = " ".join([stemmer.stem(word) for word in product_name.split()])
    return product_name

def filter_products(products_file_path, minProducts):
    products_df = pd.read_csv(products_file_path, names=['category_product'])
    # Split the first word as the category, all the rest are the product title
    products_df['category'] = products_df['category_product'].str.split().str.get(0)
    products_df['product'] = products_df['category_product'].str.split().str[1:]
    products_df['product'] = products_df['product'].str.join(' ')
    products_df.drop('category_product', axis=1, inplace=True)
    # Filter
    pruned_labels_df = products_df[products_df.groupby(['category'])['product'].transform('count') > min_products]
    return pruned_labels_df

# Directory for product data
directory = r'/workspace/datasets/product_data/products/'

parser = argparse.ArgumentParser(description='Process some integers.')
general = parser.add_argument_group("general")
general.add_argument("--input", default=directory,  help="The directory containing product data")
general.add_argument("--output", default="/workspace/datasets/fasttext/output.fasttext", help="the file to output to")
general.add_argument("--label", default="id", help="id is default and needed for downsteam use, but name is helpful for debugging")

# Consuming all of the product data, even excluding music and movies,
# takes a few minutes. We can speed that up by taking a representative
# random sample.
general.add_argument("--sample_rate", default=1.0, type=float, help="The rate at which to sample input (default is 1.0)")

# IMPLEMENT: Setting min_products removes infrequent categories and makes the classifier's task easier.
general.add_argument("--min_products", default=0, type=int, help="The minimum number of products per category (default is 0).")

args = parser.parse_args()
output_file = args.output
path = Path(output_file)
output_dir = path.parent
if os.path.isdir(output_dir) == False:
        os.mkdir(output_dir)

if args.input:
    directory = args.input
# IMPLEMENT:  Track the number of items in each category and only output if above the min
min_products = args.min_products
sample_rate = args.sample_rate
names_as_labels = False
if args.label == 'name':
    names_as_labels = True


def _label_filename(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    labels = []
    for child in root:
        if random.random() > sample_rate:
            continue
        # Check to make sure category name is valid and not in music or movies
        if (child.find('name') is not None and child.find('name').text is not None and
            child.find('categoryPath') is not None and len(child.find('categoryPath')) > 0 and
            child.find('categoryPath')[len(child.find('categoryPath')) - 1][0].text is not None and
            child.find('categoryPath')[0][0].text == 'cat00000' and
            child.find('categoryPath')[1][0].text != 'abcat0600000'):
              # Choose last element in categoryPath as the leaf categoryId or name
              if names_as_labels:
                  cat = child.find('categoryPath')[len(child.find('categoryPath')) - 1][1].text.replace(' ', '_')
              else:
                  cat = child.find('categoryPath')[len(child.find('categoryPath')) - 1][0].text
              # Replace newline chars with spaces so fastText doesn't complain
              name = child.find('name').text.replace('\n', ' ')
              labels.append((cat, transform_name(name)))
    return labels

if __name__ == '__main__':
    files = glob.glob(f'{directory}/*.xml')

    print("Writing results to %s" % output_file)
    with multiprocessing.Pool() as p:
        all_labels = tqdm(p.imap_unordered(_label_filename, files), total=len(files))


        with open(output_file, 'w') as output:
            for label_list in all_labels:
                for (cat, name) in label_list:
                    output.write(f'__label__{cat} {name}\n')
def _label_filename(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    labels = []
    for child in root:
        if random.random() > sample_rate:
            continue
        # Check to make sure category name is valid and not in music or movies
        if (child.find('name') is not None and child.find('name').text is not None and
                child.find('categoryPath') is not None and len(child.find('categoryPath')) > 0 and
                child.find('categoryPath')[len(child.find('categoryPath')) - 1][0].text is not None and
                child.find('categoryPath')[0][0].text == 'cat00000' and
                child.find('categoryPath')[1][0].text != 'abcat0600000'):
            # Choose last element in categoryPath as the leaf categoryId or name
            if names_as_labels:
                cat = child.find('categoryPath')[len(child.find('categoryPath')) - 1][1].text.replace(' ', '_')
            else:
                cat = child.find('categoryPath')[len(child.find('categoryPath')) - 1][0].text
            # Replace newline chars with spaces so fastText doesn't complain
            name = child.find('name').text.replace('\n', ' ')
            labels.append((cat, transform_name(name)))
    return labels

if __name__ == '__main__':
    files = glob.glob(f'{directory}/*.xml')
    print("Writing results to %s" % output_file)

    category_seen_count = {}
    category_buffer = {}

    with multiprocessing.Pool() as p:
        all_labels = tqdm(p.imap_unordered(_label_filename, files), total=len(files))
        with open(output_file, 'w') as output:
                for label_list in all_labels:
                    for (cat, name) in label_list:
                        if category_seen_count.get(cat) is None:
                            category_seen_count[cat] = 0
                        category_seen_count[cat] += 1

                        if category_seen_count[cat] < min_products:
                            # keep names in memory, wait till the count reaches "min_products"
                            if category_buffer.get(cat) is None:
                                category_buffer[cat] = []
                            category_buffer[cat].append(name)
                        else:
                            # add previously seen names from the buffer
                            if category_buffer.get(cat) is not None and len(category_buffer.get(cat)) > 0:
                                for name in category_buffer.get(cat):
                                    output.write(f'__label__{cat} {name}\n')
                                # remove all previous names from memory
                                # hope I'm doing it correctly)
                                category_buffer[cat] = {}
                            # add current name as well
                            output.write(f'__label__{cat} {name}\n')
