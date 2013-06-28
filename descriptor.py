#constroi o vetor descritor por mensagem
import enchant #verifica se uma palavra eh valida (instalado via yum)
import inflect #instalado via easy_install
import numpy
separadores = [" ","/","*","%","!",".","&","(",")","+","=","{","}","[","]",":",";","?","|","\"","'","\\",",","<",">","\n","\t","\r","\f","\v"]
checkWord = enchant.Dict("en_US")
class Descriptor:
    def __init__(self,d,a):#dicionario,arquivos
        self.dictionary=d
        self.archives=a
        #iniciando matriz com zeros
        self.descriptor = numpy.zeros(shape=(len(a),len(d))) #matriz len(a) X len(d)
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
    def load(self,diretorio):
        print "****** LOAD DESCRIPTOR ******"
        for i in range(0,len(self.archives)):
            if i % 1000 == 0:
                self.printProcTimePast(len(self.archives),i)
            arq = open(diretorio+self.archives[i],"r")#abrindo documento
            texto = arq.read()#lendo texto do documento
            word = ""#palavra
            for c in texto:#lendo caracter por caracter no texto
                if c in separadores: 
                    if word:
                        if not word.isdigit():#o caracter eh um separador de palavras? 
                            word = word.lower()#normalizando
                            word = word.decode('iso-8859-1').encode('utf8')#alguns caracteres invalidos para utf8
                            if len(word) > 3 and checkWord.check(word):#consideramos apenas palavras com mais de 3 digitos 
                                iw = self.getIndiceWord(word)
 #                               print str(i)+" "+str(iw)
                                if iw >= 0:
                                    self.descriptor[i][iw] += 1
                    word = ""
                else:
                    word = word + c
    def getDesc(self):
        print self.descriptor
        return self.descriptor

