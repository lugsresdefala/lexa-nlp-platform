import streamlit as st
from config import PLANS

def render_plan_upgrade() -> None:
    """Render a simplified plan upgrade form in development mode."""
    user = st.session_state.get("user")
    if not user:
        return

    with st.sidebar.expander("Upgrade de assinatura"):
        selected = st.selectbox(
            "Escolha o novo plano",
            list(PLANS.keys()),
            index=list(PLANS.keys()).index(user.get('plan', 'free')),
            format_func=lambda p: {
                'free': 'Gratuito (10.000 caracteres/mês)',
                'pro': 'Premium (100.000 caracteres/mês)',
                'enterprise': 'Enterprise (1.000.000 caracteres/mês)',
            }.get(p, p.capitalize())
        )
        
        if st.button("Atualizar plano"):
            st.session_state.user['plan'] = selected
            st.session_state.user['char_limit'] = PLANS[selected]
            st.success("Plano atualizado com sucesso!")
            st.rerun()
