import streamlit as st
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh
import os

# Configuración de la página para aprovechar el monitor del PC
st.set_page_config(page_title="Match Leader - Operaciones", layout="wide")

# Motor que actualiza la app cada 60 segundos para el reloj y alertas
st_autorefresh(interval=60000, key="reloj_interno")

st.title("⚽ Central de Operaciones - Match Leader")

# ==========================================
# SECCIÓN GLOBAL: HORA Y ALERTAS
# ==========================================
col_time1, col_time2, col_time3 = st.columns(3)

with col_time1:
    col_time_input = st.time_input("Hora Kick-off (Colombia 🇨🇴)", datetime.strptime("14:00", "%H:%M").time())
with col_time2:
    uk_time_calc = (datetime.combine(datetime.today(), col_time_input) + timedelta(hours=6)).time()
    st.metric("Hora Kick-off (Calculada UK 🇬🇧)", uk_time_calc.strftime("%H:%M"))
with col_time3:
    st.metric("Hora Actual (Local)", datetime.now().strftime("%H:%M"))

st.divider()

# Pestañas para dividir el flujo de trabajo
tab_pre, tab_in, tab_post = st.tabs(["Pre-Game", "In-Game", "Half / Post-Game"])

# ==========================================
# PESTAÑA 1: PRE-GAME
# ==========================================
with tab_pre:
    st.header("⚙️ Configuración y Mensajes")
    
    # 1. SETUP DE EQUIPOS Y HORA
    col_cfg1, col_cfg2, col_cfg3 = st.columns([2, 1, 1])
    with col_cfg1:
        snap_name = st.text_input("Snapshot Name", value="20260817-efl-car-wre")
    with col_cfg2:
        h_color = st.selectbox("Emoji Home", ["🟦", "🔴", "🟩", "🟨", "⚪", "⬛", "🟪", "🟧"], index=0)
        h_gk = st.text_input("Número GK Home", value="1")
    with col_cfg3:
        a_color = st.selectbox("Emoji Away", ["🔴", "🟦", "🟩", "🟨", "⚪", "⬛", "🟪", "🟧"], index=0)
        a_gk = st.text_input("Número GK Away", value="22")

    st.write("") # Espacio
    
    # 2. GENERADORES DE MENSAJES SLACK
    col_msg1, col_msg2 = st.columns(2)
    
    with col_msg1:
        st.subheader("💬 Slack: Inicio de Partido")
        slack_msg = f"{snap_name} - kicking off at {uk_time_calc.strftime('%H:%M')} 🇬🇧 / {col_time_input.strftime('%H:%M')} 🇨🇴\n\nHOME - {h_color} GK #{h_gk}\nAWAY - {a_color} GK #{a_gk}"
        st.text_area("Copia y pega:", value=slack_msg, height=220, key="msg_inicio")

    with col_msg2:
        st.subheader("🧵 Slack: Hilo para Operadores")
        c_link, c_seg, c_ref = st.columns(3)
        with c_link: qa_link = st.text_input("QA Link", value="https://")
        with c_seg: op_segments = st.text_input("Op Segments", value="@")
        with c_ref: op_refs = st.text_input("Op Refs", value="@")
        
        c_h_reid, c_a_reid = st.columns(2)
        with c_h_reid: op_home = st.text_input("REID Home", value="@")
        with c_a_reid: op_away = st.text_input("REID Away", value="@")

        todas_etiquetas = [tag for tag in [op_segments, op_home, op_away, op_refs] if tag.strip() != "" and tag.strip() != "@"]
        tags_juntas = " ".join(todas_etiquetas)

        texto_hilo = f"""{tags_juntas}
Hi team, hope everyone is doing great! 🤝

Our game today is {h_color} vs {a_color}. Here is our QA Link for this match: {qa_link}
Please remember to clock in. Let's have a smooth game and smash it! 🔥

Game start time: {col_time_input.strftime('%H:%M')} 🇨🇴

📌 ASSIGNMENTS:
Segments {op_segments}

REID
Home {op_home}
Away {op_away}
Refs {op_refs}"""
        st.text_area("Copia y pega:", value=texto_hilo, height=220, key="msg_hilo")

    st.divider()

    # 3. CHECKLISTS PRE-GAME
    st.header("📋 Checklists Pre-Game")
    col_pre1, col_pre2 = st.columns(2)
    
    with col_pre1:
        st.subheader("Setup Inicial")
        chk_shortcuts = st.checkbox("🟢 Shortcuts configurados")
        chk_filtros = st.checkbox("🟢 Filtros aplicados")
        p9 = st.checkbox("Parámetro #9")
        chk_p10 = st.checkbox("Parámetro #10 (Broadcast location is set)", value=p9, disabled=True)
        
        rosters = st.radio("Rosters / Lineups:", ["Faltan", "Listos"], horizontal=True)
        calib = st.radio("Cámaras:", ["Esperando", "Listas"], horizontal=True)

    with col_pre2:
        st.subheader("Tiempo Crítico (1 Hora Antes)")
        m_active = st.checkbox("Activar Mask")
        l_active = st.checkbox("Activar Live")
        
        drip_enabled = m_active and l_active
        chk_drip = st.checkbox("💧 Realizar Drip", disabled=not drip_enabled)
        
        st.subheader("Kick-off Inminente")
        chk_home = st.checkbox("🥅 Home Goal configurada")
        chk_colors = st.checkbox("🎨 Colores confirmados")

    # --- LÓGICA DE ALERTA SONORA ---
    hora_actual = datetime.now()
    hora_partido = datetime.combine(datetime.today(), col_time_input)
    minutos_faltantes = (hora_partido - hora_actual).total_seconds() / 60

    if 0 < minutos_faltantes <= 60 and not (m_active and l_active):
        st.error("🚨 ALERTA: ¡Falta 1 hora o menos! Activa MASK y LIVE inmediatamente.")
        if os.path.exists("alerta.mp3"):
            st.audio("alerta.mp3", autoplay=True)
        else:
            st.warning("⚠️ (No se encontró el archivo 'alerta.mp3' para el sonido)")

    # --- REVISIÓN DE TAREAS FALTANTES ---
    tareas_totales = 8
    tareas_hechas = sum([chk_shortcuts, chk_filtros, p9, rosters=="Listos", calib=="Listas", chk_drip, chk_home, chk_colors])
    
    st.progress(tareas_hechas / tareas_totales)
    if tareas_hechas < tareas_totales:
        st.warning(f"Faltan {tareas_totales - tareas_hechas} tareas críticas de Pre-Game.")
    else:
        st.success("✅ ¡Pre-Game 100% completado!")

