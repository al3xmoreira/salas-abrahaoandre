import streamlit as st
import sqlite3
import pandas as pd
import random

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

    # Carga inicial se o banco estiver vazio
    CURSOR.execute("SELECT COUNT(*) FROM turmas;")
    if CURSOR.fetchone()[0] == 0:
        turmas_iniciais = [
            (1, '1ª A'),
            (2, '1º Técnico (Mineração)'),
            (3, '2ª A'),
            (4, '2º Técnico (Dev. Sistemas)'),
            (5, '3ª A'),
            (6, '6º Ano'),
            (7, '7º Ano'),
            (8, '8º Ano'),
            (9, '9º Ano')
        ]
        CURSOR.executemany("INSERT INTO turmas (id, nome) VALUES (?, ?);", turmas_iniciais)
        
        alunos_iniciais = [
-- Turma: 1ª A
('ANTONIA SÂMARA DOS SANTOS SOUSA LIMA', 1),
('EMILLY NUNES DIAS', 1),
('FELYPE RODEN DE FRANÇA SANTOS', 1),
('GABRIEL HENRIQUE NUNES', 1),
('HANRY MIGUEL SANTOS MILHOMEM', 1),
('HELOISE HELENA MENDES DE PAIVA', 1),
('HENRIQUE FONSECA SOUSA', 1),
('JOÃO VITOR DA SILVA RIBEIRO', 1),
('JULIA ALVES MACEDO', 1),
('MARIA EDUARDA GOMES DA SILVA', 1),
('MARINA SOUZA GOMES', 1),
('MATHEUS BERNARDES DE FREITAS', 1),
('MATHEUS OLIVEIRA AGUILAR ROCHA', 1),
('OTÁVIO HENRIQUE BORGES LIFONSO', 1),
('PAULO HENRIQUE PINTO DE ARAÚJO', 1),
('PEDRO GABRIEL HILÁRIO DE OLIVEIRA', 1),
('PEDRO GUILHERME SANTANA E SILVA MESQUITA', 1),
('PEDRO MIGUEL RODRIGUES PEREIRA', 1),
('TAINA DE OLIVEIRA ANDRADE MIGUEL', 1),
('WESLEY PEREIRA MAGALHÃES', 1),
('WILLAMY SANTOS DA SILVA', 1),
('KAUA GABRIEL MENDES RICARDE', 1),
('EMILLY LEAL DE SOUSA', 1),
('YSADORA OLIVEIRA SANTΑΝΑ', 1),
('ENZO DA SILVA BRAGA MARTINS', 1),
('MARIA EDUARDA SOUSA DA SILVA', 1),

-- Turma: 1º Técnico (Mineração)
('ADÃO LUIZ MENDONÇA GONÇALVES', 2),
('AIRTON SILVA DE ARAUJO LUCAS', 2),
('ARTHUR SILVA PEDROSA', 2),
('BRENO VILAS BOAS SANTOS DIAS', 2),
('DANIEL HENRIQUE FIDELIS DA SILVA', 2),
('DIONARA MYLENA ARAUJO SILVA', 2),
('GABRIEL FERREIRA ALVES', 2),
('GABRIEL GONÇALVES MENEZES MARQUES', 2),
('GUILHERME ANTONIO FIDELES DA FONSECA', 2),
('GUSTAVO HENRIQUE FERREIRA DOS SANTOS', 2),
('IAN PABLO PEREIRA DA SILVA BATISTA', 2),
('ISABELA CHAMONE RABELO', 2),
('ISABELLA DE SOUSA SILVA', 2),
('JOÃO LUCAS BELARMINO VIEIRA', 2),
('LARY VICTÓRIA ARAÚJO DE OLIVEIRA', 2),
('MARIA FERNANDA RODRIGUES FERNANDES PEREIRA', 2),
('MARIA GABRIELLA RIBEIRO', 2),
('MARIA HELLOAH ROSA SILVA MACHADO', 2),
('MARIA VITÓRIA SANTOS DE FARIA', 2),
('MARIA VITTÓRIA RIBEIRO', 2),
('MIGUEL BARBOSA PACHECO', 2),
('MIGUEL SILVEIRA SOUTO', 2),
('RAQUELL DE SOUZA MACÊNA', 2),
('VICTOR HENRIQUE RIBEIRO', 2),
('VICTOR HUGO SILVA MORAIS', 2),
('ANTONELLA RODRIGUES DE OLIVEIRA PRADO', 2),

-- Turma: 2ª A
('ANA BEATRIZ MARIANO DA SILVA', 3),
('BRUNO RIBEIRO DOS SANTOS', 3),
('EVELLYN NATTÁLYA DE JESUS DA SILVA', 3),
('GUSTAVO PEREIRA DOS SANTOS', 3),
('MARIA ANGELINNY SALVINO DA SILVA', 3),
('MARIA CLARA ALVES PIRES', 3),
('MARIA EDUARDA DE OLIVEIRA REIS', 3),
('PAOLA MARTINS BORGES', 3),
('PEDRO AUGUSTO RODRIGUES LIMA', 3),
('TALISSOM OLIVEIRA DA SILVA', 3),
('VITÓRIA DA SILVA ROSA BORGES LEAL', 3),
('GABRIELLA APARECIDA MEDEIROS PIMENTA SILVA', 3),

-- Turma: 2º Técnico (Dev. Sistemas)
('ANA CLARA OLIVEIRA FERNANDES', 4),
('ANDRÉ FELIPE DA SILVA', 4),
('EDUARDA SILVA RIBEIRO', 4),
('GABRIEL ASSUNÇÃO DIAS', 4),
('GABRIEL SANTOS MARTIN', 4),
('ISAAC BARUC DE SOUSA SANTANA', 4),
('JÚLIO CÉSAR DA SILVA', 4),
('KAUANE MIKAELLY DOS SANTOS GOMES', 4),
('LEANDER DAVI SILVA HELENA', 4),
('LUCAS GABRIEL SILVA MONTEIRO', 4),
('MARCOS MIGUEL FERNANDES PAULISTA DA SILVA', 4),
('MATHEUS CARVALHO DE JESUS', 4),
('NICOLAS GONÇALVES DOS SANTOS', 4),
('NICOLAS JAFÉ DOS SANTOS RIBEIRO', 4),
('NYCOLAS FERREIRA DA SILVA', 4),
('PEDRO RUAN DA SILVA FERREIRA', 4),
('RAYSSA OLIVEIRA GOMES', 4),
('RIAN RIVEM BATISTA DE SOUZA', 4),
('SAMUELL DA SILVA CELSO', 4),
('THAYSSA CRISTINA RIBEIRO DA SILVA', 4),
('VICTOR GABRIEL RABELO RAMOS', 4),
('VICTOR HUGO DE ARAÚJO SANTOS', 4),
('VITOR VENTURA DA SILVA', 4),

-- Turma: 3ª A
('ALINE BARBOSA DA SILVA', 5),
('ANA CLARA DE JESUS BRITO', 5),
('ANA CLARA VIEIRA DIAS', 5),
('ANNA JÚLIA DE OLIVEIRA SILVA', 5),
('AUGUSTO CÉSAR SILVA DANTAS', 5),
('BRUNA CRISTINA DE SOUSA RODRIGUES', 5),
('BRYAN MIGUEL BORGES PEDROZA', 5),
('CAIO VINÍCIUS TENÓRIO', 5),
('CARLOS EDUARDO DOS SANTOS DE FARIA', 5),
('DAVI ALMEIDA PURCINA', 5),
('ESTHER VICTORIA PEREIRA LEITE', 5),
('FLÁVIO HENRYCK DAMAS DE ARAÚJO', 5),
('GABRIEL FELIPE CARDOSO PEREIRA SANTOS', 5),
('GABRIELLY SILVERIO DOS SANTOS', 5),
('GUILHERME ARRUDA SILVA', 5),
('HUDSON LEMES DE CASTRO', 5),
('JOAO VICTOR PEREIRA BARBOSA', 5),
('LARA RAIANNE SILVA BARROS', 5),
('MANOEL MARÇAL GOMES DE MIRANDA', 5),
('MARIA EDUARDA DA SILVA RIBEIRO', 5),
('MARIA EDUARDA OLIVEIRA DE ANDRADE', 5),
('MILENA GONÇALVES ROSA', 5),
('OTAVIO DE SOUSA', 5),
('RAFAELA APARECIDA ATAIDE ANDRADE', 5),
('SAIMOM HALIFER SOUZA PIRES', 5),
('VÍCTOR DE SOUZA SILVÉRIO', 5),
('VIVIANE ABADIA ALVES DUARTE', 5),
('INGRID DAYANE PASCOAL DE OLIVEIRA', 5),

-- Turma: 6º Ano
('AGATA EMANUELLY FLEURY ABADIA PEREIRA', 6),
('ALICE GABRIELLE DA SILVA SABINO', 6),
('AMANDA GABRIELY DA SILVA CARDOSO', 6),
('AMANDA OLIVEIRA DA SILVA', 6),
('ANTÔNIO DAVID OLIVEIRA PEREIRA', 6),
('BENICIO SILVA BERNARDES', 6),
('BENJAMIN DOS SANTOS MENDES', 6),
('BERNARDO HENRIQUE ALVES RIBEIRO', 6),
('BERNARDO SOUZA ARAUJO', 6),
('CARLOS EDUARDO DA SILVA SANTOS', 6),
('DAVI LUCAS SANTANA DE PAULA', 6),
('EDUARDO ANTÔNIO CIRILO DE SOUZA', 6),
('EMANUELLE DE SOUSA SILVA', 6),
('EMANUELY OLIVEIRA DOS SANTOS ASSIS', 6),
('ENZO ALEXANDRE FÉLIX MACHADO', 6),
('ENZO MARTINS DA SILVA', 6),
('EVELYN VITORIA DA SILVA', 6),
('FILIPE RODRIGUES DA COSTA', 6),
('GIOVANNA FROEDE PIRES', 6),
('ISABELLY WIGGERS DE OLIVEIRA SILVA', 6),
('ISAÍAS BARBOSA VERA', 6),
('KAUA BELCHIOR ARRUDA', 6),
('KEMILLY VITORIA FONTANA DE ANDRADE', 6),
('MARIA ALICE ALVES ROCHA SILVA', 6),
('MARIA LUIZA TOMAZ DE OLIVEIRA PIRES', 6),
('MIGUEL ANTONIO CIRILO', 6),
('MIGUEL DOS SANTOS MENDES', 6),
('MIGUEL HENRIQUE DA SILVA', 6),
('MIKAELA ALVES PIRES', 6),
('MYLENA EVANGELISTA DOS SANTOS', 6),
('SARA FERREIRA', 6),
('SOPHIA RODRIGUES DE MARINS', 6),
('SOPHIA VITÓRIA DE ARAÚJO FREITAS', 6),
('VIVIANY LIMEIRA DE ANDRADE', 6),
('AMANDA VITORYA SANTOS LIMA', 6),

-- Turma: 7º Ano
('AGATHA DA SILVA ANDRADE', 7),
('ALICE CAROLINA FERREIRA DA SILVA', 7),
('ANA BEATRIZ PEREIRA ARRUDA', 7),
('AYSHA GABRIELLY BORGES LIFONSO', 7),
('BHIANCA BERNARDES DE FREITAS', 7),
('DAVI FELIX DUARTE', 7),
('DAVI LUCAS MARQUES DE OLIVEIRA', 7),
('DAVI LUIZ DA SILVA CONCEIÇÃO', 7),
('DIEGO NASCIMENTO SILVA', 7),
('EDUARDO MAGIOTTO DOS SANTOS ALVES', 7),
('ELOÁ ESTRELA FERNANDES', 7),
('EMANUELLY VICTORIA SOUZA SANTOS', 7),
('GABRIEL AGUIAR DOS SANTOS', 7),
('GABRIEL FELIX DUARTE', 7),
('GABRIEL LEMES MORAIS DA SILVA PRADO', 7),
('GRAZIELLY DA CONCEIÇÃO SILVA', 7),
('HEITOR MENEZES MARTINS', 7),
('HEITOR PEREIRA DINIZ', 7),
('ISIS DAYARA BASTOS ANDRADE', 7),
('JOÃO MIGUEL SILVA SOUZA', 7),
('JOSÉ CARLOS CARDOSO PEREIRA SANTOS', 7),
('KEVIN HENRIQUE PEREIRA DA SILVA', 7),
('LAURA MAGALHÃES DA SILVA', 7),
('LETICIA SANTANA SANTOS', 7),
('MANUELLA DA COSTA BORGES', 7),
('MARCELA ARRUDA OLIVEIRA', 7),
('MARIA JÚLIA CARVALHO NEIVA RIBEIRO', 7),
('MATHEUS GUIMARÃES LEAL', 7),
('PABLLO ALEXSANDER SOUSA CARDOSO', 7),
('PEDRO FERNANDES VAZ DOS REIS', 7),
('RAPHAEL LEONARDO DA SILVA', 7),
('VICTTOR HUGO LOPES DE OLIVEIRA', 7),
('NÍCOLLAS MOISÉS SILVA TEREZA', 7),
('MARIA VITÓRIA VIEIRA REZENDE', 7),
('DARLLON MIKAEL RIBEIRO COSTA', 7),

-- Turma: 8º Ano
('ADILSON MARQUES DE OLIVEIRA', 8),
('ANA JÚLIA REINALDO RODRIGUES', 8),
('ARTHUR MARCELINO BRAZ', 8),
('CARLOS EDUARDO FLOR FARIA', 8),
('DAVI DE SOUSA MENDES', 8),
('DAVID RAFFAEL BARBOSA BASTOS', 8),
('DULCE MARIA OLIVEIRA MIGUEL', 8),
('EMANUELA FERREIRA HARNISCH', 8),
('GABRIEL ANTONIO ALVES DA SILVA', 8),
('GABRIEL HENRIQUE SILVA RIBEIRO', 8),
('GUILHERME KAUER DA SILVA DO NASCIMENTO', 8),
('HELOISA PEREIRA MATOS', 8),
('IGOR NERI SANTANA JÚNIOR', 8),
('IGOR VINICIUS DE SOUZA SANTOS FILHO', 8),
('ITALLO CARVELO COELHO', 8),
('ITALO AUGUSTO DE SOUZA BORBA', 8),
('JOÃO LUCAS CONCEIÇÃO SILVA', 8),
('JOÃO PEDRO CORREA DE MATOS', 8),
('JULIA ALMEIDA PEREIRA', 8),
('MARIANA NUNES DE OLIVEIRA', 8),
('MICHEL CARVALHO COSTA', 8),
('MIGUEL BUENO SAFATLE DE SOUZA', 8),
('MIRIAM MARIANO DA SILVA', 8),
('NICOLAS DOS SANTOS OLIVEIRA', 8),
('NYCOLAS PEREIRA DE SOUSA', 8),
('PAMELA EDUARDA AIRES DOS SANTOS', 8),
('PEDRO HENRIQUE VIEIRA DOS SANTOS', 8),
('SOFFIA LUIZA DE JESUS SOUZA', 8),
('SOPHIA GONÇALVES DOS SANTOS', 8),
('VERÔNICA MARIA ALVES RIBEIRO', 8),
('VITOR HUGO IVO DE PAULA', 8),
('YASMIM VITÓRIA FONTANA DE ANDRADE', 8),
('EMANUELLY VIEIRA MONTEIRO', 8),
('DHEYMIS RAMOS MARTINS', 8),

-- Turma: 9º Ano
('ALICE FURTADO DOS SANTOS JORGE', 9),
('ALICE GOMES ROSA', 9),
('ANNA LUIZA DA SILVA', 9),
('CARLOS GABRIEL RODRIGUES DA SILVA', 9),
('DAVI LUIS OLIVEIRA DE CARVALHO DA SILVA', 9),
('DAVI LUKA DA SILVA', 9),
('GABRIEL MAGIOTTO DOS SANTOS', 9),
('GABRIEL PEREIRA FERNANDES', 9),
('IAN DANIEL MENDES FLORENCIO', 9),
('ISADORA TEIXEIRA COUTINHO', 9),
('ITALO JEAN DE AZEVEDO FERREIRA', 9),
('JOÃO GUILHERME SILVA SOUSA', 9),
('JÚLIO CÉSAR DOS SANTOS DANTAS', 9),
('KAIO VICTOR TOMAZ DE OLIVEIRA PIRES', 9),
('KATHLEN YOHANA SANTANA BORGES', 9),
('KAUAN HENRIQUE GOMES DA SILVA', 9),
('KAYNAN CAVALCANTE SALVINO DE JESUS', 9),
('LUDMILLA ALVES RAMOS', 9),
('LUDMILLA PEREIRA MATOS', 9),
('MANUELLA NASCIMENTO MELO', 9),
('MARIA AMANDA ALVES CONCEIÇÃO', 9),
('MARIA EDUARDA EVANGELISTA DOS SANTOS', 9),
('MARIA RAFAELA DE SOUSA SANTANA', 9),
('MAYSA AZEVEDO ANDRADE', 9),
('NÁDLLA VITÓRIA COELHO CARVALHO', 9),
('NATA YOSSEF DOS SANTOS SILVA', 9),
('PERSEUS TSEREWEDE TSIBDA ADI', 9),
('RAFAEL HENRIQUE BARBOSA MAGELA', 9),
('RAIANNY MICAELE CRUZ DO NASCIMENTO', 9),
('DEYUSON TSAWETE TSIROWA', 9),
('GUSTAVO KASSIO SOUSA', 9),
('JOSE AUGUSTO DO NASCIMENTO PACIENCIA', 9);        ]
        CURSOR.executemany("INSERT INTO alunos (nome, turma_id) VALUES (?, ?);", alunos_iniciais)
        CONN.commit()

