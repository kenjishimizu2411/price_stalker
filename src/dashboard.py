import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re

from database import (
    get_db_connection, 
    create_user, 
    get_user_by_email, 
    add_product, 
    get_products_by_user,
    delete_product,       
    update_product_full,
    get_user_info,
    update_user_profile
)
from auth import hash_password, check_password

st.set_page_config(page_title="PriceStalker SaaS", page_icon="🕵️", layout="wide")

BANNER_HTML = """
<div style="background-color: #0a2742; color: white; padding: 25px; border-radius: 12px; border-left: 6px solid #1a4c8f; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
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
<div style="background-color: #FFD54F; color: black; padding: 15px; border-radius: 10px; border-left: 5px solid #382c04; font-size: 14px; line-height: 1.5;">
    <b>Requisito:</b><br>
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
    text-align: center;
    padding-right: 20px;
    padding-bottom: 10px;
    font-size: 10px;
    font-weight: bold;
    pointer-events: none; 
}
</style>
<div class="footer">Developed with 💙 by Kenji Shimizu</div>
"""

def sanitize_phone(phone_input):
    only_nums = re.sub(r'\D', '', phone_input)
    if len(only_nums) >= 10 and len(only_nums) <= 11:
        only_nums = "55" + only_nums
    return only_nums

def validate_email(email):
    """Verifica se o texto tem formato de e-mail (algo@algo.algo)"""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def clean_url_visual(url):
    """Encurta a URL apenas para exibição visual"""
    try:
        if "?" in url: url = url.split("?")[0]
        
        if "amazon" in url and "/dp/" in url:
            asin = url.split("/dp/")[1].split("/")[0]
            return f"amazon.com.br/dp/{asin}..."
            
        if "mercadolivre" in url:
            parts = url.split(".com.br/")
            if len(parts) > 1:
                return f"mercadolivre.com.br/{parts[1][:30]}..."
                
        if len(url) > 50:
            return url[:47] + "..."
            
        return url
    except:
        return "Link do Produto"

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

if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = None

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
        st.caption("Utilize um e-mail válido para recuperação de conta.") 
        
        st.write("WhatsApp para Notificações")
        col_ddd, col_num = st.columns([1, 4])
        with col_ddd:
            st.text_input("DDD", value="+55", disabled=True, label_visibility="collapsed")
        with col_num:
            phone_raw = st.text_input("Número", placeholder="(21) 99999-8888", label_visibility="collapsed")
        st.caption("Apenas números com DDD. Ex: (11) 99999-8888")

        st.markdown("---")
        st.markdown("##### 🔑 Chave de Acesso (Obrigatório)")
        
        st.info(
            """
            1. Adicione **+34 644 87 21 57** (CallMeBot) nos contatos.
            2. Mande a mensagem: `I allow callmebot to send me messages`
            3. Cole o código numérico recebido abaixo.
            """
        )
        
        user_api_key = st.text_input("Sua API Key CallMeBot", placeholder="Ex: 8692414")
        if user_api_key and not user_api_key.isdigit():
            st.caption("⚠️ :red[A chave deve conter apenas números!]")
        else:
            st.caption("O código que o bot te enviou no WhatsApp (apenas números).")

        st.markdown("---")
        new_pass = st.text_input("Escolha uma Senha", type="password")
        st.caption("Use uma senha segura.")
        
        if st.button("Cadastrar"):
            clean_phone = sanitize_phone(phone_raw)
            
            if not new_name or not new_email or not new_pass or not user_api_key:
                st.warning("Por favor, preencha todos os campos.")
            elif not validate_email(new_email):
                st.error("Formato de e-mail inválido.")
            elif len(clean_phone) < 12:
                 st.error("Número de telefone inválido.")
            elif not user_api_key.isdigit():
                st.error("A API Key deve conter apenas números.")
            else:
                hashed = hash_password(new_pass)
                uid = create_user(new_name, new_email, hashed, clean_phone, user_api_key)
                if uid:
                    st.session_state['user_id'] = uid
                    st.session_state['user_name'] = new_name
                    st.success("Conta criada com sucesso! Entrando...")
                    st.rerun()
                else:
                    st.error("Erro ao criar conta. E-mail já existe?")

