import pandas as pd
import ace_tools as tools

# 📂 Passo 1: Upload do arquivo CSV
print("Faça upload da base de clientes (CSV).")
uploaded_file = tools.upload_file()

if uploaded_file:
    # Ler o arquivo CSV
    df = pd.read_csv(uploaded_file)

    # Exibir resumo da base
    print("\n📊 Resumo da Base de Clientes:")
    print(f"🔹 Total de clientes: {len(df)}")
    print(f"🔹 Colunas disponíveis: {list(df.columns)}")

    # Verificar se todas as colunas esperadas existem
    colunas_esperadas = ["nome", "telefone", "email", "última_compra", "ticket_medio",
                         "frequencia_compras", "produto", "departamento", "cor"]
    
    colunas_faltando = [col for col in colunas_esperadas if col not in df.columns]
    
    if colunas_faltando:
        print(f"\n⚠️ Atenção: As seguintes colunas estão ausentes no CSV: {colunas_faltando}")
    else:
        print("\n✅ Todas as colunas necessárias estão presentes.")

    # Converter datas para formato correto
    df["última_compra"] = pd.to_datetime(df["última_compra"], errors="coerce")

    # Criar um segmento inicial com todos os clientes
    segmento = df.copy()

    print("\n🛠️ Agora você pode aplicar múltiplos filtros para segmentação!")

    # Filtro 1: Última compra
    opcao = input("Deseja filtrar por data da última compra? (s/n): ").strip().lower()
    if opcao == "s":
        dias = int(input("Clientes que compraram nos últimos quantos dias? "))
        segmento = segmento[segmento["última_compra"] >= (pd.Timestamp.today() - pd.DateOffset(days=dias))]

    # Filtro 2: Ticket médio
    opcao = input("Deseja filtrar por ticket médio? (s/n): ").strip().lower()
    if opcao == "s":
        valor = float(input("Filtrar clientes com ticket médio acima de qual valor? R$ "))
        segmento = segmento[segmento["ticket_medio"] > valor]

    # Filtro 3: Frequência de compras
    opcao = input("Deseja filtrar por frequência de compras? (s/n): ").strip().lower()
    if opcao == "s":
        qtd = int(input("Filtrar clientes que compraram mais de quantas vezes? "))
        segmento = segmento[segmento["frequencia_compras"] > qtd]

    # Filtro 4: Produto
    opcao = input("Deseja filtrar por produto? (s/n): ").strip().lower()
    if opcao == "s":
        print("\n📦 Produtos disponíveis na base:")
        produtos_disponiveis = segmento["produto"].dropna().unique()
        for idx, produto in enumerate(produtos_disponiveis, start=1):
            print(f"{idx}️⃣ {produto}")

        produto_escolhido_idx = int(input("\nDigite o número do produto desejado: ")) - 1
        if 0 <= produto_escolhido_idx < len(produtos_disponiveis):
            produto_escolhido = produtos_disponiveis[produto_escolhido_idx]
            segmento = segmento[segmento["produto"] == produto_escolhido]

    # Filtro 5: Departamento
    opcao = input("Deseja filtrar por departamento? (s/n): ").strip().lower()
    if opcao == "s":
        print("\n🏬 Departamentos disponíveis na base:")
        departamentos_disponiveis = segmento["departamento"].dropna().unique()
        for idx, departamento in enumerate(departamentos_disponiveis, start=1):
            print(f"{idx}️⃣ {departamento}")

        departamento_escolhido_idx = int(input("\nDigite o número do departamento desejado: ")) - 1
        if 0 <= departamento_escolhido_idx < len(departamentos_disponiveis):
            departamento_escolhido = departamentos_disponiveis[departamento_escolhido_idx]
            segmento = segmento[segmento["departamento"] == departamento_escolhido]

    # Filtro 6: Cor
    opcao = input("Deseja filtrar por cor do produto? (s/n): ").strip().lower()
    if opcao == "s":
        print("\n🎨 Cores disponíveis na base:")
        cores_disponiveis = segmento["cor"].dropna().unique()
        for idx, cor in enumerate(cores_disponiveis, start=1):
            print(f"{idx}️⃣ {cor}")

        cor_escolhida_idx = int(input("\nDigite o número da cor desejada: ")) - 1
        if 0 <= cor_escolhida_idx < len(cores_disponiveis):
            cor_escolhida = cores_disponiveis[cor_escolhida_idx]
            segmento = segmento[segmento["cor"] == cor_escolhida]

    # Exibir resultado da segmentação e salvar o CSV
    if not segmento.empty:
        print("\n🔍 Segmentação concluída!")
        print(f"👥 Total de clientes no segmento: {len(segmento)}")

        # Criar um novo CSV com os clientes segmentados
        nome_arquivo = "clientes_segmentados.csv"
        segmento.to_csv(nome_arquivo, index=False)

        # Exibir a listagem na tela
        tools.display_dataframe_to_user(name="Segmento de Clientes", dataframe=segmento)

        print(f"\n✅ Arquivo '{nome_arquivo}' gerado com sucesso!")
    else:
        print("\n⚠️ Nenhum cliente encontrado com os filtros aplicados. Tente ajustar os critérios!")
