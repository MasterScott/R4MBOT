'''
R 4 M B O T | @ramsolobot
'''
from telepot.loop import MessageLoop
from datetime import datetime, date
from googletrans import Translator
from time import strftime, sleep
from random import randint
import subprocess
import requests
import telepot
import tweepy
import re

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    
    id_permission = [] #adicionar manualmente, permissões especiais por chat ID
    CHAT = -123456789 #chat para envio de mensagens automaticas

    if content_type == 'new_chat_member' and chat_id in id_permission:
    	print('ENTROU!')
    	username = bot.getChat(chat_id)
    	print(username)
    	msg = 'Bem-vindo(a) a {}!\nPara mais informações sobre o grupo leia a descrição!\n'.format(username['title'])
    	bot.sendMessage(chat_id, msg)
    if content_type == 'left_chat_member':
    	print('saiu!')

    #Funções globais
    if msg['text'] == '/invite': #convite para o grupo
    	print(msg['text'])
    	bot.sendMessage(chat_id, bot.exportChatInviteLink(chat_id))
    if msg['text'] == '/btc': #busca valor do Bitcoin em reais e euro
    	bot.sendMessage(chat_id, getBTCprice())
    if msg['text'] == '/euro': #busca o valordo euro
    	bot.sendMessage(chat_id, getEURO())
    if msg['text'] == '/dolar': #busca o valordo dolar americano
    	bot.sendMessage(chat_id, getUSD())
    if msg['text'] == '/gd': #gera documentos randomicos
    	bot.sendMessage(chat_id, fakeDoc())
    if msg['text'] == '/random': #frases aleatorias, busca em arquivo de texto em sort/phrase.txt
    	bot.sendMessage(chat_id, randomPhrase(0))
    if '/news' in msg['text']: #busca noticias sobre um termo
    	del news_list[:]
    	arg = msg['text'][6:]
    	getNews(chat_id,arg)
    if '/select' in msg['text']: #seleciona a noticia que deseja visualizar
    	arg = msg['text'][8:]
    	selectNews(chat_id,int(arg))
    if '/translate' in msg['text']: #detecta um idioma e traduz pro português
    	text = msg['text'][11:]
    	bot.sendMessage(chat_id, Translate(text))
    if msg['text'] == '/help' or msg['text'] == '/start': #mostra os comandos
    	helpopt = '/btc Mostra o valor do BTC\n/dolar Mostra o valor do Dolar USD\n/euro Mostra o valor do Euro\n/news [NOTICIA] Busca uma notícia\n/translate Traduz um texto para português\n/random Frases aleatórias\n/gd Gerar documentos\n/invite Cria um convite para o grupo\n/devel informações do desenvolvedor\n'
    	if chat_id in id_permission:
    		help = helpopt+'\nComandos para grupo admin\n/tweet [seu tweet + (foto ou vídeo opcional, passar link)]\n/deltweet [ID do tweet para deletar]\n/gettweet [usuario + numero de tweets para exibir]'
    		bot.sendMessage(chat_id, help)
    	else:
    		bot.sendMessage(chat_id, helpopt)
    if msg['text'] == '/devel':
    	bot.sendMessage(chat_id, "R 4 M B O T\nDesenvolvedor: @r4msolo\nTwitter: twitter.com/r4msolo\n\nhttps://r4msolo.github.com")

    #**************** ADMIN FUNCTIONS *****************

    if chat_id in id_permission:
    	if '/tweet' in msg['text']: #usa a API do twitter para twittar
    		print("ACCESS GRANTED",chat_id)
    		arg = msg['text'][7:]
    		print('Tweet:',arg)
    		tweetLS(arg)
    		bot.sendMessage(chat_id, '[+] Tweetado')

    	if '/gettweet' in msg['text']: #exibe uma quantidade de tweats
    		user = msg['text'][10:]
    		user = user.split(' ')
    		print(user[0],user[1])
    		tweet = get_tweets(chat_id,user[0],user[1])

    	if '/deltweet' in msg['text']: #deleta um tweat pelo ID
    		print("ACCESS GRANTED",chat_id)
    		id = msg['text'][10:]
    		api.destroy_status(id)
    		bot.sendMessage(chat_id, '[-] Tweet Deletado\nID: '+id)
    		pass

