"""
Módulo do histórico de navegação.

Implementa uma pilha (LIFO) para registrar as páginas visitadas.
A estrutura garante que o comando #back sempre retorne à página
visitada imediatamente antes da atual.
"""


class Historico:
    """Pilha de URLs visitadas pelo navegador."""

    def __init__(self):
        self.__historico: list[str] = []

    def adicionar(self, url: str) -> None:
        """
        Empilha uma URL no histórico.

        Args:
            url: Endereço da página a ser registrada.
        """
        self.__historico.append(url)

    # mantém o nome antigo para não quebrar chamadas existentes
    adcionar = adicionar

    def remover(self) -> None:
        """
        Remove (desempilha) a URL do topo do histórico.

        Raises:
            IndexError: Se o histórico estiver vazio.
        """
        if self.historico_vazio():
            raise IndexError("Não é possível remover: histórico vazio.")
        self.__historico.pop()

    def url_atual(self) -> str:
        """
        Retorna a URL no topo da pilha sem removê-la.

        Returns:
            A URL mais recentemente adicionada.

        Raises:
            ValueError: Se o histórico estiver vazio.
        """
        if self.historico_vazio():
            raise ValueError("Histórico vazio.")
        return self.__historico[-1]

    def historico_vazio(self) -> bool:
        """Retorna True se o histórico não tiver nenhuma URL."""
        return len(self.__historico) == 0

    def exibir_historico(self) -> None:
        """
        Imprime as URLs do histórico do mais recente para o mais antigo.
        """
        for url in reversed(self.__historico):
            print(f"  [{url}]")

    def __str__(self) -> str:
        """Retorna o histórico em linha, do mais antigo ao mais recente."""
        return "".join(f"[{url}]" for url in self.__historico)
