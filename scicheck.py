#!/usr/bin/python

#importing libraries
import argparse
import time
import pandas as pd
import csv

#usage: scicheck -in_file infile.txt -out_file outfile.txt
# 0 = scientific name, 1 = not a scientific name

#all the options for this script
parser = argparse.ArgumentParser(description='File that takes text input and tests it against model')
parser.add_argument('--in_file', action="store", dest='in_file', required=True, help='Name of tab-separated inputted file')
parser.add_argument('--out_file', action="store", dest='out_file', required=True, help='Name of results file')


args = parser.parse_args()

#creating variables of inputted options
in_file = args.in_file
out_file = args.out_file

#Training the classifier
mixedtraining3 = pd.read_csv('mixedtrain2.csv')
del mixedtraining3['name']
X = mixedtraining3.iloc[:, 0:676].values
y = mixedtraining3['type']
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators=20, random_state=0)
classifier.fit(X, y)

#Function to run frequencies against model
def scicheck(term):
    entry = {}
    allcolumns = []
    d = []
    for char in 'abcdefghijklmnopqrstuvwxyz':
        tests = [char+b for b in 'abcdefghijklmnopqrstuvwxyz']
        allcolumns.extend(tests)
        chars = [term[i:i+2] for i in range(0, len(term))]
    allcolumns2 = allcolumns
    #print(allcolumns)
    #print(chars)
    for pair in allcolumns2:
        count = chars.count(pair)
        entry[pair] = count
        d.append(count)
    #print(d)
    y_pred = classifier.predict([d])
    saved = y_pred
    return saved[0]

#reading possible scientific names from in_file
catalogue = []
with open(in_file) as file:
    rd = csv.reader(file, delimiter="\t", quotechar='"')
    for row in rd:
        catalogue.append(row)

#joining the information together in 
catalogue2 = [''.join(x) for x in catalogue]

#iterate words through scicheck
results = []
for i in catalogue2:
    result = scicheck(i)
    input1 = (i, result)
    results.append(input1)
    
with open(out_file, "w") as rf:
    for each in results:
        rf.write(str(each) + '\n')
    
    
    
