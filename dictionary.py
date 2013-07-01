#!/usr/bin/env python
# encoding: utf-8
from sets import Set #pacote de Set
import os #pacote para leitura do diretorio
import sys #pacote sys para exit
import enchant #verifica se uma palavra eh valida (instalado via yum)
import inflect #verifica plural 
from parser import Parser,Diretorio

class Dictionary:
    def __init__(self):
        self.dictionary = list([])#dicionario
        self.predictionary = list([])#pre-dicionario
        self.length = 100 #tamanho do dicionario
        self.parser = Parser()
        self.file = self.parser.diretorio.common+"dictionary"
        self.totalPalavras=0
        self.arquivos = self.parser.getArqs()
    def write(self):
         arq = open(self.file,"w")#abrindo documento
         for d in self.dictionary:
             arq.write(d[0]+"\n")
    def load(self):
        try:
            with open(self.file,"r"): pass
        except IOError:
            print "Arquivo"+self.file+" nao encontrador. Gerando arquivo!"
            self.start()
        arq = open(self.file,"r")
        texto = arq.read()
        word = ""
        for c in texto:
            if c in self.parser.separadores and word and not word.isdigit():#o caracter eh um separador de palavras? 
                self.dictionary.append(word)
                word = ""
            else:
                word += c
    #constroi o dicionario de acordo com a probabilidade de selecionar uma palavra e esta estar
    # no maior numero de arquivos possiveis
    def build(self):
        s = self.predictionary
        tam = 0
        for i in s:
            p_palavra = float(i[1]) / float(self.totalPalavras) #proporcao de ocorrencia da palavra pelo total de palavras
            p_arq = float(i[2]) / float(len(self.arquivos)) #proporcao de qntos arquivo ocorre a palavra pelo total de arquivos
            ppa = float(p_palavra * p_arq) #Prob de selecionar uma Palavra e esta estar em um determinado Arquivo
#      ppa = 0
            if tam > self.length:
                if ppa > 0.0:
                    min = self.getMin(1)#busca pelo menor ppa
                    if min >= 0 and self.dictionary[min][1] < ppa:
                        self.dictionary[min][0] =i[0]
                        self.dictionary[min][1] = ppa
                        self.dictionary[min][2] = i[1]
                        self.dictionary[min][3] = i[2]
                    else:
                        min = findMinDic(dictionary,2)#busca pelo menor num de ocorrencia
                        if min >= 0 and dictionary[min][2] < i[1]:
                            self.dictionary[min][0] =i[0]
                            self.dictionary[min][1] = ppa
                            self.dictionary[min][2] = i[1]
                            self.dictionary[min][3] = i[2]
                        else:
                            self.dictionary.append([i[0],ppa,i[1],i[2]])
                            self.dictionary.sort(key=lambda x: x[1])
                            tam += 1
                            self.dictionary.sort(key=lambda x: x[1])
            self.write()
    def getMin(self,ind):#retorna a posicao do elemento de menor ind do dicionario
        min = -1
        pos = -1
        for i in range(0,len(self.dictionary)):
            if self.dictionary[i][ind] < min or min == -1:
                min = self.dictionary[i][ind]
                pos = i
        return pos
    def updatePre(self,w,ida):#w = palavra , ida = nome do arquivo
        s = self.predictionary
        if not s:
            s.append([w,2,1,ida])#segunda ocorrencia
            s.sort(key=lambda x: x[0]) #sort pela primeira coluna (palavras)
            return 0
#        if w < s[0][0]:
#            s.append([w,2,1,ida])#segunda ocorrencia
#            s.sort(key=lambda x: x[0]) #sort pela primeira coluna (palavras)
#            return 0
        ini, modified, fim = 0, 0, len(s)
        while ini <= fim:
            m = (ini + fim) / 2
            if m >= len(s):
                s.append([w,2,1,ida])#segunda ocorrencia
                s.sort(key=lambda x: x[0]) #sort pela primeira coluna (palavras)
                return 0
            if w == s[m][0]:
                modified = 1
                s[m][1] += 1
                if ida != s[m][3]:
                    s[m][2] += 1
                    return 0
            elif w < s[m][0]:
                fim = m - 1
            else:
                ini = m + 1
        if modified == 0:
            s.append([w,2,1,ida])#segunda ocorrencia
            s.sort(key=lambda x: x[0]) #sort pela primeira coluna (palavras)
        return 0
    def start(self):
        print "Start Dictionary"
        col_words = Set([]) #colecao de palavras UNICAS
        for f in self.arquivos:
            arq = open(self.parser.diretorio.messages+f,"r")#abrindo documento
            texto = arq.read()#lendo texto do documento
            word = ""#palavra
            for c in texto:#lendo caracter por caracter no texto
                if c in self.parser.separadores:#o caracter eh um separador de palavras?
                    if word: #palavra nao pode ser vazia
                        if not word.isdigit():#consideramos alfanumericos e removemos apenas numeros                             word = word.lower()#normalizando
                            word = word.decode('iso-8859-1').encode('utf8')#alguns caracteres invalios para utf8
                            if len(word) > 3 and self.parser.checkWord.check(word):#consideramos apeas palavras com mais de 3 digitos
                                self.totalPalavras += 1
                                if word in col_words:
                                    self.updatePre(word,f)
                                else:
                                    col_words.add(word) #colecao de palavras
                                    word = ""
                            else:
                                word = word + c
        self.build()
    
