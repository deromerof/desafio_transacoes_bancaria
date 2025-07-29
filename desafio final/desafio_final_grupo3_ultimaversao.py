# -----------------------
# depencies
# -----------------------
import json
import os
import uuid
import random
import sys

# -----------------------
# load settings
# -----------------------
sys.path.append('./data/')
from data import settings

# -----------------------
# SYSTEM functions
# -----------------------
# não alterar nada das funções de system
def gera_transacao(categoria):
    return {
        "UUID": str(uuid.uuid4()),
        "valor": round(random.uniform(1.0, 1000.0), 2),  # Preço aleatório entre 1 e 1000
        "categoria": categoria
    }

def criar_transacoes(proporcao_categorias, num_transacoes=1,  categoria=None, seed=settings.seed):
    assert sum([proporcao_categorias[k] for k in proporcao_categorias])==1, '`proporcao_categorias` não soma 100%! Favor rever.'

    # garantir reprodutibilidade dos valores
    random.seed(seed)

    # Insere as transações para uma determinada categoria.
    if categoria:
        return [gera_transacao(categoria) for _ in range(0, num_transacoes)]

    # Calcula o número de transações por categoria com base na proporção
    numero_transacoes_por_categoria = {categoria: int(num_transacoes * proporcao) for categoria, proporcao in proporcao_categorias.items()}

    # Gera as transações
    transacoes = []
    for categoria, quantidade in numero_transacoes_por_categoria.items():
        for _ in range(quantidade):
            transacoes.append(gera_transacao(categoria))

    return transacoes

def salvar_json(transacoes, path2save, filename):
    # create path if not exist
    if not os.path.exists(path2save):
        os.makedirs(path2save)
    with open(os.path.join(path2save,filename), "w") as file:
        json.dump(transacoes, file, indent=4)
    print(f"Arquivo salvo em: {os.path.abspath(os.path.curdir)+'/'+path2save+'/'+filename}")

def criar_bd(num_transacoes:int = 10000, proporcao_categorias:list = settings.categorias_proporcao, path2save="./data", filename='transactions.json'):
    salvar_json(criar_transacoes(num_transacoes=num_transacoes,  proporcao_categorias=proporcao_categorias),
                path2save, filename
    )

def load_bd(filepath='./data/transactions.json'):
    with open(filepath, "r") as file:
        bd = json.load(file)
    return bd

def tela_inicial():
    print("Bem-vindo <teu nome inteiro aqui>!")
    print('conta: 0000001-0')
    print("\nEste programa permite gerenciar transações de sua conta pessoal.")
    print("\nEscolha uma das opções abaixo:")
    print("1. Visualizar relatórios")
    print("2. Cadastrar transações")
    print("3. Editar transações")
    print("4. Excluir transações")
    print("5. Consultar transação por ID")
    print("-" * 10)
    print("0. Sair")
    print('\n')

# -----------------------
# PROGRAM functions
# -----------------------
# pode editar como quiser as funções abaixo! Somente não altere os nomes das funções.
# para alterar as funções abaixo, basta apagar o `pass` e preencher com as instruções.

def run():
    """
    Esta é a função principal que vai rodar o programa
    """
    # exibe a tela inicial
    tela_inicial()

def visualizar_relatorios():
    """
    Mostra um menu de opcoes no qual gera relatórios com base na escolha do usuário.
    """
    print("\n## Você escolheu a opção: Visualizar Relatório ##")
    print("Escolha uma das opções abaixo:")
    print("1. Valor total das transações efetuadas")
    print("2. Todas as 5 últimas transações (m5)")
    print("3. Visualizar as 5 últimas transações")
    print("4. Visualizar média de gastos gerais")
    print("-" * 10)
    print("0. Retornar ao menu anterior")
    print('\n')
    op = input("Digite o número da opção desejada: ")
    return op

