# Project Assessment

## For classifying product names to categories:

1. What precision (P@1) were you able to achieve?
```
N       9983
P@1     0.793
R@1     0.793

N       9983
P@5     0.19
R@5     0.95   

N       9983
P@10    0.0969
R@10    0.969
```  

2. What fastText parameters did you use?
```
-epoch 25 -lr 1.0 -wordNgrams 2 -minCount 50
```

3. How did you transform the product names?
```
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

```
4. How did you prune infrequent category labels, and how did that affect your precision?

```
Only retained those category labels with example count > 500
```

5. How did you prune the category tree, and how did that affect your precision?

``` 
Did not attempt
```

## For deriving synonyms from content:

1. What were the results for your best model in the tokens used for evaluation?

2. What fastText parameters did you use?
``` 
-epcoh 25 -minCount 20 
```

3. How did you transform the product names?

``` 
Basic normalization with cat /workspace/datasets/fasttext/titles.txt | 
sed -e "s/\([.\!?,'/()]\)/ \1 /g" | tr "[:upper:]" "[:lower:]" | sed "s/[^[:alnum:]]/ /g" | 
tr -s ' ' > /workspace/datasets/fasttext/normalized_titles.txt
```

## For integrating synonyms with search:

1. How did you transform the product names (if different than previously)?

2. What threshold score did you use?

3. Were you able to find the additional results by matching synonyms?

## For classifying reviews:

1. What precision (P@1) were you able to achieve?

2. What fastText parameters did you use?

3. How did you transform the review content?

4. What else did you try and learn?

