#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

def computeFraction( poi_messages, all_messages ):
    """ given a number messages to/from POI (numerator) 
        and number of all messages to/from a person (denominator),
        return the fraction of messages to/from that person
        that are from/to a POI
    """
    return (poi_messages / float(all_messages))  if all_messages != 'NaN' and all_messages != 0 else 0.


### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi', 'bonus', 'exercised_stock_options', 'total_stock_value', 'fraction_to_poi', 'salary', 'total_payments', 'shared_receipt_with_poi', 'deferred_income', 'restricted_stock', 'loan_advances', 'long_term_incentive', 'other', 'to_messages', 'expenses', 'director_fees', 'fraction_from_poi', 'restricted_stock_deferred', 'from_messages', 'deferral_payments']
k_best = 16

features_list = features_list[:k_best]

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
del data_dict['TOTAL']
del data_dict['LOCKHART EUGENE E']
del data_dict['THE TRAVEL AGENCY IN THE PARK']

### Task 3: Create new feature(s)
for name in data_dict:
    data_point = data_dict[name]
    
    fraction_from_poi = computeFraction( data_point["from_poi_to_this_person"], data_point["to_messages"] )
    data_point["fraction_from_poi"] = fraction_from_poi

    fraction_to_poi = computeFraction( data_point["from_this_person_to_poi"], data_point["from_messages"] )
    data_point["fraction_to_poi"] = fraction_to_poi


### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html


# the best classification algorithm and hyperparameter as documented in final_report.ipynb / final_report.html
from sklearn import tree
clf = tree.DecisionTreeClassifier(criterion='entropy', min_samples_split = 20)


### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)

#from tester import test_classifier
#test_classifier(clf, my_dataset, features_list)