def salvar_relatorio(conteudo_relatorio, nome_arquivo):
    """
    Salva o relatório gerado em .txt
    """
    path2save = "./reports"
    if not os.path.exists(path2save):
        os.makedirs(path2save)
    filepath = os.path.join(path2save, nome_arquivo)
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(conteudo_relatorio)
        print(f"✅ Relatório salvo em: {os.path.abspath(filepath)}")
    except Exception as e:
        print(f"❌ Erro ao salvar o relatório: {e}")


def calcular_total_transacoes(transacoes, categoria=None):
           total = sum(float(t['valor']) for t in transacoes if categoria is None or t.get('categoria') == categoria)
           return total


def mostrar_m5_transacoes():
    """
    Mostra as m5 transações realizadas, sendo m parâmetro que deve ser adicionada à função.
    \nm : 'max','min','median', sendo
    \n\t'max' mostra os top 5 maior valor,
    \n\t'min' mostra os top 5 menor valor,
    \n\t'median' mostra os top 5 valores próximos a média

    Utilize essa mesma função para o caso `por categoria`
    """
    try:
        transacoes = load_bd()
    except FileNotFoundError:
        print("❌ Nenhum banco de dados encontrado.")
        return

    if not transacoes:
        print("❌ Nenhuma transação cadastrada.")
        return

    relatorio = ""

    # Top 5 MAIORES
    top_max = sorted(transacoes, key=lambda x: x['valor'], reverse=True)[:5]
    relatorio += "\n🔺 Top 5 transações com MAIOR valor:\n"
    relatorio += "-" * 50 + "\n"
    for t in top_max:
        relatorio += f"{t['UUID'][:8]}...\t{t['categoria']:<10}\tR$ {t['valor']:,.2f}\n".replace('.', ',')

    # Top 5 MENORES
    top_min = sorted(transacoes, key=lambda x: x['valor'])[:5]
    relatorio += "\n🔻 Top 5 transações com MENOR valor:\n"
    relatorio += "-" * 50 + "\n"
    for t in top_min:
        relatorio += f"{t['UUID'][:8]}...\t{t['categoria']:<10}\tR$ {t['valor']:,.2f}\n".replace('.', ',')

    # Top 5 mais próximas da MÉDIA
    media = sum(t['valor'] for t in transacoes) / len(transacoes)
    top_median = sorted(transacoes, key=lambda x: abs(x['valor'] - media))[:5]
    relatorio += f"\n📊 Top 5 transações mais próximas da MÉDIA (R$ {media:,.2f}):\n".replace('.', ',')
    relatorio += "-" * 50 + "\n"
    for t in top_median:
        relatorio += f"{t['UUID'][:8]}...\t{t['categoria']:<10}\tR$ {t['valor']:,.2f}\n".replace('.', ',')

    # Exibe tudo na tela
    print(relatorio)

    # Pergunta se deseja salvar
    resposta = input("\nDeseja salvar este relatório em um arquivo .txt? (S/N): ").strip().lower()
    if resposta in ['s', 'sim']:
        try:
            with open("relatorio_top5.txt", "w", encoding="utf-8") as f:
                f.write(relatorio)
            print("✅ Relatório salvo com sucesso como 'relatorio_top5.txt'")
        except:
            print("❌ Erro ao salvar o relatório.")
    else:
        print("Voltando ao menu principal...")



def calcular_media():
    """
    Calcula a média dos valores das transações.
    Utilize essa mesma função para o caso `por categoria`
    """
    print("\n--- Cálculo da Média dos Valores ---")

    try:
        transacoes = load_bd()
    except FileNotFoundError:
        print("❌ Nenhuma transação encontrada. O banco de dados está vazio.")
        return

    if not transacoes:
        print("❌ Nenhuma transação encontrada.")
        return

    soma = 0
    for t in transacoes:
        soma += t['valor']

    media = soma / len(transacoes)

    print(f"✅ A média dos valores é: R$ {media:,.2f}".replace('.', ','))


