def unitTestGenerateStats():
    ### CREATES EMPTY LISTS TO STORE RESULTS OF PASED FILES
    zolaFile1Words = []
    zolaFile2Words = []
    zolaDirWords = []
    verneDirWords = []

    textParser = TextParser(False)

    # ### PARSES ALL FILES IN DIRECTORY AND RETURNS ALL WORDS IN LIST
    # textParser.processDirectory("./TextesPourEtudiants/Zola", zolaDirWords)
    # textParser.processDirectory("./TextesPourEtudiants/Verne", verneDirWords)
    #
    # ### CREATES STATISTICS FOR PARSED TEXT FILE
    # zolaFile1Stats = Statistics(zolaFile1Words)
    # zolaFile2Stats = Statistics(zolaFile2Words)
    # zolaStats = Statistics(zolaDirWords)
    # verneStats = Statistics(verneDirWords)
    #
    # # zolaFile1Stats.calculateDistance(zolaFile2Stats)
    # # #print(len(zolaFile1Stats.ngrammeNodeDict.keys()))
    # #
    # # zolaFile2Stats.calculateDistance(zolaFile1Stats)
    # # #print(len(zolaFile2Stats.ngrammeNodeDict.keys()))
    #
    # ### CALCULATES DISTANCE BETWEEN TWO TEXTS
    # zolaFile1Stats.calculateDistance(zolaStats)
    # zolaFile1Stats.calculateDistance(verneStats)

    line = "The world is, sometimes;kinda cool ish... maybe... world"
    results = []
    textParser = TextParser(False)
    textParser.processLine(line, results)
    lineStats = Statistics(results, 1)
    #lineStats.printNgrammesStat()
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
def unitTestSort():
    line = "Les chiens les chats, laa mer et laa laa femme."
    results = []
    textParser = TextParser(False)
    textParser.processLine(line, results)
    textStats = Statistics(results, 1)
    print(textStats.getNgrammeAtPosition(1))
def unitTestFrequency():
    zolaFile1Words = []
    textParser = TextParser(args.P, )
    textParser.processFile(args.d + "/Zola/Emile Zola - Germinal.txt", zolaFile1Words)

    print("LENGTH ZOLA FILE: ", len(zolaFile1Words))
    zolaFile1Stats = Statistics(zolaFile1Words,2)
    for i in range(50,100):
        print(zolaFile1Stats.getNgrammeAtPosition(i))
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