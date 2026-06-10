"""
Módulo que representa o navegador (Browser).

Responsável por:
    - Manter o estado da página atual (home)
    - Coordenar a navegação com o histórico
    - Consultar o banco de URLs
    - Exibir o conteúdo das páginas (.txt) e os links disponíveis
    - Resolver navegação por links internos (que começam com '/')
"""

import os
from historico import Historico
from banco_url import BancoURL


# Pasta onde ficam os arquivos .txt de conteúdo das páginas
PASTA_PAGINAS = "paginas"


class Browser:
    """Simula um navegador web com histórico e suporte a subpáginas."""

    def __init__(self, historico: Historico, banco: BancoURL):
        self.__historico = historico
        self.__banco = banco
        self.__home = ""  # vazio: ainda não visitou nenhuma página

    @property
    def home(self) -> str:
        return self.__home


    def navegar(self, entrada: str) -> None:
        """
        Processa a entrada do usuário e realiza a navegação.

        Dois casos:
            1. Entrada começa com '/' → link interno da página atual.
               A URL alvo é: home_atual + entrada
            2. Qualquer outra coisa → URL completa digitada pelo usuário.

        Args:
            entrada: String digitada pelo usuário no campo de URL.
        """
        entrada = entrada.strip()

        if entrada.startswith("/"):
            self._navegar_interno(entrada)
        else:
            self._navegar_url(entrada)

    def _navegar_url(self, url: str) -> None:
        """Navega para uma URL completa."""
        if not self.__banco.url_existe(url):
            print(f"\n  ✗ Erro 404 — Página '{url}' não encontrada.")
            return

        # guarda a página atual no histórico antes de sair dela
        if self.__home:
            self.__historico.adcionar(self.__home)

        self.__home = url
        self._exibir_pagina()

    def _navegar_interno(self, link: str) -> None:
        """
        Navega para um link interno da página atual.

        O link digitado (ex: '/tsi') é concatenado à home atual
        para formar a URL completa (ex: 'www.ifpb.edu.br/tsi').
        """
        if not self.__home:
            print("\n  ✗ Você ainda não está em nenhuma página.")
            print("     Digite uma URL completa primeiro.")
            return

        url_alvo = self.__home + link

        if not self.__banco.url_existe(url_alvo):
            print(f"\n  ✗ Erro 404 — Link '{link}' não existe nesta página.")
            return

        if self.__home:
            self.__historico.adcionar(self.__home)

        self.__home = url_alvo
        self._exibir_pagina()

    # ------------------------------------------------------------------
    # Voltar (#back)
    # ------------------------------------------------------------------

    def voltar(self) -> None:
        """
        Retorna à última página visitada (remove do histórico).
        """
        if self.__historico.historico_vazio():
            print("\n  ✗ Histórico vazio — não há página anterior.")
            return

        pagina_anterior = self.__historico.url_atual()
        self.__historico.remover()
        self.__home = pagina_anterior

        print(f"\n  ← Voltando para: {self.__home}")
        self._exibir_pagina()

    # ------------------------------------------------------------------
    # Exibição de conteúdo
    # ------------------------------------------------------------------

    def _exibir_pagina(self) -> None:
        """
        Exibe o conteúdo da página atual e seus links internos.

        Busca o arquivo .txt correspondente à URL em PASTA_PAGINAS.
        O nome do arquivo é derivado da URL, substituindo '/' por '_'.
        """
        print(f"\n  ✔ Página encontrada!")
        print(f"  URL: {self.__home}\n")

        # monta o nome do arquivo: www.ifpb.edu.br/tsi → www.ifpb.edu.br_tsi.txt
        nome_arquivo = self.__home.replace("/", "_") + ".txt"
        caminho = os.path.join(PASTA_PAGINAS, nome_arquivo)

        print("  " + "-" * 44)
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                for linha in f:
                    print(f"  {linha}", end="")
        else:
            print("  [Conteúdo não disponível para esta página]")
        print("\n  " + "-" * 44)

        # exibe links internos disponíveis
        subpaginas = self.__banco.get_subpaginas(self.__home)
        if subpaginas:
            print("  Links disponíveis:")
            for sub in subpaginas:
                print(f"    {sub}")
        else:
            print("  Sem links internos nesta página.")

    def exibir_estado(self) -> None:
        """Exibe o cabeçalho do browser com histórico e home atual."""
        print("\n" + "=" * 50)
        print("             NAVEGADOR  WEB")
        print("=" * 50)

        # histórico
        hist_str = str(self.__historico) if not self.__historico.historico_vazio() else "[ ]"
        print(f"  Histórico de Visitas: {hist_str}")

        # home
        home_str = self.__home if self.__home else " "
        print(f"  Home: [{home_str}]")

        print("=" * 50)
        print("  Digite a URL, /link, ou um comando (#help).")
        print("-" * 50)

    # ------------------------------------------------------------------
    # Cadastro via interface
    # ------------------------------------------------------------------

    def cadastrar_url_interativo(self, caminho_arquivo: str) -> None:
        """
        Fluxo interativo para cadastrar uma nova URL com subpáginas.

        Pergunta ao usuário a URL base e quantos/quais links internos
        deseja cadastrar. Persiste no arquivo após o cadastro.
        """
        print("\n  === Cadastrar nova URL ===")
        url = input("  URL base (ex: www.exemplo.com): ").strip()

        if not url:
            print("  ✗ URL não pode ser vazia.")
            return

        if not self.__banco.formato_valido(url):
            print("  ✗ Formato inválido. Use www., http:// ou https://")
            return

        if self.__banco.url_existe(url):
            print(f"  ✗ A URL '{url}' já está cadastrada.")
            return

        # coleta subpáginas
        subpaginas = []
        print("  Informe os links internos (ex: /tsi). ")
        print("  Deixe em branco para encerrar (máx. 2).")
        for i in range(1, 3):
            link = input(f"  Link {i}: ").strip()
            if not link:
                break
            if not link.startswith("/"):
                link = "/" + link
            subpaginas.append(link)

        # cadastra em memória e persiste
        self.__banco.cadastrar_url(url, subpaginas)
        self.__banco.salvar_no_arquivo(caminho_arquivo)

        print(f"\n  URL '{url}' cadastrada com sucesso!")
        if subpaginas:
            print(f"     Links internos: {', '.join(subpaginas)}")
