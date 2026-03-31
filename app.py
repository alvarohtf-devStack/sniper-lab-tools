import streamlit as st
from PIL import Image
from docx import Document
import io
import os
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import tempfile
import zipfile

# --- 1. CONFIGURAÇÃO DE AMBIENTE (Híbrido: Windows + Cloud) ---
def configurar_binarios():
    tesseract_local = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    poppler_local = r'C:\poppler\Library\bin'
    
    if os.path.exists(tesseract_local):
        pytesseract.pytesseract.tesseract_cmd = tesseract_local
        return poppler_local
    return None 

POPPLER_PATH = configurar_binarios()

# Configuração da Página
st.set_page_config(page_title="Sniper Lab | Hub", page_icon="🎯", layout="wide", initial_sidebar_state="collapsed")

# --- 2. LÓGICA DE NAVEGAÇÃO ---
if 'opcao' not in st.session_state:
    st.session_state.opcao = "Início"

def navegar(pagina):
    st.session_state.opcao = pagina

# --- 3. CSS SNIPER ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;700;800&display=swap');
    .stApp { background-color: #f4f7f6; font-family: 'Segoe UI', sans-serif; }
    .header-sniper {
        background-color: #1e3d1e; 
        padding: 1.5rem;
        margin: -5rem -5rem 2rem -5rem;
        text-align: center;
        color: white;
    }
    .tool-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #27ae60;
        height: 100px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNÇÕES DE SUPORTE ---
def get_pdf_page_img(pdf_path, page_num):
    try:
        # AJUSTE SNIPER: Só passa poppler_path se ele existir (Windows)
        kwargs = {'poppler_path': POPPLER_PATH} if POPPLER_PATH else {}
        images = convert_from_path(
            pdf_path, 
            first_page=page_num, 
            last_page=page_num, 
            size=(None, 400),
            **kwargs
        )
        return images[0]
    except:
        return None

# --- 5. ÁREA DE CONTEÚDO ---
st.markdown("""<div class="header-sniper"><h1>🎯 SNIPER LAB</h1><p>HUB OPERACIONAL 80/20</p></div>""", unsafe_allow_html=True)

if st.session_state.opcao == "Início":
    st.markdown("<h2 style='text-align: center;'>Arsenal de Ferramentas</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="tool-card"><h3>🔗 Juntar PDFs</h3><p>Mesclar múltiplos arquivos.</p></div>', unsafe_allow_html=True)
        if st.button("Abrir Unificador", key="btn_merge"): navegar("Juntar PDFs (Merge)")
        st.markdown('<div class="tool-card"><h3>📄 PDF para Word</h3><p>OCR de Alta Precisão.</p></div>', unsafe_allow_html=True)
        if st.button("Abrir OCR", key="btn_ocr"): navegar("PDF para Word (OCR)")
    
    with col2:
        st.markdown('<div class="tool-card"><h3>✂️ Dividir PDF</h3><p>Múltiplos intervalos + Preview.</p></div>', unsafe_allow_html=True)
        if st.button("Abrir Divisor", key="btn_split"): navegar("Dividir PDF (Split)")
        st.markdown('<div class="tool-card"><h3>📸 Imagem para PDF</h3><p>Conversor de Imagens.</p></div>', unsafe_allow_html=True)
        if st.button("Abrir Conversor", key="btn_img"): navegar("Imagem para PDF")
        
    with col3:
        st.markdown('<div class="tool-card" style="opacity:0.5"><h3>⚙️ Automação</h3><p>Em breve: Make/Zapier.</p></div>', unsafe_allow_html=True)
        st.button("Bloqueado", disabled=True, key="lock1")

else:
    if st.button("⬅ Voltar ao Arsenal"): navegar("Início")

    if st.session_state.opcao == "Dividir PDF (Split)":
        st.header("✂️ Divisor Sniper")
        arquivo = st.file_uploader("Suba o PDF", type="pdf")
        
        if arquivo:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as t_file:
                t_file.write(arquivo.getvalue())
                path_pdf = t_file.name
            
            reader = PdfReader(path_pdf)
            total = len(reader.pages)
            st.info(f"O documento possui {total} páginas.")
            
            intervalos_str = st.text_input("Intervalos (ex: 1-2, 5)", placeholder="Ex: 1-3, 10")
            
            if intervalos_str:
                try:
                    partes = intervalos_str.replace(" ", "").split(",")
                    for idx, parte in enumerate(partes):
                        st.subheader(f"🔍 Preview Intervalo {idx+1}")
                        c1, c2 = st.columns(2)
                        
                        inicio, fim = (map(int, parte.split("-"))) if "-" in parte else (int(parte), int(parte))
                        
                        with c1:
                            img_i = get_pdf_page_img(path_pdf, inicio)
                            if img_i: st.image(img_i, caption=f"Pág. {inicio}", width='stretch')
                        with c2:
                            img_f = get_pdf_page_img(path_pdf, fim)
                            if img_f: st.image(img_f, caption=f"Pág. {fim}", width='stretch')
                    
                    st.divider()
                    if st.button("🚀 Gerar Arquivos"):
                        ficheiros = []
                        for idx, p in enumerate(partes):
                            writer = PdfWriter()
                            ini, f = (map(int, p.split("-"))) if "-" in p else (int(p), int(p))
                            for i in range(max(1, ini)-1, min(total, f)):
                                writer.add_page(reader.pages[i])
                            buf = io.BytesIO()
                            writer.write(buf)
                            ficheiros.append((f"parte_{idx+1}.pdf", buf.getvalue()))

                        ca, cb = st.columns(2)
                        with ca:
                            merger = PdfMerger()
                            for _, c in ficheiros: merger.append(io.BytesIO(c))
                            b_u = io.BytesIO()
                            merger.write(b_u)
                            st.download_button("📥 PDF Único", b_u.getvalue(), "unido.pdf", width='stretch')
                        with cb:
                            b_z = io.BytesIO()
                            with zipfile.ZipFile(b_z, "w") as zf:
                                for n, c in ficheiros: zf.writestr(n, c)
                            st.download_button("📦 Arquivo ZIP", b_z.getvalue(), "partes.zip", width='stretch')
                except:
                    st.warning("Aguardando formato válido...")
            os.unlink(path_pdf)

    elif st.session_state.opcao == "Juntar PDFs (Merge)":
        st.header("🔗 Unificador")
        arquivos = st.file_uploader("Selecione os PDFs", type="pdf", accept_multiple_files=True)
        if arquivos and st.button("Fundir"):
            merger = PdfMerger()
            for f in arquivos: merger.append(f)
            out = io.BytesIO()
            merger.write(out)
            st.download_button("📥 Baixar", out.getvalue(), "unido.pdf", width='stretch')

    elif st.session_state.opcao == "PDF para Word (OCR)":
        st.header("📄 OCR Sniper")
        up = st.file_uploader("PDF Escaneado", type="pdf")
        if up and st.button("Processar OCR"):
            with st.spinner("Analisando..."):
                with tempfile.TemporaryDirectory() as tmp:
                    p = os.path.join(tmp, "t.pdf")
                    with open(p, "wb") as f: f.write(up.getbuffer())
                    # AJUSTE SNIPER AQUI TAMBÉM
                    kwargs = {'poppler_path': POPPLER_PATH} if POPPLER_PATH else {}
                    imgs = convert_from_path(p, **kwargs)
                    doc = Document()
                    for i in imgs:
                        doc.add_paragraph(pytesseract.image_to_string(i, lang='por'))
                        doc.add_page_break()
                    b = io.BytesIO()
                    doc.save(b)
                    st.download_button("📥 Baixar Word", b.getvalue(), "ocr.docx", width='stretch')

    elif st.session_state.opcao == "Imagem para PDF":
        st.header("📸 Imagem -> PDF")
        img_up = st.file_uploader("Imagem", type=["png", "jpg"])
        if img_up and st.button("Converter"):
            im = Image.open(img_up).convert('RGB')
            buf = io.BytesIO()
            im.save(buf, format="PDF")
            st.download_button("📥 Baixar PDF", buf.getvalue(), "foto.pdf", width='stretch')

st.markdown("---")
st.markdown('<div style="text-align: center; color: #95a5a6; font-size: 0.8rem;">© 2026 - Sniper Lab</div>', unsafe_allow_html=True)