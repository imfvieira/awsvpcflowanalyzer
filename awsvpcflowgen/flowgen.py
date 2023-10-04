import ipaddress
import random
import time
import datetime
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
print(listresult)
