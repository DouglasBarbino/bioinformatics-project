# -*- coding: utf-8 -*-
"""
@author: Douglas
"""

import kivy
#kivy.require('1.9.1') # replace with your current kivy version !
import os
import sys

#import InsertBD
import OperacoesBioInfo
import BDBioInfo

from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
#Para importar o kv
from kivy.lang import Builder

from Bio import SeqIO

bd = BDBioInfo.BioInfoDAO()
operacoes = OperacoesBioInfo.Operacoes(bd)

class Controller(FloatLayout):
    '''Controlador da tela inicial'''
    
    def carregar(self, menuClasse, arquivoKivy, mainClasse):  
        #Remove qualquer outra janela deste .kv que já foi aberta anteriormente
        Builder.unload_file('Kivs/voltarMenu.kv')
        Builder.unload_file(menuClasse)
        Builder.unload_file(arquivoKivy)
        #Limpa a atual janela
        self.clear_widgets()
        #Carrega o voltarMenu.kv
        Builder.load_file('Kivs/voltarMenu.kv')
        #Carrega o .kv que contém o menu superior
        if (menuClasse != 'sobre'):
            Builder.load_file(menuClasse)
        #Carrega o proximo .kv
        Builder.load_file(arquivoKivy)
        #Obtem a classe principal daquele .kv
        classe = mainClasse()
        #Carrega o novo .kv
        self.add_widget(classe)
        
    #Funções apenas para não repetir todos os comandos de carregar
    def operacoes(self):
        self.carregar('Kivs/bd.kv', 'Kivs/bd_criar.kv', ControllerBDCriar)
        
    def bioInformatica(self):
        self.carregar('Kivs/bioInformatica.kv', 'Kivs/bioInformatica_converter.kv', ControllerBioInfConverter)
        
    def sobre(self):
        self.carregar('sobre', 'Kivs/sobre.kv', ControllerSobre)
        
class ControllerVoltarMenu(FloatLayout):
    '''Controlador criado para não ser necessário repetir o código do botão de 
    voltar para a tela inicial'''
    
    def voltar(self):
        #Remove qualquer outra janela deste .kv que já foi aberta anteriormente
        Builder.unload_file('main.kv')
        #Limpa a atual janela
        self.clear_widgets()
        #Carrega o proximo .kv
        Builder.load_file('main.kv')
        #Obtem a classe principal daquele .kv
        classe = Controller()
        #Carrega o novo .kv
        self.add_widget(classe)
        
    #Metodo utilizado para formatar a sequência que será apresentada ao usuário
    #após uma pesquisa
    def formatarSequencia(self, sequencia, operacaoBioInfo):
        texto = ''
        loops = len(sequencia) // 60 
        #Correção necessária para que não seja impresso uma linha em branco 
        if (len(sequencia) % 60 == 0):
            loops -= 1         
        for i in range(0, loops + 1):
            if (i == 0):
                texto += "\n'" + sequencia[60*i:60*(i+1)]
            else:
                texto += "\n" + sequencia[60*i:60*(i+1)]
            if (i == loops):
                texto += "')\n"              
                
        return texto 
    
    def pegarDadosFasta(self, path, filename):
        try:
            input_fasta = open(os.path.join(path, filename[0]), 'r')
            for conteudo in SeqIO.parse(input_fasta, "fasta"):
                #Tem que converter para string pois ele não tem um formato específico
                nome = str(conteudo.id) 
                sequencia = str(conteudo.seq)
            input_fasta.close()
        #Caso seja aberto um arquivo que não seja .fasta ou .py
        except UnicodeDecodeError: 
            nome = ''
            sequencia = ''
        #Caso seja aberto um arquivo .py
        except UnboundLocalError:
            nome = ''
            sequencia = ''            
        
        return nome, sequencia
        
    #Para que o file chooser saiba onde iniciar a procura de arquivos
    def obterCaminho(self):
        return sys.path[0]
        