def consultar_transacao_por_ID():
    """
    Consulta uma transação específica usando apenas o UUID como identificador.
    """
    print("\n--- Consultar Transação por UUID ---")
    uuid_procurado = input("Digite o UUID da transação: ").strip().lower()

    try:
        transacoes = load_bd()
    except FileNotFoundError:
        print("❌ Nenhuma transação encontrada.")
        return

    for transacao in transacoes:
        uuid_salvo = str(transacao.get("UUID", "")).strip().lower()
        if uuid_salvo == uuid_procurado:
            print("\n✅ Transação encontrada:")
            print(f"UUID: {transacao['UUID']}")
            print(f"Categoria: {transacao.get('categoria', 'N/A')}")
            print(f"Valor: R$ {transacao['valor']:,.2f}".replace(".", ","))
            return

    print("❌ Nenhuma transação encontrada com esse UUID.")


def cadastrar_transacao():
    print("\n--- Cadastro de Nova Transação ---")

    print("\n--- Cadastro de Nova Transação ---")

    # Pede os dados ao usuário
    categoria = input("Digite a categoria da transação (ex: alimentação, transporte): ")

    # Tratamento do erro - para garantir que o usuário digite um número válido
    while True:
        valor_texto = input("Digite o valor da transação (ex: 250,00): ")
        try:
            valor = float(valor_texto.replace(",", "."))
            break
        except ValueError:
            print("❌ Valor inválido! Digite apenas números com vírgula para os centavos (ex: 99,90).")

    # Cria um dicionário com os dados da transação
    transacao = {
        "UUID": str(uuid.uuid4()),  # Gera um ID único automático
        "categoria": categoria,
        "valor": round(valor, 2)
    }

    # Tenta carregar transações existentes
    try:
        transacoes = load_bd()
    except FileNotFoundError:
        transacoes = []

    # Adiciona nova transação à lista
    transacoes.append(transacao)

    # Salva a lista atualizada
    salvar_json(transacoes, "./data", "transactions.json")

    print("\n✅ Transação cadastrada com sucesso!")
    print(transacao)
    """

    # Pede os dados ao usuário
    categoria = input("Digite a categoria da transação (ex: alimentação, transporte): ")

    # Tratamento do erro - para garantir que o usuário digite um número válido
    while True:
        valor_texto = input("Digite o valor da transação (ex: 250,00): ")
        try:
            valor = float(valor_texto.replace(",", "."))
            break
        except ValueError:
            print("❌ Valor inválido! Digite apenas números com vírgula para os centavos (ex: 99,90).")

    novo_uuid = str(uuid.uuid4())  # Gera UUID v4

    transacao = {
        "UUID": novo_uuid,
        "categoria": categoria,
        "valor": round(valor, 2)
    }


    # Adiciona à base de dados e salva
    bd.append(transacao)


    # Salva no arquivo
    try:
        with open('./data/transactions.json', 'w', encoding='utf-8') as arquivo:
            json.dump(bd, arquivo, ensure_ascii=False, indent=4)
        print("✅ Transação cadastrada com sucesso!")
        print(f"🔑 UUID: {novo_uuid}")
    except Exception as e:
        print(f"❌ Erro ao salvar a transação: {e}")
"""


def exibir_menu(transacoes):
    while True:
        print("\n--- MENU DE TRANSAÇÕES ---")
        print("1. Ver total geral de transações")
        print("2. Ver total por categoria")
        print("3. Sair")
        opcao = input("Escolha uma opção (1-3): ")
        if opcao == '1':
            total = calcular_total_transacoes(transacoes)
            print(f"💰 Total geral das transações: R$ {total:.2f}")
        elif opcao == '2':
            categoria = input("Digite o nome da categoria: ")
            total = calcular_total_transacoes(transacoes, categoria)
            print(f"📂 Total da categoria '{categoria}': R$ {total:.2f}")
        elif opcao == '3':
            print("👋 Saindo do menu. Até mais!")
            break
        else:
            print("⚠️ Opção inválida. Tente novamente.")


    # Tenta carregar transações existentes
    try:
        transacoes = load_bd()
    except FileNotFoundError:
        transacoes = []

    # Adiciona nova transação à lista
    transacoes.append(transacao)

    # Salva a lista atualizada
    salvar_json(transacoes, "./data", "transactions.json")

    print("\n✅ Transação cadastrada com sucesso!")
    print(transacao)


