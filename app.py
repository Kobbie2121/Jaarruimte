import streamlit as st
import pandas as pd

# -----------------------------
# Parameters 2025
# -----------------------------
AOW_FRANCHISE = 16322
MAX_GRONDSLAG = 137800
PCT = 0.133
FACTOR_A_MULTIPLIER = 6.27
MAX_RESERVERING = 42108

st.set_page_config(page_title="Super Simpele Pensioen & Jaarruimte Tool")

st.title("💰 Super Simpele Pensioen Calculator")
st.write("We maken het makkelijk: ontdek je jaarruimte en hoeveel je maandelijkse inleg later oplevert.")

# -----------------------------
# Opening: keuze type
# -----------------------------
st.subheader("Wat voor type ben jij?")
type_info = {
    "Werknemer": "Je inkomsten komen uit loondienst. Je baas bouwt pensioen voor je op via een pensioenfonds of verzekeraar.",
    "ZZP / Ondernemer": "Je hebt een eigen bedrijf, bijvoorbeeld een eenmanszaak of VOF. Er is nog geen pensioen opgebouwd.",
    "DGA": "Je bent directeur-grootaandeelhouder van een BV. Je pensioen wordt via de BV opgebouwd."
}
status = st.radio("Kies je situatie", options=list(type_info.keys()))
st.info(type_info[status])

# -----------------------------
# Inputs jaarruimte
# -----------------------------
st.subheader("Stap 1: Vul je gegevens in")
st.caption("Bruto inkomen = wat je in 2024 verdiende (jaaropgave / belastingaangifte).")
inkomen = st.number_input("Bruto jaarinkomen (2024)", min_value=0, value=60000, step=1000)

factorA = 0
if status in ["Werknemer", "DGA"]:
    st.caption("Factor A = pensioen dat je al opgebouwd hebt in 2024 (staat op je UPO).")
    factorA = st.number_input("Factor A (uit UPO 2024)", min_value=0, value=0, step=100)

# -----------------------------
# Berekening jaarruimte
# -----------------------------
premiegrondslag = min(max(0, inkomen - AOW_FRANCHISE), MAX_GRONDSLAG - AOW_FRANCHISE)
if status == "ZZP / Ondernemer":
    jaarruimte = max(0, PCT * premiegrondslag)
else:
    jaarruimte = max(0, (PCT * premiegrondslag) - (FACTOR_A_MULTIPLIER * factorA))

st.subheader("📊 Resultaten Jaarruimte")
st.metric("Jaarruimte 2025", f"€ {jaarruimte:,.2f}")

# Reserveringsruimte
st.caption("Reserveringsruimte = extra ruimte die je kunt inhalen van de afgelopen 10 jaar (max. 10 jaar).")
jaren_onbenut = st.slider("Aantal jaren onbenutte ruimte", 0, 10, 0)
reserveringsruimte = min(jaarruimte * jaren_onbenut, MAX_RESERVERING)
st.metric("Reserveringsruimte", f"€ {reserveringsruimte:,.2f}")

# -----------------------------
# Pensioen simulator
# -----------------------------
st.subheader("Stap 2: Pensioenopbouw simulatie")
st.caption("Voer in hoeveel je maandelijks wilt sparen en vanaf welke leeftijd je wilt starten met uitkeren.")

maandbedrag = st.number_input("Maandelijks bedrag (€)", min_value=0, value=300, step=50)
jaren_opbouw = st.number_input("Aantal jaren sparen", min_value=1, value=30, step=1)
rendement = st.number_input("Gemiddeld rendement (%)", min_value=0.0, value=8.0, step=0.1)
start_leeftijd = st.number_input("Leeftijd waarop je wilt starten met pensioen", min_value=50, max_value=80, value=65, step=1)
uitkeringsduur = st.number_input("Uitkeringsduur in jaren", min_value=5, max_value=40, value=20, step=1)
st.caption("Maandelijkse bruto uitkering = totaal opgebouwde bedrag ÷ uitkeringsduur × 12 maanden.")

# Berekening samengestelde interest
r = rendement / 100 / 12  # maandrendement
n = jaren_opbouw * 12     # totaal maanden
P = maandbedrag
fv = P * ((1 + r)**n - 1) / r

# Maandbedrag berekening
maandelijkse_uitkering = fv / (uitkeringsduur * 12)

st.subheader("📈 Verwacht pensioen")
st.metric(f"Totaal opgebouwd pensioen", f"€ {fv:,.0f}")
st.metric(f"Bruto maanduitkering ({uitkeringsduur} jaar)", f"€ {maandelijkse_uitkering:,.0f}")

# Grafiek per jaar
vals = []
tot = 0
for i in range(1, n+1):
    tot = tot*(1+r) + P
    if i % 12 == 0:
        vals.append(tot)
df = pd.DataFrame({"Jaar": list(range(1, len(vals)+1)), "Opgebouwd pensioen": vals})
st.line_chart(df.rename(columns={"Jaar": "index"}).set_index("index"))

# -----------------------------
# Disclaimer
# -----------------------------
st.info(
    "ℹ️ Dit is een eenvoudige informatieve tool. Gebruik je eigen jaaropgave of UPO voor exacte cijfers. "
    "De pensioenopbouw simulatie is een schatting op basis van gemiddeld rendement. Raadpleeg een adviseur voor je persoonlijke situatie."
)
