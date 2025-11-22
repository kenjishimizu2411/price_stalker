import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go # <--- IMPORTANTE: Nova biblioteca para gráficos avançados
import re

# --- IMPORTANTO AS FUNÇÕES DO BANCO ---
from database import (
    get_db_connection, 
    create_user, 
    get_user_by_email, 
    add_product, 
    get_products_by_user,
    delete_product,       
    update_product_full 
)
from auth import hash_password, check_password

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="PriceStalker SaaS", page_icon="🕵️", layout="wide")

# ==================================================
# HTML / CSS PERSONALIZADO
# ==================================================

BANNER_HTML = """
<div style="background-color: #0c2663; color: white; padding: 25px; border-radius: 12px; border-left: 6px solid #1a4c8f; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
    <h3 style="color: white; margin-top: 0; margin-bottom: 15px; font-family: sans-serif;">👋 Bem-vindo ao PriceStalker!</h3>
    <p style="font-size: 16px; margin-bottom: 15px;">
        O nosso objetivo é simples: <b>garantir que você pague o menor preço</b>. Funciona assim:
    </p>
    <div style="background-color: rgba(0, 0, 0, 0.2); padding: 15px; border-radius: 8px; margin-bottom: 15px;">
        1️⃣ Você cadastra o produto e define sua <b>Meta de Preço</b>.<br>
        2️⃣ Nós monitoramos a internet silenciosamente para você.<br>
        3️⃣ <b>Você só é notificado no WhatsApp</b> quando o preço atingir sua meta. Sem spam!
    </div>
    <p style="font-size: 14px; margin-bottom: 0; opacity: 0.9;">
        🚀 <i><b>Em breve:</b> Você poderá buscar apenas pelo nome do produto, sem precisar colar o link. Estamos trabalhando nisso!</i>
    </p>
</div>
"""

SIDEBAR_HTML = """
<div style="background-color: #0068c9; color: white; padding: 15px; border-radius: 10px; border-left: 5px solid #1a4c8f; font-size: 14px; line-height: 1.5;">
    💡 <b>Requisito:</b><br>
    Envie uma mensagem para o <b>CallMeBot (+34 644 87 21 57)</b> e mande o texto: <br>
    <b>'I allow callmebot to send me messages'</b> <br>
    no WhatsApp, para permitir que o PriceStalker funcione corretamente.
</div>
"""

