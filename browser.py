from historico import Historico 
from banco_url import banco_url 

class Browser:
    def __init__(self, historico: Historico, banco: banco_url):
        self.historico = historico
        self.banco = banco
        self.home = "www.google.com"

    def navegar(self, url):
        if self.banco.url_existe(url):
            self.historico.adcionar(self.home)
            self.home = url
            print(f"Navegando para: {self.home}")
            print("Página encontrada")
        else:
            print(f"Erro 404: A URL '{url}' não encontrada.")

    def voltar(self):
        if self.historico.historico_vazio():
            print("Histórico vazio. Você já está na página inicial.")
        else:
            self.historico.remover()
            if not self.historico.historico_vazio():
                self.home = self.historico.url_atual()
                print(f"Voltando para: {self.home}")
            else:
                print("Histórico vazio.")

    def exibir_estado(self):
        """Mostra o que está acontecendo no browser no momento."""
        print("\n" + "="*40)
        print("         ESTADO ATUAL DO BROWSER")
        print("="*40)
        print(f"Página aberta agora: {self.home}")
        print("-" * 40)
        print("Histórico (da mais recente para a antiga):")
        
        if self.historico.historico_vazio():
            print("[Vazio]")
        else:
            self.historico.exibir_historico()
        print("="*40 + "\n")

    def adicionar_ao_banco(self, url):
        """Interface para adicionar URLs ao banco de dados."""
        try:
            with open("urls.txt", "a", encoding="utf-8") as arquivo:
                arquivo.write(f"\n{url}")
            self.banco.ler_arquivo("urls.txt") # Recarrega o banco
            print(f"URL '{url}' adicionada ao arquivo com sucesso.")
        except Exception as e:
            print(f"Erro ao salvar URL: {e}")