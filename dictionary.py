#!/usr/bin/env python
# encoding: utf-8
from sets import Set
import os #pacote para leitura do diretorio
import sys #pacote sys para exit
diretorio = "/home/leandro/unicamp/mc906/cluster-txt/messages/"#diretorio das mensagens
#print "Entre com o diretorio dos documentos"
#Diretorio = raw_input()
arquivos = os.listdir(diretorio)#listando arquivos
separadores = [" ","/","*","%","!",".","&","(",")","+","=","{","}","[","]",":",";","?","|","\"","'","\\",",","<",">","\n","\t","\r","\f","\v"]
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
    
contador = 0
totalPalavras = 0
for f in arquivos:
    contador += 1
    print contador
    arq = open(diretorio+f,"r")#abrindo documento
    texto = arq.read()#lendo texto do documento
    word = ""#palavra
    node = [] #no que contem [palavra,n_ocorrencias,n_ocorrencia_arquivo]
    for c in texto:#lendo caracter por caracter no texto
        if c in separadores:#o caracter eh um separador de palavras?
            if word: #palavra nao pode ser vazia
                if not word.isdigit():#consideramos alfanumericos e removemos apenas numeros
                    word = word.lower()
                    if len(word) > 3:#consideramos apenas palavras com mais de 3 digitos
                        totalPalavras =+ 1
                        if word in col_words:
                            UpdateDictionary(col_dictionary,word,f)
                        else:
                            col_words.add(word) #colecao de palavras
            word = ""
        else:
            word = word + c
BuldDictionary(col_dictionary)

def BuildDictionary(s):
    for i in s:
        p_palavra = s[i][1] / total_palavras #proporcao de ocorrencia da palavra pelo total de palavras
        p_arq = s[i][2] / len(arquivos) #proporcao de qntos arquivo ocorre a palavra pelo total de arquivos
        ppa = p_palavra * p_arq #Prob de selecionar uma Palavra e esta estar em um determinado Arquivo
        tam = len(dictionary)
        if tam > NUM_WORDS_DICTIONARY:
            if ppa > dictionary[tam-1][1]:
                dictionary[tam-1][0] = s[i][0]
                dictionary[tam-1][1] = ppa
        else:
            dictionary.appen([s[i][0],ppa])
        dictionary.sort(key=lambda x: x[1]) #sort por ppa
    WriteDictionary()

def WriteDictionary():
    file = "dictionary"
    arq = open("./"+f,"w")#abrindo documento
    for i in len(dictionary):
        arq.write(dictionary[i][0])
        




