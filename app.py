import streamlit as st

st.title("Jaarruimte Calculator")

st.markdown("""
Bereken hier eenvoudig je jaarruimte voor het huidige jaar.  
Dit geeft aan hoeveel je extra mag inleggen in een pensioenproduct met belastingvoordeel.
""")

# Vraag: hoe verdien je je geld?
income_type = st.radio(
    "Hoe verdien je je geld?",
    ("Werknemer", "ZZP'er", "DGA", "Combinatie")
)

# Invoer
if income_type in ["Werknemer", "Combinatie"]:
    salary = st.number_input("Wat is je bruto salaris per jaar?", min_value=0, step=1000)

if income_type in ["ZZP'er", "Combinatie"]:
    profit = st.number_input("Wat is je winst uit onderneming per jaar?", min_value=0, step=1000)

if income_type in ["DGA", "Combinatie"]:
    dga_salary = st.number_input("Wat is je DGA-salaris per jaar?", min_value=0, step=1000)
    dga_factor_a = st.number_input("Wat is je factor A (pensioenaangroei)?", min_value=0, step=100)

# Simpele placeholder berekening (voorbeeld)
if st.button("Bereken jaarruimte"):
    jaarruimte = 0
    
    if income_type == "Werknemer":
        jaarruimte = max(0, salary * 0.13 - 5000)
    elif income_type == "ZZP'er":
        jaarruimte = max(0, profit * 0.13 - 5000)
    elif income_type == "DGA":
        jaarruimte = max(0, dga_salary * 0.13 - dga_factor_a)
    elif income_type == "Combinatie":
        jaarruimte = max(0, (salary + profit + dga_salary) * 0.13 - dga_factor_a)

    st.success(f"📊 Je jaarruimte voor dit jaar is: **€{jaarruimte:,.0f}**")

    st.markdown("""
    ⚠️ *Let op: dit is de jaarruimte voor het huidige jaar.*  
    Mogelijk heb je ook nog **reserveringsruimte** (inlegmogelijkheden van de afgelopen 10 jaar).  
    Dit kan extra belastingvoordeel opleveren of helpen om een pensioengat te dichten.
    """)

