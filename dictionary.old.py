#!/usr/bin/env python
# encoding: utf-8
from sets import Set #pacote de Set
import os #pacote para leitura do diretorio
import sys #pacote sys para exit
import enchant #verifica se uma palavra eh valida (instalado via yum)
import inflect #instalado via easy_install
import numpy
from numpy import vstack,array
from numpy.random import rand
from pylab import plot,show
from descriptor import Descriptor
import pylab
from scipy.cluster.vq import kmeans,vq,whiten
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('Agg')

from sklearn import svm #suport vector machine
#from svm import *
#print "Entre com o diretorio dos documentos"
#Diretorio = raw_input()
col_words = Set([]) #colecao de palavras UNICAS 
col_dictionary = list([]) #colecao do dicionario, onde cada no contem [palavra,n_ocorrencias,n_ocorrencia_arquivo]
dictionary = list([]) #dicionario
NUM_WORDS_DICTIONARY = 100
#incrementa o numero de ocorrencia, e se ainda nao foi incrementado, incrementamos as ocorrencia de arquivos
#faz um busca binaria
#decisao de nao mantae palavras com a contagem 1 no col_dictionary
def UpdateDictionary(s,w,name_arq):
   if not s:
       s.append([w,2,1,name_arq])#segunda ocorrencia
       s.sort(key=lambda x: x[0]) #sort pela primeira coluna (palavras)
       return 0
   if w < s[0][0]:
       s.append([w,2,1,name_arq])#segunda ocorrencia
       s.sort(key=lambda x: x[0]) #sort pela primeira coluna (palavras)
       return 0
   ini, modified, fim = 0, 0, len(s)
   while ini <= fim:
       m = (ini + fim) / 2
       if m >= len(s):
           s.append([w,2,1,name_arq])#segunda ocorrencia
           s.sort(key=lambda x: x[0]) #sort pela primeira coluna (palavras)
           return 0
       if w == s[m][0]:
           modified = 1
           s[m][1] += 1
           if name_arq != s[m][3]:
               s[m][2] += 1
           return 0
       elif w < s[m][0]:
           fim = m - 1
       else:
           ini = m + 1
   if modified == 0:
       s.append([w,2,1,name_arq])#segunda ocorrencia
       s.sort(key=lambda x: x[0]) #sort pela primeira coluna (palavras)
   return 0

def WriteDictionary():
    file = "dictionary"
    arq = open("./common/"+file,"w")#abrindo documento
    for d in dictionary:
        arq.write(d[0]+"\n")

def findMinDic(d,ind):
   min = -1
   pos = -1
   for i in range(0,len(d)):
      if d[i][ind] < min or min == -1:
         min = d[i][ind]
         pos = i
   return pos
      

def LoadDictionary():
   print "***** LOAD DICTIONARY *****"
   arq = open(diretorioRaiz+"dictionary","r")
   texto = arq.read()
   word = ""
   for c in texto:
      if c in separadores and word and not word.isdigit():#o caracter eh um separador de palavras? 
         dictionary.append(word)
         word = ""
      else:
         word += c

def BuildDictionary(s):
   tam = 0
   for i in s:
      p_palavra = float(i[1]) / float(totalPalavras) #proporcao de ocorrencia da palavra pelo total de palavras
      p_arq = float(i[2]) / float(len(arquivos)) #proporcao de qntos arquivo ocorre a palavra pelo total de arquivos
      ppa = float(p_palavra * p_arq) #Prob de selecionar uma Palavra e esta estar em um determinado Arquivo
#      ppa = 0
      if tam > NUM_WORDS_DICTIONARY:
         if ppa > 0.0:
            min = findMinDic(dictionary,1)#busca pelo menor ppa
            if min >= 0 and dictionary[min][1] < ppa:
               dictionary[min][0] =i[0]
               dictionary[min][1] = ppa
               dictionary[min][2] = i[1]
               dictionary[min][3] = i[2]
         else:
            min = findMinDic(dictionary,2)#busca pelo menor num de ocorrencia
            if min >= 0 and dictionary[min][2] < i[1]:
               dictionary[min][0] =i[0]
               dictionary[min][1] = ppa
               dictionary[min][2] = i[1]
               dictionary[min][3] = i[2]
      else:
         dictionary.append([i[0],ppa,i[1],i[2]])
         dictionary.sort(key=lambda x: x[1])
         tam += 1
   dictionary.sort(key=lambda x: x[1])
   WriteDictionary()
    
contador = 0
totalPalavras = 0
if len(sys.argv) < 2:
   for f in arquivos:
      contador += 1
      print contador
      arq = open(diretorio+f,"r")#abrindo documento
      texto = arq.read()#lendo texto do documento
      word = ""#palavra
      for c in texto:#lendo caracter por caracter no texto
         if c in separadores:#o caracter eh um separador de palavras?
            if word: #palavra nao pode ser vazia
               if not word.isdigit():#consideramos alfanumericos e removemos apenas numeros
                  word = word.lower()#normalizando
                  word = word.decode('iso-8859-1').encode('utf8')#alguns caracteres invalidos para utf8
                  if len(word) > 3 and checkWord.check(word):#consideramos apenas palavras com mais de 3 digitos
                     totalPalavras += 1
                     if word in col_words:
                        UpdateDictionary(col_dictionary,word,f)
                     else:
                        col_words.add(word) #colecao de palavras
                     word = ""
         else:
            word = word + c
      #print col_dictionary
      BuildDictionary(col_dictionary)
else:
   LoadDictionary()
   desc = Descriptor(dictionary,arquivos)
   desc.load(diretorio)
   data = desc.getDesc()
   ndata = whiten(data)#data normalizada
#   data = []4
#   for i in range(0,len(arquivos)):
#      data = numpy.concatenate((data,predata[i]));
   #centro sao os k clusters
   centro,dist = kmeans(ndata,20)#
   code,_ = vq(ndata,centro)
   res = centro[code] #matriz de pertinencia
   c = list([])
   for i in code:
      c.append(i)
#   print centro
   for i in range(0,len(centro)):
      min = -1
      for j in range(0,len(centro[i])):
         if min < 0:
            min = centro[i][j]
         elif centro[i][j] < min:
            min = centro[i][j]
            idword = j
      print "Grupo"+str(i)+" Palavra: "+dictionary[idword]
   clf = svm.SVC()
   aux = list([])
   for i in range(0,len(c)):
      aux.append(1)
   clf.fit(data,c)
   z = list([])
   for i in data:
      z.append(clf.predict(i))
   print z
#   print p
#   print c
#   print len(code)
#   print res
#   colors = ([([0.4,1,0.4],[1,0.4,0.4],[0.1,0.8,1])[i] for i in idx])
#   plot(data[code==0,0],data[code==0,1],'ob',
#        data[code==1,0],data[code==1,1],'or',
#        data[code==2,0],data[code==2,1],'og')
#   plot(centro[:,0],centro[:,1],'sg',markersize=8)
#   show()



