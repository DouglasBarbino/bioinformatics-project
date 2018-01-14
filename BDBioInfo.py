# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 18:46:55 2016

@author: Douglas
"""

from Bio import SeqIO
import sqlite3

class BioInfoDAO:
    
    def __init__(self):
        self.__conexao=sqlite3.connect("bd_bioinfo.db")
       
    #Criar o BD             
    def create(self): 
        cursor = self.__conexao.cursor()
        
        cursor.execute('''drop table if exists bioinfo''')    
        cursor.execute('''create table if not exists bioinfo
                            (descricao text PRIMARY KEY, tipo text, sequencia text) ''')    
        
        cursor.close()

    #Inserir dados
    def insert(self, descricao, tipo, sequencia): 
        cursor = self.__conexao.cursor()
        retorno = True
        
        try:
            cursor.execute('''insert into bioinfo values (?, ?, ?)''', [descricao, tipo, sequencia])
        #Erro de inserir algo cuja chave já existente
        except sqlite3.IntegrityError:
            retorno = False
        
        cursor.close()
        self.__conexao.commit()  
        
        return retorno

    #Alterar dados 
    def update(self, descricao, tipo, sequencia):   
        cursor = self.__conexao.cursor()
                
        cursor.execute('''update bioinfo       
                          set tipo = ?, sequencia = ?     
                          where descricao = ?''', [tipo, sequencia, descricao])       
        cursor.close()
        self.__conexao.commit() 

    #Selecionar dados
    def select(self): 
        cursor = self.__conexao.cursor()
        
        row = ''        
        for lines in cursor.execute('''Select * from bioinfo order by descricao'''):
            #Obtem o valor da última operação
            texto = "('" + str(lines[0]) + "', '" + str(lines[1]) + "',"
            loops = len(str(lines[2])) // 60 
            #Correção necessária para que não seja impresso uma linha em branco 
            if (len(str(lines[2])) % 60 == 0):
                loops -= 1            
            for i in range(0, loops + 1):
                if (i == 0):
                    texto += "\n'" + str(lines[2][60*i:60*(i+1)])
                else:
                    texto += "\n" + str(lines[2][60*i:60*(i+1)])
                if (i == loops):
                    texto += "')\n"                
            row += texto + '\n'
                    
        if row == None:
            resultado = "Sem resultado"
        else:
            resultado = row
        cursor.close()
        
        return resultado
      
    #Selecionar dados passando como parâmetro a descricao
    def selectPorDescricao(self, descricao): 
        cursor = self.__conexao.cursor()
        
        cursor.execute('''Select * from bioinfo 
                            where descricao = ?''', [descricao])
        #Obtem o valor da última operação
        row = cursor.fetchone()
                    
        if row == None:
            resultado = "Sem resultado"
        else:
            resultado = row
        cursor.close()
        
        return resultado
        
    #Selecionar apenas a descrição de cada item existente no banco de dados
    def selectDescricao(self): 
        cursor = self.__conexao.cursor()
        
        lista = []
        for lines in cursor.execute('''Select descricao from bioinfo order by descricao'''):
            #Obtem o valor da última operação, e mesmo que só retorne um valor 
            #é necessário o [0]
            lista.append(str(lines[0]))
                    
        if lista == None:
            resultado = "Sem resultado"
        else:
            #Transforma tudo em tupla pois é o formato que o Spinner usa
            resultado = tuple(lista)
        cursor.close()
        
        return resultado

    #Deletar dados 
    def delete(self, descricao):    
        cursor = self.__conexao.cursor()
        
        cursor.execute('''delete from bioinfo where descricao = ?''', [descricao])
        cursor.close()
        self.__conexao.commit()  

    #Fechar BD
    def close(self): 
        self.__conexao.close()  
    
#Só executa se foi ele que chamou    
if __name__ == "__main__":
    bd = BioInfoDAO()
    bd.create()
    bd.insert('teste1', 'DNA', 'cactcgggactgacggaaatataagcgtggctgaacctggggccgtccgtt')
    bd.insert('teste2', 'DNA', 'atgactcgaggtccacaccatcgtacagatgcgtttcgcgagacaaccctaactcgatga')
    bd.insert('teste3', 'Proteína', 'KIDNSYQIQPSYNSI')
    bd.insert('teste4', 'Proteína', 'NVPEGWDFCVEDWSAPMQWM')
    
    input_dna = open('dna2.fasta', 'r')
    for dna1 in SeqIO.parse(input_dna, "fasta"):
        #Tem que converter para string pois ele não tem um formato específico
        bd.insert(str(dna1.id), 'DNA', str(dna1.seq))
    input_dna.close()
    
    input_proteina = open('proteína2.fasta', 'r')
    for proteina1 in SeqIO.parse(input_proteina, "fasta"):
        #Tem que converter para string pois ele não tem um formato específico
        bd.insert(str(proteina1.id), 'DNA', str(proteina1.seq))
    input_proteina.close()
    
    #bd.select()
    #bd.selectPorDescricao('teste2')
    #bd.close()