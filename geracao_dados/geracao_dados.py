import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# Inicializa o Faker
fake = Faker('pt_BR')

def gerar_dados_vendas(quantidade_linhas=50000):
    # 1. CATÁLOGO DE PRODUTOS
    catalogo = {
        'Eletrônicos': [('Smartphone Top', 4500.0), ('Smartphone Intermediário', 1800.0), ('Notebook Gamer', 7500.0), ('Notebook Básico', 2500.0), ('Smart TV 55', 3200.0), ('Fone Bluetooth', 250.0), ('Smartwatch', 800.0)],
        'Vestuário': [('Camiseta de Algodão', 59.9), ('Calça Jeans', 149.9), ('Tênis Esportivo', 350.0), ('Jaqueta de Couro', 499.9), ('Vestido Estampado', 189.9), ('Moletom', 120.0)],
        'Casa e Decoração': [('Luminária de Chão', 199.9), ('Jogo de Cama 400 Fios', 250.0), ('Sofá Retrátil', 2200.0), ('Quadro Decorativo', 90.0), ('Tapete Sala', 350.0), ('Poltrona', 600.0)],
        'Beleza': [('Perfume Importado', 450.0), ('Perfume Nacional', 120.0), ('Kit Skincare', 280.0), ('Creme Anti-idade', 150.0), ('Base Maquiagem', 90.0), ('Shampoo Profissional', 80.0)],
        'Esporte e Lazer': [('Bicicleta Aro 29', 1500.0), ('Whey Protein', 140.0), ('Bola de Futebol', 80.0), ('Kit Halteres', 180.0), ('Barraca de Camping', 450.0)],
        'Livros': [('Box Ficção', 120.0), ('Livro Finanças', 50.0), ('Biografia', 65.0), ('Livro Técnico TI', 150.0)],
        'Games': [('Console Nova Geração', 4200.0), ('Controle Extra', 450.0), ('Jogo Lançamento', 350.0), ('Cadeira Gamer', 1200.0)]
    }

    # 2. DISTRIBUIÇÃO GEOGRÁFICA
    estados_dist = {
        'SP': {'peso': 35, 'cidades': ['São Paulo', 'Campinas', 'Guarulhos', 'São Bernardo do Campo', 'Ribeirão Preto']},
        'RJ': {'peso': 12, 'cidades': ['Rio de Janeiro', 'Niterói', 'Duque de Caxias', 'Nova Iguaçu']},
        'MG': {'peso': 10, 'cidades': ['Belo Horizonte', 'Uberlândia', 'Contagem', 'Juiz de Fora']},
        'PR': {'peso': 8, 'cidades': ['Curitiba', 'Londrina', 'Maringá', 'Cascavel']},
        'RS': {'peso': 7, 'cidades': ['Porto Alegre', 'Caxias do Sul', 'Pelotas', 'Canoas']},
        'SC': {'peso': 6, 'cidades': ['Florianópolis', 'Joinville', 'Blumenau', 'São José']},
        'BA': {'peso': 5, 'cidades': ['Salvador', 'Feira de Santana', 'Vitória da Conquista']},
        'PE': {'peso': 4, 'cidades': ['Recife', 'Jaboatão dos Guararapes', 'Olinda']},
        'CE': {'peso': 4, 'cidades': ['Fortaleza', 'Caucaia', 'Juazeiro do Norte']},
        'DF': {'peso': 3, 'cidades': ['Brasília', 'Taguatinga', 'Ceilândia']},
        'GO': {'peso': 3, 'cidades': ['Goiânia', 'Aparecida de Goiânia', 'Anápolis']},
        'PA': {'peso': 2, 'cidades': ['Belém', 'Ananindeua', 'Santarém']},
        'AM': {'peso': 1, 'cidades': ['Manaus', 'Parintins']}
    }
    ufs = list(estados_dist.keys())
    pesos_ufs = [estados_dist[uf]['peso'] for uf in ufs]

    meios_acesso = ['Google Ads', 'Anúncio Instagram', 'Afiliado', 'Acesso Direto (Site)', 'E-mail Marketing', 'Busca Orgânica']
    dias_semana_pt = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']

    # ==========================================
    # NOVO: MOTOR DE INTELIGÊNCIA TEMPORAL
    # ==========================================
    data_fim = datetime.today()
    data_inicio = data_fim - timedelta(days=730) # Últimos 2 anos
    datas_possiveis = pd.date_range(start=data_inicio, end=data_fim)

    pesos_datas = []
    for data in datas_possiveis:
        peso = 1.0

        # Sazonalidade Mensal
        if data.month == 12: peso *= 2.5      # Natal (Altíssimo)
        elif data.month == 11: peso *= 1.8    # Black Friday / Aquecimento
        elif data.month == 5: peso *= 1.3     # Dia das Mães
        elif data.month in [1, 2]: peso *= 0.6 # Ressaca financeira de começo de ano

        # Efeito Salário (Início do mês vende mais)
        if data.day <= 8: peso *= 1.5         # Período de pagamento
        elif data.day >= 25: peso *= 0.7      # Fim do orçamento mensal

        # Dias da Semana (Foco em Fim de Semana)
        if data.weekday() == 4: peso *= 1.5   # Sexta-feira
        elif data.weekday() == 5: peso *= 1.8 # Sábado (Pico)
        elif data.weekday() == 6: peso *= 1.4 # Domingo
        else: peso *= 0.8                     # Segunda a Quinta

        # Picos Específicos (Ex: Semana da Black Friday)
        if data.month == 11 and 20 <= data.day <= 30:
            peso *= 2.5

        pesos_datas.append(peso)

    # Distribuição de Horários (Pico entre 18h e 22h, madrugadas quase zeradas)
    # Índices de 0 a 23 representam as horas.
    pesos_horas = [0.5, 0.2, 0.1, 0.1, 0.1, 0.3, 1.0, 2.0, 4.0, 5.0,
                   6.0, 6.0, 7.0, 7.0, 8.0, 9.0, 10.0, 12.0, 20.0, 25.0,
                   22.0, 18.0, 10.0, 4.0]

    # Sorteia todas as datas e horários de uma vez (muito mais rápido)
    datas_sorteadas = random.choices(datas_possiveis, weights=pesos_datas, k=quantidade_linhas)
    horas_sorteadas = random.choices(range(24), weights=pesos_horas, k=quantidade_linhas)

    dados = []

    for i in range(quantidade_linhas):
        # 1. APLICAR DATA E HORA SORTEADAS
        data_venda = datas_sorteadas[i]
        dia_semana = dias_semana_pt[data_venda.weekday()]
        hora = horas_sorteadas[i]
        minuto = random.randint(0, 59)
        horario_str = f"{hora:02d}:{minuto:02d}:{random.randint(0,59):02d}"

        # 2. PERFIL DO CLIENTE
        idade = int(random.gauss(35, 12))
        idade = max(18, min(75, idade))
        sexo = random.choices(['F', 'M', 'Outro'], weights=[0.52, 0.46, 0.02])[0]

        uf = random.choices(ufs, weights=pesos_ufs)[0]
        cidade = random.choice(estados_dist[uf]['cidades'])

        # 3. DEFINIÇÃO DA CATEGORIA (Viés de Compra)
        pesos_cat = {'Eletrônicos': 15, 'Vestuário': 20, 'Casa e Decoração': 15, 'Beleza': 15, 'Esporte e Lazer': 10, 'Livros': 10, 'Games': 5}

        if sexo == 'F':
            pesos_cat['Beleza'] += 20
            pesos_cat['Vestuário'] += 10
            pesos_cat['Casa e Decoração'] += 15
        elif sexo == 'M':
            pesos_cat['Eletrônicos'] += 15
            pesos_cat['Esporte e Lazer'] += 15
            pesos_cat['Games'] += 10

        if idade < 30:
            pesos_cat['Games'] += 20
            pesos_cat['Eletrônicos'] += 15
        elif idade > 50:
            pesos_cat['Casa e Decoração'] += 20
            pesos_cat['Livros'] += 15

        categoria = random.choices(list(pesos_cat.keys()), weights=list(pesos_cat.values()))[0]

        # 4. ESCOLHA DO PRODUTO E PREÇO
        produto_info = random.choice(catalogo[categoria])
        nome_produto = produto_info[0]

        variacao = random.uniform(0.70, 1.20)
        preco_unitario = round(produto_info[1] * variacao, 2)

        if preco_unitario > 1500:
            quantidade = random.choices([1, 2], weights=[0.95, 0.05])[0]
        elif preco_unitario < 100:
            quantidade = random.choices([1, 2, 3, 4, 5], weights=[0.5, 0.25, 0.15, 0.05, 0.05])[0]
        else:
            quantidade = random.choices([1, 2, 3], weights=[0.75, 0.20, 0.05])[0]

        valor_total_compra = preco_unitario * quantidade

        # 5. PAGAMENTO, PARCELAS E CUPOM
        usou_cupom = random.choices(['Sim', 'Não'], weights=[0.3, 0.7])[0]

        if valor_total_compra > 1000:
            forma_pagto = random.choices(['Cartão de Crédito', 'Pix', 'Boleto'], weights=[0.85, 0.10, 0.05])[0]
        elif valor_total_compra < 150:
            forma_pagto = random.choices(['Cartão de Crédito', 'Pix', 'Boleto'], weights=[0.35, 0.55, 0.10])[0]
        else:
            forma_pagto = random.choices(['Cartão de Crédito', 'Pix', 'Boleto'], weights=[0.60, 0.30, 0.10])[0]

        if forma_pagto == 'Cartão de Crédito':
            if valor_total_compra > 2000: parcelas = random.randint(6, 12)
            elif valor_total_compra > 500: parcelas = random.randint(2, 6)
            else: parcelas = random.randint(1, 3)
        else:
            parcelas = 1

        # 6. CANAL DE AQUISIÇÃO
        if idade < 30:
            acesso = random.choices(meios_acesso, weights=[0.2, 0.4, 0.1, 0.1, 0.05, 0.15])[0]
        else:
            acesso = random.choices(meios_acesso, weights=[0.2, 0.15, 0.1, 0.2, 0.2, 0.15])[0]

        # Adiciona a linha
        dados.append({
            'Data': data_venda.strftime('%d/%m/%Y'),
            'Horário': horario_str,
            'Dia da Semana': dia_semana,
            'Categoria': categoria,
            'Nome Do Produto': nome_produto,
            'Preço Unitário (R$)': preco_unitario,
            'Quantidade': quantidade,
            'Valor Total (R$)': round(valor_total_compra, 2),
            'Usou Cupom': usou_cupom,
            'Forma de Pagamento': forma_pagto,
            'Parcelas': parcelas,
            'Meio de Acesso': acesso,
            'Idade Do Cliente': idade,
            'Sexo': sexo,
            'Cidade': cidade,
            'UF': uf
        })

        if (i + 1) % 10000 == 0:
            print(f"Gerado {i + 1} de {quantidade_linhas} registros...")

    df = pd.DataFrame(dados)
    return df

quantidade_desejada = 50000
print(f"Iniciando a geração de {quantidade_desejada} linhas com padrões realistas de tempo...")
df_vendas_realista = gerar_dados_vendas(quantidade_desejada)

nome_arquivo = 'dados_vendas_consultoria_avancado.xlsx'
print(f"Salvando dados no arquivo '{nome_arquivo}'...")
df_vendas_realista.to_excel(nome_arquivo, index=False)
print("Finalizado com sucesso!")