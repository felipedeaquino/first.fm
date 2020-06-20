__version__ = '0.1.0'

from urllib.request import urlopen
import datetime
from datetime import timedelta
from bs4 import BeautifulSoup

inputUser = input('Qual nick do Last.fm tu quer o relatório? ') #inserir usuário

now = datetime.datetime.now().timestamp() #manda timestamp de agora
byeFloat = int(now) #deixa de ser float
endDate = str(byeFloat) #vira string p ir p url
weekAgo = byeFloat - 604800 #uma semana atrás
startDate = str(weekAgo) #string p ir p url

# Agora é hora fazer o "scrape" da página de destino, trabalhando com o arquivo html

def seekAndDestroy(start, end):
    url = ('https://www.last.fm/user/' + inputUser + '/library/artists?from='+ start + '&to=' + end)
    content = urlopen(url) #acessa o conteúdo
    soup = BeautifulSoup(content.read(), 'html.parser') #"lê" o conteúdo 
    findTags = soup.find_all("meta",  property="og:description") #busca tags relacionadas ao objetivo
    if len(findTags) > 1: #encontrou artista?
        getArtists = str(findTags[1]['content']) #elimina o ruído
        listArtists = getArtists.split(',') #gera lista
        if len(listArtists) <=  10: 
            tweet(listArtists)
        else:
            parsedArtists = listArtists[:10]
            tweet(parsedArtists)
    else:
        print('Não há artistas no período analisado')
    
def tweet(listArtists):
    strArtists = str(listArtists)
    strArtists = strArtists.replace("' ",'') #passo 1 limpando string
    strArtists = strArtists.replace("',",',') #passo 2 limpando string
    strArtists = strArtists.replace("[",'') #passo 3 limpando string
    strArtists = strArtists.replace("]",'') #passo 4 limpando string
    strArtists = strArtists.replace('"','') #passo 5 limpando string
    spaces = strArtists.replace("  ", ' ') #passo 6 limpando string
    a = len(inputUser) #contando caracteres do nickname
    b = len("'s top  artists this week: .") #contando caracteres da frase padrão
    c = a + b + len(spaces) #soma dos caracteres p verificar se cabe num tuíte
    if c > 280:
        listArtists = listArtists.pop() #teoricamente exclui o último artista e volta p recalcular
        tweet(listArtists)
    else:
        tweet = (str(inputUser) + "'s top " + str(len(listArtists)) + " artists this week: " + spaces + ".") #output que quero tuitar
        tweet = tweet.replace(" '",' ') #passo 7 limpando string
        tweet = tweet.replace("'.",'.') #passo 8 limpando string
        print(tweet)


listArtists = seekAndDestroy(startDate, endDate)
