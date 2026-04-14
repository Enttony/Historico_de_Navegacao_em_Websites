#Início da formação do histórico do browser

class Historico:
    def __init__(self):
        self.__historico = []
    #Adcionar uma url
    def adcionar(self, url):
        self.__historico.append(url)
    #Retira a url
    def remover(self):
    # verifica se está vazio antes de remover
        if self.historico_vazio():
            raise IndexError("Não é possível remover, histórico vazio")

        self.__historico.pop()
    #Demonstrar qual url atual
    def url_atual(self):
        if self.historico_vazio() == True:
            raise ValueError('Histórico Vazio')
        topo = self.__historico[-1]
        return topo
    #Indicar se o histórioco está vazio
    def historico_vazio(self)-> bool:
        if len(self.__historico) == 0:
            return True
        else:
            return False
    #Formatar saída
    '''Isso Retorna na forma de pilha tradicional, sendo a url mais acima a mais nova que foi adcionada e a mais abaixo foi a primeira a ser adcionanda'''
    def exibir_historico(self) -> any:
        for url in self.__historico[::-1]:
            print(f'[{url}]')
    
    def __str__(self):
        return "".join(f'[{url}]' for url in self.__historico)

