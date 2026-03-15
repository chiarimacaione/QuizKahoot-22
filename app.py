import streamlit as st
import pandas as pd
import os

# --- PALETA DE COLORES ---
FONDO_AMARILLO = "#FFCE00"
NEGRO_PURO = "#000000"
BLANCO_MAC = "#FFFFFF"
CYAN_A_D = "#69c7e5"  
LILA_B_C = "#e2a9f1"

st.set_page_config(page_title="Chiara's 22 Exam", layout="centered", initial_sidebar_state="auto")

# --- CSS CON TAMAÑOS Y MARGENES AJUSTADOS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Jersey+25&family=Righteous&display=swap');

    .stApp {{
        background-color: {FONDO_AMARILLO};
        background-image: radial-gradient(#e5b900 3px, transparent 3px);
        background-size: 30px 30px;
    }}
    #MainMenu, footer {{visibility: hidden;}}
    header {{background: transparent !important;}}
    .block-container {{ padding: 0rem 1rem 3rem 1rem; max-width: 600px; margin-top: -30px; }}

    /* HEADER NEGRO AJUSTADO (MÁS AIRE ARRIBA) */
    .retro-header {{
        background-color: {NEGRO_PURO};
        color: {BLANCO_MAC};
        margin: 0rem -1rem 2rem -1rem; 
        padding: 40px 20px 20px 20px; 
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        border-bottom: 6px solid {NEGRO_PURO};
    }}
    .retro-header h1 {{ 
        font-family: 'Jersey 25', sans-serif; 
        color: {BLANCO_MAC} !important; 
        font-size: 55px !important;
        margin: 0 0 5px 0; 
        line-height: 1.1;
        font-weight: normal;
        position: relative;
        left: 2px; /* Ajuste óptico */
    }}
    .retro-header h2 {{ 
        font-family: 'Jersey 25', sans-serif; 
        color: {CYAN_A_D} !important; 
        font-size: 36px !important; 
        margin: 0; 
        letter-spacing: 3px; 
        font-weight: normal; 
    }}

    /* TARJETAS MAC OS */
    .mac-window {{
        background-color: {BLANCO_MAC};
        border: 4px solid {NEGRO_PURO};
        border-radius: 12px;
        box-shadow: 6px 6px 0px {NEGRO_PURO};
        margin-bottom: 25px;
        overflow: hidden;
    }}
    .mac-topbar {{
        background-color: {BLANCO_MAC};
        border-bottom: 4px solid {NEGRO_PURO};
        padding: 8px 15px;
        display: flex;
        gap: 8px;
    }}
    .mac-dot {{ width: 14px; height: 14px; border-radius: 50%; border: 2px solid {NEGRO_PURO}; }}
    .mac-content {{
        padding: 15px 20px;
        font-family: 'Jersey 25', sans-serif;
        font-size: 32px;
        color: {NEGRO_PURO};
    }}

    /* TÍTULOS DE PREGUNTA */
    h2.pregunta-title {{
        font-family: 'Righteous', sans-serif !important;
        text-align: center;
        font-size: 42px !important;
        margin-bottom: 25px !important;
        color: {NEGRO_PURO} !important;
        font-weight: normal;
    }}

    /* FORZAR LA GRILLA 2x2 Y CENTRARLA */
    div[data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 15px !important;
    }}
    div[data-testid="stColumn"] {{
        width: calc(50% - 10px) !important;
        flex: 0 0 calc(50% - 10px) !important;
        min-width: calc(50% - 10px) !important;
    }}

    /* ESTILO GLOBAL DE BOTONES */
    button[kind="primary"], button[kind="secondary"], button[kind="tertiary"] {{
        width: 100% !important;
        height: 150px !important; 
        border-radius: 20px !important;
        border: 4px solid {NEGRO_PURO} !important;
        box-shadow: 6px 6px 0px {NEGRO_PURO} !important;
        padding: 0 !important;
        transition: none !important;
    }}
    
    /* LETRA GIGANTE DENTRO DE LOS BOTONES */
    button p, button div, button span {{
        font-family: 'Righteous', sans-serif !important;
        font-size: 60px !important; 
        color: {NEGRO_PURO} !important; 
        margin: 0 !important;
        line-height: 1 !important;
    }}

    /* COLORES FIJOS */
    button[kind="primary"], button[kind="primary"]:hover, button[kind="primary"]:active, button[kind="primary"]:focus {{ background-color: {CYAN_A_D} !important; }}
    button[kind="secondary"], button[kind="secondary"]:hover, button[kind="secondary"]:active, button[kind="secondary"]:focus {{ background-color: {LILA_B_C} !important; }}
    
    /* BOTONES DE ACCIÓN (BLANCOS)*/
    button[kind="tertiary"], button[kind="tertiary"]:hover, button[kind="tertiary"]:active, button[kind="tertiary"]:focus {{
        background-color: {BLANCO_MAC} !important;
        height: 70px !important;
        width: 100% !important;
    }}
    button[kind="tertiary"] p {{
        font-size: 32px !important;
        font-family: 'Jersey 25', sans-serif !important;
    }}

    /* TABLA HIGH SCORE DEL ADMIN AJUSTADA */
    .arcade-board {{
        background-color: {NEGRO_PURO};
        border: 6px solid {BLANCO_MAC};
        border-radius: 15px;
        padding: 25px 20px;
        box-shadow: 10px 10px 0px rgba(0,0,0,0.5);
    }}
    .arcade-title {{
        font-family: 'Righteous', sans-serif;
        color: {FONDO_AMARILLO};
        text-align: center;
        font-size: 48px;
        margin-bottom: 25px;
        letter-spacing: 2px;
    }}
    .arcade-table {{
        width: 100%;
        border-collapse: collapse;
        font-family: 'Jersey 25', sans-serif;
        font-size: 32px;
        color: {BLANCO_MAC};
        text-align: center;
    }}
    .arcade-table th {{
        color: {LILA_B_C};
        border-bottom: 4px dashed {CYAN_A_D};
        padding: 15px 10px;
        font-size: 28px;
        font-weight: normal;
        letter-spacing: 2px;
    }}
    .arcade-table td {{
        padding: 15px 5px;
        border-bottom: 2px solid #333;
    }}
    .arcade-table tr:nth-child(1) td {{ color: {FONDO_AMARILLO}; font-size: 45px; }}
    </style>

    <div class="retro-header">
        <h1>¿QUIÉN CONOCE MÁS A CHIARA?</h1>
        <h2>THE 22 EXAM</h2>
    </div>
    """, unsafe_allow_html=True)


# --- BASE DE DATOS LOCAL ---
DB_FILE = "resultados.csv"
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["Nombre", "Puntaje"]).to_csv(DB_FILE, index=False)

if 'user' not in st.session_state: st.session_state.user = ""
if 'score' not in st.session_state: st.session_state.score = 0
if 'step' not in st.session_state: st.session_state.step = 0
if 'answered' not in st.session_state: st.session_state.answered = False

@st.cache_data
def load_data():
    return pd.read_csv('preguntas.csv', sep=';', encoding='latin-1')
df = load_data()

# --- PANEL ADMIN SECRETO (Barra Lateral) ---
if st.query_params.get("admin") == "true":
    with st.sidebar:
        st.markdown("<h2 style='font-family: Jersey 25; font-size: 40px; color: white;'>ADMIN PANEL</h2>", unsafe_allow_html=True)
        if st.button("VER PODIO", type="tertiary", use_container_width=True):
            st.session_state.view_podio_admin = True
        if st.button("LIMPIAR TABLA", type="tertiary", use_container_width=True):
            pd.DataFrame(columns=["Nombre", "Puntaje"]).to_csv(DB_FILE, index=False)
            st.success("Limpieza completa.")

# --- MOSTRAR PODIO PARA PROYECTAR ---
if st.session_state.get('view_podio_admin'):
    html_podio = """
    <div class="arcade-board">
        <div class="arcade-title">TABLA DE PUNTAJES</div>
        <table class="arcade-table">
            <tr><th>RANK</th><th>JUGADOR</th><th>PTS</th></tr>
    """
    
    if os.path.exists(DB_FILE):
        ranking_admin = pd.read_csv(DB_FILE).sort_values(by="Puntaje", ascending=False).head(10)
        ranking_admin = ranking_admin.reset_index(drop=True)
        
        for i, row in ranking_admin.iterrows():
            html_podio += f"<tr><td>#{i+1}</td><td>{row['Nombre']}</td><td>{row['Puntaje']}</td></tr>"
            
    html_podio += "</table></div><br>"
    st.markdown(html_podio, unsafe_allow_html=True)
        
    if st.button("OCULTAR PODIO", type="tertiary", use_container_width=True):
        st.session_state.view_podio_admin = False
        st.rerun()

# --- FLUJO DE JUEGO PRINCIPAL ---
elif st.session_state.user == "":
    st.markdown("""
        <div class="mac-window">
            <div class="mac-topbar">
                <div class="mac-dot" style="background:#ff5f56;"></div>
                <div class="mac-dot" style="background:#ffbd2e;"></div>
                <div class="mac-dot" style="background:#27c93f;"></div>
            </div>
            <div class="mac-content" style="flex-direction: column; text-align: center;">
                <div style="font-family: Righteous; font-size: 42px; margin-bottom: 1px;">Registrate</div>
                y preparate para el examen...
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    nombre = st.text_input("", placeholder="Escribí tu nombre/apodo...")
    if st.button("INICIAR", type="tertiary", use_container_width=True):
        if nombre:
            st.session_state.user = nombre
            st.rerun()