class ControllerSobre(ControllerVoltarMenu):
    '''Controlador da tela que mostra as informações do programa'''
    def texto(self):
        #Optei por inserir o texto dentro do main.py por poder formatá-lo e 
        #tornar mais fácil editá-lo
        texto =     '''
        Sistema com operações básicas de Bioinformática.\n
        Autor: Douglas Antonio Martins Barbino - 551511\n
        Funções básicas de Bioinformática escolhidas por meio de:\n
        http://www.ifsc.usp.br/~rdemarco/FFI0760/introducao.pdf\n
        Mais informacoes sobre a biblioteca Biopython utilizada:\n
        http://biopython.org/DIST/docs/tutorial/Tutorial.html'''
                    
        return texto
        
class ControllerBD(ControllerVoltarMenu):
    '''Controlador geral das telas referentes ao banco de dados para não ser
    necessário repetir a implementação dos botões superiores para escolher a
    operação do banco de dados'''
    
    def carregar(self, arquivoKivy, mainClasse):
        #Remove qualquer outra janela deste .kv que já foi aberta anteriormente
        Builder.unload_file(arquivoKivy)
        #Limpa a atual janela
        self.clear_widgets()
        #Carrega o proximo .kv
        Builder.load_file(arquivoKivy)
        #Obtem a classe principal daquele .kv
        classe = mainClasse()
        #Carrega o novo .kv
        self.add_widget(classe)
        
    #Funções apenas para não repetir todos os comandos de carregar        
    def bd_criar(self):
        self.carregar('Kivs/bd_criar.kv', ControllerBDCriar)
        
    def bd_atualizar(self):
        self.carregar('Kivs/bd_atualizar.kv', ControllerBDAtualizar)
        
    def bd_visualizar(self):
        self.carregar('Kivs/bd_visualizar.kv', ControllerBDVisualizar)
        
    def bd_pesquisar(self):
        self.carregar('Kivs/bd_pesquisar.kv', ControllerBDPesquisar)
        
    def bd_deletar(self):
        self.carregar('Kivs/bd_deletar.kv', ControllerBDDeletar)
        
class ControllerBioInf(ControllerVoltarMenu):
    '''Controlador geral das telas referentes as operações de Bioinformática 
    para não ser necessário repetir a implementação dos botões superiores para 
    escolher a operação'''

    def carregar(self, arquivoKivy, mainClasse):
        #Remove qualquer outra janela deste .kv que já foi aberta anteriormente
        Builder.unload_file(arquivoKivy)
        #Limpa a atual janela
        self.clear_widgets()
        #Carrega o proximo .kv
        Builder.load_file(arquivoKivy)
        #Obtem a classe principal daquele .kv
        classe = mainClasse()
        #Carrega o novo .kv
        self.add_widget(classe)
        
    #Funções apenas para não repetir todos os comandos de carregar        
    def bioinf_converter(self):
        self.carregar('Kivs/bioInformatica_converter.kv', ControllerBioInfConverter)
        
    def bioinf_complemento(self):
        self.carregar('Kivs/bioInformatica_complemento.kv', ControllerBioInfComplemento)
        
    def bioinf_massa(self):
        self.carregar('Kivs/bioInformatica_massa.kv', ControllerBioInfMassa)

class ControllerBDCriar(ControllerBD):
    '''Controlador da operação de criar um dado no banco de dados'''
    
    def criar(self, nome, tipo, sequencia):
        if (tipo == True):
            retorno = bd.insert(nome, 'DNA', sequencia)
        else:
            retorno = bd.insert(nome, 'Proteína', sequencia)
        #Verifica se tudo ocorreu bem na inserção do dado para atribuir a mensagem da janela de popup
        if (retorno):
            self.ids.bd_criar_popup_label.text = "Dado inserido com sucesso!"
        else:
            self.ids.bd_criar_popup_label.text = "Erro! Chave já existente!"
     
    #Coloca os dados obtidos no arquivo .fasta nos textInputs correspondentes       
    def preencherDados(self, path, filename):
        nome, sequencia = self.pegarDadosFasta(path, filename)
        self.ids.bd_criar_nome.text = nome
        self.ids.bd_criar_seq.text = sequencia

