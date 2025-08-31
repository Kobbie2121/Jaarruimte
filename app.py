import streamlit as st

# -------------------------
# Parameters (controleer jaarlijks)
# -------------------------
AOW_FRANCHISE = 16322        # AOW-franchise 2025 (voorbeeld — update jaarlijks)
MAX_GRONDSLAG = 137800       # maximale pensioengrondslag 2025
PERCENTAGE = 0.133           # 13,3% (jaarruimte-percentage)
FACTOR_A_MULTIPLIER = 6.27   # factor A vermenigvuldiger
K_BEDRAG = 1388              # vast bedrag K (controleer elk jaar)

# PAGE
st.set_page_config(page_title="Jaarruimte Calculator", layout="centered")
st.title("🔎 Jaarruimte Calculator — huidig jaar")
st.write("We berekenen alleen **jaarruimte voor het huidige jaar**. Geen reserveringsruimte of terugrekeningen naar voorgaande jaren.")

# -------------------------
# Vraag: hoe verdien je je geld?
# -------------------------
st.header("Stap 1 — Hoe verdien je je geld?")
st.write("Kies wat het beste bij jou past. Heb je meerdere inkomstenbronnen? Kies dan 'Combinatie'.")

income_type = st.radio(
    label="Hoe verdien je je geld?",
    options=("Werknemer", "ZZP'er", "DGA", "Combinatie")
)

# -------------------------
# Inputs per type (met dummy-uitleg)
# -------------------------
st.header("Stap 2 — Vul je cijfers in (gebruik jaaropgave / UPO / aangifte)")

# containers for inputs
salary = 0.0
profit = 0.0
dga_salary = 0.0
factor_a = 0.0

def euro_input(label, key, default=0):
    return st.number_input(label, min_value=0.0, value=float(default), step=100.0, format="%.2f")

if income_type == "Werknemer":
    salary = euro_input("Bruto jaarsalaris (loon uit loondienst)", "salary_w",
                        default=60000)
    st.caption("ℹ️ Gebruik het bedrag 'loon voor de loonheffing' van je jaaropgave of het verzamelinkomen Box 1 uit je aangifte.")
    factor_a = euro_input("Factor A (pensioenaangroei, uit UPO)", "factora_w", default=0)
    st.caption("ℹ️ Factor A staat op je UPO. Vul 0 in als je geen werkgeverspensioen hebt.")

elif income_type == "ZZP'er":
    profit = euro_input("Winst uit onderneming (jaar)", "profit_z", default=60000)
    st.caption("ℹ️ Gebruik je winst zoals in je belastingaangifte (na zakelijke aftrekposten). ZZP'ers hebben meestal Factor A = 0.")

elif income_type == "DGA":
    dga_salary = euro_input("DGA salaris (pensioengevend salaris)", "salary_d", default=60000)
    st.caption("ℹ️ Gebruik het salaris dat je jezelf uitkeert (gebruikelijk loon). Dividend telt niet mee voor deze berekening.")
    factor_a = euro_input("Factor A (pensioenaangroei via BV / UPO)", "factora_d", default=0)
    st.caption("ℹ️ Factor A staat op het UPO van je BV (of vraag je accountant).")

else:  # Combinatie
    st.write("Kies welke inkomens je hebt (vink aan) en vul de bedragen in.")
    c1 = st.checkbox("Inkomen uit loondienst (werknemer)", value=True)
    if c1:
        salary = euro_input("Bruto jaarsalaris (loon uit loondienst)", "salary_c_w", default=60000)
        st.caption("ℹ️ Jaaropgave: 'loon voor de loonheffing'.")
    c2 = st.checkbox("Winst uit onderneming (ZZP)", value=False)
    if c2:
        profit = euro_input("Winst uit onderneming (jaar)", "profit_c_z", default=0)
        st.caption("ℹ️ Gebruik winst na kosten, zoals in aangifte.")
    c3 = st.checkbox("DGA salaris (BV)", value=False)
    if c3:
        dga_salary = euro_input("DGA salaris (pensioengevend salaris)", "salary_c_d", default=0)
        st.caption("ℹ️ Gebruik je officiële DGA-salaris; dividend telt niet mee.")
    # Factor A: alleen relevant als er werkgever/BV pensioen is
    if c1 or c3:
        factor_a = euro_input("Factor A (totale pensioenaangroei uit UPO's)", "factora_c", default=0)
        st.caption("ℹ️ Als je pensioen via werkgever(s) of BV opgebouwd wordt, tel de Factor A's op en vul hier het totaal in. Vul 0 als niets.")

# -------------------------
# Bereken en toon duidelijke waarschuwing
# -------------------------
st.markdown("---")
st.header("Stap 3 — Bereken je jaarruimte (huidig jaar)")

if st.button("Bereken jaarruimte"):
    # valideer inputs
    total_income = float(salary or 0) + float(profit or 0) + float(dga_salary or 0)
    if total_income <= 0:
        st.error("Vul minimaal één inkomen in (loon, winst of DGA-salaris).")
    else:
        # premiegrondslag: eerst cap op max grondslag, dan franchise aftrekken
        capped_income = min(total_income, MAX_GRONDSLAG)
        premiegrondslag = max(0.0, capped_income - AOW_FRANCHISE)

        # onderdelen berekenen
        part_percentage = PERCENTAGE * premiegrondslag
        part_factorA = FACTOR_A_MULTIPLIER * float(factor_a or 0)
        jaarruimte_raw = part_percentage - part_factorA - K_BEDRAG
        jaarruimte = max(0.0, jaarruimte_raw)

        # Toon resultaat + breakdown
        st.success(f"📊 Je geschatte jaarruimte voor dit jaar: **€ {jaarruimte:,.2f}**")

        with st.expander("Toon berekeningsstappen (uitgelegd)"):
            st.write(f"- Totaal opgegeven inkomen (gecap): € {capped_income:,.2f}  (max {MAX_GRONDSLAG:,})")
            st.write(f"- AOW-franchise: € {AOW_FRANCHISE:,.2f}")
            st.write(f"- Premiegrondslag (inkomen - franchise): € {premiegrondslag:,.2f}")
            st.write(f"- 13,3% van premiegrondslag: € {part_percentage:,.2f}")
            st.write(f"- Aftrek voor Factor A (6,27 × Factor A): € {part_factorA:,.2f}")
            st.write(f"- Vaste correctie (K): € {K_BEDRAG:,.2f}")
            st.write(f"- Jaarruimte = 13,3% × grondslag − 6,27 × Factor A − K = **€ {jaarruimte:,.2f}**")

        st.markdown(
            """
            ⚠️ **Belangrijk:**  
            - Deze calculator berekent **alleen** de jaarruimte voor het **huidige jaar**.  
            - **Reserveringsruimte** (mogelijkheden om in te halen uit eerdere jaren) is complex en is **niet** automatisch in deze tool verwerkt.  
            - Controleer altijd je **UPO** voor de exacte Factor A en je jaaropgave/belastingaangifte voor verzamelinkomen.  
            - Parameters zoals franchise, K-bedrag en maximale grondslag kunnen jaarlijks veranderen — controleer en update deze in de tool indien nodig.
            """
        )

# Footer korte hulp
st.markdown("---")
st.caption("Hulp nodig? Gebruik de link in de bio/website voor extra uitlegvideos. Deze calculator is informatief; raadpleeg een belastingadviseur voor maatwerk.")
