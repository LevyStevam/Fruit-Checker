import streamlit as st

BACKEND_URL = "http://localhost:8000"
login_url = f"{BACKEND_URL}/login/google"

# Título

# Formulário centralizado
with st.form(key="login_form"):
    col1, col2, col3 = st.columns([1, 2.5, 1])
    with col2:
        st.title("Login com Google")
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            submitted = st.form_submit_button("Google Login", type="primary", help="Click to login")
            if submitted:
                st.markdown(f'<meta http-equiv="refresh" content="0;URL={login_url}">', unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state.user = None

params = st.experimental_get_query_params()
if "email" in params and "name" in params:
    st.session_state.user = {
        "email": params["email"][0],
        "name": params["name"][0]
    }

if st.session_state.user:
    st.success(f"Bem-vindo, {st.session_state.user['name']}!")
    st.info(f"E-mail: {st.session_state.user['email']}")

