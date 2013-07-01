#constroi o vetor descritor por mensagem
import enchant #verifica se uma palavra eh valida (instalado via yum)
import inflect #instalado via easy_install
import numpy
from parser import Parser,Diretorio
class Descriptor:
    def __init__(self,d):#dicionario,arquivos
        self.parser = Parser()
        self.arqSpacer = "|"
        self.arqSaver = "descriptor"
        self.dictionary=d
        self.archives=self.parser.getArqs()
        #iniciando matriz com zeros
        self.descriptor = numpy.zeros(shape=(len(self.archives),len(d))) #matriz len(a) X len(d)
    def printProcTimePast(self,total,past):
        p = past*100/total
        pontos = ""
        for x in xrange(p):
            pontos += "."
        print pontos+" "+str(past*100/total)+"%"
    def getIndiceWord(self,w):#retorna o indice da palavra no dicionario
        for i in range(0,len(self.dictionary)):
            if self.dictionary[i]==w:
                return i
        return -1
    def write(self):#escreve o descritor em um arquivo
        arq = open("./common/"+self.arqSaver,"w")
        for i in self.descriptor:
            for j in i:
                arq.write(str(j)+self.arqSpacer)
            arq.write("\n")
    def loadFromArq(self):
        try:
            with open("./common/"+self.arqSaver,"r"): pass
        except IOError:
            print "Arquivo"+"./common/"+self.arqSaver+" nao encontrador. Gerando arquivo!"
            return 0
        arq = open("./common/"+self.arqSaver,"r")
        t = arq.read()
        word = ""
        i=0
        j=0
        for c in t:
            if c == self.arqSpacer:
                self.descriptor[i][j]=float(word)
                j+=1
                word = ""
            elif c =="\n":
                i+=1
                j=0
            else:
                word += c
        return 1
    def load(self):
        if self.loadFromArq() == 1:
            return 
        print "****** LOAD DESCRIPTOR ******"
        for i in range(0,len(self.archives)):
            if i % 1000 == 0:
                self.printProcTimePast(len(self.archives),i)
            arq = open(self.parser.diretorio.messages+self.archives[i],"r")#abrindo documento
            texto = arq.read()#lendo texto do documento
            word = ""#palavra
            for c in texto:#lendo caracter por caracter no texto
                if c in self.parser.separadores: 
                    if word:
                        if not word.isdigit():#o caracter eh um separador de palavras? 
                            word = word.lower()#normalizando
                            word = word.decode('iso-8859-1').encode('utf8')#alguns caracteres invalidos para utf8
                            if len(word) > 3 and self.parser.checkWord.check(word):#consideramos apenas palavras com mais de 3 digitos 
                                iw = self.getIndiceWord(word)
 #                               print str(i)+" "+str(iw)
                                if iw >= 0:
                                    self.descriptor[i][iw] += 1
                    word = ""
                else:
                    word = word + c
        self.write()
    def getDesc(self):
        print self.descriptor
        return self.descriptor

