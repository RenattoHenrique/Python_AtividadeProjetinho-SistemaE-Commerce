import os
import Formatação_cores

os.system("cls")


def carregar_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='UTF8') as f:
            return f.readlines()
    except:
        return []

def salvar_arquivo(nome_arquivo, dados, sobrescrever=False):
    try:
        modo = 'w' if sobrescrever else 'a+'
        with open(nome_arquivo, modo, encoding='UTF8') as f:
            f.writelines(dados)
    except Exception as e:
        print(f"{Formatação_cores.RED}Erro ao salvar o arquivo: {e}{Formatação_cores.RESET}")

def gerar_codigo(arquivo):
    registros = carregar_arquivo(arquivo)
    if registros:
        ultimo_registro = registros[-1].split(";")[0]
        return str(int(ultimo_registro) + 1)
    return "1"

def cadastrar_produto():
    os.system("cls")
    produtos = carregar_arquivo('produtos.txt')
    codigo = gerar_codigo('produtos.txt')
    nome = input("Nome do produto: ")
    descricao = input("Descrição do produto: ")

    while True:
        try:
            preco_compra = float(input("Preço de compra do produto: "))
            break
        except:
            print(f"{Formatação_cores.RED}Erro: Insira um valor numérico válido para o preço de compra.{Formatação_cores.RESET}")
    
    while True:
        try:
            preco_venda = float(input("Preço de venda do produto: "))
            break
        except:
            print(f"{Formatação_cores.RED}Erro: Insira um valor numérico válido para o preço de venda.{Formatação_cores.RESET}")

    produtos.append(f"{codigo};{nome};{descricao};{preco_compra};{preco_venda}\n")
    salvar_arquivo('produtos.txt', produtos, sobrescrever=True)
    print(f"{Formatação_cores.GREEN}Produto cadastrado com sucesso!{Formatação_cores.RESET}")

def remover_produto():
    os.system("cls")
    codigo = input("Código do produto a ser removido: ")
    produtos = carregar_arquivo('produtos.txt')
    novo_produtos = [p for p in produtos if not p.startswith(codigo)]
    
    if len(produtos) == len(novo_produtos):
        print(f"{Formatação_cores.RED}Produto não encontrado.{Formatação_cores.RESET}")
    else:
        salvar_arquivo('produtos.txt', novo_produtos, sobrescrever=True)
        salvar_arquivo('compras.txt', [c for c in carregar_arquivo('compras.txt') if not c.startswith(codigo)], sobrescrever=True)
        salvar_arquivo('vendas.txt', [v for v in carregar_arquivo('vendas.txt') if not v.startswith(codigo)], sobrescrever=True)
        print(f"{Formatação_cores.GREEN}Produto e seus registros de compras e vendas removidos com sucesso.{Formatação_cores.RESET}")

def atualizar_produto():
    os.system("cls")
    codigo = input("Código do produto a ser atualizado: ")
    produtos = carregar_arquivo('produtos.txt')
    for i, produto in enumerate(produtos):
        if produto.startswith(codigo):
            nome = input("Novo nome do produto: ")
            descricao = input("Nova descrição do produto: ")
            
            while True:
                try:
                    preco_compra = float(input("Novo preço de compra: "))
                    break
                except:
                    print(f"{Formatação_cores.RED}Erro: Insira um valor numérico válido para o preço de compra.{Formatação_cores.RESET}")

            while True:
                try:
                    preco_venda = float(input("Novo preço de venda: "))
                    break
                except:
                    print(f"{Formatação_cores.RED}Erro: Insira um valor numérico válido para o preço de venda.{Formatação_cores.RESET}")
            
            produtos[i] = f"{codigo};{nome};{descricao};{preco_compra};{preco_venda}\n"
            salvar_arquivo('produtos.txt', produtos, sobrescrever=True)
            print(f"{Formatação_cores.GREEN}Produto atualizado com sucesso.{Formatação_cores.RESET}")
            return
    print(f"{Formatação_cores.RED}Produto não encontrado.{Formatação_cores.RESET}")

