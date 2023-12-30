import ipaddress
import random
import time
import datetime
import rrdtool

vpcflowtype = 'default'
vpcflowlen = 14
vpcflows = []
#objeto 5tuple = {srcIP: 172.16.0.1, sport: 11111, destIP: 10.20.30.40, dport: 22, prot : 6 } com dados da 5 tuple
ipsrc = [] #IPs de origem e contagem de cada cada item da lista será uma lista contando o IP
nipsrc = {} # dicionário com IP de origem: quantidade
nipdst = {} # dicionário com IP de destino: quantidade
ipdst = [] #IPs de destino e contagem
sport = [] #portas de origem e contagem
dport = [] #portas de destino e contagem
prot = [] #protocolos e contagem
nprot = [] #dicionário com protocolos e quantidade
bytestotal = 0
qtdconn = 0
fivetuple = {}
#objeto conexão, com todos os dados da conexão.
conn = {}
rrd_filename =''
####criar rrdtool se não tiver criado
def createrrdtoolDB():
  try:
    rrd_filename = 'bytestotal.rrd'
    rrdtool.create(
      rrd_filename,
      "--step", "300",  # Intervalo de atualização (em segundos)
      "DS:entrada:COUNTER:600:0:U",  # Definição do dado (tráfego de entrada)
      "DS:saida:COUNTER:600:0:U",    # Definição do dado (tráfego de saída)
      "RRA:AVERAGE:0.5:1:2016",      # Retenção de dados (média dos últimos 7 dias)
      "RRA:AVERAGE:0.5:12:240",      # Retenção de dados (média dos últimos 30 dias)
    )
    return(rrd_filename)
  except:
    print('erro ao criar banco de dados rrdtool')
####atualizar arquivo de banco de dados.
def updaterrdtoolDB(valor_entrada,valor_saida=0):
  try:
    rrdtool.update(rrd_filename, "N:%s:%s" % (valor_entrada, valor_saida))
  except:
    print('Erro ao atualizar banco de dados')
#função para remover duplicados de listas
#transforma a lista em um dicionário usando cada item da lista como uma key, depois converte o dicionário em uma lista
def removeduplicates_list(x):
  return list( dict.fromkeys(x) )

###gerador de flows###gera N Flows de forma aleatória com N entre 10 e 1000 e retorna uma lista como resultado
def vpcflowgenerate(n):
  #criar n flow aleatórios e retornar uma lista com todos os flow.
  i= 0
  newflow = []
  tmpdata = ''
  prots = ['1','6','17']
  flow = '2 '
  
  actionlog = ["ACCEPT", "REJECT"]
  logstatus = ['OK']
  base = "0123456789abcdefghijklmnopqrstuvxwz"
  u = 0
  while u < n:
    if flow == '2 ': pass
    else: flow = '2 '
    print('execução numero: '+str(u) )
    while i < 13: #criação da conta #criar uma accountid 1235b8ca123456789 - 18 caracteres
      tmpdata = tmpdata + str(random.randint(0,9))
      i=i+1
      if i == 13: 
        flow = flow + str(tmpdata) + ' '
        tmpdata = ''
        i =0
        break
  
    if i != 0:
      print('if conta')
      i = 0
      while i < 17: #criação da interface
        tmpdata = tmpdata + random.choice(base)
        i=i+1
        if i == 17: 
          flow = flow + 'eni-'+tmpdata
          tmpdata = ''
    else: 
      print('else conta')
      while i < 17: #criação da interface
        tmpdata = tmpdata + random.choice(base)
        i=i+1
        if i == 17: 
          flow = flow + 'eni-'+tmpdata
          tmpdata = ''
    i = 0
    print(flow)    
    #criação de IPs:
    #255.255.255.255 = 4294967295
    #1.0.0.0 = 16777216
    flow = flow + ' ' + str(ipaddress.ip_address(random.randint(16777216,4294967295)))
    flow = flow + ' ' + str(ipaddress.ip_address(random.randint(16777216,4294967295)))
    
    #portas
    #decidir o protocolo. Se ICMP (1) não tem porta
    prot = random.choice(prots)
    if int(prot) > 2:
      flow = flow + ' ' + str(random.randint(4000,65535)) + ' ' + str(random.randint(0,1024)) + ' ' + str(prot)
    else:
      flow = flow + ' - -' + ' ' + str(prot)
    
    print(flow) 
    start = int(time.time())
    end = start + random.randint(100,2000)
    #packets bytes start end action log-status#packets bytes start end action log-status#
    flow = flow + ' ' + str(random.randint(1,20)) + ' ' + str(random.randint(10,10000)) + ' ' + str(start) + ' ' + str(end) + ' ' + random.choice(actionlog) + ' ' + 'OK'
    print(flow)
    newflow.append(flow)
    flow = ''
    #print(acctemp)
    #criar uma accountid 1235b8ca123456789 - 18 caracteres
    #255.255.255.255 = 4294967295
    #1.0.0.0 = 16777216
    u = u + 1
  return(newflow)

listresult = (vpcflowgenerate(random.randint(10,1000)))

#listresult = ['2 123456789010 eni-1235b8ca123456789 172.31.9.69 172.31.9.12 49761 3389 6 20 4249 1418530010 1418530070 REJECT OK']
#processar a lista. Cada VPC flow é processado.
for flows in listresult:
  if len(flows.split()) == 14:
      #print('oi')
      data = flows.split() #separar o flow por espaços
      vpcversion = data [0]  #vpcflow version
      awsACC = data [1]  #AWS Acc
      vif = data [2]  #ENI ID
      fivetuple['sip'] = data[3]  #sourceip
      fivetuple['dip'] = data[4]  #destinationip
      fivetuple['sport'] = data[5]  #sourceport
      fivetuple['dport'] = data[6]  #destinationport
      fivetuple['prot'] = data[7]  #protocol
      pkts = data [8]  #packets
      bytestotal = bytestotal + int(data[9])  #bytes
      starttime = data[10] #starttime epoch
      endtime = data[11] #endtime epoch
      action = data[12] #action
      lstatus = data[13] #logstatus
      ipsrc.append(data[3])
      prot.append(data[7])
  else: 
    print('falha na linha: %s', flows)

####Processar cada lista criada para contatagens e gerar o resultado em um dicionário
####

#protocolos
nprot = dict.fromkeys(prot)
print(nprot)
for itens in prot:
  if itens in nprot.keys():
    i = itens
    n = nprot[itens]
    if n == None:
      n = 1
    else:
      n = n+1
    nprot[itens] = n
print(nprot)

  
if rrd_filename == '':
  rrd_filename = createrrdtoolDB()

    


print(fivetuple)
print(len(prot))
print(len(removeduplicates_list(prot)))
print(removeduplicates_list(prot))

print("total de bytes: " + str(bytestotal) + ' em: ' + str(qtdconn) + ' conexões')

updaterrdtoolDB(bytestotal)

