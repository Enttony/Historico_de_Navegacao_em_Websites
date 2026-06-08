"""
Ponto de entrada principal do simulador de navegação web.

Responsável por:
    - Inicializar os objetos do sistema
    - Carregar o banco de URLs do arquivo
    - Executar o loop principal de interação com o usuário
    - Despachar cada comando para o método correto
"""

from historico import Historico
from banco_url import BancoURL
from browser import Browser

# Arquivo com as URLs cadastradas
ARQUIVO_URLS = "urls.txt"


def exibir_ajuda() -> None:
    """Exibe a lista de todos os comandos disponíveis no sistema."""
    print("\n" + "=" * 50)
    print("              AJUDA — COMANDOS")
    print("=" * 50)
    comandos = [
        ("#help",             "Exibe esta mensagem de ajuda"),
        ("#back",             "Volta para a última página visitada"),
        ("#showhist",         "Mostra o histórico de páginas"),
        ("#adicionar",        "Cadastra uma nova URL (modo interativo)"),
        ("#remover <url>",    "Remove uma URL do banco e do arquivo"),
        ("#sair",             "Encerra o navegador"),
        ("<url>",             "Navega para uma URL completa"),
        ("/<link>",           "Acessa um link interno da página atual"),
    ]
    for cmd, desc in comandos:
        print(f"  {cmd:<22} → {desc}")
    print("=" * 50)


def main() -> None:
    """Função principal: inicializa o sistema e roda o loop de interação."""

    # ---------- inicialização ----------
    historico = Historico()
    banco = BancoURL()
    browser = Browser(historico, banco)

    try:
        banco.ler_arquivo(ARQUIVO_URLS)
    except FileNotFoundError as erro:
        print(f"Aviso: {erro}")
        print("O sistema iniciará sem URLs pré-cadastradas.\n")

    # ---------- loop principal ----------
    while True:
        try:
            browser.exibir_estado()
            entrada = input("  url: ").strip()

            # --- comandos especiais ---

            if entrada == "#sair":
                print("\n  Encerrando navegador. Até mais!\n")
                break

            elif entrada == "#help":
                exibir_ajuda()

            elif entrada == "#back":
                browser.voltar()

            elif entrada == "#showhist":
                print()
                if historico.historico_vazio():
                    print("  Histórico vazio.")
                else:
                    print("  Histórico (mais recente → mais antigo):")
                    historico.exibir_historico()

            elif entrada == "#adicionar":
                browser.cadastrar_url_interativo(ARQUIVO_URLS)

            elif entrada.startswith("#remover "):
                url_remover = entrada.replace("#remover ", "", 1).strip()
                if not banco.url_existe(url_remover):
                    print(f"\n  ✗ URL '{url_remover}' não encontrada no banco.")
                else:
                    # remove do banco em memória e regrava o arquivo
                    urls_restantes = {
                        u: banco.get_subpaginas(u)
                        for u in banco.listar_urls()
                        if u != url_remover
                    }
                    # recria o banco sem a url removida
                    novo_banco = BancoURL()
                    for u, subs in urls_restantes.items():
                        novo_banco.cadastrar_url(u, subs)
                    novo_banco.salvar_no_arquivo(ARQUIVO_URLS)
                    banco.ler_arquivo(ARQUIVO_URLS)
                    print(f"\n  ✔ URL '{url_remover}' removida com sucesso.")

            elif entrada.startswith("#"):
                print(f"\n  ✗ Comando '{entrada}' não reconhecido.")
                print("     Digite #help para ver os comandos disponíveis.")

            # --- navegação (URL completa ou link interno) ---
            elif entrada:
                browser.navegar(entrada)

        except KeyboardInterrupt:
            print("\n\n  Navegador encerrado pelo usuário.\n")
            break
        except Exception as erro:
            print(f"\n  Erro inesperado: {erro}")


if __name__ == "__main__":
    main()
