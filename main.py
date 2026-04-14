# importa as classes do projeto
from historico import Historico
from banco_url import banco_url
from browser import Browser

def main():
    # cria os objetos principais
    historico = Historico()
    banco = banco_url()

    meu_browser = Browser(historico, banco)

    # carrega as urls do arquivo
    try:
        banco.ler_arquivo("urls.txt")
    except Exception as erro:
        print(f"Erro ao carregar urls: {erro}")

    # loop principal
    while True:
        try:
            meu_browser.exibir_estado()

            # recebe comando do usuário
            comando = input("Digite URL ou comando: ")

            # encerra o navegador
            if comando == "#sair":
                print("Encerrando navegador...")
                break

            # volta para página anterior
            elif comando == "#back":
                meu_browser.voltar()

            # mostra histórico
            elif comando == "#showhist":
                if historico.historico_vazio():
                    print("Histórico vazio")
                else:
                    historico.exibir_historico()

            # adiciona nova url apenas ao histórico
            elif comando.startswith("#add "):
                url = comando.replace("#add ", "")
                historico.adcionar(url)
                print("URL adicionada ao histórico")

            # adiciona nova url ao arquivo e ao banco
            elif comando.startswith("#adicionar "):
                url = comando.replace("#adicionar ", "")

                with open("urls.txt", "a", encoding="utf-8") as arquivo:
                    arquivo.write(f"\n{url}")

                # recarrega as urls do arquivo
                banco.ler_arquivo("urls.txt")

                print("URL adicionada ao arquivo")

            # remove url do arquivo e atualiza o banco
            elif comando.startswith("#remover "):
                url = comando.replace("#remover ", "")

                # lê todas as linhas do arquivo
                with open("urls.txt", "r", encoding="utf-8") as arquivo:
                    linhas = arquivo.readlines()

                # reescreve sem a url removida
                with open("urls.txt", "w", encoding="utf-8") as arquivo:
                    for linha in linhas:
                        if linha.strip() != url:
                            arquivo.write(linha)

                # recarrega as urls do arquivo
                banco.ler_arquivo("urls.txt")

                print("URL removida do arquivo")

            # navegação normal
            else:
                meu_browser.navegar(comando)

        # tratamento de erro
        except Exception as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    main()