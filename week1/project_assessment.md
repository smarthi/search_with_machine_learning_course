# Project Assessment

## 1. Do you understand the steps involved in creating and deploying an LTR model? Name them and describe what each step does in your own words.
      Yes! 

        - Create featureset by picking features that are most influential for use in the LTR model. These 
          features could be a combination of query-dependent (like matching query terms to documents) and
          query-independent features (like sales price, popularity scrores, user ratings). Also need to collect and factor in
          judgements (both implicit and explicit).

        - Train and validate LTR model on the featureset. In this step, we will be training several different models with different permutations and combinations 
          of the features from the featureset, and test the model on held out data( test data). While we have trained an XGoost model
          in this project- other possible models for LTE could be LambdaMart, Ranking SM etc..

        - Deploy the best model to the Search engine.

       Model Monitoring happens once the model is rolled out to production to gauge and ensure the model performance. 

## 2. What is a feature and featureset?

        Feature: an attribute of the document or query that can be used as a signal to build a LTR model. 
        FeatureSet: a collection of features, that can be used to train an LTR model.

      The featureSet could be useful later to better explain a Model's performance and scoring behavior.

## 3. What is the difference between precision and recall?

     Precision: Fraction of relevant search results returned from all of the returned results (measure of search quality)
      Recall: Fraction of relevant search results returned from all of the relevant results

## 4. What are some of the traps associated with using click data in your model?

      Traps associated with using Click Data for LTR Model training:
        a) Positional Bias: The Top K results are more likely to see clicks despite not being relevant
        b) Selection Bias: Since the clicks depend on user behavior, a user could potentially click the wrong and
         irrelevant results and training a LTR model with this data wouldn't generalize well across previously 
         unseen search queries.
        c) Need many users to geenrate a well-distributed click data, and not be biased towards a few users' behavior.
       
## 5. What are some of the ways we are faking our data and how would you prevent that in your application?
        We are generating synthetic impressions based on users having seen a product but not based on user conversions.
        The model trained on this is most likely a bad model. In a real world scenario, the impressions and 
        clicks would both be captured to avoid generating synthetic data.

## 6. What is target leakage and why is it a bad thing?
       When data that's being used to train the model performance makes it into test, the model already has 
       learnt the data and wouldn't generalize well to predictions on unseen data.
        
## 7. When can using prior history cause problems in search and LTR?
        Prior history is based on historical data and may not be relevant in present times due to changed circumstances.
        This is more of an issue in the ECommerce world wherein historical data has products that are no more in vogue, 
         an example being 'iPhone 4' in the Best Buy dataset from 2011 that is irrelevant in 2022.
        This could cause some products to be ranked different (too high or too low) from what the present popularity 
        of the product should actually be.

------
Submit your project along with your best MRR scores

Simple MRR is 0.335
LTR Simple MRR is 0.419
Hand tuned MRR is 0.422
LTR Hand Tuned MRR is 0.426

Simple p@10 is 0.096
LTR simple p@10 is 0.167
Hand tuned p@10 is 0.178
LTR hand tuned p@10 is 0.169
Simple better: 533      LTR_Simple Better: 754  Equal: 9
HT better: 698  LTR_HT Better: 764      Equal: 15
