import streamlit as st
import sqlite3
import pandas as pd
import random
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Gestão de Ensalamento - Provas",
    page_icon="🏫",
    layout="wide"
)

# --- CONEXÃO E CRIAÇÃO DO BANCO DE DADOS ---
CONN = sqlite3.connect("escola.db", check_same_thread=False)
CURSOR = CONN.cursor()

def inicializar_banco():
    CURSOR.execute("""
    CREATE TABLE IF NOT EXISTS turmas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL
    );
    """)
    
    CURSOR.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        turma_id INTEGER,
        FOREIGN KEY (turma_id) REFERENCES turmas (id) ON DELETE CASCADE
    );
    """)
    CONN.commit()

    CURSOR.execute("SELECT COUNT(*) FROM turmas;")
    if CURSOR.fetchone()[0] == 0:
        turmas_iniciais = [
            (1, '1ª A'), (2, '1º Técnico (Mineração)'), (3, '2ª A'),
            (4, '2º Técnico (Dev. Sistemas)'), (5, '3ª A'), (6, '6º Ano'),
            (7, '7º Ano'), (8, '8º Ano'), (9, '9º Ano')
        ]
        CURSOR.executemany("INSERT INTO turmas (id, nome) VALUES (?, ?);", turmas_iniciais)
        
        alunos_iniciais = [
            # 1ª A
            ('ANTONIA SÂMARA DOS SANTOS SOUSA LIMA', 1), ('EMILLY NUNES DIAS', 1), ('FELYPE RODEN DE FRANÇA SANTOS', 1),
            ('GABRIEL HENRIQUE NUNES', 1), ('HANRY MIGUEL SANTOS MILHOMEM', 1), ('HELOISE HELENA MENDES DE PAIVA', 1),
            ('HENRIQUE FONSECA SOUSA', 1), ('JOÃO VITOR DA SILVA RIBEIRO', 1), ('JULIA ALVES MACEDO', 1),
            ('MARIA EDUARDA GOMES DA SILVA', 1), ('MARINA SOUZA GOMES', 1), ('MATHEUS BERNARDES DE FREITAS', 1),
            ('MATHEUS OLIVEIRA AGUILAR ROCHA', 1), ('OTÁVIO HENRIQUE BORGES LIFONSO', 1), ('PAULO HENRIQUE PINTO DE ARAÚJO', 1),
            ('PEDRO GABRIEL HILÁRIO DE OLIVEIRA', 1), ('PEDRO GUILHERME SANTANA E SILVA MESQUITA', 1), ('PEDRO MIGUEL RODRIGUES PEREIRA', 1),
            ('TAINA DE OLIVEIRA ANDRADE MIGUEL', 1), ('WESLEY PEREIRA MAGALHÃES', 1), ('WILLAMY SANTOS DA SILVA', 1),
            ('KAUA GABRIEL MENDES RICARDE', 1), ('EMILLY LEAL DE SOUSA', 1), ('YSADORA OLIVEIRA SANTΑΝΑ', 1),
            ('ENZO DA SILVA BRAGA MARTINS', 1), ('MARIA EDUARDA SOUSA DA SILVA', 1),
            
            # 1º Técnico (Mineração)
            ('ADÃO LUIZ MENDONÇA GONÇALVES', 2), ('AIRTON SILVA DE ARAUJO LUCAS', 2), ('ARTHUR SILVA PEDROSA', 2),
            ('BRENO VILAS BOAS SANTOS DIAS', 2), ('DANIEL HENRIQUE FIDELIS DA SILVA', 2), ('DIONARA MYLENA ARAUJO SILVA', 2),
            ('GABRIEL FERREIRA ALVES', 2), ('GABRIEL GONÇALVES MENEZES MARQUES', 2), ('GUILHERME ANTONIO FIDELES DA FONSECA', 2),
            ('GUSTAVO HENRIQUE FERREIRA DOS SANTOS', 2), ('IAN PABLO PEREIRA DA SILVA BATISTA', 2), ('ISABELA CHAMONE RABELO', 2),
            ('ISABELLA DE SOUSA SILVA', 2), ('JOÃO LUCAS BELARMINO VIEIRA', 2), ('LARY VICTÓRIA ARAÚJO DE OLIVEIRA', 2),
            ('MARIA FERNANDA RODRIGUES FERNANDES PEREIRA', 2), ('MARIA GABRIELLA RIBEIRO', 2), ('MARIA HELLOAH ROSA SILVA MACHADO', 2),
            ('MARIA VITÓRIA SANTOS DE FARIA', 2), ('MARIA VITTÓRIA RIBEIRO', 2), ('MIGUEL BARBOSA PACHECO', 2),
            ('MIGUEL SILVEIRA SOUTO', 2), ('RAQUELL DE SOUZA MACÊNA', 2), ('VICTOR HENRIQUE RIBEIRO', 2),
            ('VICTOR HUGO SILVA MORAIS', 2), ('ANTONELLA RODRIGUES DE OLIVEIRA PRADO', 2),
            
            # 2ª A
            ('ANA BEATRIZ MARIANO DA SILVA', 3), ('BRUNO RIBEIRO DOS SANTOS', 3), ('EVELLYN NATTÁLYA DE JESUS DA SILVA', 3),
            ('GUSTAVO PEREIRA DOS SANTOS', 3), ('MARIA ANGELINNY SALVINO DA SILVA', 3), ('MARIA CLARA ALVES PIRES', 3),
            ('MARIA EDUARDA DE OLIVEIRA REIS', 3), ('PAOLA MARTINS BORGES', 3), ('PEDRO AUGUSTO RODRIGUES LIMA', 3),
            ('TALISSOM OLIVEIRA DA SILVA', 3), ('VITÓRIA DA SILVA ROSA BORGES LEAL', 3), ('GABRIELLA APARECIDA MEDEIROS PIMENTA SILVA', 3),
            
            # 2º Técnico (Dev. Sistemas)
            ('ANA CLARA OLIVEIRA FERNANDES', 4), ('ANDRÉ FELIPE DA SILVA', 4), ('EDUARDA SILVA RIBEIRO', 4),
            ('GABRIEL ASSUNÇÃO DIAS', 4), ('GABRIEL SANTOS MARTIN', 4), ('ISAAC BARUC DE SOUSA SANTANA', 4),
            ('JÚLIO CÉSAR DA SILVA', 4), ('KAUANE MIKAELLY DOS SANTOS GOMES', 4), ('LEANDER DAVI SILVA HELENA', 4),
            ('LUCAS GABRIEL SILVA MONTEIRO', 4), ('MARCOS MIGUEL FERNANDES PAULISTA DA SILVA', 4), ('MATHEUS CARVALHO DE JESUS', 4),
            ('NICOLAS GONÇALVES DOS SANTOS', 4), ('NICOLAS JAFÉ DOS SANTOS RIBEIRO', 4), ('NYCOLAS FERREIRA DA SILVA', 4),
            ('PEDRO RUAN DA SILVA FERREIRA', 4), ('RAYSSA OLIVEIRA GOMES', 4), ('RIAN RIVEM BATISTA DE SOUZA', 4),
            ('SAMUELL DA SILVA CELSO', 4), ('THAYSSA CRISTINA RIBEIRO DA SILVA', 4), ('VICTOR GABRIEL RABELO RAMOS', 4),
            ('VICTOR HUGO DE ARAÚJO SANTOS', 4), ('VITOR VENTURA DA SILVA', 4),
            
            # 3ª A
            ('ALINE BARBOSA DA SILVA', 5), ('ANA CLARA DE JESUS BRITO', 5), ('ANA CLARA VIEIRA DIAS', 5),
            ('ANNA JÚLIA DE OLIVEIRA SILVA', 5), ('AUGUSTO CÉSAR SILVA DANTAS', 5), ('BRUNA CRISTINA DE SOUSA RODRIGUES', 5),
            ('BRYAN MIGUEL BORGES PEDROZA', 5), ('CAIO VINÍCIUS TENÓRIO', 5), ('CARLOS EDUARDO DOS SANTOS DE FARIA', 5),
            ('DAVI ALMEIDA PURCINA', 5), ('ESTHER VICTORIA PEREIRA LEITE', 5), ('FLÁVIO HENRYCK DAMAS DE ARAÚJO', 5),
            ('GABRIEL FELIPE CARDOSO PEREIRA SANTOS', 5), ('GABRIELLY SILVERIO DOS SANTOS', 5), ('GUILHERME ARRUDA SILVA', 5),
            ('HUDSON LEMES DE CASTRO', 5), ('JOAO VICTOR PEREIRA BARBOSA', 5), ('LARA RAIANNE SILVA BARROS', 5),
            ('MANOEL MARÇAL GOMES DE MIRANDA', 5), ('MARIA EDUARDA DA SILVA RIBEIRO', 5), ('MARIA EDUARDA OLIVEIRA DE ANDRADE', 5),
            ('MILENA GONÇALVES ROSA', 5), ('OTAVIO DE SOUSA', 5), ('RAFAELA APARECIDA ATAIDE ANDRADE', 5),
            ('SAIMOM HALIFER SOUZA PIRES', 5), ('VÍCTOR DE SOUZA SILVÉRIO', 5), ('VIVIANE ABADIA ALVES DUARTE', 5),
            ('INGRID DAYANE PASCOAL DE OLIVEIRA', 5),
            
            # 6º Ano
            ('AGATA EMANUELLY FLEURY ABADIA PEREIRA', 6), ('ALICE GABRIELLE DA SILVA SABINO', 6), ('AMANDA GABRIELY DA SILVA CARDOSO', 6),
            ('AMANDA OLIVEIRA DA SILVA', 6), ('ANTÔNIO DAVID OLIVEIRA PEREIRA', 6), ('BENICIO SILVA BERNARDES', 6),
            ('BENJAMIN DOS SANTOS MENDES', 6), ('BERNARDO HENRIQUE ALVES RIBEIRO', 6), ('BERNARDO SOUZA ARAUJO', 6),
            ('CARLOS EDUARDO DA SILVA SANTOS', 6), ('DAVI LUCAS SANTANA DE PAULA', 6), ('EDUARDO ANTÔNIO CIRILO DE SOUZA', 6),
            ('EMANUELLE DE SOUSA SILVA', 6), ('EMANUELY OLIVEIRA DOS SANTOS ASSIS', 6), ('ENZO ALEXANDRE FÉLIX MACHADO', 6),
            ('ENZO MARTINS DA SILVA', 6), ('EVELYN VITORIA DA SILVA', 6), ('FILIPE RODRIGUES DA COSTA', 6),
            ('GIOVANNA FROEDE PIRES', 6), ('ISABELLY WIGGERS DE OLIVEIRA SILVA', 6), ('ISAÍAS BARBOSA VERA', 6),
            ('KAUA BELCHIOR ARRUDA', 6), ('KEMILLY VITORIA FONTANA DE ANDRADE', 6), ('MARIA ALICE ALVES ROCHA SILVA', 6),
            ('MARIA LUIZA TOMAZ DE OLIVEIRA PIRES', 6), ('MIGUEL ANTONIO CIRILO', 6), ('MIGUEL DOS SANTOS MENDES', 6),
            ('MIGUEL HENRIQUE DA SILVA', 6), ('MIKAELA ALVES PIRES', 6), ('MYLENA EVANGELISTA DOS SANTOS', 6),
            ('SARA FERREIRA', 6), ('SOPHIA RODRIGUES DE MARINS', 6), ('SOPHIA VITÓRIA DE ARAÚJO FREITAS', 6),
            ('VIVIANY LIMEIRA DE ANDRADE', 6), ('AMANDA VITORYA SANTOS LIMA', 6),
            
            # 7º Ano
            ('AGATHA DA SILVA ANDRADE', 7), ('ALICE CAROLINA FERREIRA DA SILVA', 7), ('ANA BEATRIZ PEREIRA ARRUDA', 7),
            ('AYSHA GABRIELLY BORGES LIFONSO', 7), ('BHIANCA BERNARDES DE FREITAS', 7), ('DAVI FELIX DUARTE', 7),
            ('DAVI LUCAS MARQUES DE OLIVEIRA', 7), ('DAVI LUIZ DA SILVA CONCEIÇÃO', 7), ('DIEGO NASCIMENTO SILVA', 7),
            ('EDUARDO MAGIOTTO DOS SANTOS ALVES', 7), ('ELOÁ ESTRELA FERNANDES', 7), ('EMANUELLY VICTORIA SOUZA SANTOS', 7),
            ('GABRIEL AGUIAR DOS SANTOS', 7), ('GABRIEL FELIX DUARTE', 7), ('GABRIEL LEMES MORAIS DA SILVA PRADO', 7),
            ('GRAZIELLY DA CONCEIÇÃO SILVA', 7), ('HEITOR MENEZES MARTINS', 7), ('HEITOR PEREIRA DINIZ', 7),
            ('ISIS DAYARA BASTOS ANDRADE', 7), ('JOÃO MIGUEL SILVA SOUZA', 7), ('JOSÉ CARLOS CARDOSO PEREIRA SANTOS', 7),
            ('KEVIN HENRIQUE PEREIRA DA SILVA', 7), ('LAURA MAGALHÃES DA SILVA', 7), ('LETICIA SANTANA SANTOS', 7),
            ('MANUELLA DA COSTA BORGES', 7), ('MARCELA ARRUDA OLIVEIRA', 7), ('MARIA JÚLIA CARVALHO NEIVA RIBEIRO', 7),
            ('MATHEUS GUIMARÃES LEAL', 7), ('PABLLO ALEXSANDER SOUSA CARDOSO', 7), ('PEDRO FERNANDES VAZ DOS REIS', 7),
            ('RAPHAEL LEONARDO DA SILVA', 7), ('VICTTOR HUGO LOPES DE OLIVEIRA', 7), ('NÍCOLLAS MOISÉS SILVA TEREZA', 7),
            ('MARIA VITÓRIA VIEIRA REZENDE', 7), ('DARLLON MIKAEL RIBEIRO COSTA', 7),
            
            # 8º Ano
            ('ADILSON MARQUES DE OLIVEIRA', 8), ('ANA JÚLIA REINALDO RODRIGUES', 8), ('ARTHUR MARCELINO BRAZ', 8),
            ('CARLOS EDUARDO FLOR FARIA', 8), ('DAVI DE SOUSA MENDES', 8), ('DAVID RAFFAEL BARBOSA BASTOS', 8),
            ('DULCE MARIA OLIVEIRA MIGUEL', 8), ('EMANUELA FERREIRA HARNISCH', 8), ('GABRIEL ANTONIO ALVES DA SILVA', 8),
            ('GABRIEL HENRIQUE SILVA RIBEIRO', 8), ('GUILHERME KAUER DA SILVA DO NASCIMENTO', 8), ('HELOISA PEREIRA MATOS', 8),
            ('IGOR NERI SANTANA JÚNIOR', 8), ('IGOR VINICIUS DE SOUZA SANTOS FILHO', 8), ('ITALLO CARVELO COELHO', 8),
            ('ITALO AUGUSTO DE SOUZA BORBA', 8), ('JOÃO LUCAS CONCEIÇÃO SILVA', 8), ('JOÃO PEDRO CORREA DE MATOS', 8),
            ('JULIA ALMEIDA PEREIRA', 8), ('MARIANA NUNES DE OLIVEIRA', 8), ('MICHEL CARVALHO COSTA', 8),
            ('MIGUEL BUENO SAFATLE DE SOUZA', 8), ('MIRIAM MARIANO DA SILVA', 8), ('NICOLAS DOS SANTOS OLIVEIRA', 8),
            ('NYCOLAS PEREIRA DE SOUSA', 8), ('PAMELA EDUARDA AIRES DOS SANTOS', 8), ('PEDRO HENRIQUE VIEIRA DOS SANTOS', 8),
            ('SOFFIA LUIZA DE JESUS SOUZA', 8), ('SOPHIA GONÇALVES DOS SANTOS', 8), ('VERÔNICA MARIA ALVES RIBEIRO', 8),
            ('VITOR HUGO IVO DE PAULA', 8), ('YASMIM VITÓRIA FONTANA DE ANDRADE', 8), ('EMANUELLY VIEIRA MONTEIRO', 8),
            ('DHEYMIS RAMOS MARTINS', 8),
            
            # 9º Ano
            ('ALICE FURTADO DOS SANTOS JORGE', 9), ('ALICE GOMES ROSA', 9), ('ANNA LUIZA DA SILVA', 9),
            ('CARLOS GABRIEL RODRIGUES DA SILVA', 9), ('DAVI LUIS OLIVEIRA DE CARVALHO DA SILVA', 9), ('DAVI LUKA DA SILVA', 9),
            ('GABRIEL MAGIOTTO DOS SANTOS', 9), ('GABRIEL PEREIRA FERNANDES', 9), ('IAN DANIEL MENDES FLORENCIO', 9),
            ('ISADORA TEIXEIRA COUTINHO', 9), ('ITALO JEAN DE AZEVEDO FERREIRA', 9), ('JOÃO GUILHERME SILVA SOUSA', 9),
            ('JÚLIO CÉSAR DOS SANTOS DANTAS', 9), ('KAIO VICTOR TOMAZ DE OLIVEIRA PIRES', 9), ('KATHLEN YOHANA SANTANA BORGES', 9),
            ('KAUAN HENRIQUE GOMES DA SILVA', 9), ('KAYNAN CAVALCANTE SALVINO DE JESUS', 9), ('LUDMILLA ALVES RAMOS', 9),
            ('LUDMILLA PEREIRA MATOS', 9), ('MANUELLA NASCIMENTO MELO', 9), ('MARIA AMANDA ALVES CONCEIÇÃO', 9),
            ('MARIA EDUARDA EVANGELISTA DOS SANTOS', 9), ('MARIA RAFAELA DE SOUSA SANTANA', 9), ('MAYSA AZEVEDO ANDRADE', 9),
            ('NÁDLLA VITÓRIA COELHO CARVALHO', 9), ('NATA YOSSEF DOS SANTOS SILVA', 9), ('PERSEUS TSEREWEDE TSIBDA ADI', 9),
            ('RAFAEL HENRIQUE BARBOSA MAGELA', 9), ('RAIANNY MICAELE CRUZ DO NASCIMENTO', 9), ('DEYUSON TSAWETE TSIROWA', 9),
            ('GUSTAVO KASSIO SOUSA', 9), ('JOSE AUGUSTO DO NASCIMENTO PACIENCIA', 9)
        ]
        CURSOR.executemany("INSERT INTO alunos (nome, turma_id) VALUES (?, ?);", alunos_iniciais)
        CONN.commit()

inicializar_banco()

# --- FUNÇÃO DE GERAÇÃO DE PDF ---
def gerar_pdf_ensalamento(dict_salas, titulo_arquivo="Ensalamento"):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'HeaderTitle',
        parent=styles['Heading1'],
        fontSize=14,
        alignment=1, # Centralizado
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'HeaderSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        alignment=1,
        spaceAfter=15
    )
    cell_style = ParagraphStyle('Cell', parent=styles['Normal'], fontSize=9)
    cell_bold = ParagraphStyle('CellBold', parent=styles['Normal'], fontSize=9, fontName='Helvetica-Bold')

    salas_keys = list(dict_salas.keys())
    for idx_sala, num_sala in enumerate(salas_keys):
        # Cabeçalho da Escola
        story.append(Paragraph("COLÉGIO ESTADUAL EM PERÍODO INTEGRAL ABRAHÃO ANDRÉ", title_style))
        story.append(Paragraph(f"<b>LISTA DE ENSALAMENTO - SALA {num_sala}</b>", subtitle_style))
        
        # Tabela de Alunos
        data = [[Paragraph("<b>Pos.</b>", cell_bold), Paragraph("<b>Nome do Aluno</b>", cell_bold), Paragraph("<b>Turma Origem</b>", cell_bold)]]
        
        for pos, aluno in enumerate(dict_salas[num_sala], start=1):
            data.append([
                Paragraph(str(pos), cell_style),
                Paragraph(aluno["Nome do Aluno"], cell_style),
                Paragraph(aluno["Turma de Origem"], cell_style)
            ])
            
        tabela = Table(data, colWidths=[40, 340, 150])
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E0E0E0")),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#B0B0B0")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#000000")),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        story.append(tabela)
        
        # Quebra de página entre salas (exceto na última)
        if idx_sala < len(salas_keys) - 1:
            story.append(PageBreak())

    doc.build(story)
    buffer.seek(0)
    return buffer

# --- INTERFACE PRINCIPAL ---
st.title("🏫 Sorteador & Misturador de Salas de Prova")

menu = st.sidebar.radio("Navegação", ["🎲 Gerar Ensalamento", "⚙️ Gerenciar Turmas e Alunos"])

if menu == "🎲 Gerar Ensalamento":
    st.header("Sorteio para Segunda-Feira")
    
    turmas_df = pd.read_sql_query("SELECT * FROM turmas", CONN)
    
    if turmas_df.empty:
        st.warning("Nenhuma turma encontrada.")
    else:
        turmas_selecionadas = st.multiselect(
            "Selecione as turmas participantes do exame:",
            options=turmas_df["nome"].tolist(),
            default=turmas_df["nome"].tolist()
        )
        
        if turmas_selecionadas:
            num_salas = len(turmas_selecionadas)
            st.info(f"📌 **{num_salas} salas** serão criadas automaticamente para receber a distribuição.")
            
            # Opções de nome do arquivo de exportação
            nome_customizado = st.text_input("Nome base do arquivo para exportação:", value="ensalamento_provas")
            
            if st.button("🔀 Sortear e Misturar Alunos", type="primary"):
                ids_turmas = turmas_df[turmas_df["nome"].isin(turmas_selecionadas)]["id"].tolist()
                
                salas = [[] for _ in range(num_salas)]
                total_alunos = 0
                
                # Distribuição Estratificada por Turma
                for t_id in ids_turmas:
                    nome_t = turmas_df[turmas_df["id"] == t_id]["nome"].values[0]
                    alunos = pd.read_sql_query("SELECT nome FROM alunos WHERE turma_id = ?", CONN, params=(t_id,))["nome"].tolist()
                    
                    if alunos:
                        random.shuffle(alunos)
                        total_alunos += len(alunos)
                        offset_sala = random.randint(0, num_salas - 1)
                        
                        for idx, aluno in enumerate(alunos):
                            sala_destinada = (idx + offset_sala) % num_salas
                            salas[sala_destinada].append({
                                "Nome do Aluno": aluno,
                                "Turma de Origem": nome_t
                            })
                
                if total_alunos == 0:
                    st.error("Não há alunos cadastrados nas turmas selecionadas.")
                else:
                    # Intercalação anti-cola
                    dict_salas_final = {}
                    for i in range(num_salas):
                        por_turma = {}
                        for aluno in salas[i]:
                            t_nome = aluno["Turma de Origem"]
                            if t_nome not in por_turma:
                                por_turma[t_nome] = []
                            por_turma[t_nome].append(aluno)
                        
                        sala_intercalada = []
                        while any(por_turma.values()):
                            for t_nome in list(por_turma.keys()):
                                if por_turma[t_nome]:
                                    sala_intercalada.append(por_turma[t_nome].pop(0))
                        
                        dict_salas_final[i + 1] = sala_intercalada

                    st.session_state['resultado_salas'] = dict_salas_final
                    st.session_state['total_alunos'] = total_alunos

            # Se houver resultado armazenado, exibe os cartões e botões de download
            if 'resultado_salas' in st.session_state:
                dict_salas_final = st.session_state['resultado_salas']
                total_alunos = st.session_state['total_alunos']
                
                st.success(f"Distribuição concluída! {total_alunos} alunos organizados em {len(dict_salas_final)} salas.")
                
                # Botões de Exportação Geral
                col_exp1, col_exp2 = st.columns(2)
                
                with col_exp1:
                    pdf_geral = gerar_pdf_ensalamento(dict_salas_final, nome_customizado)
                    st.download_button(
                        label="📄 Baixar PDF Completo (Todas as Salas)",
                        data=pdf_geral,
                        file_name=f"{nome_customizado}_geral.pdf",
                        mime="application/pdf",
                        type="primary"
                    )
                
                with col_exp2:
                    listas_export = []
                    for s_num, s_alunos in dict_salas_final.items():
                        df_temp = pd.DataFrame(s_alunos)
                        df_temp["Sala Destino"] = f"Sala {s_num}"
                        listas_export.append(df_temp)
                    csv_geral = pd.concat(listas_export).to_csv(index_label="Carteira").encode("utf-8")
                    st.download_button(
                        label="📥 Baixar Planilha Geral (CSV)",
                        data=csv_geral,
                        file_name=f"{nome_customizado}_geral.csv",
                        mime="text/csv"
                    )

                st.markdown("---")
                
                # Exibição Visual por Sala + Download Individual em PDF por Sala
                cols = st.columns(min(len(dict_salas_final), 3))
                
                for i, (num_sala, sala_alunos) in enumerate(dict_salas_final.items()):
                    col_idx = i % 3
                    with cols[col_idx]:
                        st.subheader(f"🚪 Sala {num_sala} ({len(sala_alunos)} alunos)")
                        df_sala = pd.DataFrame(sala_alunos)
                        df_sala.index = range(1, len(df_sala) + 1)
                        st.dataframe(df_sala, use_container_width=True)
                        
                        # PDF Individual da Sala
                        pdf_sala_ind = gerar_pdf_ensalamento({num_sala: sala_alunos}, nome_customizado)
                        st.download_button(
                            label=f"📄 PDF - Sala {num_sala}",
                            data=pdf_sala_ind,
                            file_name=f"{nome_customizado}_Sala_{num_sala}.pdf",
                            mime="application/pdf",
                            key=f"btn_pdf_sala_{num_sala}"
                        )

elif menu == "⚙️ Gerenciar Turmas e Alunos":
    st.header("Cadastro e Manutenção de Alunos")
    
    turmas_df = pd.read_sql_query("SELECT * FROM turmas", CONN)
    
    col1, col2 = st.columns(2)
    with col1:
        nova_turma = st.text_input("Cadastrar Nova Turma:")
        if st.button("Adicionar Turma"):
            if nova_turma.strip():
                try:
                    CURSOR.execute("INSERT INTO turmas (nome) VALUES (?)", (nova_turma.strip(),))
                    CONN.commit()
                    st.success("Turma cadastrada com sucesso!")
                    st.rerun()
                except:
                    st.error("Erro ao cadastrar turma.")
    
    if not turmas_df.empty:
        st.markdown("---")
        turma_sel = st.selectbox("Selecione a turma para visualizar ou editar os alunos:", turmas_df["nome"])
        t_id = int(turmas_df[turmas_df["nome"] == turma_sel]["id"].values[0])
        
        alunos_df = pd.read_sql_query("SELECT id, nome FROM alunos WHERE turma_id = ?", CONN, params=(t_id,))
        
        st.subheader(f"Alunos da turma {turma_sel} ({len(alunos_df)})")
        
        edited_df = st.data_editor(alunos_df, num_rows="dynamic", key="editor_alunos")
        
        if st.button("Salvar Alterações na Lista de Alunos"):
            CURSOR.execute("DELETE FROM alunos WHERE turma_id = ?", (t_id,))
            for _, row in edited_df.iterrows():
                if pd.notna(row["nome"]) and str(row["nome"]).strip():
                    CURSOR.execute("INSERT INTO alunos (nome, turma_id) VALUES (?, ?)", (row["nome"].strip(), t_id))
            CONN.commit()
            st.success("Lista de alunos atualizada!")
            st.rerun()