def getBTCprice():
	print('[!] Buscando valor do BTC')
	request = requests.get('https://www.mercadobitcoin.net/api/BTC/ticker/')
	btcH = request.json()['ticker']['high']
	btcL = request.json()['ticker']['low']
	btcLT = request.json()['ticker']['last']
	btcV = request.json()['ticker']['vol']
	btcD = datetime.fromtimestamp(request.json()['ticker']['date'])
	request2= requests.get("https://blockchain.info/ticker")
	eurobtc = request2.json()['EUR']['last']
	msg = "*...::::BITCOIN::::...*\nÚltimo Valor:\nR$ {2}\n€ {5:.2f}\nAlta: R$ {0}\nBaixa: R$ {1}\nVolume negociado nas últimas 24 Hrs: BTC {3}\nHorário que os valores foram gerados: {4} GMT(UTC+00)".format(btcH[:-6],btcL[:-6],btcLT[:-6],btcV[:-6],btcD,eurobtc)
	return msg

def getEURO():
	print('[!] Buscando o valor do EURO')
	request = requests.get('https://economia.awesomeapi.com.br/all/EUR-BRL')
	euro = request.json()['EUR']['bid']
	msg = float(euro)
	msg = f"...::::Euro::::...\nR$ {msg:.2f}"
	return msg

def getUSD():
	print('[!] Buscando o valor do DÓLAR')
	request = requests.get('https://economia.awesomeapi.com.br/all/USD-BRL')
	dolar = request.json()['USD']['bid']
	msg = float(dolar)
	msg = f"...::::Dolar USD::::...\nR$ {msg:.2f}"
	return msg

def Translate(text):
	transtext = translate.translate(text, dest='pt') #mudar dest para o idioma de sua escolha
	return transtext.text

def get_tweets(chat_id,usuario, limite):
	resultados = api.user_timeline(screen_name=usuario, count=limite, tweet_mode='extended')
	tweets = [] # lista de tweets inicialmente vazia
	for r in resultados:
		tweet = re.sub(r'http\S+', '', r.full_text)
		tweets.append('[LINK] https://twitter.com/{0}/status/{1}\n'.format(usuario,r.id))
		tweets.append(tweet.replace('\n', ' ')) # adiciona na lista
	
	tweets = '\n'.join(tweets)
	print(tweets)
	bot.sendMessage(chat_id, 'Tweet {}\n\n{}'.format(usuario,tweets))

def tweetLS(tweet):
	#create tweet
	api.update_status(tweet)

def randomPhrase(choice):
	if choice == 1:
		file = open('sort/morning.txt','r')
	else:
		file = open('sort/phrase.txt','r')
	arq = file.readlines()
	random = randint(0,len(arq)-1)
	file.close()
	return arq[random]

def checkLanguage(text):
	check = translate.detect(text)
	return check.lang

def getDate():
	today = date.today()
	return today

def selectNews(chat_id, id):
	new = str(news_list[id])
	new = new.split('\n')
	nt = ''
	link = ''
	for l in new:
		if 'http' in l:
			link = l
		if '§' in l:
			nt = l.replace('§','\n\n')
		else: 
			chkLNG = checkLanguage(l)
			if chkLNG != 'pt':
				nt = nt+'\n'+l
	bot.sendMessage(chat_id, Translate(nt)+link)

