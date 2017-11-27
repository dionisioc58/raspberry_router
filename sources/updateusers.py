#!/usr/bin/python
# Alterar lista de autenticação de usuários do freeradius no Raspberry PI

import requests
import json
import subprocess

print 'Atualizando a base de autenticacoes...'

client_id = '<substituir pelo client-id fornecido>'
client_secret = '<substituir pelo secret fornecido>'
xapikey = '<substituir pelo x-api-key fornecido>'
URL_BASE = 'https://apitestes.info.ufrn.br/'

#injetando parametros na url
url_token = URL_BASE + 'authz-server/oauth/token?client_id={0}&client_secret={1}&grant_type=client_credentials'.format(client_id, client_secret)

#efetuando uma requisicao a api passando a url como parametro
requisicao_token = requests.post(url_token)

print 'Conectando a base de dados...'

#convertendo a resposta json em um objeto python
resposta = json.loads(requisicao_token.content)

#salvamos o token em uma variavel pra usar em um exemplo de chamada a api
token = resposta['access_token']

#montamos a url de participantes injetando o token como parametro
URL = URL_BASE+ 'turma/v0.1/participantes?id-turma=57609285'

headers = {'Authorization': 'bearer ' + token, 'x-api-key': xapikey}

#agora fazemos uma requisicao aos participantes da turma
requisicao_participantes = requests.get(URL, headers=headers)

#convertemos a resposta para json
participantes = json.loads(requisicao_participantes.content)

#imprime a tabela no arquivo de usuarios
print 'Salvando o arquivo...'
f = open('/etc/freeradius/3.0/users', 'w')
for participante in participantes:
	linha = participante['login'] + '\tCleartext-Password := "' + `participante['identificador']` + '"\t # Nome: ' + participante['nome'] + '\n'
	f.write(linha.encode('utf-8'))
f.close()

#reiniciar o servidor freeradius para perceber as alteracoes
print 'Reiniciar o servico...'
p = subprocess.Popen(["sudo", "service", "freeradius", "restart"], stdout=subprocess.PIPE)
out, err = p.communicate()

print 'Atualizacao concluida com sucesso!'
