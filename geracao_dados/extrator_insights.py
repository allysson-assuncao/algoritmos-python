import pandas as pd
import numpy as np

def calcular_e_exportar_insights():
    print("Lendo dados do arquivo 'SovereignData_Consultoria.xlsx'...")

    # Carregando as planilhas
    try:
        df_energia = pd.read_excel('SovereignData_Consultoria.xlsx', sheet_name='Energia_PUE')
        df_ociosidade = pd.read_excel('SovereignData_Consultoria.xlsx', sheet_name='Ociosidade_CPU')
        df_inventario = pd.read_excel('SovereignData_Consultoria.xlsx', sheet_name='Inventario_ROI')
        df_emissoes = pd.read_excel('SovereignData_Consultoria.xlsx', sheet_name='Emissoes_Carbono')
        df_churn = pd.read_excel('SovereignData_Consultoria.xlsx', sheet_name='Clientes_Lucro')
    except Exception as e:
        print(f"Erro ao ler a planilha. Verifique se o arquivo existe. Erro: {e}")
        return

    # --- CÁLCULOS PILAR 1 ---
    pue_medio = round(df_energia['PUE_Horario'].mean(), 2)
    pue_maximo = round(df_energia['PUE_Horario'].max(), 2)

    # Sazonalidade Verão vs Inverno
    df_energia['Mes'] = pd.to_datetime(df_energia['Data_Hora']).dt.month
    consumo_verao = df_energia[df_energia['Mes'].isin([12, 1, 2])]['Consumo_Refrigeracao_kWh'].sum()
    consumo_inverno = df_energia[df_energia['Mes'].isin([6, 7, 8])]['Consumo_Refrigeracao_kWh'].sum()
    aumento_refrig_verao_pct = round(((consumo_verao - consumo_inverno) / consumo_inverno) * 100, 1)

    tarifa_kwh = 0.65 # Tarifa comercial média fictícia em R$
    custo_refrig_anual = round(df_energia['Consumo_Refrigeracao_kWh'].sum() * tarifa_kwh, 2)

    cpu_min = round(df_ociosidade['Uso_Medio_CPU_%'].min(), 1)

    # --- CÁLCULOS PILAR 2 ---
    hw_ponta = df_inventario[df_inventario['Categoria'] == 'De Ponta (Bleeding Edge)']
    hw_cons = df_inventario[df_inventario['Categoria'] == 'Consolidado (Geração Estável)']

    vida_ponta = round(hw_ponta['Vida_Util_Projetada_Meses'].mean(), 1)
    vida_consolidado = round(hw_cons['Vida_Util_Projetada_Meses'].mean(), 1)

    falhas_ponta = round(hw_ponta['Chamados_Manutencao'].mean(), 1)
    falhas_consolidado = round(hw_cons['Chamados_Manutencao'].mean(), 1)

    reposicoes_ponta = hw_ponta['Reposicoes_Pecas'].sum()
    reposicoes_consolidado = hw_cons['Reposicoes_Pecas'].sum()

    custo_manu_ponta = round(hw_ponta['Custo_Manutencao_R$'].mean(), 2)
    custo_manu_cons = round(hw_cons['Custo_Manutencao_R$'].mean(), 2)
    dif_manu_pct = round(((custo_manu_ponta - custo_manu_cons) / custo_manu_cons) * 100, 1)

    roi_ponta = round(hw_ponta['Custo_Performance_Anual_R$'].mean(), 2)
    roi_consolidado = round(hw_cons['Custo_Performance_Anual_R$'].mean(), 2)

    # --- CÁLCULOS PILAR 3 ---
    emissoes_totais_ton = round(df_emissoes['CO2e_Energia_Ton'].sum(), 1)
    vazamento_hfc_kg = round(df_emissoes['Vazamento_HFC_kg'].sum(), 1)
    custo_carbono_anual = round(df_emissoes['Custo_Compensacao_R$'].sum(), 2)

    df_cruzamento = pd.merge(df_churn, df_emissoes.groupby('Mes')['Custo_Compensacao_R$'].sum().reset_index(), on='Mes')
    df_cruzamento['Impacto_Pct'] = (df_cruzamento['Custo_Compensacao_R$'] / df_cruzamento['Lucro_Estimado_R$']) * 100
    impacto_lucro_pct = round(df_cruzamento['Impacto_Pct'].max(), 1)

    # --- CÁLCULOS PILAR 4 ---
    priv_med_inicio = df_churn.iloc[0]['Clientes_Priv_Medios']
    priv_med_fim = df_churn.iloc[-1]['Clientes_Priv_Medios']
    churn_priv_pct = round(((priv_med_inicio - priv_med_fim) / priv_med_inicio) * 100, 1)

    pub_med_inicio = df_churn.iloc[0]['Clientes_Pub_Medios']
    pub_med_fim = df_churn.iloc[-1]['Clientes_Pub_Medios']
    queda_pub_med_pct = round(((pub_med_inicio - pub_med_fim) / pub_med_inicio) * 100, 1)

    pub_peq_inicio = df_churn.iloc[0]['Clientes_Pub_Pequenos']
    pub_peq_fim = df_churn.iloc[-1]['Clientes_Pub_Pequenos']
    cresc_pub_peq_pct = round(((pub_peq_fim - pub_peq_inicio) / pub_peq_inicio) * 100, 1)

    receita_final = df_churn.iloc[-1]['Receita_Bruta_R$']
    lucro_final = df_churn.iloc[-1]['Lucro_Estimado_R$']

    lucro_inicio = df_churn.iloc[0]['Lucro_Estimado_R$']
    queda_lucro_pct = round(((lucro_inicio - lucro_final) / lucro_inicio) * 100, 1)

    # --- GERAÇÃO DO ARQUIVO MARKDOWN ---
    conteudo_md = f"""# Relatório de Insights Estratégicos: TIC Verde & Sustentabilidade

**Pilar 1: Eficiência Energética e Pegada Ambiental**
1. O PUE (Power Usage Effectiveness) médio anual da operação foi de **{pue_medio}**, indicando alto desperdício energético se comparado ao padrão ideal da indústria.
2. Devido à falta de confinamento térmico (corredor quente/frio), o consumo de refrigeração no verão foi **{aumento_refrig_verao_pct}%** maior do que no inverno, impactando diretamente a pegada ambiental.
3. A ineficiência térmica gerou um custo operacional estimado em **R$ {custo_refrig_anual:,.2f}** no ano, um gasto puramente focado em dissipar o calor do hardware legado.
4. Durante uma semana padrão, o uso de CPU atingiu vales de **{cpu_min}%** de madrugada, mas o consumo energético não caiu proporcionalmente, atestando a falta de políticas de desligamento automático.
5. **(Estratégia Google AI):** Se aplicarmos inteligência artificial para prever a carga térmica, podemos mitigar os picos críticos de PUE que chegaram a **{pue_maximo}** nos dias mais quentes.

**Pilar 2: Gestão do Ciclo de Vida e Redução de Resíduos**
6. A vida útil média projetada para o hardware "De Ponta" é de apenas **{vida_ponta}** meses, enquanto o hardware "Consolidado" atinge **{vida_consolidado}** meses.
7. Servidores "De Ponta" apresentaram em média **{falhas_ponta}** chamados de manutenção por máquina/ano, demonstrando alta instabilidade térmica frente à média de **{falhas_consolidado}** dos consolidados.
8. A alta taxa de falhas forçou **{reposicoes_ponta}** reposições físicas de peças no hardware de ponta contra **{reposicoes_consolidado}** no consolidado, acelerando gravemente a geração de e-lixo.
9. O custo médio de manutenção de uma máquina "De Ponta" foi de **R$ {custo_manu_ponta:,.2f}**, sendo **{dif_manu_pct}%** mais caro que as máquinas de geração anterior.
10. O custo financeiro por cada unidade de performance (TeraFLOP) ao ano é de **R$ {roi_ponta:,.2f}** no equipamento de ponta contra **R$ {roi_consolidado:,.2f}** no consolidado, justificando a adoção da Economia Circular.

**Pilar 3: Pegada Ecológica e Mercado de Carbono**
11. O consumo de energia baseado na matriz atual emitiu **{emissoes_totais_ton:,.1f}** toneladas de CO2 equivalente (Escopo 2) no último ano.
12. O estresse nos sistemas legados causou o vazamento estimado de **{vazamento_hfc_kg:,.1f}** kg de gases HFCs, agravando nosso impacto no aquecimento global.
13. A migração para o Mercado Livre de Energia com certificados I-REC poderia neutralizar instantaneamente as **{emissoes_totais_ton:,.1f}** toneladas geradas pela rede elétrica.
14. Para compensar ativamente as emissões atuais no Mercado Voluntário, seria necessário um desembolso anual de **R$ {custo_carbono_anual:,.2f}** em Créditos de Carbono.
15. No mês mais crítico do ano, o custo de neutralização ambiental consumiria **{impacto_lucro_pct}%** do lucro estimado, mostrando que a poluição é um risco direto ao fluxo de caixa.

**Pilar 4: Sustentabilidade como Diferencial de Negócio (Churn ESG)**
16. Pela incapacidade de fornecer um "Dashboard de Sustentabilidade Digital", a base de clientes privados de médio porte sofreu uma evasão de **{churn_priv_pct}%** no ano.
17. Contratos do setor público de médio porte, que possuem editais rigorosos de TIC Verde, sofreram uma queda de **{queda_pub_med_pct}%**.
18. Houve um crescimento de **{cresc_pub_peq_pct}%** nos clientes públicos pequenos, que mascarou temporariamente a perda de grandes contratos corporativos.
19. No último mês mapeado, a receita bruta da operação foi de **R$ {receita_final:,.2f}**, resultando em um lucro de **R$ {lucro_final:,.2f}**.
20. Considerando a saída dos clientes ESG exigentes, a margem de lucro líquido da empresa sofreu uma queda de **{queda_lucro_pct}%** entre o primeiro e o último mês de análise.
"""

    with open('insights_estrategicos.md', 'w', encoding='utf-8') as f:
        f.write(conteudo_md)

    print("Arquivo 'insights_estrategicos.md' gerado com sucesso!")

if __name__ == '__main__':
    calcular_e_exportar_insights()