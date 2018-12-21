# encoding: utf-8
import tweepy

def twitters(termo):
    consumer_key = 'v6pBsk9vNUis6zcUQSEznqIho'
    consumer_secret = 'jLScaANklngvbbSweier0PLFnWlrk3TDnrw8e5CTXwz7wKViC2'

    access_token = '1071399057912938498-vDKgDdYfNiFyirdCNvBbxgsusdJRol'
    access_token_secret = 'vAUmb4IXhVCNX8cCjJLxWqDGacfVh3jUSGRysZWNXXw0S'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    #Variável que irá armazenar todos os Tweets com a palavra escolhida na função search da API
    public_tweets = api.search(termo, count=100, lang='pt', result_type='recent')

    return public_tweets