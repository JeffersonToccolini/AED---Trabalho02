from pymongo import MongoClient
from cryptography.fernet import Fernet


# 1,auburn,33590,2014,gmc,sierra 1500 crew cab slt,8 cylinders

def inserir_dados(chave):
    conn = MongoClient()
    # Database
    db = conn.database
    # Cria a collection
    collection = db.teste
    arquivo = "vehicles.csv"
    with open(arquivo) as arq:
        for linha in arq:
            lines = linha.split(",")
            temp = lines[6].replace("\n", "")
            if len(lines[3]) == 0:
                lines[3] = 0
            fernet = Fernet(chave)
            temp2 = fernet.encrypt(lines[1].encode())
            lines[1] = temp2.decode()
            emp_rec1 = {
                "_id": lines[0],
                "cidade": lines[1],
                "valor": lines[2],
                "ano": int(lines[3]),
                "marca": lines[4],
                "modelo": lines[5],
                "cilindros": temp,
            }
            collection.insert_one(emp_rec1)


def gerar_chave():
    chave = Fernet.generate_key()
    with open('filekey.key', 'wb') as arq:
        arq.write(chave)
    return chave


conn = MongoClient()
db = conn.database
collection = db.teste
while True:
    print("Digite a sua escolha ! \n"
          "1 - Inserir dados na DB \n"
          "2 - Pergunta 01 :  Maior valor do carro ? \n"
          "3 - Pergunta 02 :  Mostrar todos os carros de um cidade.   \n"
          "4 - Pergunta 03 :  Quantos carros existem com 8 cilindros ? \n"
          "5 - Pergunta 04 :  Quantos carros foram vendidos em 2016 até o ano atual ?\n")

    escolha = int(input())
    if escolha == 1:
        print("Chave gerada ! ")
        chave = gerar_chave().decode()
        print(chave)
        inserir_dados(chave)
    elif escolha == 2:
        cursor = collection.find().sort("valor", -1).limit(1)
        for lin in cursor:
            print("O maior valor de um carro é de : {} ".format(lin["valor"]))
    elif escolha == 3:
        cidade = input("Digite o estado : ")
        chave = input("Digite a chave : ")
        cursor = collection.find()
        fernet = Fernet(chave)
        for lin in cursor:
            tx = fernet.decrypt(lin["cidade"]).decode()
            if tx == cidade:
                print(lin)
    elif escolha == 4:
        cursor = collection.count_documents({"cilindros": "8 cylinders"})
        print("Existem {} carros com 8 cilindros ".format(cursor))
    elif escolha == 5:
        cursor = collection.count_documents({"ano": {"$gt": 2015}})
        print("Foram vendidos {} carros de 2016 até 2022".format(cursor))
