#cada eni é uma interface, precisa contar os itens indibiduais para cada
#cada ENI é um arquivo rrdtool.
#preciso saber quais eni, criar um arquivo rrd para cada métrica
#métricas: Pacotes, bytes, ações
#https://blaqfireroundup.wordpress.com/2020/06/24/analyzing-vpc-flow-logs-with-python-pyspark-and-pandas/
import sys
#import pyrrd.rrd
import ipaddress
import random
import time
import datetime

vpcflowtype = 'default'
vpcflowlen = 14
vpcflows = []
#objeto 5tuple = {srcIP: 172.16.0.1, sport: 11111, destIP: 10.20.30.40, dport: 22, prot : 6 } com dados da 5 tuple
ipsrc = [] #IPs de origem e contagem de cada cada item da lista será uma lista contando o IP
ipdst = [] #IPs de destino e contagem
sport = [] #portas de origem e contagem
dport = [] #portas de destino e contagem
prot = [] #protocolos e contagem
bytestotal = 0
qtdconn = 0
fivetuple = {}
#objeto conexão, com todos os dados da conexão.
conn = {}

listresult = ['2 123456789010 eni-1235b8ca123456789 172.31.9.69 172.31.9.12 49761 3389 6 20 4249 1418530010 1418530070 REJECT OK']

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

#print(fivetuple)
print("total de bytes: " + str(bytestotal) + ' em: ' + str(qtdconn) + ' conexões')

 