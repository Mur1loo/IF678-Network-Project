from Pc import Pc

pc1 = Pc(1)
pc2 = Pc(2)
pc3 = Pc(3)
pc4 = Pc(4)
pc5 = Pc(5)
pc6 = Pc(6)
pc1.setnext_prev(pc2, pc6)
pc2.setnext_prev(pc3, pc1)
pc3.setnext_prev(pc4, pc2)
pc4.setnext_prev(pc5, pc3)
pc5.setnext_prev(pc6, pc4)
pc6.setnext_prev(pc1, pc5)
listpc = [pc1, pc2, pc3, pc4, pc5, pc6]

while True:
    action = int(input('Qual PC pretende usar?'))
    recive = int(input('Qual PC vai receber a mensagem?'))
    listpc[recive - 1].portchange(action*1000 + recive)
    listpc[recive - 1].starserver()
    listpc[action - 1].portchange(action*1000 + recive)
    listpc[action - 1].sendmessage(listpc[recive - 1])
