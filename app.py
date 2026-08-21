import streamlit as st
import pandas as pd
import plotly.express as px
from tokenizer.tokenizer import Tokenizer
from tokenizer.keywords import get_default_keywords
from utils.file_handler import decode_bytes
from utils.exporter import export_to_csv, export_to_txt

# Page configuration
st.set_page_config(
    page_title="Source Code Tokenizer & Lexical Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom space theme styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap');

    /* Full App background */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1610296669228-602fa827fc1f?auto=format&fit=crop&w=2560&q=80");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* Transparent container backdrop */
    [data-testid="stHeader"] {
        background: rgba(0, 0, 0, 0) !important;
    }
    
    /* Sidebar glassmorphic background */
    [data-testid="stSidebar"] {
        background: rgba(10, 12, 22, 0.85) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(164, 133, 255, 0.2);
    }
    
    /* Sidebar headers, text, labels */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #e0d5ff !important;
        font-weight: 600;
    }
    
    /* Main title custom gradient styling */
    .main-title {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 72px !important;
        font-weight: 900 !important;
        color: #ff007f !important;
        text-shadow: 0 0 10px #00f5d4, 0 0 20px #00f5d4, 0 0 40px #7928ca, 0 0 60px #7928ca !important;
        text-align: center;
        padding: 20px 0;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        -webkit-text-fill-color: #ff007f !important;
    }
    
    @keyframes gradient-flow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Subheaders headers styling */
    h2, h3, h4, h5, h6, label, p, span {
        color: #f0f0f8 !important;
    }

    /* Glassmorphic Metric Cards */
    .metric-card {
        background: rgba(18, 18, 35, 0.7) !important;
        backdrop-filter: blur(12px) saturate(180%);
        border: 1px solid rgba(164, 133, 255, 0.15) !important;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(164, 133, 255, 0.45) !important;
        box-shadow: 0 10px 30px rgba(164, 133, 255, 0.25);
    }
    .metric-title {
        color: #a485ff !important;
        font-size: 13px;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .metric-value {
        color: #ffffff;
        font-size: 32px;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(164, 133, 255, 0.5);
    }
    
    /* Input fields (TextArea, input, selectbox dropdown) */
    .stTextArea textarea, .stTextInput input, .stSelectbox [role="combobox"] {
        background: rgba(10, 10, 20, 0.75) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(164, 133, 255, 0.35) !important;
        color: #e0d5ff !important;
        border-radius: 8px !important;
        transition: border-color 0.3s ease;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #00f5d4 !important;
        box-shadow: 0 0 10px rgba(0, 245, 212, 0.2) !important;
    }

    /* Actions Streamlit Button CSS overrides */
    div.stButton > button {
        background: linear-gradient(135deg, #7928CA 0%, #FF0080 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(255, 0, 128, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        box-shadow: 0 4px 25px rgba(255, 0, 128, 0.7) !important;
        transform: scale(1.02);
    }
    
    /* Glassmorphic download buttons */
    div.stDownloadButton > button {
        background: rgba(20, 20, 40, 0.8) !important;
        backdrop-filter: blur(8px);
        color: #e0d5ff !important;
        border: 1px solid rgba(164, 133, 255, 0.4) !important;
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }
    div.stDownloadButton > button:hover {
        background: rgba(164, 133, 255, 0.2) !important;
        border-color: #00f5d4 !important;
        box-shadow: 0 0 15px rgba(0, 245, 212, 0.3) !important;
    }

    /* Error card container styles */
    .error-card {
        background: rgba(90, 30, 40, 0.45) !important;
        backdrop-filter: blur(8px);
        border-left: 5px solid #ff4b4b !important;
        border-top: 1px solid rgba(255,75,75,0.2) !important;
        border-right: 1px solid rgba(255,75,75,0.2) !important;
        border-bottom: 1px solid rgba(255,75,75,0.2) !important;
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 8px;
        color: #ffcccc !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE INIT -----------------
if 'code_input' not in st.session_state:
    st.session_state['code_input'] = ""
if 'file_uploader_key' not in st.session_state:
    st.session_state['file_uploader_key'] = 0
if 'tokenize_triggered' not in st.session_state:
    st.session_state['tokenize_triggered'] = False

# ----------------- SIDEBAR -----------------
st.sidebar.title("🛠️ Lexer Settings")

# Language selection
language = st.sidebar.selectbox(
    "Source Language",
    ["C / C++", "Java", "Python"],
    help="Select the target programming language rules to load."
)

# Manage Dynamic Keywords
if 'prev_lang' not in st.session_state or st.session_state['prev_lang'] != language:
    st.session_state['prev_lang'] = language
    default_kws = sorted(list(get_default_keywords(language)))
    st.session_state['keywords_text'] = ", ".join(default_kws)

keywords_input = st.sidebar.text_area(
    "Configure Keywords (comma-separated):",
    value=st.session_state['keywords_text'],
    height=200,
    help="Modify keywords dynamically. The lexer will adapt to this list."
)
st.session_state['keywords_text'] = keywords_input
custom_keywords = {k.strip() for k in keywords_input.split(",") if k.strip()}

# Options
include_comments = st.sidebar.checkbox("Include Comments", value=True, help="If unchecked, comment tokens will be skipped in the output stream.")



# ----------------- MAIN HEADER -----------------
st.markdown("<h1 class='main-title'>🔍 Source Code Tokenizer</h1>", unsafe_allow_html=True)

st.markdown("---")

# ----------------- INPUT SECTION -----------------
st.subheader("📝 Input Source Code")

input_option = st.radio("Choose Input Method:", ("Paste Source Code", "Upload Source File"), horizontal=True)

raw_code = ""

if input_option == "Paste Source Code":
    # Text area for pasted code
    pasted_code = st.text_area(
        "Paste your code here:",
        value=st.session_state['code_input'],
        height=250,
        placeholder="int main() {\n    int sum = 10 + 20;\n    return 0;\n}",
        key="paste_area"
    )
    st.session_state['code_input'] = pasted_code
    raw_code = pasted_code
else:
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload a source code file (.c, .cpp, .java, .py, .txt):",
        type=["c", "cpp", "java", "py", "txt"],
        key=f"file_uploader_{st.session_state['file_uploader_key']}"
    )
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        raw_code = decode_bytes(file_bytes)
        st.session_state['code_input'] = raw_code
        st.code(raw_code, language=language.lower().replace(" / c++", "cpp").replace(" ", ""))

# Action buttons
col_btn1, col_btn2, _ = st.columns([1, 1, 6])
with col_btn1:
    tokenize_clicked = st.button("🚀 Tokenize Code", type="primary", use_container_width=True)
with col_btn2:
    clear_clicked = st.button("🧹 Clear", use_container_width=True)

if clear_clicked:
    st.session_state['code_input'] = ""
    st.session_state['file_uploader_key'] += 1  # Force recreate uploader
    st.session_state['tokenize_triggered'] = False
    st.rerun()

# Trigger logic
if tokenize_clicked:
    st.session_state['tokenize_triggered'] = True

# ----------------- TOKENIZATION ENGINE RUN -----------------
if st.session_state['tokenize_triggered'] and raw_code.strip() != "":
    # Run Tokenizer
    lexer = Tokenizer(
        source_code=raw_code,
        language=language,
        include_comments=include_comments,
        custom_keywords=custom_keywords
    )
    tokens, errors = lexer.tokenize()
    
    # 1. 📊 RESULTS DASHBOARD
    st.markdown("---")
    st.subheader("📊 Lexer Analysis Dashboard")
    
    # Compute Metrics
    keywords_cnt = sum(1 for t in tokens if t.type == "KEYWORD")
    identifiers_cnt = sum(1 for t in tokens if t.type == "IDENTIFIER")
    numbers_cnt = sum(1 for t in tokens if t.type in ("INTEGER", "FLOAT"))
    operators_cnt = sum(1 for t in tokens if "OPERATOR" in t.type or t.type == "INCREMENT_DECREMENT")
    strings_cnt = sum(1 for t in tokens if t.type in ("STRING", "CHARACTER"))
    comments_cnt = sum(1 for t in tokens if t.type == "COMMENT")
    errors_cnt = len(errors)
    total_tokens = len(tokens)
    
    # Render dashboard metrics in custom cards
    met_col1, met_col2, met_col3, met_col4 = st.columns(4)
    with met_col1:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-title'>Total Tokens</div>
            <div class='metric-value'>{total_tokens}</div>
        </div>""", unsafe_allow_html=True)
    with met_col2:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-title'>Keywords</div>
            <div class='metric-value'>{keywords_cnt}</div>
        </div>""", unsafe_allow_html=True)
    with met_col3:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-title'>Identifiers</div>
            <div class='metric-value'>{identifiers_cnt}</div>
        </div>""", unsafe_allow_html=True)
    with met_col4:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-title'>Operators</div>
            <div class='metric-value'>{operators_cnt}</div>
        </div>""", unsafe_allow_html=True)
        
    st.write("") # spacing
    
    met_col5, met_col6, met_col7, met_col8 = st.columns(4)
    with met_col5:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-title'>Numbers</div>
            <div class='metric-value'>{numbers_cnt}</div>
        </div>""", unsafe_allow_html=True)
    with met_col6:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-title'>Strings & Chars</div>
            <div class='metric-value'>{strings_cnt}</div>
        </div>""", unsafe_allow_html=True)
    with met_col7:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-title'>Comments</div>
            <div class='metric-value'>{comments_cnt}</div>
        </div>""", unsafe_allow_html=True)
    with met_col8:
        borderColor = "#bf616a" if errors_cnt > 0 else "#2e3440"
        textColor = "#bf616a" if errors_cnt > 0 else "#eceff4"
        st.markdown(f"""<div class='metric-card' style='border: 1px solid {borderColor};'>
            <div class='metric-title' style='color: #bf616a;'>Lexical Errors</div>
            <div class='metric-value' style='color: {textColor};'>{errors_cnt}</div>
        </div>""", unsafe_allow_html=True)
        
    st.write("")
    
    # 2. 🚨 LEXICAL ERRORS DISPLAY
    if errors_cnt > 0:
        st.subheader("🚨 Lexical Errors Detected")
        err_df = pd.DataFrame([e.to_dict() for e in errors])
        st.dataframe(err_df, use_container_width=True)
        
        # Friendly notifications
        for i, err in enumerate(errors[:3], 1):
            st.markdown(f"""
            <div class="error-card">
                <strong>Error #{i}:</strong> Line {err.line}, Column {err.column} <br/>
                Character/Lexeme: <code>{err.lexeme}</code> — {err.message}
            </div>
            """, unsafe_allow_html=True)
        if errors_cnt > 3:
            st.caption(f"... and {errors_cnt - 3} more errors listed in the table above.")
        st.write("")

    # 3. 📊 CHARTS & DISTRIBUTIONS
    st.subheader("📈 Token Distributions")
    col_chart, col_df_full = st.columns([5, 5])
    
    with col_chart:
        if total_tokens > 0:
            df_tokens = pd.DataFrame([t.to_dict() for t in tokens])
            df_grouped = df_tokens["type"].value_counts().reset_index()
            df_grouped.columns = ["Token Type", "Count"]
            
            fig = px.bar(
                df_grouped,
                x="Token Type",
                y="Count",
                color="Token Type",
                title="Frequency of Token Types",
                text="Count",
                template="plotly_dark"
            )
            fig.update_layout(
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0d5ff')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No tokens to display chart.")
            
    with col_df_full:
        # Search & Filterable Table
        st.markdown("**🔍 Token Stream Filter & Search**")
        search_query = st.text_input("Filter tokens by Type or Lexeme:", placeholder="e.g. KEYWORD, int, ASSIGNMENT_OPERATOR")
        
        if total_tokens > 0:
            df_tokens = pd.DataFrame([t.to_dict() for t in tokens])
            df_tokens.insert(0, "Token No.", range(1, len(df_tokens) + 1))
            
            if search_query:
                filtered_df = df_tokens[
                    df_tokens['type'].str.contains(search_query, case=False, na=False) |
                    df_tokens['lexeme'].str.contains(search_query, case=False, na=False)
                ]
            else:
                filtered_df = df_tokens
                
            st.dataframe(filtered_df, height=350, use_container_width=True)
        else:
            st.info("Token stream is empty.")

    # 4. 📥 DOWNLOAD SECTION
    if total_tokens > 0:
        st.subheader("📥 Export & Download Token Stream")
        
        csv_data = export_to_csv(tokens)
        txt_data = export_to_txt(tokens)
        
        col_dl1, col_dl2, _ = st.columns([2, 2, 4])
        with col_dl1:
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name="token_stream.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_dl2:
            st.download_button(
                label="📥 Download TXT (Stream format)",
                data=txt_data,
                file_name="token_stream.txt",
                mime="text/plain",
                use_container_width=True
            )
            
elif st.session_state['tokenize_triggered'] and raw_code.strip() == "":
    st.warning("⚠️ Please provide source code before tokenizing!")
