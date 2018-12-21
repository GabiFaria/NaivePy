def get_lexico ():
    lexico = open('lexico_v2.1txt', 'r', encoding = 'utf-8')
    dataset = lexico.read()
    dataset = dataset.split('\n')
    dataset = [data.split(',') for data in dataset]

    date = {}
    for palavra in dataset:
        if(palavra != ['']):
            date[palavra[0]] = int(palavra[2])
    
    return date

data = get_lexico()

print(len(data))