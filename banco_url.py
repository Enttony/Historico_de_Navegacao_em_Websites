class banco_url:
    def __init__ (self):
        self.__banco_url = {}

    def ler_arquivo(self, caminho:str):
        try:
            with open (caminho,"r") as arquivo:
                for linha in arquivo:
                    linha = linha.strip()
                    if not linha:
                        continue

                    linha_partida = linha.split()
                    home = linha_partida[0]
                    subpaginas = linha_partida[1:]

                    if self.formato_valido(home) == True:
                        self.__banco_url[home] = subpaginas

                    
        except FileNotFoundError:
            raise FileNotFoundError(f'O Arquivo {caminho} não foi encontrado')
    
    def formato_valido(self, url: str) -> bool:
        return (url.startswith("www.")) or (url.startswith("http://")) or (url.startswith())


    def url_existe(self, url) ->bool:
        for home, subpaginas in self.__banco_url.items():
            if url == home:
                return True
            for sub in subpaginas:
                if url == home + sub:
                    return True
            return False
