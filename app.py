import streamlit as st
from PIL import Image
from pdf2docx import Converter
from docx import Document
import io
import os
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import tempfile

# --- 1. CONFIGURAÇÃO DE AMBIENTE (Caminhos do seu PC) ---
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
POPPLER_PATH = r'C:\poppler\Library\bin'

st.set_page_config(page_title="Sniper Lab | Hub de Ferramentas", page_icon="🎯", layout="wide")

# --- 2. INJEÇÃO DE CSS (Sua Identidade Visual) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;700;800&display=swap');
    .stApp {{ background-color: #f4f7f6; font-family: 'Segoe UI', sans-serif; }}
    [data-testid="stSidebar"] {{ background-color: #2c3e50; }}
    [data-testid="stSidebar"] * {{ color: #ffffff !important; }}
    h1, h2, h3 {{ color: #2c3e50 !important; font-weight: 800 !important; }}
    
    .stButton>button {{
        background-color: #27ae60 !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 10px 25px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(39, 174, 96, 0.3) !important;
        border: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. HEADER (Simulando seu Site) ---
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; background: white; padding: 15px 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 25px;">
        <div style="font-weight: 800; font-size: 1.5rem; color: #27ae60; letter-spacing: -1px;">SNIPER LAB</div>
        <div style="font-weight: 500; color: #2d3436;">HUB DE FERRAMENTAS</div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. FUNÇÕES DE MISSÃO (Lógica Protegida) ---

def merge_pdfs(lista_pdfs):
    merger = PdfMerger()
    for pdf in lista_pdfs:
        merger.append(pdf)
    output = io.BytesIO()
    merger.write(output)
    merger.close()
    return output.getvalue()

def split_pdf(pdf_file, pg_inicio, pg_fim):
    reader = PdfReader(pdf_file)
    writer = PdfWriter()
    
    # Ajuste para índice 0 (usuário digita 1, o código lê 0)
    for i in range(pg_inicio - 1, pg_fim):
        writer.add_page(reader.pages[i])
        
    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()

def ocr_process(pdf_file):
    with tempfile.TemporaryDirectory() as path:
        temp_pdf = os.path.join(path, "temp.pdf")
        with open(temp_pdf, "wb") as f:
            f.write(pdf_file.getbuffer())
        try:
            images = convert_from_path(temp_pdf, poppler_path=POPPLER_PATH)
            doc = Document()
            for image in images:
                texto = pytesseract.image_to_string(image, lang='por')
                doc.add_paragraph(texto)
                doc.add_page_break()
            target = io.BytesIO()
            doc.save(target)
            return target.getvalue()
        except Exception as e:
            st.error(f"Erro OCR: {e}")
            return None

# --- 5. MENU LATERAL ---
with st.sidebar:
    st.markdown("### 🛠️ Menu Sniper")
    opcao = st.selectbox("Operação:", ["Início", "Juntar PDFs (Merge)", "Dividir PDF (Split)", "PDF para Word (OCR)", "Imagem para PDF"])
    st.markdown("---")
    st.info("Focando nos 20% de esforço que geram 80% de resultado.")
    st.link_button("🏠 Voltar para o Portal", "https://seu-site-index.com")

# --- 6. ÁREA DE CONTEÚDO ---
if opcao == "Início":
    st.markdown("""
        <div style="background: linear-gradient(135deg, #27ae60, #2c3e50); color: white; padding: 40px; border-radius: 15px; text-align: center;">
            <h1>Bem-vindo ao Hub de Automação</h1>
            <p>Transformando documentos complexos em dados prontos para o lucro.</p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div style="background: white; padding: 20px; border-radius: 12px; border-left: 5px solid #27ae60; box-shadow: 0 4px 15px rgba(0,0,0,0.05);"><h3>📄 Conversor Inteligente</h3><p>IA para PDFs escaneados com OCR de alta precisão.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="background: white; padding: 20px; border-radius: 12px; border-left: 5px solid #2c3e50; box-shadow: 0 4px 15px rgba(0,0,0,0.05);"><h3>🔗 Unificador Sniper</h3><p>Junte múltiplos relatórios em um único arquivo PDF.</p></div>', unsafe_allow_html=True)

elif opcao == "Juntar PDFs (Merge)":
    st.header("🔗 Juntar vários PDFs")
    arquivos = st.file_uploader("Selecione os arquivos", type="pdf", accept_multiple_files=True)
    if arquivos and st.button("Iniciar Fusão"):
        pdf_final = merge_pdfs(arquivos)
        st.download_button("📥 Baixar PDF Unificado", pdf_final, "unificado_sniper.pdf")

elif opcao == "Dividir PDF (Split)":
    st.header("✂️ Dividir PDF por Intervalo")
    arquivo_split = st.file_uploader("Suba o PDF que deseja cortar", type="pdf")
    if arquivo_split:
        reader_temp = PdfReader(arquivo_split)
        total_pags = len(reader_temp.pages)
        st.write(f"O documento possui **{total_pags}** páginas.")
        
        c1, c2 = st.columns(2)
        with c1:
            inicio = st.number_input("Página Inicial", min_value=1, max_value=total_pags, value=1)
        with c2:
            fim = st.number_input("Página Final", min_value=1, max_value=total_pags, value=total_pags)
            
        if st.button("Cortar PDF"):
            if inicio <= fim:
                pdf_cortado = split_pdf(arquivo_split, inicio, fim)
                st.download_button("📥 Baixar PDF Cortado", pdf_cortado, "cortado_sniper.pdf")
            else:
                st.error("A página inicial não pode ser maior que a final.")

elif opcao == "PDF para Word (OCR)":
    st.header("📄 Conversor OCR Robusto")
    upload_pdf = st.file_uploader("Suba seu PDF técnico", type=["pdf"])
    if upload_pdf and st.button("Iniciar Operação"):
        with st.spinner("IA Sniper Analisando..."):
            docx_data = ocr_process(upload_pdf)
            if docx_data:
                st.download_button("📥 Baixar Documento Final", docx_data, "resultado_sniper.docx")

elif opcao == "Imagem para PDF":
    st.header("📸 Imagem para PDF")
    upload = st.file_uploader("Suba sua imagem", type=["png", "jpg", "jpeg"])
    if upload and st.button("Converter"):
        img = Image.open(upload).convert('RGB')
        buf = io.BytesIO()
        img.save(buf, format="PDF")
        st.download_button("📥 Baixar PDF", buf.getvalue(), "imagem_convertida.pdf")

# --- 7. FOOTER ---
st.markdown("---")
st.markdown('<div style="text-align: center; color: #95a5a6; font-size: 0.8rem;">© 2026 - Sniper Lab | Operando sob o Princípio de Pareto</div>', unsafe_allow_html=True)
