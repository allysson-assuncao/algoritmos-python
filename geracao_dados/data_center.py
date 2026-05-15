import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


def gerar_dados_datacenter():
    print("Iniciando simulação de dados do Data Center (Últimos 12 meses)...")

    # Configurações de Tempo
    data_fim = datetime(2026, 5, 10)
    data_inicio = data_fim - timedelta(days=364)
    datas_horarias = pd.date_range(start=data_inicio, end=data_fim + timedelta(hours=23), freq='h')

    # ==========================================
    # TABELA 1 & 2: ENERGIA, CLIMA E OCIOSIDADE (8760 linhas)
    # ==========================================
    horas_do_dia = datas_horarias.hour
    meses_do_ano = datas_horarias.month

    # Clima (Sazonalidade e ciclo diário)
    temp_base = 22
    sazonalidade_mes = np.where(np.isin(meses_do_ano, [12, 1, 2]), 6,
                                np.where(np.isin(meses_do_ano, [6, 7, 8]), -4, 0))
    ciclo_diario = -5 * np.cos(np.pi * horas_do_dia / 12)
    ruido_temp = np.random.normal(0, 1, len(datas_horarias))
    temperatura_externa = temp_base + sazonalidade_mes + ciclo_diario + ruido_temp

    # MODIFICAÇÃO: Ociosidade mais realista (reduzida pela metade)
    # Servidores não ficam em 5%, eles mantêm um uso de base de ~35% de madrugada
    uso_cpu_base = 35 + 45 * np.exp(-0.5 * ((horas_do_dia - 14) / 5) ** 2)
    uso_cpu = uso_cpu_base + np.random.normal(0, 5, len(datas_horarias))
    uso_cpu = np.clip(uso_cpu, 15, 90)  # Fica entre 15% e 90%

    qtd_servidores = 500
    consumo_ti_base = 150  # kW constantes
    consumo_ti_variavel = (uso_cpu / 100) * 100
    consumo_ti_total = consumo_ti_base + consumo_ti_variavel

    fator_refrigeracao = 0.6 + np.maximum(0, (temperatura_externa - 24) * 0.05)
    consumo_refrigeracao = consumo_ti_total * fator_refrigeracao * np.random.uniform(0.95, 1.05, len(datas_horarias))

    pue = (consumo_ti_total + consumo_refrigeracao) / consumo_ti_total

    df_energia = pd.DataFrame({
        'Data_Hora': datas_horarias,
        'Temp_Externa_C': np.round(temperatura_externa, 1),
        'Consumo_TI_kWh': np.round(consumo_ti_total, 2),
        'Consumo_Refrigeracao_kWh': np.round(consumo_refrigeracao, 2),
        'Consumo_Total_kWh': np.round(consumo_ti_total + consumo_refrigeracao, 2),
        'PUE_Horario': np.round(pue, 2)
    })

    # MODIFICAÇÃO: Cálculo de desperdício ajustado (menos drástico)
    df_ociosidade = pd.DataFrame({
        'Data_Hora': datas_horarias,
        'Uso_Medio_CPU_%': np.round(uso_cpu, 1),
        'Servidores_Ligados': qtd_servidores,
        'Desperdicio_Estimado_kWh': np.where(uso_cpu < 40, np.round(consumo_ti_base * 0.4, 2), 0)  # 40% do base
    })

    # ==========================================
    # TABELA 3: INVENTÁRIO E CICLO DE VIDA (500 linhas)
    # ==========================================
    ids_servidores = [f"SRV-{str(i).zfill(4)}" for i in range(1, 501)]
    categorias = random.choices(['Última Geração', 'Geração Estável'], weights=[0.6, 0.4], k=500)

    meses_uso = [random.randint(2, 12) for _ in range(500)]
    falhas = []
    vida_util = []

    for cat in categorias:
        if cat == 'Última Geração':
            # MODIFICAÇÃO: Disparidade ligeiramente menor
            falhas.append(np.random.poisson(lam=1.8))
            vida_util.append(random.randint(36, 48))  # Vida útil razoável, mas ainda menor
        else:
            falhas.append(np.random.poisson(lam=0.8))
            vida_util.append(random.randint(48, 60))

    df_inventario = pd.DataFrame({
        'ID_Servidor': ids_servidores,
        'Categoria': categorias,
        'Meses_em_Operacao': meses_uso,
        'Chamados_Manutencao': falhas,
        'Vida_Util_Projetada_Meses': vida_util
    })

    # ==========================================
    # TABELA 4: EMISSÕES SEMANAIS (52 linhas)
    # ==========================================
    df_energia_semana = df_energia.set_index('Data_Hora').resample('W').sum()
    semanas = df_energia_semana.index

    fator_co2_kwh = 0.00008
    co2_energia = df_energia_semana['Consumo_Total_kWh'] * fator_co2_kwh
    vazamento_hfc = df_energia_semana['Temp_Externa_C'] / 1000

    # Custo de compensação aumenta gradativamente por conta das perdas de refrigeração
    custo_compensacao = co2_energia.values * 150

    df_emissoes = pd.DataFrame({
        'Semana': semanas.strftime('%Y-%m-%d'),
        'Mes': semanas.strftime('%Y-%m'),  # Adicionado para cruzar com lucro depois
        'CO2e_Energia_Ton': np.round(co2_energia.values, 2),
        'Vazamento_HFC_kg': np.round(vazamento_hfc.values, 2),
        'Custo_Compensacao_R$': np.round(custo_compensacao, 2)
    })

    # ==========================================
    # TABELA 5: EVOLUÇÃO DE CLIENTES E LUCRO (12 linhas)
    # ==========================================
    meses_churn = pd.date_range(start=data_inicio, periods=12, freq='ME')

    # MODIFICAÇÃO: Alvos são clientes Pequenos e Médios (públicos e privados)
    pub_peq = 120  # Vai crescer 30% (meta: ~156)
    pub_med = 20  # Vai cair até 60% (meta: ~8)
    priv_peq = 200  # Queda leve
    priv_med = 45  # Vai cair, mas sobrar ao menos 20% (meta: ~12)

    dados_churn = []

    for i in range(12):
        # Movimentações mensais
        pub_peq += random.randint(2, 4)  # Cresce ~3 por mês (+36 no ano)
        pub_med -= random.choices([0, 1, 2], weights=[0.2, 0.6, 0.2])[0]  # Cai ~1 por mês
        priv_med -= random.choices([2, 3], weights=[0.6, 0.4])[0]  # Cai ~2.5 por mês
        priv_peq -= random.randint(1, 3)  # Fuga leve de startups exigentes

        # Receitas Fictícias: Peq=R$2k, Med=R$15k. Custo Opex Fixo=R$700k
        receita_total = (pub_peq * 2000) + (pub_med * 15000) + (priv_peq * 2000) + (max(0, priv_med) * 15000)
        lucro_estimado = receita_total - 700000

        dados_churn.append({
            'Mes': meses_churn[i].strftime('%Y-%m'),
            'Clientes_Pub_Pequenos': pub_peq,
            'Clientes_Pub_Medios': max(0, pub_med),
            'Clientes_Priv_Pequenos': priv_peq,
            'Clientes_Priv_Medios': max(0, priv_med),
            'Receita_Bruta_R$': receita_total,
            'Lucro_Estimado_R$': lucro_estimado
        })

    df_churn = pd.DataFrame(dados_churn)

    # ==========================================
    # EXPORTAÇÃO
    # ==========================================
    with pd.ExcelWriter('SovereignData_Consultoria.xlsx') as writer:
        df_energia.to_excel(writer, sheet_name='Energia_PUE', index=False)
        df_ociosidade.to_excel(writer, sheet_name='Ociosidade_CPU', index=False)
        df_inventario.to_excel(writer, sheet_name='Inventario_Hardware', index=False)
        df_emissoes.to_excel(writer, sheet_name='Emissoes_Carbono', index=False)
        df_churn.to_excel(writer, sheet_name='Clientes_Lucro', index=False)

    print("Tabelas salvas no arquivo 'SovereignData_Consultoria.xlsx'")

    # ==========================================
    # GERAÇÃO DOS GRÁFICOS (1 de cada)
    # ==========================================
    plt.style.use('ggplot')

    # Gráfico 1: PUE vs Temperatura
    df_daily = df_energia.set_index('Data_Hora').resample('D').mean()
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()
    ax1.plot(df_daily.index, df_daily['PUE_Horario'], 'g-')
    ax2.plot(df_daily.index, df_daily['Temp_Externa_C'], 'r--', alpha=0.5)
    ax1.set_ylabel('PUE Médio Diário', color='g')
    ax2.set_ylabel('Temperatura Externa (°C)', color='r')
    plt.title('Eficiência: PUE sofre com o calor externo')
    plt.savefig('grafico_1_PUE_vs_Temp.png')
    plt.close()

    # Gráfico 2: Ociosidade (Menos drástica)
    df_semana = df_ociosidade.iloc[1000:1168]
    plt.figure(figsize=(10, 5))
    plt.fill_between(df_semana['Data_Hora'], df_semana['Uso_Medio_CPU_%'], color='skyblue', alpha=0.8)
    plt.plot(df_semana['Data_Hora'], [100] * len(df_semana), 'r-', alpha=0.5, label='Capacidade Energética Máxima')
    plt.title('Ociosidade: Margem de Otimização fora do Horário Comercial')
    plt.legend()
    plt.savefig('grafico_2_Ociosidade.png')
    plt.close()

    # MODIFICAÇÃO: Gráfico 3 em Percentual (Pizza)
    plt.figure(figsize=(8, 6))
    falhas_totais = df_inventario.groupby('Categoria')['Chamados_Manutencao'].sum()
    plt.pie(falhas_totais, labels=falhas_totais.index, autopct='%1.1f%%', startangle=90, colors=['#ff9999', '#66b3ff'])
    plt.title('Distribuição Percentual de Falhas por Geração de Hardware')
    plt.savefig('grafico_3_Falhas_Percentual.png')
    plt.close()

    # MODIFICAÇÃO: Gráfico 4 (Custo de Compensação vs. Lucro Operacional)
    df_emissoes_mensal = df_emissoes.groupby('Mes')['Custo_Compensacao_R$'].sum().reset_index()
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()

    # Barra para o custo de emissão e Linha para o Lucro
    ax1.bar(df_emissoes_mensal['Mes'], df_emissoes_mensal['Custo_Compensacao_R$'], color='salmon', alpha=0.7,
            label='Custo de Compensação CO2')
    ax2.plot(df_churn['Mes'], df_churn['Lucro_Estimado_R$'], color='darkblue', marker='o', linewidth=2,
             label='Lucro Estimado')

    ax1.set_ylabel('Custo para Anular Emissões (R$)', color='salmon')
    ax2.set_ylabel('Lucro Estimado (R$)', color='darkblue')
    plt.title('O Impacto da Poluição: Queda de Lucros vs. Custo de Compensação (ESG)')
    fig.autofmt_xdate(rotation=45)
    plt.savefig('grafico_4_Custos_Emissoes_vs_Lucro.png')
    plt.close()

    # Gráfico 5: Movimentação de Clientes (Carteira Média)
    plt.figure(figsize=(10, 5))
    plt.plot(df_churn['Mes'], df_churn['Clientes_Priv_Medios'], marker='o', color='red',
             label='Privado Médio (Queda ESG)')
    plt.plot(df_churn['Mes'], df_churn['Clientes_Pub_Medios'], marker='s', color='orange',
             label='Público Médio (Queda Licitações)')
    plt.plot(df_churn['Mes'], df_churn['Clientes_Pub_Pequenos'], marker='^', color='green',
             label='Público Pequeno (Crescimento)')
    plt.title('Evolução da Carteira: Fuga do Setor Médio')
    plt.legend()
    plt.xticks(rotation=45)
    plt.savefig('grafico_5_Movimentacao_Clientes.png')
    plt.close()

    print("Gráficos gerados e salvos como PNG.")


if __name__ == '__main__':
    gerar_dados_datacenter()
