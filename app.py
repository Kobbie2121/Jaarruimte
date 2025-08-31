import streamlit as st

# -------------------------
# Parameters 2025
# -------------------------
FRANCHISE = 13785        # AOW-franchise
MAX_GRONDSLAG = 137000   # maximale pensioengrondslag
PERCENTAGE = 0.30        # 30% voor jaarruimte berekening
FACTOR_A_MULTIPLIER = 6.27
K_BEDRAG = 1288

# -------------------------
# Page setup
# -------------------------
st.set_page_config(page_title="Jaarruimte Calculator", layout="centered")
st.title("🔎 Jaarruimte Calculator — huidig jaar")
st.write("Bereken eenvoudig je jaarruimte voor het huidige jaar. Alleen huidig jaar, geen reserveringsruimte. Dummy-uitleg bij elk veld.")

# -------------------------
# Vraag: hoe verdien je geld?
# -------------------------
st.header("Hoe verdien je je geld?")
st.write("Kies wat het beste bij jou past. Heb je meerdere inkomstenbronnen? Kies 'Combinatie'.")
income_type = st.radio(
    "Hoe verdien je je geld?",
    ("Werknemer", "ZZP'er", "DGA", "Combinatie")
)

# -------------------------
# Invoer per type
# -------------------------
salary = 0.0
profit = 0.0
dga_salary = 0.0
factor_a = 0.0

def euro_input(label, key, default=0):
    return st.number_input(label, min_value=0.0, value=float(default), step=100.0, format="%.2f")

# Werknemer
if income_type == "Werknemer":
    salary = euro_input("Bruto jaarsalaris (loon uit loondienst)", "salary_w", 135200)
    st.caption("ℹ️ Jaaropgave: 'loon voor de loonheffing' of verzamelinkomen Box 1.")
    factor_a = euro_input("Factor A (pensioenaangroei, uit UPO)", "factora_w", 2216)
    st.caption("ℹ️ Factor A staat op je UPO. Vul 0 in als je geen pensioen via werkgever hebt.")

# ZZP'er
elif income_type == "ZZP'er":
    profit = euro_input("Winst uit onderneming (jaar)", "profit_z", 60000)
    st.c
