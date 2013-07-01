#!/usr/bin/env python
# encoding: utf-8
from os import sys
from dictionary import Dictionary
from descriptor import Descriptor
from cluster import Cluster
from classifier import Classifier

dic = Dictionary()
if len(sys.argv) < 2:#nao ha argumentos
    dic.start()
dic.load()
desc = Descriptor(dic.dictionary)
desc.load() 
cluster = Cluster(desc.getDesc(),20)
cluster.perform()
train = list([])
test  = list([])
for i in range(0,(len(cluster.resp)*20/100)):
    test.append(cluster.resp[i])
for i in cluster.matrix:
    train.append(i)
classifier = Classifier(desc.getDesc(),train,test)
classifier.perform()
