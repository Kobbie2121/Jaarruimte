import streamlit as st

# -----------------------------
# Parameters 2025
# -----------------------------
AOW_FRANCHISE = 16322
MAX_GRONDSLAG = 137800
PCT = 0.133
FACTOR_A_MULTIPLIER = 6.27
MAX_RESERVERING = 42108

st.set_page_config(page_title="Super Simpele Jaarruimte Calculator")

st.title("💰 Pensioen Jaarruimte Calculator")
st.write("We helpen je te ontdekken hoeveel je nog fiscaal aftrekbaar kunt storten. Geen stress, gewoon makkelijk!")

# -----------------------------
# Opening: keuze type
# -----------------------------
st.subheader("Wat voor type ben jij?")

type_info = {
    "Werknemer": "Je inkomsten komen uit loondienst. Je baas bouwt pensioen voor je op via een pensioenfonds of verzekeraar.",
    "ZZP / Ondernemer": "Je hebt een eigen bedrijf, bijvoorbeeld een eenmanszaak of VOF. Er is nog geen pensioen opgebouwd.",
    "DGA": "Je bent directeur-grootaandeelhouder van een BV. Je pensioen wordt via de BV opgebouwd."
}

status = st.radio(
    "Kies je situatie",
    options=list(type_info.keys()),
)

st.info(type_info[status])

# -----------------------------
# Inputs per type
# -----------------------------
st.subheader("Vul je gegevens in")

# Verzamelinkomen uitleg
st.caption("ℹ️ Verzamelinkomen = alles wat je in 2024 hebt verdiend uit werk en woning, bruto. Kijk op je jaaropgave of belastingaangifte.")

inkomen = st.number_input(
    "Bruto jaarinkomen (2024)",
    min_value=0,
    value=60000,
    step=1000
)

# Factor A alleen relevant voor Werknemer en DGA
factorA = 0
if status in ["Werknemer", "DGA"]:
    st.caption("ℹ️ Factor A = pensioen dat je al bij je werkgever of BV hebt opgebouwd in 2024. Staat op je UPO.")
    factorA = st.number_input(
        "Factor A (uit UPO 2024)",
        min_value=0,
        value=0,
        step=100
    )

# -----------------------------
# Berekening
# -----------------------------
premiegrondslag = min(max(0, inkomen - AOW_FRANCHISE), MAX_GRONDSLAG - AOW_FRANCHISE)

if status == "ZZP / Ondernemer":
    jaarruimte = max(0, PCT * premiegrondslag)
else:  # Werknemer of DGA
    jaarruimte = max(0, (PCT * premiegrondslag) - (FACTOR_A_MULTIPLIER * factorA))

# Reserveringsruimte voorbeeld
st.subheader("Reserveringsruimte")
st.caption("ℹ️ Dit is hoeveel je eventueel extra mag storten over de afgelopen jaren (max 10 jaar terug).")
jaren_onbenut = st.slider("Aantal jaren onbenutte ruimte (max 10)", 0, 10, 0)
reserveringsruimte = min(jaarruimte * jaren_onbenut, MAX_RESERVERING)

# -----------------------------
# Resultaten tonen
# -----------------------------
st.subheader("📊 Resultaten")
st.metric("Jaarruimte 2025", f"€ {jaarruimte:,.2f}")
st.metric("Reserveringsruimte", f"€ {reserveringsruimte:,.2f}")

# -----------------------------
# Disclaimer
# -----------------------------
st.info(
    "ℹ️ Dit is een super simpele informatieve tool. Gebruik je jaaropgave of belastingaangifte om de cijfers in te vullen. "
    "Raadpleeg altijd een adviseur of de Belastingdienst voor jouw persoonlijke situatie."
)

