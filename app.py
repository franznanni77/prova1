import streamlit as st
import pulp
from collections import defaultdict

def main():
    st.title("Ottimizzatore di Campagne Marketing")
    st.write("""
    Questa applicazione utilizza la Programmazione Lineare (PuLP) per 
    distribuire i lead tra diverse campagne al fine di massimizzare il profitto.
    """)

    # 1. INPUT UTENTE
    # ---------------------------------------------------------------------------------
    st.subheader("Impostazioni iniziali")

    # Numero di campagne
    n = st.number_input(
        "Numero di campagne (minimo 2, massimo 10):",
        min_value=2, max_value=10, value=2, step=1
    )

    st.write("Inserisci i dati per ciascuna campagna:")

    campaigns = []
    for i in range(n):
        st.markdown(f"**Campagna #{i+1}**")
        name = st.text_input(f"Nome campagna #{i+1}", key=f"name_{i}")

        category = st.selectbox(
            f"Categoria campagna #{i+1}",
            options=["laser", "corpo"],
            key=f"cat_{i}"
        )

        cost = st.number_input(
            f"Costo per lead (campagna #{i+1}):", 
            min_value=0.0, value=0.0, step=1.0, 
            format="%.2f",
            key=f"cost_{i}"
        )
        revenue = st.number_input(
            f"Ricavo per lead (campagna #{i+1}):", 
            min_value=0.0, value=0.0, step=1.0,
            format="%.2f",
            key=f"revenue_{i}"
        )

        net_profit = revenue - cost

        campaigns.append({
            "name": name if name else f"Campagna_{i+1}",
            "category": category,
            "cost": cost,
            "revenue": revenue,
            "net_profit": net_profit
        })

    total_leads = st.number_input(
        "Totale dei lead da produrre:", 
        min_value=1.0, value=10000.0, step=100.0
    )

    corpo_percent = st.slider(
        "Percentuale minima di lead 'corpo' (0% = 0.0, 100% = 1.0):",
        min_value=0.0, max_value=1.0, value=0.33, step=0.01
    )

    st.markdown("---")
    st.write("""
    *Vincolo aggiuntivo*: in ogni categoria con almeno 2 campagne, 
    la **campagna meno profittevole** deve ricevere **almeno il 20%** 
    dei lead di quella categoria.
    """)

    # Pulsante per eseguire l'ottimizzazione
    if st.button("Esegui Ottimizzazione"):

        # 2. DEFINIZIONE DEL PROBLEMA DI LP
        # ---------------------------------------------------------------------------------
        prob = pulp.LpProblem("MarketingCampaignOptimization", pulp.LpMaximize)

        # Variabili di decisione: x_i >= 0
        x = {}
        for i, camp in enumerate(campaigns):
            x[i] = pulp.LpVariable(f"x_{i}", lowBound=0, cat="Continuous")

        # 3. FUNZIONE OBIETTIVO
        # ---------------------------------------------------------------------------------
        # massimizzare SUM( (ricavo - costo) * x_i )
        profit_expr = [
            camp["net_profit"] * x[i]
            for i, camp in enumerate(campaigns)
        ]
        prob += pulp.lpSum(profit_expr), "Total_Profit"

        # 4. VINCOLI
        # ---------------------------------------------------------------------------------
        
        # (a) Somma dei lead = total_leads
        prob += pulp.lpSum([x[i] for i in x]) == total_leads, "Totale_lead"

        # (b) Somma dei lea
