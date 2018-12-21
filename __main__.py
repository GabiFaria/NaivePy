#Python >= Python3.5

import twitter
import matplotlib.pyplot as plt
import lexico


def get_Data():
    sentilex = open('SentiLex-PT02/SentiLex-flex-PT02.txt', 'r', encoding='utf-8')
    dataset = sentilex.read()
    dataset = dataset.split("\n")

    dataset = [data.split('.') for data in dataset]

    date = {}
    for ds in dataset:

        info = ds[1]
        palavras = ds[0].split(',')
        palavra1 = palavras[0].lower()
        palavra2 = palavras[1].lower()

        info = info.split(';')
        info = [a.split('=') for a in info]

        for arg in info:
            if arg[0] == 'POL:N0':
                date[palavra1] = int(arg[1])
                date[palavra2] = int(arg[1])

            elif arg[0] == 'POL:N1':
                if(palavra1 in date.keys()):
                    date[palavra1] = 0
                else:
                    date[palavra1] = int(arg[1])
                
                if(palavra2 in date.keys()):
                    date[palavra2] = 0
                else:
                    date[palavra2] = int(arg[1])
    return date

def chr_remove(old, to_remove):
    new_string = old
    for x in to_remove:
        new_string = new_string.replace(x, '')
    return new_string

def navie (freq: dict(), string:str):
    pos = 0
    neg = 0
    contPalavra = 0

    avaliados = 0

    for palavra in string.split(" "):
        p = palavra.lower()
        p = chr_remove(p, ".*@#$%¨&-+§!,'()?" + '"')
        contPalavra +=1
        if(p in freq.keys()):
            avaliados += 1
            if freq[p] > 0:
                pos += 1
                
            elif freq[p] < 0:
                neg += 1

    if(pos == 0 and neg == 0):
        return None, avaliados

    pos = pos/contPalavra
    neg = neg/contPalavra


    if pos > neg:
        return 1, avaliados
    else:
        return 0, avaliados

data = lexico.get_lexico()

val = [0, 0, 0]

termo = input('Qual termo deseja pesquisar? ')

aval = 0

for termos in twitter.twitters(termo):
    result, avaliados = navie(data, termos.text)
    aval += avaliados
    if result == 1:
        val[0] += 1
    if result == 0:
        val[1] += 1
    if result == None:
        val[2] += 1

fig, ax = plt.subplots()

ax.set_xlabel('Twitters Classificados: {}/100\nPalavras avaliadas: {}'. format(val[0]+val[1], aval))
val = [(val[0]/sum(val))*100, (val[1]/sum(val))*100, (val[2]/sum(val))*100]
names = ['Positivos : {0:.2f}%'.format(val[0]), 'Negativos : {0:.2f}%'.format(val[1]), 'Neutros ou Inconclusivos : {0:.2f}%'.format(val[2])]

ax.bar(names, val)
ax.set_ylabel('(%)')
ax.set_title('Análise de sentimentos.\nTermo procurado: "{}"'.format(termo))

plt.show()