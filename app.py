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
    st.caption("ℹ️ Gebruik winst zoals in belastingaangifte.")
    factor_a = euro_input("Factor A (pensioenaangroei verplicht pensioen, indien van toepassing)", "factora_z", 0)
    st.caption("ℹ️ Vul hier de verplicht opgebouwde Factor A in (bijvoorbeeld via lijfrente of bedrijfspensioen). Vul 0 als niet van toepassing.")

# DGA
elif income_type == "DGA":
    dga_salary = euro_input("DGA salaris (pensioengevend salaris)", "salary_d", 60000)
    st.caption("ℹ️ Gebruik je gebruikelijk loon uit de BV; dividend telt niet mee.")
    factor_a = euro_input("Factor A (pensioenaangroei via BV / UPO)", "factora_d", 2216)
    st.caption("ℹ️ Factor A staat op UPO of vraag accountant. Vul 0 als niets opgebouwd.")

# Combinatie
else:
    st.write("Kies welke inkomens je hebt en vul de bedragen in.")
    c1 = st.checkbox("Inkomen uit loondienst (werknemer)", value=True)
    if c1:
        salary = euro_input("Bruto jaarsalaris (loon uit loondienst)", "salary_c_w", 135200)
    c2 = st.checkbox("Winst uit onderneming (ZZP)", value=False)
    if c2:
        profit = euro_input("Winst uit onderneming (jaar)", "profit_c_z", 0)
        factor_a = euro_input("Factor A (pensioenaangroei ZZP, indien verplicht)", "factora_c_z", 0)
        st.caption("ℹ️ Vul hier de verplicht opgebouwde Factor A in. Vul 0 als niet van toepassing.")
    c3 = st.checkbox("DGA salaris (BV)", value=False)
    if c3:
        dga_salary = euro_input("DGA salaris (pensioengevend salaris)", "salary_c_d", 60000)
    if c1 or c3:
        factor_a = euro_input("Factor A (totale pensioenaangroei uit UPO's)", "factora_c", 2216)

# -------------------------
# Bereken jaarruimte (button direct onder laatste vraag)
# -------------------------
if st.button("Bereken jaarruimte"):
    total_income = float(salary or 0) + float(profit or 0) + float(dga_salary or 0)
    if total_income <= 0:
        st.error("Vul minimaal één inkomen in.")
    else:
        capped_income = min(total_income, MAX_GRONDSLAG)
        premiegrondslag = max(0.0, capped_income - FRANCHISE)

        part_percentage = PERCENTAGE * premiegrondslag
        part_factorA = FACTOR_A_MULTIPLIER * float(factor_a or 0)
        jaarruimte_raw = part_percentage - part_factorA - K_BEDRAG
        jaarruimte = max(0.0, jaarruimte_raw)

        st.success(f"📊 Je geschatte jaarruimte voor dit jaar: **€ {jaarruimte:,.0f}**")

        with st.expander("Toon berekeningsstappen"):
            st.write(f"- Totaal inkomen (gecap op max grondslag): € {capped_income:,.2f}")
            st.write(f"- AOW-franchise: € {FRANCHISE:,.2f}")
            st.write(f"- Premiegrondslag: € {premiegrondslag:,.2f}")
            st.write(f"- 30% van premiegrondslag: € {part_percentage:,.2f}")
            st.write(f"- Aftrek Factor A (6,27 × {factor_a}): € {part_factorA:,.2f}")
            st.write(f"- K-bedrag: € {K_BEDRAG:,.2f}")
            st.write(f"- Jaarruimte = 30% × grondslag − 6,27 × Factor A − K = **€ {jaarruimte:,.0f}**")

        st.markdown("""
        ⚠️ **Belangrijk:**  
        - Deze calculator berekent **alleen de jaarruimte van het huidige jaar**.  
        - **Reserveringsruimte** (mogelijkheden om in te halen uit eerdere jaren) wordt **niet** berekend.  
        - Controleer altijd je **UPO** voor exacte Factor A en je jaaropgave voor verzamelinkomen.  
        - Parameters zoals franchise, K-bedrag en maximale grondslag kunnen jaarlijks veranderen; update indien nodig.
        """)

st.caption("Hulp nodig? Zie uitlegvideo's of raadpleeg een belastingadviseur voor maatwerk.")