def getNews(chat_id, keyword):
	print('[!] Buscando notícias')
	word_search = keyword.replace(" ","-")
	today = getDate()
	date_today = str(today.year)+'-'+str(today.month)+'-'+str(today.day)
	if today.month == 1:	#Condição criada para pegar noticias do mês passado caso o mês seja janeiro
		month = 12
		year = today.year - 1
	else:
		month = today.month - 1
		year = today.year
	limit_date = str(year)+'-'+str(month)+'-'+str(today.day)
	print('Limit_date',limit_date)
	request = requests.get('https://newsapi.org/v2/everything?q={0}&from={1}&to={2}&sortBy=popularity&apiKey={3}'.format(word_search,limit_date,date_today,news_api))
	c = request.json()

	results = c['totalResults']
	titles = []
	if results == 0:
		bot.sendMessage(chat_id, '[ ! ] Nenhuma notícia relacionada à {} foi encontrada esse mês.'.format(keyword))
	else:
		for e, l in enumerate(c['articles']):
			title = c['articles'][e]['title']
			desc  = c['articles'][e]['description']
			link  = c['articles'][e]['url']
			content = title+'§\n'+desc+'\n'+link
			news_list.append(content)
			chkLNG = checkLanguage(title)
			if chkLNG != 'pt':
				if e == 0:
					bot.sendMessage(chat_id, '[!] Traduzindo titulos, aguarde...')
				title = Translate(title)
			title = '[{0}] {1}\n'.format(e,title)
			titles.append(title)

		titles = "{0} artigos encontrados esse mês, exibindo os mais relevantes\n\n{1}\n\nuse: /select [Numero da Noticia] para visualizar descrição\n".format(results,'\n'.join(titles))
		bot.sendMessage(chat_id, titles)

def fakeDoc():
	site = "https://www.4devs.com.br/ferramentas_online.php"
	form = {'acao':'gerar_pessoa','sexo':'I','pontuacao':'S','idade':'0','cep_estado':'','txt_qtde':'1','cep_cidade':''}
	x=requests.post(site,data=form)
	y = x.json()
	name = y['nome']
	ysold = y['idade']
	cpf = y['cpf']
	rg = y['rg']
	born = y['data_nasc']
	signo = y['signo']
	mother = y['mae']
	father = y['pai']
	email = y['email']
	passw = y['senha']
	cep = y['cep']
	address = y['endereco']
	number = y['numero']
	dist = y['bairro']
	city = y['cidade']
	state = y['estado']
	tel = y['telefone_fixo']
	cel = y['celular']
	heigh = y['altura']
	weight = y['peso']
	blood = y['tipo_sanguineo']
	color = y['cor']
	response = 'Nome: {}\nIdade: {}\nCPF: {}\nRG: {}\nData Nascimento: {}\nSigno: {}\nMãe: {}\nPai: {}\nEmail: {}\nSenha: {}\nCEP: {}\nEndereço: {}\nNúmero: {}\nBairro: {}\nCidade: {}\nEstado: {}\nTelefone: {}\nCelular: {}\nAltura: {}\nPeso: {}\nTipo sanguineo: {}\nCor favorita: {}\n'.format(name,ysold,cpf,rg,born,signo,mother,father,email,passw,cep,address,number,dist,city,state,tel,cel,heigh,weight,blood,color,color)
	return response
#===================================================================
#Rotina
def checkClock():
	#Fuso horário diferente +3 horas
	clock = strftime('%H:%M:%S')
	today = getDate()
	
	if clock == '21:00:00':
		pass
	if clock == '07:00:00':
		phrase = randomPhrase(1)
		bot.sendMessage(CHAT, phrase)
	if clock == '00:00:00':
		pass
	if clock == '18:00:00':
		pass

	if today.month == 12 and today.day == 25 and clock == '00:00:00':
		bot.sendMessage(CHAT, 'Ho-ho-ho!\nFeliz natal!')
#=====================================================================

#variaveis de inicialização
botname = 'R 4 M B O T'
print('Inicializando',botname)

print('carregando keys...')
bot = telepot.Bot('123456789abcdefghijk') #ALTERAR PELA SUA CHAVE DE API DO BOT

#news api
news_api = 'XXXXXXXXXXXX' #ALTERAR PELO SUA API KEY https://newsapi.org/
news_list = ['1337']

#Google Translator
translate = Translator()

#tweepy #https://developer.twitter.com/en/docs
consumer_key = 'xxxxxxxx-12345'
consumer_secret = 'XXXXXXXXX-12345678'

access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
access_token_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth)
#=====================================================================

MessageLoop(bot, handle).run_as_thread()

run = True

while run:
	try:
		checkClock()
		sleep(1)
	except:
		if KeyboardInterrupt:
			print('Finished')
			run = False