class ControllerBDAtualizar(ControllerBD):
    '''Controlador da operação de atualizar um dado no banco de dados'''
    
    #Coloca os dados da chave existentes no Spinner
    def obterDescricoes(self):
        tuplaDescricoes = bd.selectDescricao()
        self.ids.bd_atualizar_nome.values = tuplaDescricoes
        self.ids.bd_atualizar_nome.text = tuplaDescricoes[0]
    
    def atualizar(self, nome, tipo, sequencia):
        if (tipo == True):
            bd.update(nome, 'DNA', sequencia)
        else:
            bd.update(nome, 'Proteína', sequencia)
            
    #Coloca os dados obtidos no arquivo .fasta nos textInputs correspondentes 
    def preencherDados(self, path, filename):
        nome, sequencia = self.pegarDadosFasta(path, filename)
        #No caso de atualizar só será atribuido o valor da sequência
        self.ids.bd_atualizar_seq.text = sequencia

class ControllerBDVisualizar(ControllerBD):
    '''Controlador da operação de visualizar os dados no banco de dados'''
    
    def carregarVisual(self):
        return(bd.select())

class ControllerBDPesquisar(ControllerBD):
    '''Controlador da operação de pesquisar um determinado dado no banco de dados'''
    
    #Coloca os dados da chave existentes no Spinner
    def obterDescricoes(self):
        tuplaDescricoes = bd.selectDescricao()
        self.ids.bd_pesquisar_nome.values = tuplaDescricoes
        self.ids.bd_pesquisar_nome.text = tuplaDescricoes[0]    
    
    def pesquisar(self, nome):
        resultado = bd.selectPorDescricao(nome)
        if (resultado != "Sem resultado"):
            texto = "('" + str(resultado[0]) + "', '" + str(resultado[1]) + "',"
            texto += self.formatarSequencia(str(resultado[2]), False)
        else:
            texto = resultado
        self.ids.bd_pesquisar_dados.text = texto

class ControllerBDDeletar(ControllerBD):
    '''Controlador da operação de deletar um determinado dado no banco de dados'''
    
    #Coloca os dados da chave existentes no Spinner
    def obterDescricoes(self):
        tuplaDescricoes = bd.selectDescricao()
        self.ids.bd_deletar_nome.values = tuplaDescricoes
        self.ids.bd_deletar_nome.text = tuplaDescricoes[0]    
    
    def deletar(self, nome):
        bd.delete(nome)

class ControllerBioInfConverter(ControllerBioInf):
    '''Controlador da operação de converter sequencia de DNA para proteina'''
    
    #Coloca os dados da chave existentes no Spinner
    def obterDescricoes(self):
        tuplaDescricoes = bd.selectDescricao()
        self.ids.bioinf_converter_nome.values = tuplaDescricoes
        self.ids.bioinf_converter_nome.text = tuplaDescricoes[0]    
    
    def converter(self, nome):
        self.ids.bioinf_converter_resultado.text = str(operacoes.converterDNAParaProteina(nome))
        #Permitir incluir esse resultado no banco de dados ou criar uma arquivo
        #.fasta do resultado
        if (self.ids.bioinf_converter_resultado.text == "Você não passou como parâmetro um DNA"):
            self.ids.bioinf_converter_adicionarbd.disabled = True
            self.ids.bioinf_converter_criarFasta.disabled = True
        else:
            self.ids.bioinf_converter_adicionarbd.disabled = False
            self.ids.bioinf_converter_criarFasta.disabled = False
        
    def adicionarConversao(self, nome, sequencia):
        retorno = bd.insert('proteína_' + nome, 'Proteína', sequencia)
        
        #Verifica se tudo ocorreu bem na inserção do dado para atribuir a mensagem da janela de popup
        if (retorno):
            self.ids.bioinf_converter_popup_label.text = "Dado inserido com sucesso!"
        else:
            self.ids.bioinf_converter_popup_label.text = "Erro! Chave já existente!"
            
    def criarFasta(self, nome, sequencia):
        nomeArquivo = "proteina_" + nome + ".fasta"
        arquivoFasta = open(nomeArquivo, 'w')
        arquivoFasta.write(">" + "proteína_" + nome)
        #Como arquivos .fasta coloca apenas 60 bases/aminoácido de uma sequência   
        #em uma linha, precisamos obter quantas vezes precisaremos dividir a 
        #sequência dada como parâmetro
        loops = len(sequencia) // 60 
        #Correção necessária para que não seja impresso uma linha em branco 
        if (len(sequencia) % 60 == 0):
            loops -= 1        
        for i in range(0, loops + 1):
            arquivoFasta.write("\n" + sequencia[60*i:60*(i+1)])
        arquivoFasta.close()
    
