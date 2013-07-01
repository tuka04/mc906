#!/usr/bin/env python
# encoding: utf-8
# classificacao das mensagens utilizando svm (support vector machines)
from sklearn import svm,metrics #suport vector machine
from sklearn.feature_extraction.text import HashingVectorizer
from numpy import *
class Classifier:
    def __init__(self,d,tr,te):
        self.training = tr
        self.test = te
        self.data = d
        self.prediction = list([])
    def perform(self):
        s = svm.SVC()#support vector classifier
        s.fit(self.data,self.training)
        self.prediction = s.predict(self.data)
        pred = map(tuple,self.prediction)
        print self.prediction
        print "Matriz de confusao"
        mc = metrics.confusion_matrix(self.test, pred)
        print mc
        desc = str(s).split('(')[0]
