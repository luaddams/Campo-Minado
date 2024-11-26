import os
import random
import time

#Limpar o terminal de forma compatível com Windows e Unix
def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

#Cria o campo baseado na dificuldade escolhida
def criar_campo(dificuldade):
    if dificuldade == "fácil": #Cria uma matriz 5x5, esconde 5 bombas
        tamanho = 5
        bombas = 5
    elif dificuldade == "normal": #Cria uma matriz 8x8, esconde 12 bombas
        tamanho = 8
        bombas = 12
    elif dificuldade == "difícil": #Cria uma matriz 10x10, esconde 20 bombas
        tamanho = 10
        bombas = 20
    else:
        raise ValueError("Dificuldade inválida")

    jogo = [["⬜️" for i in range(tamanho)] for i in range(tamanho)]
    
    #Coloca bombas aleatoriamente na matriz
    bombas_colocadas = 0  #Contador

    while bombas_colocadas < bombas:
        linha = random.randint(0, tamanho - 1)
        coluna = random.randint(0, tamanho - 1)
        if jogo[linha][coluna] != "💣":
            jogo[linha][coluna] = "💣"
            bombas_colocadas += 1
    return jogo, tamanho

#Imprime o tabuleiro e esconde as minas
def mostra_tabuleiro(jogo, tamanho, revelar_minas=False, nome_jogador=""):
    print(f"Jogador: {nome_jogador}")

    #Cabeçalho
    print("  ", end=" ")
    for i in range(1, tamanho + 1):
        print(f"{chr(64 + i):>2} ", end="")  #Alinha as letras das colunas
    print("  ")

    for i in range(tamanho):
        print(f"{i + 1:2} ", end="")  #Alinha os números das linhas
        for j in range(tamanho):
            #Garantir que todos os símbolos ocupem o mesmo espaço
            if jogo[i][j] == "💣":
                if revelar_minas:
                    print(f"{'💣':>2} ", end="")
                else:
                    print(f"{'⬜️':>2} ", end="")
            else:
                #Para os números e células vazias, também garantir o alinhamento
                print(f"{jogo[i][j]:>2} ", end="")
        print("")

#Conta as bombas que tem nas adjacencias
def conta_bombas(jogo, linha, coluna, tamanho):
    direções = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    bombas_ao_redor = 0
    for d in direções:
        nova_linha, nova_coluna = linha + d[0], coluna + d[1]
        if 0 <= nova_linha < tamanho and 0 <= nova_coluna < tamanho:
            if jogo[nova_linha][nova_coluna] == "💣":
                bombas_ao_redor += 1
    return bombas_ao_redor

#Revela se a posição escolhida não possui bomba, conta e exibe o número de bombas ao redor da célula
def revela_celulas(jogo, linha, coluna, tamanho):
    if jogo[linha][coluna] != "⬜️":
        return
    bombas_ao_redor = conta_bombas(jogo, linha, coluna, tamanho)
    if bombas_ao_redor == 0:
        jogo[linha][coluna] = "X"
        direções = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for d in direções:
            nova_linha, nova_coluna = linha + d[0], coluna + d[1]
            if 0 <= nova_linha < tamanho and 0 <= nova_coluna < tamanho:
                revela_celulas(jogo, nova_linha, nova_coluna, tamanho)
    else:
        jogo[linha][coluna] = f"{bombas_ao_redor}"

#Verifica se o jogador ganhou, a condição é que todas as células estejam abertas sem bomba
def verifica_vitoria(jogo, tamanho):
    for i in range(tamanho):
        for j in range(tamanho):
            if jogo[i][j] == "⬜️":
                return False
    return True