def comprar_produto():
    os.system("cls")
    codigo = input("Código do produto: ")
    produtos = carregar_arquivo('produtos.txt')

    if not any(produto.startswith(codigo) for produto in produtos):
        print(f"{Formatação_cores.RED}Erro: Produto não encontrado.{Formatação_cores.RESET}")
        return

    data_compra = input("Data da compra: ")
    codigo_compra = gerar_codigo('compras.txt')

    while True:
        try:
            quantidade = int(input("Quantidade comprada: "))
            break
        except:
            print(f"{Formatação_cores.RED}Erro: Insira um valor numérico válido para a quantidade.{Formatação_cores.RESET}")

    compras = carregar_arquivo('compras.txt')
    compras.append(f"{codigo_compra};{codigo};{data_compra};{quantidade}\n")
    salvar_arquivo('compras.txt', compras, sobrescrever=True)
    print(f"{Formatação_cores.GREEN}Compra registrada com sucesso.{Formatação_cores.RESET}")

def vender_produto():
    os.system("cls")
    codigo = input("Código do produto a ser vendido: ")
    produtos = carregar_arquivo('produtos.txt')

    if not any(produto.startswith(codigo) for produto in produtos):
        print(f"{Formatação_cores.RED}Erro: Produto não encontrado.{Formatação_cores.RESET}")
        return

    data_venda = input("Data da venda: ")
    codigo_venda = gerar_codigo('vendas.txt')

    while True:
        try:
            quantidade = int(input("Quantidade a ser vendida: "))
            break
        except:
            print(f"{Formatação_cores.RED}Erro: Insira um valor numérico válido para a quantidade.{Formatação_cores.RESET}")

    compras = carregar_arquivo('compras.txt')
    vendas = carregar_arquivo('vendas.txt')

    qtd_comprada = sum(int(c.split(";")[3]) for c in compras if c.split(";")[1] == codigo)
    qtd_vendida = sum(int(v.split(";")[3]) for v in vendas if v.split(";")[1] == codigo)

    if quantidade > (qtd_comprada - qtd_vendida):
        print(f"{Formatação_cores.RED}Erro: Quantidade insuficiente para venda.{Formatação_cores.RESET}")
        return

    vendas.append(f"{codigo_venda};{codigo};{data_venda};{quantidade}\n")
    salvar_arquivo('vendas.txt', vendas, sobrescrever=True)
    print(f"{Formatação_cores.GREEN}Venda registrada com sucesso.{Formatação_cores.RESET}")

def cancelar_compra():
    os.system("cls")
    codigo = input("Código da compra a ser cancelada: ")
    compras = carregar_arquivo('compras.txt')
    novas_compras = [compra for compra in compras if not compra.startswith(codigo)]
    if len(compras) == len(novas_compras):
        print(f"{Formatação_cores.RED}Compra não encontrada.{Formatação_cores.RESET}")
    else:
        salvar_arquivo('compras.txt', novas_compras, sobrescrever=True)
        print(f"{Formatação_cores.GREEN}Compra cancelada com sucesso.{Formatação_cores.RESET}")

def cancelar_venda():
    os.system("cls")
    codigo = input("Código da venda a ser cancelada: ")
    vendas = carregar_arquivo('vendas.txt')
    novas_vendas = [venda for venda in vendas if not venda.startswith(codigo)]
    if len(vendas) == len(novas_vendas):
        print(f"{Formatação_cores.RED}Venda não encontrada.{Formatação_cores.RESET}")
    else:
        salvar_arquivo('vendas.txt', novas_vendas, sobrescrever=True)
        print(f"{Formatação_cores.GREEN}Venda cancelada com sucesso.{Formatação_cores.RESET}")

