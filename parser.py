#!/usr/bin/env python
# encoding: utf-8
from sets import Set #pacote de Set
import os #pacote para leitura do diretorio
import sys #pacote sys para exit
import enchant #verifica se uma palavra eh valida (instalado via yum)
import inflect #verifica plural 

class Parser:
    def __init__(self):
        self.separadores = [" ","/","*","%","!",".","&","(",")","+","=","{","}","[","]",":",";","?","|","\"","'","\\",",","<",">","\n","\t","\r","\f","\v"]
        self.diretorio = Diretorio()
        self.checkWord = enchant.Dict("en_US")
    def getArqs(self):
        return os.listdir(self.diretorio.messages)
class Diretorio:
    def __init__(self):
        self.raiz = "./"
        self.messages = self.raiz+"cluster-txt/messages/"
        self.common = self.raiz+"common/"