def editar_transacao_por_ID(): # Editado por Bernardo
    """
    Edita uma transação específica pelo seu UUID.
    """
    print("\n--- Editar Transação por ID ---") # Pede o UUID da transação a ser editada removendo espaços em branco
    uuid_editar = input("Digite o UUID da transação que deseja editar: ").strip()

    try:
        transacoes = load_bd(filepath='./data/transactions.json')
    except FileNotFoundError: # Carrega as transações do arquivo JSON e trata a exceção caso o arquivo não exista
        print("\n--- Nenhuma transação encontrada ---")
        return

    for transacao in transacoes:
        if transacao.get("UUID") == uuid_editar:
            print(f"Transação encontrada: {transacao}") # Mostra os dados atuais da transação
            nova_categoria = input(f"Nova categoria (atual: {transacao['categoria']}) ou Enter para manter: ").strip()
            novo_valor = input(f"Novo valor (atual: R$ {transacao['valor']:,.2f}) ou Enter para manter: ").strip()
            # Pede a nova categoria e o novo valor ao usuário, mantendo os valores atuais se o usuário pressionar Enter

            transacao_editada = transacao.copy() # Fazendo uma cópia para confirmar antes de salvar
            if nova_categoria:
                transacao_editada['categoria'] = nova_categoria # Atualiza a categoria se o usuário fornecer um novo valor
            if novo_valor:
                try: # Verifica se o valor é válido, transforma para float e troca vírgula por ponto
                    transacao_editada['valor'] = round(float(novo_valor.replace(",", ".")), 2)
                except ValueError:
                    print("--- Valor inválido! Mantendo valor anterior ---")

            # Mostra a transação editada antes de confirmar
            print("\nTransação editada (prévia):")
            print(transacao_editada)
            confirmar = input("Deseja salvar as alterações? (S/N): ").strip().lower()
            if confirmar in ['s', 'sim']:
                transacao.update(transacao_editada)
                # Salva a lista de transaçções atualizadas no arquivo JSON
                salvar_json(transacoes, "./data", "transactions.json")
                print("\n✅ Transação editada com sucesso!")
                print(transacao) # Mostra a transação editada e mensagem de sucesso
            else:
                print("Alterações descartadas.")
            return

    print("--- Nenhuma transação encontrada com esse UUID. ---") # Caso não encontre a transação com o UUID fornecido

def excluir_transacao(): # Editado por Bernardo
    """
    Exclui uma transação específica pelo UUID.
    """
    print("\n--- Excluir Transação ---") # Pede o UUID a ser excluído removendo espaços em branco
    uuid_excluir = input("Digite o UUID da transação que deseja excluir: ").strip()

    try:
        transacoes = load_bd(filepath='./data/transactions.json')
    except FileNotFoundError: # Tratamento de exceção para caso não exista o arquivo
        print("\n--- Nenhuma transação encontrada ---")
        return

    # Busca a transação pelo UUID
    transacao_encontrada = None
    for t in transacoes:
        if t.get("UUID") == uuid_excluir:
            transacao_encontrada = t
            break # Para o loop se encontrar a transação

    if not transacao_encontrada: # Caso não encontre a transação
        print("--- Nenhuma transação encontrada com esse UUID ---")
        return

    # Mostra os dados da transação encontrada
    print(f"Transação encontrada: {transacao_encontrada}") # Mostra os dados atuais da transação

    # Pede confirmação do usuário para excluir a transação
    confirmar = input("Deseja realmente excluir esta transação? (S/N): ").strip().lower()
    if confirmar not in ['s', 'sim']:
        print("Exclusão cancelada pelo usuário.")
        return

    # Remove a transação da lista e salva o JSON atualizado
    transacoes.remove(transacao_encontrada)
    salvar_json(transacoes, "./data", "transactions.json")
    print("\n✅ Transação excluída com sucesso!")

