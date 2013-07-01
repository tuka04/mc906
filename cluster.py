#!/usr/bin/env python
# encoding: utf-8
# clusterizacao das mensagens utilizando k-means
from pylab import plot,show #plot em grafico
from numpy import vstack,array#array 
from numpy.random import rand#randomico
from scipy.cluster.vq import kmeans,vq,whiten #kmeans
from sklearn import metrics
from sklearn import cluster, datasets
#clusterizacao utilizando k-means
class Cluster:
    def __init__(self,s,k):#s sao as seeds para o algoritmo, k o num de clusters
        self.centro = list([])
        self.sens = 0.0#sensibilidade
        self.seeds = s
        self.resp = list(list([]))
        self.matrix = list(list([]))
        self.k=k
    def perform(self):
        print "Start KMeans"
        data = whiten(self.seeds)#normalizando os dados
        self.centro,self.sens = kmeans(data,self.k)
        self.matrix,_ = vq(data,self.centro)
        self.resp = self.centro[self.matrix]
        print "Sensibilidade: "+str(self.sens)
        
