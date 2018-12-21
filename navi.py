import matplotlib.pyplot as plt

def getData ():
    baseDir = "sentiment/"
    data = []
    with open(baseDir + "imdb_labelled.txt", "r", encoding='utf-8') as arq:
        data = arq.read().split("\n")

    with open(baseDir + "yelp_labelled.txt", "r", encoding='utf-8') as arq:
        data += arq.read().split("\n")

    with open(baseDir + "amazon_cells_labelled.txt", "r", encoding='utf-8') as arq:
        data += arq.read().split("\n")

    return data

def dataTratament (data):
    newData = []
    for d in data:
        if len(d.split("\t")) == 2 and d.split("\t")[1] != "":
            newData.append(d.split("\t"))

    return newData

def selectDatas (data):
    lendata = len(data)
    trainingPercentage = 1
    training = []
    validation = []

    for index in range(0, lendata):
        if index < lendata * trainingPercentage:
            training.append(data[index])
        else:
            validation.append(data[index])

    return training, validation

def preProcessing ():
    data = getData()
    data = dataTratament(data)

    return selectDatas(data)

def training (trainingData):
    trainingComments = [registro_treino[0] for registro_treino in trainingData]
    trainingValues = [registro_treino[1] for registro_treino in trainingData]

    return frequencia(trainingComments, trainingValues)

def chr_remove(old, to_remove):
    new_string = old
    for x in to_remove:
        new_string = new_string.replace(x, '')
    return new_string

def frequencia (data = [], values = []):
    freq = {}

    for index, frase in enumerate(data):
        for palavra in frase.split(" "):
            #p = palavra
            p = str(palavra).lower()
            p = chr_remove(p, ".!,'()?" + '"')

            if p in list(freq.keys()):
                if(values[index] == '0'):
                    freq[p]["freq"] += 1
                    freq[p]["neg"] += 1
                if(values[index] == '1'):
                    freq[p]["freq"] += 1
                    freq[p]["pos"] += 1
            else:
                if(values[index] == '0'):
                    freq[p] = {"freq" : 1, "pos" : 0, "neg" : 1}
                if(values[index] == '1'):
                    freq[p] = {"freq" : 1, "pos" : 1, "neg" : 0}
    freq.pop('')
    for palavra in freq.keys():
        freq[palavra]["pos"] = freq[palavra]["pos"] / float(freq[palavra]["freq"])
        freq[palavra]["neg"] = 1.0 - freq[palavra]["pos"]

    return freq

def navie (freq: dict(), string:str):
    pos = 1
    neg = 1
    for palavra in string.split(" "):
        p = palavra.lower()
        if(p in freq):
            #print("{} : pos {}; neg {}".format(p, freq[p]["pos"], freq[p]["neg"]))
            pos *= freq[p]["pos"]
            neg *= freq[p]["neg"]
    
    #print("{} : {}".format(pos, neg))
    if pos > neg:
        return 1
    else:
        return 0

f = training(preProcessing()[0])

data = dataTratament(getData())


names = ["Acertos", "Erros"]
values = [0, 0]

for elem in data:
    if(navie(f, elem[0]) == int(elem[1])):
        values[0] += 1
    else:
        values[1] += 1

plt.bar(names, values)
plt.show()