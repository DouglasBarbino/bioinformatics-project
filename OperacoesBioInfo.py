# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 17:52:52 2016

@author: Douglas
"""

#Para converter um DNA para proteina
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC

class Operacoes():
    
    def __init__(self, bd):
        self.__bd = bd
        
    def getBD(self):
        return self.__bd

    def setBD(self, bd):
        self.__bd = bd
        
    bd = property(fget=getBD, fset=setBD) 
        
    def converterDNAParaProteina(self, chave):
        #Primeiro passo: Buscar no BD o dado
        registro = self.buscarBanco(chave)
        #Erro causado caso não foi encontrado o registro
        if (registro == "Sem registro"):
            return registro
        #Segundo passo: Verificar se é um DNA
        if (registro[1] != 'DNA'):
            valorFinal = "Você não passou como parâmetro um DNA"
            return valorFinal
        #Terceiro passo: Transcrição do DNA para RNAt
        dna = Seq(registro[2], IUPAC.unambiguous_dna)
        rnaTransportador = dna.reverse_complement()
        #Quarto passo: Transcrição do RNAt para RNAm (o códon)
        rnaMensageiro = rnaTransportador.reverse_complement().transcribe()
        #Quinto passo: Tradução do RNAm para os aminoácidos, gerando a proteina
        proteina = rnaMensageiro.translate() #Para finalizar em algo de fim de leitura colocar no final (to_stop=True)
        return proteina
        
    def complementoReversoDNA(self, chave):
        #Primeiro passo: Buscar no BD o dado
        registro = self.buscarBanco(chave)
        #Erro causado caso não foi encontrado o registro
        if (registro == "Sem registro"):
            return registro
        #Segundo passo: Verificar se é um DNA
        if (registro[1] != 'DNA'):
            valorFinal = "Você não passou como parâmetro um DNA"
            return valorFinal
        #Terceiro passo: Realizar o complemento reverso (inverter o DNA e trocar as bases A-T e C-G)
        dna = Seq(registro[2], IUPAC.unambiguous_dna)
        compRev = dna.reverse_complement()
        return compRev
        
    def buscarBanco(self, chave):
        #Primeiro passo de qualquer operação: Buscar no BD o dado
        resultado = self.__bd.selectPorDescricao(chave)
        return resultado
        
    def calculoMassaMolecularProteina(self, chave):
        #Primeiro passo: Buscar no BD o dado
        registro = self.buscarBanco(chave)
        #Erro causado caso não foi encontrado o registro
        if (registro == "Sem registro"):
            return registro
        #Segundo passo: Verificar se é uma proteína
        if (registro[1] != 'Proteína'):
            valorFinal = "Você não passou como parâmetro uma proteína"
            return valorFinal
        #A partir daqui já sabemos que o cálculo será realizado, então podemos 
        #inicializar o dicionário com os pesos de cada aminoácido           
        
        #Massa molecular dos aminoácidos extraido de:
        #http://www.webqc.org/aminoacids.php
        
        #Aminoácidos B e Z correspondem a quando não se há certeza se o 
        #aminoácido encontrado foi o D/N e Q/E, respectivamente
        
        #Terceiro passo: Percorrer a proteína para calcular a sua massa (em Daltons(Da), g/mol)
        massaAminoacidos = {"A":89.0935, "C":121.1590, 
                            "D":133.1032, "E":147.1299, 
                            "F":165.1900, "G":75.0669, 
                            "H":155.1552, "I":131.1736, 
                            "K":146.1882, "L":131.1736, 
                            "M":149.2124, "N":132.1184, 
                            "P":115.1310, "Q":146.1451, 
                            "R":174.2017, "S":105.0930, 
                            "T":119.1197, "V":117.1469, 
                            "W":204.2262, "Y":181.1894,
                            "B":132.6108, "Z":146.6375}
        proteina = Seq(registro[2], IUPAC.protein)
        massaTotal = 0
        for letra in proteina:
            if (letra != "*"):
                for i in massaAminoacidos:
                    if (i == letra):
                        massaTotal += massaAminoacidos[i]
        return massaTotal