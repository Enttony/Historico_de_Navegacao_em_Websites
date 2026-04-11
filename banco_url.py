class banco_url:
    def __init__ (self):
        self.__url = []

    def ler_arquivo(self, caimho:str):
        try:
            open with(caminho,"r") as arquivo:
            for x in arquivo:
                url = x.strip()
                if url:
                    self.__url.append(url)
        except FileNotFoundError:
            raise FileNotFoundError(f'O Arquivo {caminho} não foi encontrado')