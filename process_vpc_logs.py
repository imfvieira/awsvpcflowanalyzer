import sys
import pyrrd.rrd


'''[version, account, eni, source, destination, srcport, destport="22", protocol="6", packets, bytes, windowstart, windowend, action="REJECT", flowlogstatus]
2 086112738802 eni-0d5d75b41f9befe9e 61.177.172.128 172.31.83.158 39611 22 6 1 40 1563108188 1563108227 REJECT OK
2 086112738802 eni-0d5d75b41f9befe9e 182.68.238.8 172.31.83.158 42227 22 6 1 44 1563109030 1563109067 REJECT OK
2 086112738802 eni-0d5d75b41f9befe9e 42.171.23.181 172.31.83.158 52417 22 6 24 4065 1563191069 1563191121 ACCEPT OK
2 086112738802 eni-0d5d75b41f9befe9e 61.177.172.128 172.31.83.158 39611 80 6 1 40 1563108188 1563108227 REJECT OK'''


with open('vpcsample.txt','r' ) as file:
    for lines in file:
        print(lines)
        dataFlow = lines.split()
        print(len(dataFlow))
        print(dataFlow)

#cada eni é uma interface, precisa contar os itens indibiduais para cada
#cada ENI é um arquivo rrdtool.
#preciso saber quais eni, criar um arquivo rrd para cada métrica
#métricas: Pacotes, bytes, ações
#https://blaqfireroundup.wordpress.com/2020/06/24/analyzing-vpc-flow-logs-with-python-pyspark-and-pandas/
