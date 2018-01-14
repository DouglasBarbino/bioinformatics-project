# -*- coding: utf-8 -*-
"""
Created on Wed May 25 18:35:50 2016

@author: Douglas
"""

import BDBioInfo
#import Bio
from Bio import SeqIO

def insereDados():
    bd = BDBioInfo.BioInfoDAO()
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
        
    input_proteina = open('proteina2.fasta', 'r')
    for proteina1 in SeqIO.parse(input_proteina, "fasta"):
        #Tem que converter para string pois ele não tem um formato específico
        bd.insert(str(proteina1.id), 'Proteína', str(proteina1.seq))
    input_proteina.close()
    
if __name__ == "__main__":
    insereDados()