FOOTER_STYLE = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: transparent;
    color: #808080;
    text-align: right;
    padding-right: 20px;
    padding-bottom: 10px;
    font-size: 12px;
    font-weight: bold;
    pointer-events: none; 
}
</style>
<div class="footer">Developed by Kenji Shimizu</div>
"""

# ==================================================
# FUNÇÕES AUXILIARES
# ==================================================

def sanitize_phone(phone_input):
    only_nums = re.sub(r'\D', '', phone_input)
    if len(only_nums) >= 10 and len(only_nums) <= 11:
        only_nums = "55" + only_nums
    return only_nums

def get_price_history_df(product_id):
    conn = get_db_connection()
    if not conn: return pd.DataFrame()
    try:
        query = "SELECT price, scraped_at FROM price_history WHERE product_id = %s ORDER BY scraped_at ASC"
        df = pd.read_sql(query, conn, params=(product_id,))
        return df
    except Exception:
        return pd.DataFrame()
    finally:
        conn.close()

# ==================================================
# LÓGICA PRINCIPAL
# ==================================================

if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = None

# --- TELA DE LOGIN / CADASTRO ---
if st.session_state['user_id'] is None:
    st.title("🕵️ Bem-vindo ao PriceStalker")
    
    tab1, tab2 = st.tabs(["Entrar", "Criar Conta"])
    
    with tab1:
        email_login = st.text_input("E-mail")
        senha_login = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            user = get_user_by_email(email_login)
            if user:
                stored_hash = user[3]
                if check_password(senha_login, stored_hash):
                    st.session_state['user_id'] = user[0]
                    st.session_state['user_name'] = user[1]
                    st.success("Login realizado!")
                    st.rerun()
                else:
                    st.error("Senha incorreta.")
            else:
                st.error("E-mail não encontrado.")

    with tab2:
        st.subheader("Novo Cadastro")
        new_name = st.text_input("Seu Nome")
        new_email = st.text_input("Seu E-mail")
        
        st.write("WhatsApp para Notificações")
        col_ddd, col_num = st.columns([1, 4])
        with col_ddd:
            st.text_input("DDD", value="+55", disabled=True, label_visibility="collapsed")
        with col_num:
            phone_raw = st.text_input("Número", placeholder="(21) 99999-8888", label_visibility="collapsed")
        
        new_pass = st.text_input("Escolha uma Senha", type="password")
        
        if st.button("Cadastrar"):
            clean_phone = sanitize_phone(phone_raw)
            if len(clean_phone) < 12:
                 st.error("Número de telefone inválido.")
            elif new_email and new_pass and new_name:
                hashed = hash_password(new_pass)
                uid = create_user(new_name, new_email, hashed, clean_phone)
                if uid:
                    st.session_state['user_id'] = uid
                    st.session_state['user_name'] = new_name
                    st.success("Conta criada! Entrando...")
                    st.rerun()
                else:
                    st.error("Erro ao criar conta.")
            else:
                st.warning("Preencha todos os campos.")

# --- ÁREA LOGADA ---
else:
    # BARRA LATERAL
    with st.sidebar:
        st.write(f"Olá, **{st.session_state['user_name']}**!")
        if st.button("Sair"):
            st.session_state['user_id'] = None
            st.rerun()
        st.markdown("---")
        st.markdown(SIDEBAR_HTML, unsafe_allow_html=True)
    
    st.title("🕵️ Painel de Controle")

    # BANNER EXPLICATIVO
    st.markdown(BANNER_HTML, unsafe_allow_html=True)

    # FORMULÁRIO
    with st.expander("➕ Adicionar Novo Monitoramento", expanded=False):
        with st.form("add_prod", clear_on_submit=True):
            col1, col2 = st.columns(2)
            name = col1.text_input("Nome do Produto")
            url = col2.text_input("URL do Produto")
            
            col3, col4 = st.columns(2)
            target = col3.number_input("Preço Alvo (R$)", min_value=0.0)
            
            format_func = lambda x: f"{x} hora (Recomendado) ⭐" if x == 1 else f"{x} horas"
            interval = col4.selectbox("Checar a cada:", [1, 6, 12, 24], format_func=format_func)
            
            if st.form_submit_button("Salvar Monitoramento"):
                if name and url and target > 0:
                    add_product(st.session_state['user_id'], name, url, target, interval)
                    st.success("Produto adicionado!")
                    st.rerun()
                else:
                    st.warning("Preencha os dados corretamente.")

    # LISTA E GRÁFICOS
    st.markdown("---")
    st.subheader("📋 Meus Produtos Monitorados")

    user_products = get_products_by_user(st.session_state['user_id'])
    
    if user_products:
        for prod in user_products:
            p_id, p_name, p_url, p_target, p_interval = prod
            
            with st.expander(f"📦 {p_name} (Meta: R$ {p_target})", expanded=False):
                
                c_edit, c_del = st.columns([4, 1])
                
                with c_edit:
                    st.markdown("#### ✏️ Editar Detalhes")
                    ec1, ec2, ec3 = st.columns([3, 3, 2])
                    
                    ed_name = ec1.text_input("Nome", value=p_name, key=f"name_{p_id}")
                    ed_url = ec2.text_input("URL", value=p_url, key=f"url_{p_id}")
                    ed_target = ec3.number_input("Meta (R$)", value=float(p_target), step=10.0, key=f"tgt_{p_id}")
                    
                    save_col1, save_col2 = st.columns([5, 1])
                    with save_col2:
                        st.write("") 
                        st.write("") 
                        if st.button("💾 Salvar", key=f"save_{p_id}"):
                            if update_product_full(p_id, ed_name, ed_url, ed_target):
                                st.success("Atualizado!")
                                st.rerun()
                            else:
                                st.error("Erro.")

                with c_del:
                    st.write("") 
                    st.write("") 
                    if st.button("🗑️", key=f"del_{p_id}", type="primary", help="Excluir"):
                        if delete_product(p_id):
                            st.rerun()

                # --- 4. GRÁFICO AVANÇADO (ZONA VERDE/VERMELHA) ---
                st.markdown("---")
                st.markdown("#### 📊 Análise de Meta vs. Preço")
                
                df_hist = get_price_history_df(p_id)
                
                if not df_hist.empty:
                    # Tratamento de Dados (Média Diária)
                    df_hist['scraped_at'] = pd.to_datetime(df_hist['scraped_at'])
                    df_hist['date_obj'] = df_hist['scraped_at'].dt.date
                    df_daily = df_hist.groupby('date_obj')['price'].mean().reset_index()
                    df_daily = df_daily.sort_values('date_obj')
                    df_daily['dia_str'] = pd.to_datetime(df_daily['date_obj']).dt.strftime('%d/%m')
                    
                    # Definição do Limite Superior do Gráfico
                    # (Pega o maior valor entre o preço máximo e a meta, e dá 20% de margem)
                    max_y_val = max(df_daily['price'].max(), float(p_target)) * 1.2
                    
                    # --- CRIAÇÃO DO GRÁFICO COM GO (Graph Objects) ---
                    fig = go.Figure()

                    # 1. Zonas de Fundo (O Segredo!)
                    # Zona Verde (De 0 até a Meta) -> Bom pra comprar
                    fig.add_shape(
                        type="rect",
                        xref="paper", yref="y",
                        x0=0, y0=0, x1=1, y1=p_target,
                        fillcolor="rgba(114, 252, 195, 0.1)", # Verde transparente
                        layer="below", line_width=0,
                    )
                    
                    # Zona Vermelha (Da Meta até o Infinito) -> Caro
                    fig.add_shape(
                        type="rect",
                        xref="paper", yref="y",
                        x0=0, y0=p_target, x1=1, y1=max_y_val,
                        fillcolor="rgba(252, 146, 114, 0.1)", # Vermelho transparente
                        layer="below", line_width=0,
                    )
                    for index, row in df_daily.iterrows():
                        fig.add_shape(
                            type="line",
                            x0=row['dia_str'], y0=p_target,
                            x1=row['dia_str'], y1=row['price'],
                            line=dict(
                                color="rgba(202, 202, 250, 0.3)", # Azul bem clarinho (transparente)
                                width=2, 
                                dash="dot" # Tracejado para ficar elegante
                            ),
                            layer="below" # Fica atrás da bolinha e da linha principal
                        )
                    # 2. Linha do Preço
                    fig.add_trace(go.Scatter(
                        x=df_daily['dia_str'], 
                        y=df_daily['price'],
                        mode='lines+markers+text',
                        name='Preço',
                        line=dict(color='#cacafa', width=8),
                        marker=dict(size=8, color='#cacafa'),
                        text=df_daily['price'].apply(lambda x: f"{x:.2f}"),
                        textposition="top center"
                    ))

                    # 3. Linha da Meta (Referência Forte)
                    fig.add_hline(
                        y=p_target, 
                        line_dash="solid", 
                        line_color="#cacafa", 
                        line_width=2,
                        annotation_text=f"<b>META: R$ {p_target}</b>", 
                        annotation_position="bottom right",
                        annotation_font_color="#cacafa"
                    )

                    # Ajustes de Layout
                    fig.update_layout(
                        yaxis_range=[0, max_y_val],
                        yaxis_title="Preço (R$)",
                        xaxis_title=None,
                        plot_bgcolor="rgba(0,0,0,0)",
                        margin=dict(t=30, b=30, l=30, r=30),
                        showlegend=False,
                        hovermode="x unified"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Aguardando a primeira leitura do robô... 🤖")

    else:
        st.info("Você ainda não monitora nenhum produto. Adicione um acima! ☝️")

    st.markdown(FOOTER_STYLE, unsafe_allow_html=True)