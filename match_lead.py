import streamlit as st
from datetime import datetime, timedelta
from streamlit_drawable_canvas import st_canvas

# Configuración general
st.set_page_config(page_title="Match Leader Central", layout="wide")
st.title("⚽ Match Leader - Central de Operaciones")

# Crear pestañas para cada fase del juego
tab_pre, tab_in, tab_post = st.tabs(["Pre-Game", "In-Game", "Half / Post-Game"])

# ==========================================
# PESTAÑA 1: PRE-GAME
# ==========================================
with tab_pre:
    st.header("⚙️ Configuración del Partido")
    col_cfg1, col_cfg2, col_cfg3 = st.columns([2, 1.5, 1.5])

    with col_cfg1:
        snapshot_name = st.text_input("Snapshot Name", value="20260817-efl-car-wre")

    with col_cfg2:
        col_time_input = st.time_input("Hora Kick-off (COL 🇨🇴)", datetime.strptime("14:00", "%H:%M").time())

    with col_cfg3:
        uk_time_calc = (datetime.combine(datetime.today(), col_time_input) + timedelta(hours=6)).time()
        st.metric("Hora Kick-off (UK 🇬🇧)", uk_time_calc.strftime("%H:%M"))

    st.subheader("👕 Equipos y Arqueros")
    col_home, col_away = st.columns(2)

    with col_home:
        st.markdown("### HOME")
        home_color = st.selectbox("Emoji Home", ["🟦", "🔴", "🟩", "🟨", "⚪", "⬛", "🟪", "🟧"], index=0)
        home_gk = st.text_input("Número GK Home", value="1")

    with col_away:
        st.markdown("### AWAY")
        away_color = st.selectbox("Emoji Away", ["🔴", "🟦", "🟩", "🟨", "⚪", "⬛", "🟪", "🟧"], index=0)
        away_gk = st.text_input("Número GK Away", value="22")

    st.divider()
    st.subheader("💬 Mensaje de Inicio para Slack")
    col_str = col_time_input.strftime("%H:%M")
    uk_str = uk_time_calc.strftime("%H:%M")
    
    slack_template = f"""{snapshot_name} - kicking off at {uk_str} 🇬🇧 / {col_str} 🇨🇴

HOME - {home_color} GK #{home_gk}
AWAY - {away_color} GK #{away_gk}"""

    st.text_area("Copia esto y pégalo en Slack:", value=slack_template, height=120)

    st.divider()
    st.subheader("📋 Pre-Game Checklist")
    col_chk1, col_chk2 = st.columns(2)

    with col_chk1:
        st.checkbox("🟢 Shortcuts configurados")
        st.checkbox("🟢 Filtros aplicados")
        p9 = st.checkbox("Parámetro #9")
        st.checkbox("Parámetro #10 (Broadcast location is set)", value=p9, disabled=True)
        st.radio("Rosters / Lineups:", ["Esperando...", "Disponibles OK"], horizontal=True)
        st.radio("Calibración Cámaras:", ["Esperando auto...", "Manual requerida", "Todas OK"], horizontal=True)

    with col_chk2:
        st.caption("1 Hora Antes:")
        m_active = st.checkbox("Activar Mask")
        l_active = st.checkbox("Activar Live")
        drip_enabled = m_active and l_active
        st.checkbox("💧 Realizar Drip", disabled=not drip_enabled)
        
        st.caption("Kick-off Inminente:")
        st.checkbox("🥅 Home Goal (Portería contraria)")
        st.checkbox("🎨 Confirmar colores de equipos")
        st.checkbox("💬 Mensaje Slack enviado")

# ==========================================
# PESTAÑA 2: IN-GAME
# ==========================================
with tab_in:
    st.header("🔄 Bloc de Sustituciones")
    st.caption("Anota rápido aquí. Espera el choque de manos, ejecútalo en el PC y borra el lienzo (icono de papelera).")
    
    col_home_sub, col_away_sub = st.columns(2)
    with col_home_sub:
        st.subheader("🟦 HOME")
        st_canvas(stroke_width=4, stroke_color="#000000", background_color="#e6f2ff", height=200, drawing_mode="freedraw", key="home_notes")
    with col_away_sub:
        st.subheader("🔴 AWAY")
        st_canvas(stroke_width=4, stroke_color="#000000", background_color="#ffe6e6", height=200, drawing_mode="freedraw", key="away_notes")

    st.divider()
    st.header("🟥 TARJETAS ROJAS")
    st_canvas(stroke_width=6, stroke_color="#ff0000", background_color="#ffffff", height=120, drawing_mode="freedraw", key="rojas_notes")

# ==========================================
# PESTAÑA 3: POST-GAME
# ==========================================
with tab_post:
    st.header("⏳ HALF TIME")
    st.checkbox("🧹 Hacer SWEEP de Half Time", key="ht_sweep")
    
    st.divider()
    st.header("🏁 POST GAME")
    col_pg1, col_pg2 = st.columns(2)

    with col_pg1:
        st.subheader("1. Secuencia de Cierre")
        st.error("⚠️ El End Match se marca SOLO DESPUÉS de que el LIVE esté COMPLETO.")
        live_completo = st.checkbox("1️⃣ LIVE COMPLETO")
        end_match = st.checkbox("2️⃣ Marcar END MATCH", disabled=not live_completo)
        st.checkbox("3️⃣ Apagar el LIVE", disabled=not end_match)
        st.checkbox("4️⃣ Invalidar el Drip")

    with col_pg2:
        st.subheader("2. Revisión y Sweep")
        st.checkbox("🔁 Revisar Task Repeating")
        queue_vacia = st.checkbox("🈳 Queue vacía (Cero tasks)")
        st.checkbox("🧹 Hacer SWEEP", disabled=not queue_vacia)
        st.checkbox("✅ Hacer TRACK FINISHER")
        st.checkbox("💬 Mandar Emojis al chat (ej. :sweep:)")