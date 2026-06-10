"""
Módulo responsável pelo armazenamento e consulta das URLs cadastradas.

Estrutura interna:
    Dicionário onde cada chave é uma URL completa e o valor é
    uma lista com os links internos (subpáginas) daquela URL.

    Exemplo:
        {
            "www.ifpb.edu.br":           ["/tsi", "/rc"],
            "www.ifpb.edu.br/tsi":       ["/professores", "/alunos"],
            "www.ifpb.edu.br/rc":        ["/coordenacao"],
            "www.google.com":            []
        }

    Essa estrutura permite:
        - Verificar se uma URL existe em O(1)
        - Recuperar seus links internos em O(1)
        - Construir a URL filha concatenando chave + link interno
"""


class BancoURL:
    """Banco de dados de URLs válidas com suporte a subpáginas."""

    def __init__(self):
        # chave: url completa | valor: lista de links internos
        self.__banco: dict[str, list[str]] = {}

    # ------------------------------------------------------------------
    # Carregamento a partir de arquivo
    # ------------------------------------------------------------------

    def ler_arquivo(self, caminho: str) -> None:
        """
        Lê o arquivo de URLs e popula o banco interno.

        Formato de cada linha:
            <url>  [/link1  /link2  ...]

        Exemplos de linhas válidas:
            www.google.com
            www.ifpb.edu.br /tsi /rc
            www.ifpb.edu.br/tsi /professores /alunos

        Raises:
            FileNotFoundError: se o arquivo não existir.
        """
        self.__banco = {}

        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                for linha in arquivo:
                    linha = linha.strip()
                    if not linha or linha.startswith("#"):
                        continue

                    partes = linha.split()
                    url_base = partes[0]
                    subpaginas = partes[1:]  # pode ser lista vazia

                    if self.formato_valido(url_base):
                        self.__banco[url_base] = subpaginas

        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo '{caminho}' não encontrado.")

    # ------------------------------------------------------------------
    # Validação de formato
    # ------------------------------------------------------------------

    def formato_valido(self, url: str) -> bool:
        """
        Verifica se a URL tem um formato básico aceito pelo sistema.

        Aceita URLs que comecem com 'www.', 'http://' ou 'https://'.
        Para subpáginas internas (que começam com '/'), a validação
        é feita de forma contextual em outros métodos.

        Returns:
            True se o formato for válido, False caso contrário.
        """
        return (
            url.startswith("www.")
            or url.startswith("http://")
            or url.startswith("https://")
        )

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------

    def url_existe(self, url: str) -> bool:
        """
        Verifica se uma URL está cadastrada no banco.

        Args:
            url: URL completa a ser verificada.

        Returns:
            True se existir, False caso contrário.
        """
        return url in self.__banco

    def get_subpaginas(self, url: str) -> list[str]:
        """
        Retorna a lista de links internos de uma URL.

        Args:
            url: URL completa cadastrada no banco.

        Returns:
            Lista de strings com os links internos (ex: ['/tsi', '/rc']).
            Lista vazia se a URL não tiver subpáginas ou não existir.
        """
        return self.__banco.get(url, [])

    def listar_urls(self) -> list[str]:
        """Retorna todas as URLs cadastradas no banco."""
        return list(self.__banco.keys())

    # ------------------------------------------------------------------
    # Cadastro de novas URLs
    # ------------------------------------------------------------------

    def cadastrar_url(self, url: str, subpaginas: list[str] = None) -> bool:
        """
        Cadastra uma nova URL no banco em memória.

        Não grava no arquivo; use salvar_no_arquivo() para persistir.

        Args:
            url:        URL base a ser cadastrada.
            subpaginas: Lista opcional de links internos (ex: ['/tsi']).

        Returns:
            True se cadastrada com sucesso, False se já existia.
        """
        if url in self.__banco:
            return False
        self.__banco[url] = subpaginas if subpaginas else []
        return True

    def salvar_no_arquivo(self, caminho: str) -> None:
        """
        Grava o estado atual do banco no arquivo de URLs.

        Args:
            caminho: Caminho do arquivo a ser sobrescrito.
        """
        with open(caminho, "w", encoding="utf-8") as arquivo:
            for url, subpaginas in self.__banco.items():
                if subpaginas:
                    linha = f"{url} {' '.join(subpaginas)}\n"
                else:
                    linha = f"{url}\n"
                arquivo.write(linha)

    # ------------------------------------------------------------------
    # Representação
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return f"BancoURL({len(self.__banco)} URLs cadastradas)"