# -----------------------
# MAIN SCRIPT
# -----------------------
# não alterar nada abaixo
if __name__ == "__main__":

    # -----------------------
    # NÃO ALTERAR ESTE BLOCO
    # -----------------------
    # criar o banco de dados caso ele não exista
    print(os.path.abspath('.'))
    if not os.path.exists('./data/transactions.json'):
        criar_bd()

    # load bd
    bd = load_bd()
    # -----------------------

    # -----------------------
    # ABAIXO PODE ALTERAR
    # -----------------------
    #limpar console (opcional)
    os.system('cls' if os.name == 'nt' else 'clear')


    # inicia o programa
while True:
        tela_inicial()
        opcao_menu = input("Digite o número da opção desejada: ")

        if opcao_menu == '0':
            print("Encerrando o programa. Até logo!")
            break


#OPÇÃO 1 DO MENU - VISUALIZAR RELATÓRIO
        elif opcao_menu == '1':  # Visualizar relatórios
            while True:
                opcao_relatorio = visualizar_relatorios()

                match opcao_relatorio:
                    case '1':
                        print("\n📊 Opção selecionada: Valor total das transações efetuadas")

                        try:
                             transacoes = load_bd()
                             if not transacoes:
                                 print("❌ Nenhuma transação encontrada no banco de dados.")
                                 continue

                        except (FileNotFoundError, json.JSONDecodeError):
                             print("❌ Nenhuma transação encontrada.")
                             continue

                        categoria = input("Deseja filtrar por categoria? Se sim, digite o nome (ou pressione Enter para somar todas): ").strip()

                        try:
                            # Filtra se necessário

                            transacoes_filtradas = (
                                transacoes if categoria == ""
                                else [t for t in transacoes if t.get("categoria") == categoria]
                            )
                            total = calcular_total_transacoes(transacoes_filtradas)
                            quantidade = len(transacoes_filtradas)
                        except Exception as e:
                            print(f"❌ Erro ao calcular total: {e}")
                            continue


                        # Exibe na tela
                        relatorio_str = ""
                        if categoria == "":
                            relatorio_str += f"\n💰 Total de todas as transações: R$ {total:,.2f}".replace(".", ",") + "\n"
                            relatorio_str += f"📦 Quantidade de transações: {quantidade}"
                        else:
                            relatorio_str += f"\n📂 Total da categoria '{categoria}': R$ {total:,.2f}".replace(".", ",") + "\n"
                            relatorio_str += f"📦 Quantidade de transações na categoria '{categoria}': {quantidade}"

                        print(relatorio_str) # Imprime o relatório no console

                        # Pergunta se o usuário deseja salvar o relatório
                        salvar_opcao = input("\nDeseja salvar este relatório em um arquivo de texto? (S/N): ").strip().lower()
                        if salvar_opcao in ['s', 'sim']:
                            nome_arquivo = input("Digite o nome do arquivo (ex: relatorio_total.txt): ").strip()
                            if not nome_arquivo.endswith(".txt"):
                                nome_arquivo += ".txt"
                            salvar_relatorio(relatorio_str, nome_arquivo)
                        continue

                    case '2':
                        print("Opção selecionada: todas as 5 últimas transações (m5)\n")
                        mostrar_m5_transacoes()
                        continue
                 
                    
                    
                    case '3':
                        print("Opção selecionada: Visualizar as 5 últimas transações\n")
                        
                        try:
                            transacoes = load_bd()
                            if not transacoes:
                                print("❌ Nenhuma transação encontrada no banco de dados.")
                                continue
                        except (FileNotFoundError, json.JSONDecodeError):
                            print("❌ Erro ao carregar as transações.")
                            continue

                        # Seleciona as 5 últimas transações

                        ultimas_transacoes = transacoes[-5:]

                        print("\n🧾 Últimas 5 transações registradas:")
                        for i, transacao in enumerate(ultimas_transacoes, start=1):
                            uuid = transacao.get("UUID", "N/A")
                            categoria = transacao.get("categoria", "Não especificada")
                            valor = transacao.get("valor", 0.0)
                            print(f"{i}. UUID: {uuid}")
                            print(f"   Categoria: {categoria}")
                            print(f"   Valor: R$ {valor:,.2f}".replace(".", ","))
                            print("-" * 40)
                        
                        # Soma dos 5 valores
    
                        total_5 = calcular_total_transacoes(ultimas_transacoes)
                        print(f"\n💰 Soma total das últimas 5 transações: R$ {total_5:,.2f}".replace(".", ","))

                        continue

                    case '4':
                        print("Opção selecionada: média de gastos gerais\n")
                        calcular_media()
                        continue                    
                    
                    case '0':
                        print("Retornando ao menu principal...\n")
                        break
                    case _:
                        print("Opção inválida. Tente novamente.")
                        continue

