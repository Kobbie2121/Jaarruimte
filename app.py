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
# Stap 1: hoe verdien je geld?
# -------------------------
st.header("Stap 1 — Hoe verdien je je geld?")
st.write("Kies wat het beste bij jou past. Heb je meerdere inkomstenbronnen? Kies dan 'Combinatie'.")
income_type = st.radio(
    "Hoe verdien je je geld?",
    ("Werknemer", "ZZP'er", "DGA", "Combinatie")
)

# -------------------------
# Stap 2: invoer per type
# -------------------------
st.header("Stap 2 — Vul je cijfers in (gebruik jaaropgave / UPO / aangifte)")

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

# ZZP
elif income_type == "ZZP'er":
    profit = euro_input("Winst uit onderneming (jaar)", "profit_z", 60000)
    st.caption("ℹ️ Gebruik winst zoals in belastingaangifte. ZZP'er heeft meestal Factor A = 0.")

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
    c3 = st.checkbox("DGA salaris (BV)", value=False)
    if c3:
        dga_salary = euro_input("DGA salaris (pensioengevend salaris)", "salary_c_d", 60000)
    if c1 or c3:
        factor_a = euro_input("Factor A (totale pensioenaangroei uit UPO's)", "factora_c", 2216)

# -------------------------
# Stap 3: Bereken jaarruimte
# -------------------------
st.markdown("---")
st.header("Stap 3 — Bereken jaarruimte (huidig jaar)")

if st.button("Bereken jaarruimte"):
    total_income = float(salary or 0) + float(profit or 0) + float(dga_salary or 0)
    if total_income <= 0:
        st.error("Vul minimaal één inkomen in.")
    else:
        # premiegrondslag
        capped_income = min(total_income, MAX_GRONDSLAG)
        premiegrondslag = max(0.0, capped_income - FRANCHISE)

        # berekening
        part_percentage = PERCENTAGE * premiegrondslag
        part_factorA = FACTOR_A_MULTIPLIER * float(factor_a or 0)
        jaarruimte_raw = part_percentage - part_factorA - K_BEDRAG
        jaarruimte = max(0.0, jaarruimte_raw)

        # resultaat tonen
        st.success(f"📊 Je geschatte jaarruimte voor dit jaar: **€ {jaarruimte:,.0f}**")

        # breakdown
        with st.expander("Toon berekeningsstappen"):
            st.write(f"- Totaal inkomen (gecap op max grondslag): € {capped_income:,.2f}")
            st.write(f"- AOW-franchise: € {FRANCHISE:,.2f}")
            st.write(f"- Premiegrondslag: € {premiegrondslag:,.2f}")
            st.write(f"- 30% van premiegrondslag: € {part_percentage:,.2f}")
            st.write(f"- Aftrek Factor A (6,27 × {factor_a}): € {part_factorA:,.2f}")
            st.write(f"- K-bedrag: € {K_BEDRAG:,.2f}")
            st.write(f"- Jaarruimte = 30% × grondslag − 6,27 × Factor A − K = **€ {jaarruimte:,.0f}**")

        # disclaimer
        st.markdown("""
        ⚠️ **Belangrijk:**  
        - Deze calculator berekent **alleen de jaarruimte van het huidige jaar**.  
        - **Reserveringsruimte** (mogelijkheden om in te halen uit eerdere jaren) is complex en wordt **niet** berekend.  
        - Controleer altijd je **UPO** voor de exacte Factor A en je jaaropgave voor verzamelinkomen.  
        - Parameters zoals franchise, K-bedrag en maximale grondslag veranderen jaarlijks; update indien nodig.
        """)

st.markdown("---")
st.caption("Hulp nodig? Zie uitlegvideo's of raadpleeg een belastingadviseur voor maatwerk.")
