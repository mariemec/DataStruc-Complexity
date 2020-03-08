### APP5-info
### Travail par: Marie-Eve Castonguay casm1907 et Simon Pelletier pels1201

import math
import time
import argparse
import glob
import sys
import os
from pathlib import Path
from random import randint
from random import choice
import numpy
import re

### Ajouter ici les signes de ponctuation a retirer
PONC = ["!", '"', "'", ")", "(", ",", ".", ";", ":", "?", "-", "_", "»", "«"]

#  Vous devriez inclure vos classes et methodes ici, qui seront appellees a partir du main
def mergeSort(array):
    if len(array) > 1:
        mid = len(array) // 2  # Finding the mid of the array
        L = array[:mid]  # Dividing the array elements
        R = array[mid:]  # into 2 halves

        mergeSort(L)  # Sorting the first half
        mergeSort(R)  # Sorting the second half

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i].count < R[j].count:
                array[k] = L[i]
                i += 1
            else:
                array[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            array[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            array[k] = R[j]
            j += 1
            k += 1
    return array

class TextParser:
    def __init__(self, includePonctuation = False):
        self.includePonctuation = includePonctuation

    def addWord(self, word, results):
        if (word in PONC and self.includePonctuation) or len(word)>2:
            results.append(word)

    def processLine(self, line, results):
        splitline = ""
        if self.includePonctuation:
            splitline = re.sub('([!".,!?():;_\'«»–])', r' \1 ', line)
            #splitline = re.sub('\s{2,}', ' ', line)
            splitline = splitline.split()
        else:
            splitline = re.sub('([!".,!?():;_\'«»–])', r' ', line)
            splitline = splitline.split()

        for word in splitline:
            self.addWord(word.lower(), results)

    def processFile(self, filename, results):
        tfile = open(filename, 'r')
        #print (filename)
        for line in tfile:
            self.processLine(line, results)
        tfile.close()

    def processDirectory(self, rootDirectory, results):
        for file in os.listdir(rootDirectory):
            if file != ".DS_Store": #Dossier cacher dans TextesPourEtudiants qui fait crash le programme
                self.processFile(rootDirectory + "/" + file, results)

class NgrammeNode:
    def __init__(self, ngrammeString):
        self.ngrammeString = ngrammeString
        self.nextNgrammeDict = {}
        self.count = 1

        self.nextNgrammeValues = []
        self.nextProbability = []

    def increaseCount(self):
        self.count += 1

    def printNode(self):
        print("{0} : {1} fois".format(self.ngrammeString, self.count))

    def increaseNextNodeCount(self, nextNgrammeString):
        nextNgrammeNode = self.nextNgrammeDict.get(nextNgrammeString)
        if nextNgrammeNode != None:
            nextNgrammeNode.increaseCount()

        else:
            self.nextNgrammeDict[nextNgrammeString] = NgrammeNode(nextNgrammeString)

    def calculateProbability(self):
        if len(self.nextNgrammeValues) == 0:
            self.nextNgrammeValues = list(self.nextNgrammeDict.values())  #Stocks values of nextDict in list

            total =0
            i = 0
            while ( i < len(self.nextNgrammeValues)):
                node = self.nextNgrammeValues[i]
                total = total + node.count
                i = i + 1

            i = 0
            while (i < len(self.nextNgrammeValues)):
                node = self.nextNgrammeValues[i]
                prob = node.count / total
                self.nextProbability.append(prob)
                i = i + 1

    def generateNextNgrammeString(self):            # Markov algorithm to pseudo-randomize next Ngramme
        if len(self.nextNgrammeDict.values()) == 0: #handles the case where a node doesn't have any NextNgrammeStrings
            return None

        nextNode = numpy.random.choice(self.nextNgrammeValues, 1, False, self.nextProbability) #returns an array, we only care about the [0] value
        nextString = nextNode[0].ngrammeString
        return nextString

class Statistics:
    def __init__(self, listOfWords, nsize = 1):
        self.nsize = nsize
        self.ngrammeNodeDict = {}  # dictionnary of nodes of all n-grams for given text
        self.sortedNgrammeNodeList = []
        self.generateStats(listOfWords)

    def initializeNgrammeProbabilities(self):
        for node in self.ngrammeNodeDict.values():
            node.calculateProbability()

    def generateStats(self, listOfWords): # updates dictionary for a list of words
        index = 0
        wordCount = len(listOfWords)

        currentngrammeString = ""
        previousngrammeString = ""

        while (index + self.nsize) <= wordCount:
            # build ngrammeString
            for i in range(self.nsize):
                if i == 0:
                    currentngrammeString = listOfWords[index]
                else:
                    currentngrammeString = currentngrammeString + " " + listOfWords[index + i]

            #include ngrammenode count
            ngrammeNode = self.ngrammeNodeDict.get(currentngrammeString)
            if ngrammeNode != None:
                ngrammeNode.increaseCount()
            else:
                self.ngrammeNodeDict[currentngrammeString] = NgrammeNode(currentngrammeString)

            #include ngrammenode next count
            if index > 0:
                previousNgrammeNode = self.ngrammeNodeDict.get(previousngrammeString)
                previousNgrammeNode.increaseNextNodeCount(currentngrammeString)
            previousngrammeString = currentngrammeString
            index = index + self.nsize
        self.initializeNgrammeProbabilities()

        
    def printNgrammesStat(self):
        for value in self.ngrammeNodeDict.values():
            print(value.ngrammeString)
            print(value.count)

    def calculateDistance(self, otherStat):
        #Etablir les ngrammes en commun de deux textes
        commonNgrammeKeys = list(set(self.ngrammeNodeDict.keys() & otherStat.ngrammeNodeDict.keys()))

        selfCountList = []
        totalSelfCount = 0

        otherCountList = []
        totalOtherCount = 0

        for key in commonNgrammeKeys:
            selfCount = self.ngrammeNodeDict.get(key).count
            selfCountList.append(selfCount)
            totalSelfCount = totalSelfCount + selfCount

            otherCount = otherStat.ngrammeNodeDict.get(key).count
            otherCountList.append(otherCount)
            totalOtherCount = totalOtherCount + otherCount

        index = 0
        sum = 0
        while index < len(selfCountList):
            a = selfCountList[index]/totalSelfCount
            t = otherCountList[index]/totalOtherCount
            sum = sum + ((a - t) * (a - t))
            index = index + 1
        distance = math.sqrt(sum)
        return distance

    def getNemeMostFrequentNgrammeString(self,position):
        ### Tri des Ngrammes en ordre croissant selon leur frequence (plus commun est le dernier element)
        if not self.sortedNgrammeNodeList:
            self.sortedNgrammeNodeList = list(self.ngrammeNodeDict.values())
            mergeSort(self.sortedNgrammeNodeList)
        node = self.sortedNgrammeNodeList[-position]
        return node.ngrammeString

    def generateText(self, nbwords):
        results = []
        if self.nsize == 1:
            randomChoice = randint(10, 20) #Choix du premier unigramme, assez loin pour pas que ce soit un signe de PONC

        if self.nsize == 2:
            randomChoice = randint(1,10)
        mostFrequentWord = self.getNemeMostFrequentNgrammeString(randomChoice)
        currentNgrammeString = mostFrequentWord
        results.append(currentNgrammeString)

        i = 1
        while i < nbwords:
            node = self.ngrammeNodeDict.get(currentNgrammeString)

            currentNgrammeString = node.generateNextNgrammeString()     #Appel l'algorithme de Markov (pseudo-random, selon les probabilites des prochains n-grammes)
            if currentNgrammeString is None:
                currentNgrammeString = mostFrequentWord
            results.append(currentNgrammeString)

            i = i + 1
        return results

    def generateTextFile(self, filename, nbwords, author, isMultipleAuthors):
        print("Generation en cours...")
        textWords = self.generateText(nbwords)
        tfile = open(filename, 'a')
        tfile.write(author + '\n')
        if isMultipleAuthors:
            tfile.write('\n -----DEBUT----- \n')

        for word in range(len(textWords)):
            tfile.write(textWords[word] + " ")

        if isMultipleAuthors:
            tfile.write('\n -----FIN----- \n\n')
        tfile.close()
        print("Fichier généré a éte mis à jour pour: ", author)

def unitTestGenerateStats(argsd, argsP):
    ### CREATES EMPTY LISTS TO STORE RESULTS OF PASED FILES
    zolaFile1Words = []
    zolaFile2Words = []
    zolaDirWords = []
    verneDirWords = []

    ### PARSES TEXT AND RETURNS ALL WORDS IN LIST
    textParser = TextParser(argsP, )
    textParser.processFile(argsd + "/Zola/Emile Zola - Germinal.txt", zolaFile1Words)
    print("LENGTH ZOLA FILE: ", len(zolaFile1Words))

    textParser.processFile(argsd + "/Zola/Emile Zola - Nana.txt", zolaFile2Words)
    print("LENGTH ZOLA FILE: ", len(zolaFile2Words))

    ### PARSES ALL FILES IN DIRECTORY AND RETURNS ALL WORDS IN LIST
    textParser.processDirectory(argsd + "/Zola", zolaDirWords)
    textParser.processDirectory(argsd + "/Verne", verneDirWords)

    ### CREATES STATISTICS FOR PARSED TEXT FILE
    zolaFile1Stats = Statistics(zolaFile1Words)
    zolaFile2Stats = Statistics(zolaFile2Words)
    zolaStats = Statistics(zolaDirWords)
    verneStats = Statistics(verneDirWords)

    # zolaFile1Stats.calculateDistance(zolaFile2Stats)
    # #print(len(zolaFile1Stats.ngrammeNodeDict.keys()))
    #
    # zolaFile2Stats.calculateDistance(zolaFile1Stats)
    # #print(len(zolaFile2Stats.ngrammeNodeDict.keys()))

    ### CALCULATES DISTANCE BETWEEN TWO TEXTS
    zolaFile1Stats.calculateDistance(zolaStats)
    zolaFile1Stats.calculateDistance(verneStats)
def unitTestMergeSort():
    dict = {}
    dict["key1"] = NgrammeNode("key1")
    dict["key1"].increaseCount()
    dict["key1"].increaseCount()
    dict["key1"].increaseCount()
    dict["key1"].increaseCount()
    dict["key2"] = NgrammeNode("key2")
    dict["key2"].increaseCount()
    dict["key2"].increaseCount()
    dict["key3"] = NgrammeNode("key3")
    dict["key3"].increaseCount()
    dict["key3"].increaseCount()
    dict["key3"].increaseCount()
    dict["key4"] = NgrammeNode("key4")
    dict["key4"].increaseCount()
    dict["key5"] = NgrammeNode("key5")
    dict["key5"].increaseCount()
    dict["key5"].increaseCount()
    dict["key5"].increaseCount()
    dict["key5"].increaseCount()
    dict["key5"].increaseCount()

    v = list(dict.values())
    for node in v:
        node.printNode()

    mergeSort(v)

    print(v)
    for node in v:
        node.printNode()
def unitTestFrequency():
    zolaFile1Words = []
    textParser = TextParser(args.P, )
    textParser.processFile(args.d + "/Zola/Emile Zola - Germinal.txt", zolaFile1Words)

    print("LENGTH ZOLA FILE: ", len(zolaFile1Words))
    zolaFile1Stats = Statistics(zolaFile1Words,2)
    for i in range(50,100):
        print(zolaFile1Stats.getNemeMostFrequentNgrammeString(i))
def unitTestMarkov():
    line = "a a b a b a a b c"
    decomposedLine = []
    decomposedDir = []
    textParser = TextParser(False)

    # textParser.processLine(line, decomposedLine)
    # lineStats = Statistics(decomposedLine, 2)
    # lineStats.generateText(30)

    textParser.processDirectory("./TextesPourEtudiants/Zola", decomposedDir)
    zolaStats = Statistics(decomposedDir, 2)
    zolaStats.generateText(50)
def unitTestLineParse():
    line = "Allo! Je pense que, peut-etre, ce n'est pas si mal( que ca."
    results = []
    textParser = TextParser()
    textParser.processLine(line,results)
    print(results)

### Main: lecture des parametres et appel des methodes appropriees
###
###       argparse permet de lire les parametres sur la ligne de commande
###             Certains parametres sont obligatoires ("required=True")
###             Ces parametres doivent etres fournis a python lorsque l'application est execu
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='markov_casm1907_pels1201.py')
    parser.add_argument('-d', required=True, help='Repertoire contenant les sous-repertoires des auteurs')
    parser.add_argument('-a', help='Auteur a traiter')
    parser.add_argument('-f', help='Fichier inconnu a comparer')
    parser.add_argument('-m', required=True, type=int, choices=range(1, 3),
                        help='Mode (1 ou 2) - unigrammes ou digrammes')
    parser.add_argument('-F', type=int, help='Indication du rang (en frequence) du mot (ou bigramme) a imprimer')
    parser.add_argument('-G', type=int, help='Taille du texte a generer')
    parser.add_argument('-g', help='Nom de base du fichier de texte a generer')
    parser.add_argument('-v', action='store_true', help='Mode verbose')
    parser.add_argument('-P', action='store_true', help='Retirer la ponctuation')
    parser.add_argument('-A', action='store_true', help = 'Tous les auteurs sont a traiter')
    args = parser.parse_args()

    ### Lecture du repertoire des auteurs, obtenir la liste des auteurs
    ### Note:  args.d est obligatoire
    ### auteurs devrait comprendre la liste des repertoires d'auteurs, peu importe le systeme d'exploitation
    cwd = os.getcwd()
    if os.path.isabs(args.d):
        rep_aut = args.d
    else:
        rep_aut = os.path.join(cwd, args.d)

    rep_aut = os.path.normpath(rep_aut)
    authors = os.listdir(rep_aut)


    ### Enlever les signes de ponctuation (ou non) - Definis dans la liste PONC
    if args.P:
        remove_ponc = True
    else:
        remove_ponc = False

    ### Si mode verbose, refleter les valeurs des parametres passes sur la ligne de commande
    if args.v:
        print("Mode verbose:")
        print("Calcul avec les auteurs du repertoire: " + args.d)
        if args.f:
            print("Fichier inconnu a,"
                  " etudier: " + args.f)

        print("Calcul avec des " + str(args.m) + "-grammes")
        if args.F:
            print(str(args.F) + "e mot (ou digramme) le plus frequent sera calcule")

        if args.a:
            print("Auteur etudie: " + args.a)

        if args.P:
            print("Retirer les signes de ponctuation suivants: {0}".format(" ".join(str(i) for i in PONC)))

        if args.G:
            print("Generation d'un texte de " + str(args.G) + " mots")

        if args.g:
            print("Nom de base du fichier de texte genere: " + args.g)

        print("Repertoire des auteurs: " + rep_aut)
        print("Liste des auteurs: ")
        for a in authors:
            aut = a.split("/")
            print("    " + aut[-1])

## A partir d'ici, vous devriez inclure les appels a votre code

    start = time.time()

    if args.A and args.a:
        print("SVP ajuster votre ligne de commande avec -a (auteur specifique) OU -A (tous les auteurs)")
    if args.A: # traite tous les auteurs du repertoire
        print("Estimated runtime: 40 seconds..")
        for a in authors:
            if a != ".DS_Store":
                authorWords = []
                textParser = TextParser(args.P)
                textParser.processDirectory(args.d + "/"+ a, authorWords)
                authorStats = Statistics(authorWords, args.m)
                if args.F != None:
                    ngrammeString = authorStats.getNemeMostFrequentNgrammeString(args.F)
                    print("Le %d ieme %d-gramme le plus commun pour %s est:" %(args.F,args.m,a), ngrammeString)

                if args.f != None:
                    monFichierWords = []
                    textParser.processFile(args.f,monFichierWords)
                    monFichierStats = Statistics(monFichierWords, args.m)
                    print("Distance du fichier avec " + a + " : %0.3f" % monFichierStats.calculateDistance(authorStats))

                if args.G is not None and args.g is not None:
                    authorStats.generateTextFile(args.g, args.G, a, True)


    if args.a: # traite un auteur specifique du repertoire
        authorWords = []
        textParser = TextParser(args.P)
        textParser.processDirectory(args.d + "/" + args.a, authorWords)
        authorStats = Statistics(authorWords,args.m)
        if args.F is not None:
            print("Estimated runtime: 5 seconds..")
            ngrammeString = authorStats.getNemeMostFrequentNgrammeString(args.F)
            print("Le %d ieme %d-gramme le plus commun pour %s est:" % (args.F, args.m, args.a), ngrammeString)

        if args.f is not None:
            print("Estimated runtime: 5 seconds..")
            monFichierWords = []
            textParser.processFile(args.f, monFichierWords)
            monFichierStats = Statistics(monFichierWords, args.m)
            print("Distance avec " + args.a + " : %0.3f" % monFichierStats.calculateDistance(authorStats))

        if args.G is not None and args.g is not None:
            print("Estimated runtime: 6 seconds..")
            authorStats.generateTextFile(args.g, args.G, args.a, False)


    end = time.time()
    print("Runtime: ", end-start)