class banco_url:
    def __init__(self):
        self.__banco_url = {}

    def ler_arquivo(self, caminho: str):
        # limpa o banco antes de recarregar
        self.__banco_url = {}

        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                for linha in arquivo:
                    linha = linha.strip()

                    if not linha:
                        continue

                    linha_partida = linha.split()
                    home = linha_partida[0]
                    subpaginas = linha_partida[1:]

                    if self.formato_valido(home):
                        self.__banco_url[home] = subpaginas

        except FileNotFoundError:
            raise FileNotFoundError(f"O arquivo {caminho} não foi encontrado")

    def formato_valido(self, url: str) -> bool:
        return (
            url.startswith("www.")
            or url.startswith("http://")
            or url.startswith("https://")
        )

    def url_existe(self, url) -> bool:
        for home, subpaginas in self.__banco_url.items():
            if url == home:
                return True

            for sub in subpaginas:
                if url == home + sub:
                    return True

        return False

    def get_subpaginas(self, url: str) -> list:
        # retorna as subpáginas da url
        if url in self.__banco_url:
            return self.__banco_url[url]
        return []

    def __str__(self):
        return f"BancoURL({len(self.__banco_url)} URLs cadastradas)"