else:
    if st.session_state.step < len(df):
        pregunta_actual = df.iloc[st.session_state.step]['pregunta']
        
        st.markdown(f"""
            <div class="mac-window" style="margin-bottom: 15px;">
                <div class="mac-topbar">
                    <div class="mac-dot" style="background:#ff5f56;"></div>
                    <div class="mac-dot" style="background:#ffbd2e;"></div>
                    <div class="mac-dot" style="background:#27c93f;"></div>
                </div>
                <div class="mac-content" style="display: flex; justify-content: space-between;">
                    <span>JUGADOR: {st.session_state.user}</span>
                    <span style="color: #ff5f56;">PTS: {st.session_state.score}</span>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 16px;">
                <div style="font-family: 'Righteous', sans-serif; font-size: 38px; color: #000; margin-bottom: -10px;">
                    PREGUNTA #{st.session_state.step + 1}
                </div>
                <div style="font-family: 'Righteous', sans-serif; font-size: 32px; color: #000; line-height: 1.1; padding: 10px 0;">
                    {pregunta_actual}
                </div>
            </div>
        """, unsafe_allow_html=True)

        if not st.session_state.answered:
            c1, c2 = st.columns(2)
            with c1: a = st.button("A", type="primary", use_container_width=True)
            with c2: b = st.button("B", type="secondary", use_container_width=True)
            
            c3, c4 = st.columns(2)
            with c3: c = st.button("C", type="secondary", use_container_width=True)
            with c4: d = st.button("D", type="primary", use_container_width=True)

            res = None
            if   a: res = 'A'
            elif b: res = 'B'
            elif c: res = 'C'
            elif d: res = 'D'

            if res:
                st.session_state.answered = True
                correcta = df.iloc[st.session_state.step]['correcta']
                if res == correcta:
                    st.session_state.score += 100
                st.rerun()
        else:
            st.markdown("""
                <div class="mac-window">
                    <div class="mac-content" style="flex-direction: column; text-align: center;">
                        <span style="font-family: Righteous; font-size: 45px; display: block; margin-bottom: 15px;">RESPUESTA ENVIADA</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("SIGUIENTE", type="tertiary", use_container_width=True):
                st.session_state.step += 1
                st.session_state.answered = False
                st.rerun()
    else:
        # Final
        if 'saved' not in st.session_state:
            res_df = pd.read_csv(DB_FILE)
            new_row = pd.DataFrame([{"Nombre": st.session_state.user, "Puntaje": st.session_state.score}])
            pd.concat([res_df, new_row]).to_csv(DB_FILE, index=False)
            st.session_state.saved = True

        st.markdown(f"""
            <div class="mac-window">
                <div class="mac-topbar">
                    <div class="mac-dot" style="background:#ff5f56;"></div>
                    <div class="mac-dot" style="background:#ffbd2e;"></div>
                    <div class="mac-dot" style="background:#27c93f;"></div>
                </div>
                <div class="mac-content" style="flex-direction: column; text-align: center;">
                    <h1 style="font-family:'Righteous'; font-size:40px; margin:0;">FIN DEL EXAMEN</h1>
                    <p style="margin-top:10px;">Obtuviste:</p>
                    <p style="font-size: 70px; font-family: 'Righteous'; color:{CYAN_A_D}; text-shadow: 4px 4px 0px #000; margin: 10px 0;">{st.session_state.score} PUNTOS</p>
                    <p>Atenta al podio...</p>
                </div>
            </div>
        """, unsafe_allow_html=True)