def listar_produtos():
    os.system("cls")
    produtos = carregar_arquivo('produtos.txt')
    compras = carregar_arquivo('compras.txt')
    vendas = carregar_arquivo('vendas.txt')
    
    if produtos:
        print(f"{Formatação_cores.YELLOW}Produtos cadastrados:\n{Formatação_cores.RESET}")
        for produto in produtos:
            codigo, nome, descricao, preco_compra, preco_venda = produto.strip().split(";")
            qtd_comprada = sum(int(c.split(";")[3]) for c in compras if c.split(";")[1] == codigo)
            qtd_vendida = sum(int(v.split(";")[3]) for v in vendas if v.split(";")[1] == codigo)
            preco_compra_formatado = Formatação_cores.Moeda.formatar(float(preco_compra))
            preco_venda_formatado = Formatação_cores.Moeda.formatar(float(preco_venda))
            
            print(f"{Formatação_cores.YELLOW}Código: {codigo}{Formatação_cores.RESET}")
            print(f"Nome: {nome}")
            print(f"Descrição: {descricao}")
            print(f"Preço Compra: {preco_compra_formatado}")
            print(f"Preço Venda: {preco_venda_formatado}")
            print(f"Quantidade Comprada: {qtd_comprada}")
            print(f"Quantidade Vendida: {qtd_vendida}\n")
    else:
        print(f"{Formatação_cores.RED}Nenhum produto cadastrado.{Formatação_cores.RESET}")

def detalhar_produto():
    os.system("cls")
    codigo = input("Código do produto: ")
    print("\n")
    produtos = carregar_arquivo('produtos.txt')
    compras = carregar_arquivo('compras.txt')
    vendas = carregar_arquivo('vendas.txt')

    for produto in produtos:
        if produto.startswith(codigo):
            codigo, nome, descricao, preco_compra, preco_venda = produto.strip().split(";")
            qtd_comprada = sum(int(c.split(";")[3]) for c in compras if c.split(";")[1] == codigo)
            qtd_vendida = sum(int(v.split(";")[3]) for v in vendas if v.split(";")[1] == codigo)
            valor_investido = qtd_comprada * float(preco_compra)
            valor_arrecadado = qtd_vendida * float(preco_venda)
            lucro = valor_arrecadado - valor_investido
            
            print(f"{Formatação_cores.YELLOW}Código do produto: {codigo}{Formatação_cores.RESET}")
            print(f"Nome do produto: {nome}")
            print(f"Descrição do produto: {descricao}")
            print(f"Preço de compra do produto: {Formatação_cores.Moeda.formatar(float(preco_compra))}")
            print(f"Preço de venda do produto: {Formatação_cores.Moeda.formatar(float(preco_venda))}")
            print(f"Quantidade Comprada: {qtd_comprada}")
            print(f"Quantidade Vendida: {qtd_vendida}")
            print(f"Valor total investido: {Formatação_cores.Moeda.formatar(valor_investido)}")
            print(f"Valor total arrecadado: {Formatação_cores.Moeda.formatar(valor_arrecadado)}")
            print(f"Lucro: {Formatação_cores.Moeda.formatar(lucro)}\n")

            print("Compras do produto:")
            for compra in compras:
                if compra.split(";")[1] == codigo:
                    print(f"  {compra.strip()}")

            print("\nVendas do produto:")
            for venda in vendas:
                if venda.split(";")[1] == codigo:
                    print(f"  {venda.strip()}")
            return
    print(f"{Formatação_cores.RED}Produto não encontrado.{Formatação_cores.RESET}")

def saldo_financeiro():
    os.system("cls")
    produtos = carregar_arquivo('produtos.txt')
    compras = carregar_arquivo('compras.txt')
    vendas = carregar_arquivo('vendas.txt')

    total_investido = 0
    total_arrecadado = 0

    for produto in produtos:
        codigo, nome, descricao, preco_compra, preco_venda = produto.strip().split(";")
        qtd_comprada = sum(int(c.split(";")[3]) for c in compras if c.split(";")[1] == codigo)
        qtd_vendida = sum(int(v.split(";")[3]) for v in vendas if v.split(";")[1] == codigo)
        total_investido += qtd_comprada * float(preco_compra)
        total_arrecadado += qtd_vendida * float(preco_venda)
    
    lucro_total = total_arrecadado - total_investido
    print('╔'+'═' * 36  +'╗')
    print('║ ' + f"{Formatação_cores.YELLOW}Total investido: {Formatação_cores.Moeda.formatar(total_investido)}{Formatação_cores.RESET}" + " " * 12 + '║')
    print('║ ' + f"{Formatação_cores.YELLOW}Total arrecadado: {Formatação_cores.Moeda.formatar(total_arrecadado)}{Formatação_cores.RESET}"+ " " * 11 + '║')
    print('║ ' + f"{Formatação_cores.YELLOW}Lucro total: {Formatação_cores.Moeda.formatar(lucro_total)}{Formatação_cores.RESET}"+ " " * 16 + '║')
    print('╚'+'═' * 36  +'╝')

