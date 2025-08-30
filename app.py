import streamlit as st

# Parameters 2025 (update jaarlijks)
PCT = 0.30
FRANCHISE = 13785
MAX_GRONDSLAG = 137000
K = 1288
MAX_RESERVERING = 42108  # voor 2025

st.set_page_config(page_title="Jaarruimte & Reserveringsruimte Calculator")

st.title("💰 Jaarruimte & Reserveringsruimte Calculator")
st.write("Vul je gegevens in en zie hoeveel je fiscaal mag inleggen.")

# Inputs
inkomen = st.number_input("Verzamelinkomen (Box 1)", min_value=0, value=60000, step=1000)
factorA = st.number_input("Factor A (uit UPO)", min_value=0, value=1000, step=100)

# Berekening jaarruimte
premiegrondslag = min(max(0, inkomen - FRANCHISE), MAX_GRONDSLAG)
jaarruimte = max(0, PCT * premiegrondslag - (6.27 * factorA) - K)

st.subheader("📊 Resultaten")
st.metric("Jaarruimte (2025)", f"€ {jaarruimte:,.2f}")

# Reserveringsruimte voorbeeld (hier simpel: jaarruimte * aantal jaren)
jaren_onbenut = st.slider("Aantal jaren onbenutte ruimte (max 10)", 0, 10, 3)
reserveringsruimte = min(jaarruimte * jaren_onbenut, MAX_RESERVERING)

st.metric("Reserveringsruimte", f"€ {reserveringsruimte:,.2f}")

# Disclaimer
st.info("Dit is een informatieve tool. Raadpleeg de Belastingdienst of een adviseur voor jouw persoonlijke situatie.")
