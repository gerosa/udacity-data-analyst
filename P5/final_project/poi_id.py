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
features_list = ['poi', 'bonus', 'exercised_stock_options', 'total_stock_value', 'fraction_to_poi', 'salary', 'total_payments', 'shared_receipt_with_poi']
#features_list = ['poi', 'bonus', 'exercised_stock_options', 'total_stock_value', 'fraction_to_poi', 'salary', 'total_payments', 'shared_receipt_with_poi', 'deferred_income', 'restricted_stock', 'loan_advances', 'long_term_incentive', 'other', 'to_messages', 'expenses', 'director_fees', 'fraction_from_poi', 'restricted_stock_deferred', 'from_messages', 'deferral_payments']

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
del data_dict['TOTAL']

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

# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()

#from sklearn import tree
#clf = tree.DecisionTreeClassifier(min_samples_split = 10)

#from sklearn.ensemble import RandomForestClassifier
#clf = RandomForestClassifier(n_estimators=100, criterion='entropy')


#from sklearn.grid_search import GridSearchCV


#param_grid = {
#        'min_samples_split': [10, 15, 20],
#        'max_features': ['auto', .5, None],
#        'class_weight': ['balanced', None]}

#clf = GridSearchCV(clf, param_grid)


### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)


# Remove this

clf.fit(features_train, labels_train)

#print clf.best_estimator_

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score

predictions = clf.predict(features_test)

print('Confusion Matrix')
print(confusion_matrix(labels_test, predictions))

print('Accuracy: {}'.format(accuracy_score(labels_test, predictions) ) )
print('Recall: {}'.format(recall_score(labels_test, predictions) )) 
print('Precision: {}'.format(precision_score(labels_test, predictions) )) 

predictions = clf.predict(features_train)

print('Confusion Matrix')
print(confusion_matrix(labels_train, predictions))

print('Accuracy: {}'.format(accuracy_score(labels_train, predictions) ) )
print('Recall: {}'.format(recall_score(labels_train, predictions) )) 
print('Precision: {}'.format(precision_score(labels_train, predictions) )) 