def autenticar():
    senha = "8787"

    while True:
        tentativa = input(f"{Formatação_cores.YELLOW}Digite a senha para acessar o sistema: {Formatação_cores.RESET}")
        if tentativa == senha:
            return True 
            break
        else:
            print(f"\n{Formatação_cores.RED}Senha incorreta. Acesso negado.{Formatação_cores.RESET}")

def menu():
    if not autenticar():
        return
    
    while True:
        os.system("cls")

        frase = f"{Formatação_cores.GREEN}ESCOLHA UMA OPÇÃO{Formatação_cores.RESET}"

        Button1 =   "1 - Cadastrar Produto"
        Button2 =   "2 - Comprar Produto"
        Button3 =   "3 - Vender Produto"
        Button4 =   "4 - Listar Produtos"
        Button5 =   "5 - Detalhar Produto"
        Button6 =   "6 - Remover Produto"
        Button7 =   "7 - Atualizar Produto"
        Button8 =   "8 - Cancelar Compra"
        Button9 =   "9 - Cancelar Venda"
        Button10 = "10 - Saldo Financeiro"
        Button11 = f"{Formatação_cores.RED}11 - Sair{Formatação_cores.RESET}"

        print('╔'+'═' * 23  +'╗')
        print('║   ' + frase +' ' * 3 +'║')
        print('╚'+'═' * 23  +'╝')
        print('╔'+'═' * 23  +'╗')
        print('║ ' + Button1 +' ' * 1  +'║')
        print('║ ' + Button2 +' ' * 3  +'║')
        print('║ ' + Button3 +' ' * 4  +'║')
        print('║ ' + Button4 +' ' * 3  +'║')
        print('║ ' + Button5 +' ' * 2  +'║')
        print('║ ' + Button6 +' ' * 3  +'║')
        print('║ ' + Button7 +' ' * 1  +'║')
        print('║ ' + Button8 +' ' * 3  +'║')
        print('║ ' + Button9 +' ' * 4  +'║')
        print('║ ' + Button10 +' ' * 1  +'║')
        print('╚'+'═' * 23  +'╝')
        print('╔'+'═' * 23  +'╗')
        print('║ ' + Button11 +' ' * 13  +'║')
        print('╚'+'═' * 23  +'╝')
        print('\n')
        
        opcao = input(f"{Formatação_cores.YELLOW} Digite sua escolha: {Formatação_cores.RESET}")
        

        if opcao == "1":
            cadastrar_produto()
            input("\nPressione Enter para voltar ao menu...")
        elif opcao == "2":
            comprar_produto()
            input("\nPressione Enter para voltar ao menu...")
        elif opcao == "3":
            vender_produto()
            input("\nPressione Enter para voltar ao menu...")
        elif opcao == "4":
            listar_produtos()
            input("\nPressione Enter para voltar ao menu...")
        elif opcao == "5":
            detalhar_produto()
            input("\nPressione Enter para voltar ao menu...")
        elif opcao == "6":
            remover_produto()
            input("\nPressione Enter para voltar ao menu...")
        elif opcao == "7":
            atualizar_produto()
            input("\nPressione Enter para voltar ao menu...")
        elif opcao == "8":
            cancelar_compra()
            input("\nPressione Enter para voltar ao menu...")
        elif opcao == "9":
            cancelar_venda()
            input("\nPressione Enter para voltar ao menu...")
        elif opcao == "10":
            saldo_financeiro()
            input("\nPressione Enter para voltar ao menu...")
        elif opcao == "11":
            os.system("cls")
            print("Saindo...")
            break
        else:
            print(f"{Formatação_cores.RED}Opção inválida! Tente novamente.{Formatação_cores.RESET}")

menu()