#Função para salvar o jogo, onde os dados serão armazenados em um arquivo txt
def salvar_jogo(jogo, tamanho, nome_jogador, dificuldade, tempo_inicial):
    tempo_total = time.time() - tempo_inicial  #Calcula o tempo decorrido
    with open(f"salvo_{nome_jogador}.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(f"{nome_jogador}\n")
        arquivo.write(f"{dificuldade}\n")
        arquivo.write(f"{tamanho}\n")
        arquivo.write(f"{tempo_total}\n")  #Salva o tempo decorrido
        for linha in jogo:
            arquivo.write(" ".join(linha) + "\n")  #Usando espaços para separar as células
    print("\nProgresso salvo! Você pode continuar da próxima vez pela opção 'Continuar'.")
    
#Função para carregar jogo salvo
def carregar_jogo(nome_jogador):
    try:
        with open(f"salvo_{nome_jogador}.txt", "r", encoding="utf-8") as arquivo:
            nome_jogador = arquivo.readline().strip()
            dificuldade = arquivo.readline().strip()
            tamanho = int(arquivo.readline().strip())
            tempo_total = float(arquivo.readline().strip())  # Lê o tempo decorrido
            jogo = []
            for _ in range(tamanho):
                jogo.append(arquivo.readline().strip().split(" "))
        return jogo, tamanho, nome_jogador, dificuldade, tempo_total
    except FileNotFoundError:
        print("Arquivo de salvamento não encontrado.")
        return None

def excluir_jogo(nome_jogador):
    try:
        os.remove(f"salvo_{nome_jogador}.txt")
    except FileNotFoundError:
        pass

#Função para registrar o recorde incluindo a dificuldade
def registrar_recorde(nome_jogador, tempo, dificuldade):
    with open("recordes.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{nome_jogador}: {tempo:.2f} segundos | Dificuldade: {dificuldade}\n")

#Função para mostrar os recordes
def mostrar_recordes():
    try:
        with open("recordes.txt", "r", encoding="utf-8") as arquivo:
            recordes = []
            #Lê todos os recordes e armazena em uma lista
            for linha in arquivo:
                partes = linha.strip().split(" | ")
                nome_tempo = partes[0].split(": ")
                nome_jogador = nome_tempo[0]
                tempo = float(nome_tempo[1].replace(" segundos", ""))
                dificuldade = partes[1].replace("Dificuldade: ", "")
                recordes.append((nome_jogador, tempo, dificuldade))
            
            #Ordena a lista de recordes pela coluna de tempo (segundo item da tupla)
            recordes.sort(key=lambda x: x[1])

            #Exibe apenas a tabela de recordes
            print("\nRecordes (ordenados por tempo de conclusão):\n")
            print(f"{'Jogador':<20} {'Tempo (segundos)':<20} {'Dificuldade'}")
            print("-" * 60)
            for jogador, tempo, dificuldade in recordes:
                print(f"{jogador:<20} {tempo:<20.2f} {dificuldade}")
            
            #Aguardar o usuário pressionar Ctrl + C para voltar ao menu
            print("\nPressione Ctrl + C para voltar ao menu.")
            while True:
                pass  #Aguarda Ctrl + C (não faz nada até o erro ser gerado)
    except FileNotFoundError:
        print("Nenhum recorde encontrado.")
    except KeyboardInterrupt:
        print("\nVoltando ao menu principal...")
        limpar_terminal()  #Limpa a tela ao voltar ao menu
        return  #Retorna ao menu sem encerrar o programa

#Função para listar jogos salvos, onde aparecerá na opção "continuar"
def listar_jogos_salvos():
    jogos = [f for f in os.listdir() if f.startswith("salvo_") and f.endswith(".txt")]
    if not jogos:
        print("Nenhum jogo salvo encontrado!")
        return None
    print("Jogos salvos:")
    for i, jogo in enumerate(jogos, start=1):
        nome_jogador = jogo[6:-4]  #Extrai o nome do jogador do nome do arquivo
        print(f"{i}- {nome_jogador}")
    return jogos

#Lógica principal para o campo minado, que determina a jogada do usuário
def jogada(jogo, tamanho, nome_jogador, dificuldade, tempo_inicial):
    while True:
        try:
            print('Digite Ctrl + C para sair')
            x = int(input(f"Digite o número da linha (De 1 a {tamanho}): ")) - 1
            y_letra = input(f"Digite a letra da coluna (De A a {chr(64 + tamanho)}): ").strip().upper()
            if len(y_letra) != 1 or not ('A' <= y_letra <= chr(64 + tamanho)):
                raise ValueError("Coluna inválida")
            y = ord(y_letra) - 65

            if 0 <= x < tamanho and 0 <= y < tamanho:
                linha = x
                coluna = y
                if jogo[linha][coluna] == "💣":
                    mostra_tabuleiro(jogo, tamanho, revelar_minas=True, nome_jogador=nome_jogador)
                    print("\n💣💣💣 Você explodiu! 💣💣💣")
                    try:
                        os.remove(f"salvo_{nome_jogador}.txt")  # Tenta excluir o arquivo de salvamento
                    except FileNotFoundError:
                        print("Nenhum jogo salvo para excluir.")
                    jogo_novo = input("Jogar novamente? (s/n): ").upper()
                    if jogo_novo == "S":
                        jogo, tamanho = criar_campo(dificuldade)
                        tempo_inicial = time.time()  # Reinicia o temporizador
                        limpar_terminal()
                        mostra_tabuleiro(jogo, tamanho, nome_jogador=nome_jogador)
                    else:
                        print("Obrigado por jogar")
                        main()
                        return
                elif jogo[linha][coluna] == "⬜️":
                    revela_celulas(jogo, linha, coluna, tamanho)
                    limpar_terminal()
                    mostra_tabuleiro(jogo, tamanho, nome_jogador=nome_jogador)
                    if verifica_vitoria(jogo, tamanho):
                        mostra_tabuleiro(jogo, tamanho, revelar_minas=True, nome_jogador=nome_jogador)
                        tempo_final = time.time()
                        tempo_total = tempo_final - tempo_inicial
                        print(f"\n Parabéns, {nome_jogador}! Você venceu!")
                        print(f"Tempo total: {tempo_total:.2f} segundos")
                        registrar_recorde(nome_jogador, tempo_total, dificuldade)
                        try:
                            os.remove(f"salvo_{nome_jogador}.txt")  #Tenta excluir o arquivo de salvamento
                        except FileNotFoundError:
                            print("-")
                        main()  #Voltar ao menu principal após vencer
                        return
            else:
                print("Coordenadas fora do tabuleiro! Tente novamente.")
        except ValueError:
            print("Erro! ⚠️ Verifique o valor digitado!")
        except KeyboardInterrupt:
            salvar_jogo(jogo, tamanho, nome_jogador, dificuldade, tempo_inicial)
            main()
            break
            
#Função para continuar jogo salvo
def continuar_jogo():
    jogos = listar_jogos_salvos()
    if not jogos:
        print("Nenhum jogo salvo encontrado.")
        return False  #Retorna False se não houver jogos salvos
    while True:
        try:
            escolha = int(input("Escolha o número do jogo que deseja continuar: "))
            if 1 <= escolha <= len(jogos):
                jogo_escolhido = jogos[escolha - 1]
                nome_jogador = jogo_escolhido[6:-4]
                jogo, tamanho, nome_jogador, dificuldade, tempo_inicial = carregar_jogo(nome_jogador)
                if jogo:
                    print(f"Bem-vindo de volta, {nome_jogador}! Continuando seu jogo...")
                    limpar_terminal()
                    mostra_tabuleiro(jogo, tamanho, nome_jogador=nome_jogador)
                    tempo_inicial = time.time() - tempo_inicial  #Ajusta o tempo inicial
                    jogada(jogo, tamanho, nome_jogador, dificuldade, tempo_inicial)
                break
            else:
                print("Número inválido, tente novamente.")
        except ValueError:
            print("Entrada inválida, tente novamente.")
        except KeyboardInterrupt:
            print("\nO jogo foi encerrado.")
            return False
    
#Menu para a seleção de dificuldades
def novo_jogo(nome):
    print('1- Fácil')
    print('2- Normal')
    print('3- Difícil')
    print('4- Voltar')
    while True:
        opcao2 = input('Escolha uma opção: ')
        if opcao2 == '1':
            jogo, tamanho = criar_campo("fácil")
            tempo_inicial = time.time()
            limpar_terminal()
            mostra_tabuleiro(jogo, tamanho, nome_jogador=nome)
            jogada(jogo, tamanho, nome, "fácil", tempo_inicial)
        elif opcao2 == '2':
            jogo, tamanho = criar_campo("normal")
            tempo_inicial = time.time()
            limpar_terminal()
            mostra_tabuleiro(jogo, tamanho, nome_jogador=nome)
            jogada(jogo, tamanho, nome, "normal", tempo_inicial)
        elif opcao2 == '3':
            jogo, tamanho = criar_campo("difícil")
            tempo_inicial = time.time()
            limpar_terminal()
            mostra_tabuleiro(jogo, tamanho, nome_jogador=nome)
            jogada(jogo, tamanho, nome, "difícil", tempo_inicial)
        elif opcao2 == '4':
            main()
            break
        else:
            print('Opção inválida, escolha novamente: ')


def menu():
    print('💣    --  💣  --  💣  --  💣  --  💣  --  💣  -- 💣')
    print('--  ▄▀ ▄▀▄ █▄░▄█ █▀▄ ▄▀▄     █▄░▄█ ▀ █▄░█ ▄▀▄ █▀▄ ▄▀▄  --')
    print('--  █░ █▀█ █░█░█ █░█ █░█     █░█░█ █ █░▀█ █▀█ █░█ █░█  --')
    print('💣  ░▀ ▀░▀ ▀░░░▀ █▀░ ░▀░     ▀░░░▀ ▀ ▀░░▀ ▀░▀ ▀▀░ ░▀░  💣')
    print('-'*58)
    print('                            Feito por: Luísa Gonçalves')
    print('-'*58)
    print('1- Novo Jogo')
    print('2- Continuar')
    print('3- Recordes')
    print('4- Sair')
    opcao1 = input('Escolha uma opção: ')
    return opcao1

#Menu principal
def main():
    while True:
        try:
            op = menu()
            limpar_terminal()  
            if op == '1':
                nome = input('Digite seu nome: ')
                novo_jogo(nome)
            elif op == '2':
               if continuar_jogo() is False:  #Se o jogo foi interrompido ou não existe jogo salvo
                    continue  #Retorna ao menu sem continuar
            elif op == '3':
                mostrar_recordes()
            elif op == '4':
                print('💣 Obrigado por jogar! 💣')
                exit() 
            else:
                print('Opção inválida, tente novamente.')
        except NameError:
            print('Nenhum jogo salvo encontrado. Por favor, inicie um novo jogo.')
        except KeyboardInterrupt:
            print("\nO jogo foi encerrado.")
            break  

if __name__ == "__main__":
    main()