# ==========================================
# PESTAÑA 2: IN-GAME
# ==========================================
with tab_in:
    st.header("⏱️ Recordatorios In-Game")
    st.info("💡 Tu atención debe estar en la interfaz principal y la transmisión.")
    st.checkbox("📌 Confirmar visualmente choques de manos en sustituciones.")
    st.checkbox("📌 Validar doble amarilla / roja directa con la transmisión.")

# ==========================================
# PESTAÑA 3: POST-GAME
# ==========================================
with tab_post:
    st.header("⏳ HALF TIME")
    st.checkbox("🧹 Hacer SWEEP de Half Time")
    
    st.divider()
    st.header("🏁 POST GAME")
    st.error("⚠️ SECUENCIA ESTRICTA: El End Match se marca SOLO DESPUÉS de que el LIVE esté COMPLETO.")
    
    col_pg1, col_pg2 = st.columns(2)

    with col_pg1:
        st.subheader("Secuencia de Cierre")
        live_completo = st.checkbox("1️⃣ LIVE COMPLETO")
        end_match = st.checkbox("2️⃣ Marcar END MATCH", disabled=not live_completo)
        if live_completo and not end_match:
            st.warning("👉 Marca el End Match ahora.")
            
        apagar_live = st.checkbox("3️⃣ Apagar el LIVE", disabled=not end_match)
        st.checkbox("4️⃣ Invalidar el Drip")

    with col_pg2:
        st.subheader("Limpieza Final")
        st.checkbox("🔁 Revisar Task Repeating")
        queue_vacia = st.checkbox("🈳 Queue vacía (Cero tasks)")
        st.checkbox("🧹 Hacer SWEEP", disabled=not queue_vacia)
        st.checkbox("✅ Hacer TRACK FINISHER")
        
        st.divider()
        st.subheader("💬 Emojis Rápidos para Slack")
        st.code(":sweep:", language=None)
        st.code(":end_match:", language=None)