else:
    with st.sidebar:
        user_data = get_user_info(st.session_state['user_id'])
        if user_data:
            u_name, u_email, u_phone, u_key, u_daily_only = user_data
            
            if 'editing_profile' not in st.session_state:
                st.session_state['editing_profile'] = False

            if not st.session_state['editing_profile']:
                st.markdown(f"### 👋 Olá, {u_name.split()[0]}!")
                st.markdown(
                    f"""
<div style="background-color: #1e2530; padding: 15px; border-radius: 10px; border: 1px solid #333; margin-bottom: 10px;">
    <p style="margin:0; color: #888; font-size: 12px;">👤 Nome Completo</p>
    <p style="margin:0; font-weight: bold; margin-bottom: 8px;">{u_name}</p>
    <p style="margin:0; color: #888; font-size: 12px;">📧 E-mail</p>
    <p style="margin:0; font-weight: bold; margin-bottom: 8px;">{u_email}</p>
    <p style="margin:0; color: #888; font-size: 12px;">📱 WhatsApp</p>
    <p style="margin:0; font-weight: bold;">{u_phone}</p>
</div>
""", 
                    unsafe_allow_html=True
                )
                if st.button("✏️ Editar Perfil"):
                    st.session_state['editing_profile'] = True
                    st.rerun()
            else:
                st.markdown("### ✏️ Editando Perfil")
                with st.form("edit_profile_form"):
                    new_u_name = st.text_input("Nome", value=u_name)
                    new_u_email = st.text_input("E-mail", value=u_email)
                    new_u_phone = st.text_input("WhatsApp (55...)", value=u_phone)
                    new_u_key = st.text_input("API Key CallMeBot", value=u_key if u_key else "")
                    
                    st.markdown("---")
                    new_daily_only = st.checkbox("🚫 Evitar Spam: Notificar apenas uma vez por dia por produto", value=u_daily_only)

                    if st.form_submit_button("💾 Salvar"):
                        clean_phone = sanitize_phone(new_u_phone)
                        if update_user_profile(st.session_state['user_id'], new_u_name, new_u_email, clean_phone, new_u_key, new_daily_only):
                            st.success("Perfil atualizado!")
                            st.session_state['user_name'] = new_u_name
                            st.session_state['editing_profile'] = False
                            st.rerun()
                        else:
                            st.error("Erro ao atualizar.")
                
                if st.button("Cancelar Edição"):
                    st.session_state['editing_profile'] = False
                    st.rerun()

        st.markdown("---")
        if st.button("Sair"):
            st.session_state['user_id'] = None
            st.rerun()
        st.markdown(SIDEBAR_HTML, unsafe_allow_html=True)
    
    st.title("🕵️ Painel de Controle")
    st.markdown(BANNER_HTML, unsafe_allow_html=True)

    with st.expander("➕ Adicionar Novo Monitoramento", expanded=False):
        with st.form("add_prod", clear_on_submit=True):
            col1, col2 = st.columns(2)
            name = col1.text_input("Nome do Produto")
            url = col2.text_input("URL do Produto")
            col3, col4 = st.columns(2)
            target = col3.number_input("Preço Alvo (R$)", min_value=0.0)
            format_func = lambda x: f"{x} horas (Recomendado) ⭐" if x == 12 else f"{x} horas"
            interval = col4.selectbox("Checar a cada:", [12, 24, 6, 1], format_func=format_func)
            
            if st.form_submit_button("Salvar Monitoramento"):
                if name and url and target > 0:
                    add_product(st.session_state['user_id'], name, url, target, interval)
                    st.success("Produto adicionado!")
                    st.rerun()
                else:
                    st.warning("Preencha os dados corretamente.")

    st.markdown("---")
    st.subheader("📋 Meus Produtos Monitorados")

    user_products = get_products_by_user(st.session_state['user_id'])
    
    if user_products:
        product_map = {prod[1]: prod for prod in user_products}
        
        selected_product_name = st.selectbox(
            "Selecione o produto para gerenciar:", 
            list(product_map.keys()),
            index=None,
            placeholder="Escolha um produto na lista..."
        )
        
        if selected_product_name:
            prod = product_map[selected_product_name]
            p_id, p_name, p_url, p_target, p_interval = prod
            
            with st.container(border=True):
                
                c_title, c_del = st.columns([12, 1])
                with c_title:
                    st.markdown(f"### 📦 {p_name}")
                with c_del:
                    if st.button("🗑️", key=f"del_{p_id}", type="primary", help="Excluir este produto"):
                        if delete_product(p_id):
                            st.rerun()

                short_link = clean_url_visual(p_url)
                st.markdown(f"🔗 **Link:** [{short_link}]({p_url})")
                
                st.write("")

                c_spacer, c_img, c_dados = st.columns([0.2, 2, 5]) 
                
                with c_img:
                    st.image("https://cdn-icons-png.flaticon.com/512/679/679720.png", width=130, caption="Produto")

                with c_dados:
                    st.markdown("#### ✏️ Editar Detalhes")
                    ed_name = st.text_input("Nome do Produto", value=p_name, key=f"name_{p_id}")
                    ed_url = st.text_input("URL do Produto", value=p_url, key=f"url_{p_id}")
                    
                    c_meta, c_save = st.columns([3, 1.5])
                    with c_meta:
                        ed_target = st.number_input("Meta de Preço (R$)", value=float(p_target), step=10.0, key=f"tgt_{p_id}")
                    with c_save:
                        st.markdown("<div style='height: 29px'></div>", unsafe_allow_html=True)
                        if st.button("💾 Salvar", key=f"save_{p_id}", use_container_width=True):
                            if update_product_full(p_id, ed_name, ed_url, ed_target):
                                st.success("Salvo!")
                                st.rerun()
                            else:
                                st.error("Erro.")

                st.markdown("---")
                st.markdown("#### 📊 Histórico de Variação")
                
                df_hist = get_price_history_df(p_id)
                
                if not df_hist.empty:
                    media = df_hist['price'].mean()
                    minimo = df_hist['price'].min()
                    maximo = df_hist['price'].max()
                    
                    kpi1, kpi2, kpi3 = st.columns(3)
                    kpi1.metric("🏷️ Preço Médio", f"R$ {media:.2f}")
                    kpi2.metric("📉 Mínimo Histórico", f"R$ {minimo:.2f}")
                    kpi3.metric("📈 Máximo Histórico", f"R$ {maximo:.2f}")
                    
                    st.write("") 

                    df_hist['scraped_at'] = pd.to_datetime(df_hist['scraped_at'])
                    df_hist['date_obj'] = df_hist['scraped_at'].dt.date
                    df_daily = df_hist.groupby('date_obj')['price'].mean().reset_index()
                    df_daily = df_daily.sort_values('date_obj')
                    df_daily['dia_str'] = pd.to_datetime(df_daily['date_obj']).dt.strftime('%d/%m')
                    
                    max_y_val = max(df_daily['price'].max(), float(p_target)) * 1.2
                    
                    fig = go.Figure()

                    fig.add_shape(type="rect", xref="paper", yref="y", x0=0, y0=0, x1=1, y1=p_target,
                        fillcolor="rgba(114, 252, 195, 0.0)", layer="below", line_width=0)
                    
                    fig.add_shape(type="rect", xref="paper", yref="y", x0=0, y0=p_target, x1=1, y1=max_y_val,
                        fillcolor="rgba(252, 146, 114, 0.0)", layer="below", line_width=0)

                    for index, row in df_daily.iterrows():
                        fig.add_shape(type="line", x0=row['dia_str'], y0=p_target, x1=row['dia_str'], y1=row['price'],
                            line=dict(color="rgba(202, 202, 250, 0.3)", width=0, dash="dot"), layer="below")

                    cores_barras = ['#00C853' if x <= float(p_target) else '#D32F2F' for x in df_daily['price']]
                    
                    fig.add_trace(go.Bar(
                        x=df_daily['dia_str'], y=df_daily['price'],
                        name='Preço', marker_color=cores_barras, width=0.8,
                        text=df_daily['price'].apply(lambda x: f"{x:.2f}"), textposition='outside'
                    ))

                    fig.add_hline(y=p_target, line_dash="dash", line_color="#FFFFFF", line_width=0.6,
                        annotation_text=f"<b>META: R$ {p_target}</b>", annotation_position="bottom right", annotation_font_color="#FFFFFF")

                    fig.update_layout(yaxis_range=[0, max_y_val], yaxis_title="Preço (R$)", xaxis_title=None,
                        plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=30, b=30, l=30, r=30), showlegend=False, hovermode="x unified")
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Aguardando a primeira leitura do robô para gerar gráfico... 🤖")
    
    else:
        st.info("Você ainda não monitora nenhum produto. Adicione um acima! ☝️")

    st.markdown(FOOTER_STYLE, unsafe_allow_html=True)