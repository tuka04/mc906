#!/usr/bin/env python
# encoding: utf-8
# clusterizacao das mensagens utilizando k-means
from pylab import plot,show #plot em grafico
from numpy import vstack,array#array 
from numpy.random import rand#randomico
from scipy.cluster.vq import kmeans,vq #kmeans

def RunK_Means(d):
    centroids = kmeans(d,2)
    idx = vq(d,centroids)
    for i in idx:
        print i