class ControllerBioInfComplemento(ControllerBioInf):
    '''Controlador da operação de realizar o complemento reverso de DNA'''
    
    #Coloca os dados da chave existentes no Spinner
    def obterDescricoes(self):
        tuplaDescricoes = bd.selectDescricao()
        self.ids.bioinf_complemento_nome.values = tuplaDescricoes
        self.ids.bioinf_complemento_nome.text = tuplaDescricoes[0]    
    
    def complemento(self, nome):
        self.ids.bioinf_complemento_resultado.text = str(operacoes.complementoReversoDNA(nome))
        #Permitir incluir esse resultado no banco de dados ou criar uma arquivo
        #.fasta do resultado
        if (self.ids.bioinf_complemento_resultado.text == "Você não passou como parâmetro um DNA"):
            self.ids.bioinf_complemento_adicionarbd.disabled = True
            self.ids.bioinf_complemento_criarFasta.disabled = True
        else:
            self.ids.bioinf_complemento_adicionarbd.disabled = False
            self.ids.bioinf_complemento_criarFasta.disabled = False
        
    def adicionarComplemento(self, nome, sequencia):
        retorno = bd.insert('complemento_reverso_' + nome, 'DNA', sequencia)
        
        #Verifica se tudo ocorreu bem na inserção do dado para atribuir a mensagem da janela de popup
        if (retorno):
            self.ids.bioinf_complemento_popup_label.text = "Dado inserido com sucesso!"
        else:
            self.ids.bioinf_complemento_popup_label.text = "Erro! Chave já existente!"
            
    def criarFasta(self, nome, sequencia):
        nomeArquivo = "complemento_reverso_" + nome + ".fasta"
        arquivoFasta = open(nomeArquivo, 'w')
        arquivoFasta.write(">" + "complemento_reverso_" + nome)
        #Como arquivos .fasta coloca apenas 60 bases/aminoácido de uma sequência   
        #em uma linha, precisamos obter quantas vezes precisaremos dividir a 
        #sequência dada como parâmetro
        loops = len(sequencia) // 60 
        #Correção necessária para que não seja impresso uma linha em branco 
        if (len(sequencia) % 60 == 0):
            loops -= 1
        for i in range(0, loops + 1):
            arquivoFasta.write("\n" + sequencia[60*i:60*(i+1)])
        arquivoFasta.close()

class ControllerBioInfMassa(ControllerBioInf):
    '''Controlador da operação de calcular a massa molecular de uma proteina'''
    
    #Coloca os dados da chave existentes no Spinner
    def obterDescricoes(self):
        tuplaDescricoes = bd.selectDescricao()
        self.ids.bioinf_massa_nome.values = tuplaDescricoes
        self.ids.bioinf_massa_nome.text = tuplaDescricoes[0]    
    
    def massa(self, nome):
        valor = operacoes.calculoMassaMolecularProteina(nome)
        if (valor == "Você não passou como parâmetro uma proteína"):
            self.ids.bioinf_massa_resultado.text = "Você não passou como parâmetro uma proteína"
        else:
            self.ids.bioinf_massa_resultado.text = "Esta proteína pesa %s daltons (g/mol)" % (str(valor))
            
class MainApp(App):
    def build(self):
        #InsertBD.insereDados()
        return Controller()

if __name__ == '__main__':
    MainApp().run()