inicializar_banco()

# --- INTERFACE PRINCIPAL ---
st.title("🏫 Sorteador & Misturador de Salas de Prova")

menu = st.sidebar.radio("Navegação", ["🎲 Gerar Ensalamento", "⚙️ Gerenciar Turmas e Alunos"])

# MÓDULO: GERAR ENSALAMENTO
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
            
            if st.button("🔀 Sortear e Misturar Alunos", type="primary"):
                ids_turmas = turmas_df[turmas_df["nome"].isin(turmas_selecionadas)]["id"].tolist()
                
                turmas_com_alunos = {}
                total_alunos = 0
                for t_id in ids_turmas:
                    nome_t = turmas_df[turmas_df["id"] == t_id]["nome"].values[0]
                    alunos = pd.read_sql_query("SELECT nome FROM alunos WHERE turma_id = ?", CONN, params=(t_id,))["nome"].tolist()
                    random.shuffle(alunos)
                    turmas_com_alunos[nome_t] = alunos
                    total_alunos += len(alunos)
                
                if total_alunos == 0:
                    st.error("Não há alunos cadastrados nas turmas selecionadas.")
                else:
                    # Intercalação Round-Robin
                    alunos_intercalados = []
                    while any(turmas_com_alunos.values()):
                        for t_nome in list(turmas_com_alunos.keys()):
                            if turmas_com_alunos[t_nome]:
                                alunos_intercalados.append({
                                    "Nome do Aluno": turmas_com_alunos[t_nome].pop(0),
                                    "Turma de Origem": t_nome
                                })
                    
                    # Distribuição equilibrada nas salas
                    salas = [[] for _ in range(num_salas)]
                    for idx, aluno in enumerate(alunos_intercalados):
                        sala_destinada = idx % num_salas
                        salas[sala_destinada].append(aluno)
                    
                    st.success(f"Distribuição concluída com sucesso! Total de {total_alunos} alunos divididos em {num_salas} salas.")
                    
                    # Exibição visual das salas
                    cols = st.columns(min(num_salas, 3))
                    listas_exportacao = []
                    
                    for i, sala in enumerate(salas):
                        col_idx = i % 3
                        with cols[col_idx]:
                            st.subheader(f"🚪 Sala {i+1} ({len(sala)} alunos)")
                            df_sala = pd.DataFrame(sala)
                            df_sala.index = range(1, len(df_sala) + 1)
                            st.dataframe(df_sala, use_container_width=True)
                            
                            df_export = df_sala.copy()
                            df_export["Sala Destino"] = f"Sala {i+1}"
                            listas_exportacao.append(df_export)
                    
                    # Exportação CSV
                    df_geral = pd.concat(listas_exportacao)
                    csv = df_geral.to_csv(index_label="Carteira/Posição").encode("utf-8")
                    st.download_button(
                        label="📥 Baixar Lista Geral para Impressão (CSV)",
                        data=csv,
                        file_name="ensalamento_provas.csv",
                        mime="text/csv"
                    )

# MÓDULO: GERENCIAR TURMAS E ALUNOS
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
        
        # Tabela editável diretamente na interface web
        edited_df = st.data_editor(alunos_df, num_rows="dynamic", key="editor_alunos")
        
        if st.button("Salvar Alterações na Lista de Alunos"):
            CURSOR.execute("DELETE FROM alunos WHERE turma_id = ?", (t_id,))
            for _, row in edited_df.iterrows():
                if pd.notna(row["nome"]) and str(row["nome"]).strip():
                    CURSOR.execute("INSERT INTO alunos (nome, turma_id) VALUES (?, ?)", (row["nome"].strip(), t_id))
            CONN.commit()
            st.success("Lista de alunos atualizada!")
            st.rerun()