#OPÇÃO 2 DO MENU - CADASTRAR
        elif opcao_menu == '2': # Cadastrar Transações
            print("Opção selecionada: Cadastrar transações")
            while True:
                confirmar = input("Deseja realmente cadastrar uma nova transação? (S/N): ").strip().lower() #opção de escolha ao usuário
                if confirmar in ['s', 'sim']:
                    cadastrar_transacao()
                    break
                elif confirmar in ['não', 'nao', 'n']:
                    print("Retornando ao menu principal...")
                    tela_inicial()
                    break
                else:
                   print("❌ Opção inválida! Digite 'sim' ou 'não'.")

#OPÇÃO 3 DO MENU - EDITAR TRANSAÇÃO

        elif opcao_menu == '3':
            print("Opção selecionada: Editar transações")
            while True:
                confirmar = input("Deseja realmente editar uma nova transação? (S/N): ").strip().lower() #opção de escolha ao usuário
                if confirmar in ['s', 'sim']:
                    editar_transacao_por_ID()
                    break
                elif confirmar in ['não', 'nao', 'n']:
                    print("Retornando ao menu principal...")
                    tela_inicial()
                    break
                else:
                   print("❌ Opção inválida! Digite 'sim' ou 'não'.")



#OPÇÃO 4 DO MENU - EXCLUIR TRANSAÇÃO
        elif opcao_menu == '4':
            print("Opção selecionada: Excluir transações")
            while True:
                confirmar = input("Deseja realmente excluir uma transação? (S/N): ").strip().lower() #opção de escolha ao usuário
                if confirmar in ['s', 'sim']:
                    excluir_transacao() # Chamando a função de exclusão
                    break
                elif confirmar in ['não', 'nao', 'n']:
                    print("Retornando ao menu principal...")
                    tela_inicial()
                    break
                else:
                   print("❌ Opção inválida! Digite 'sim' ou 'não'.")


#OPÇÃO 5 DO MENU - CONSULTA ID
        elif opcao_menu == '5':
            print("Opção selecionada: Consultar transação por ID")
            while True:
                confirmar = input("Deseja realmente consultar uma transação? (S/N): ").strip().lower() #opção de escolha ao usuário
                if confirmar in ['s', 'sim']:
                    consultar_transacao_por_ID()
                    break
                elif confirmar in ['não', 'nao', 'n']:
                    print("Retornando ao menu principal...")
                    tela_inicial()
                    break
                else:
                    print("❌ Opção inválida! Digite 'sim' ou 'não'.")


#OPCAO 6 DO MENU - calcular_total_transacoes
        elif opcao_menu == '6':
            print("Opção selecionada: calcular_total_transacoes")
            try:
                transacoes = load_bd()
            except FileNotFoundError:
                 print("❌ Nenhuma transação encontrada.")
                 continue

            categoria = input("Deseja filtrar por categoria? Se sim, digite o nome (ou pressione Enter para somar todas): ").strip()

            if categoria == "":
                total = calcular_total_transacoes(transacoes)
            else:
                total = calcular_total_transacoes(transacoes, categoria)

            print(f"\n💰 Total das transações: R$ {total:,.2f}".replace(".", ","))



#OPÇÃO INVÁLIDA
        else:
            print("Opção inválida. Tente novamente.")

# Execução do programa
# -------------------------------
run()