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
import streamlit.components.v1 as components # Import necessário para a Tag

# --- 1. CONFIGURAÇÃO DE AMBIENTE ---
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

# --- INJEÇÃO DA GOOGLE TAG (ANALYTICS) ---
# Isso injeta o script no cabeçalho invisível do app
components.html(
    """
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-NGBVHMR43R"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-NGBVHMR43R');
    </script>
    """,
    height=0, # Deixamos altura 0 para não criar espaço em branco na tela
)

# --- 2. LÓGICA DE NAVEGAÇÃO ---
if 'opcao' not in st.session_state:
    st.session_state.opcao = "Início"

def navegar(pagina):
    st.session_state.opcao = pagina

# --- 3. CSS SNIPER V2 ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    .stApp { background-color: #f0f2f5; font-family: 'Inter', sans-serif; }
    
    /* Header Sniper */
    .header-sniper {
        background: linear-gradient(135deg, #1e3d1e 0%, #0d1a0d 100%);
        padding: 3rem 1rem;
        margin: -6rem -5rem 2rem -5rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .tool-card {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        border-top: 5px solid #27ae60;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.2s;
        margin-bottom: 1rem;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .tool-card h3 { color: #1e3d1e !important; margin-bottom: 5px; font-weight: 800; }
    .tool-card p { color: #576574 !important; font-size: 0.9rem; line-height: 1.3; }
    
    div.stButton > button {
        width: 100%;
        background-color: #1e3d1e;
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 0.5rem;
        font-weight: 700;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #27ae60;
        color: white !important;
        transform: translateY(-2px);
    }

    @media (max-width: 768px) {
        .header-sniper { margin: -6rem -1rem 1rem -1rem; padding: 2rem 1rem; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNÇÕES DE SUPORTE ---
def get_pdf_page_img(pdf_path, page_num):
    try:
        kwargs = {'poppler_path': POPPLER_PATH} if POPPLER_PATH else {}
        images = convert_from_path(pdf_path, first_page=page_num, last_page=page_num, size=(None, 400), **kwargs)
        return images[0]
    except: return None

# --- 5. ÁREA DE CONTEÚDO ---
st.markdown("""<div class="header-sniper"><h1>🎯 SNIPER LAB</h1><p>OPERATIONAL HUB 80/20</p></div>""", unsafe_allow_html=True)

if st.session_state.opcao == "Início":
    st.markdown("<h2 style='text-align: center; color: #1e3d1e;'>Arsenal de Ferramentas</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="tool-card"><h3>🔗 Juntar PDFs</h3><p>Mescle vários documentos em um único arquivo final de forma organizada.</p></div>', unsafe_allow_html=True)
        st.button("Abrir Unificador", key="btn_merge", on_click=navegar, args=("Juntar PDFs (Merge)",))
        
        st.markdown('<div class="tool-card"><h3>📄 PDF para Word</h3><p>Transforme arquivos escaneados em texto editável usando OCR de alta precisão.</p></div>', unsafe_allow_html=True)
        st.button("Abrir OCR", key="btn_ocr", on_click=navegar, args=("PDF para Word (OCR)",))
    
    with col2:
        st.markdown('<div class="tool-card"><h3>✂️ Dividir PDF</h3><p>Extraia páginas específicas ou intervalos criando novos arquivos com preview visual instantâneo.</p></div>', unsafe_allow_html=True)
        st.button("Abrir Divisor", key="btn_split", on_click=navegar, args=("Dividir PDF (Split)",))
        
        st.markdown('<div class="tool-card"><h3>📸 Conversor Inteligente</h3><p>Transforme fotos e capturas de tela em documentos PDF de alta qualidade. Suporte universal para JPG, PNG, WebP e mais, com otimização automática de cores.</p></div>', unsafe_allow_html=True)
        st.button("Abrir Conversor", key="btn_img", on_click=navegar, args=("Imagem para PDF",))
        
    with col3:
        st.markdown('<div class="tool-card" style="opacity:0.6; border-top-color: #95a5a6;"><h3>⚙️ Automação</h3><p>Integração direta com fluxos Make.com e Zapier para processos do SESMT.</p></div>', unsafe_allow_html=True)
        st.button("Em Breve", disabled=True, key="lock1")

else:
    st.button("⬅ Voltar ao Arsenal", on_click=navegar, args=("Início",))
    st.markdown("---")

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
                            st.download_button("📥 PDF Único", b_u.getvalue(), "unido.pdf")
                        with cb:
                            b_z = io.BytesIO()
                            with zipfile.ZipFile(b_z, "w") as zf:
                                for n, c in ficheiros: zf.writestr(n, c)
                            st.download_button("📦 Arquivo ZIP", b_z.getvalue(), "partes.zip")
                except: st.warning("Aguardando formato válido...")
            os.unlink(path_pdf)

    elif st.session_state.opcao == "Juntar PDFs (Merge)":
        st.header("🔗 Unificador")
        arquivos = st.file_uploader("Selecione os PDFs", type="pdf", accept_multiple_files=True)
        if arquivos and st.button("Fundir"):
            merger = PdfMerger()
            for f in arquivos: merger.append(f)
            out = io.BytesIO()
            merger.write(out)
            st.download_button("📥 Baixar", out.getvalue(), "unido.pdf")

    elif st.session_state.opcao == "PDF para Word (OCR)":
        st.header("📄 OCR Sniper")
        up = st.file_uploader("PDF Escaneado", type="pdf")
        if up and st.button("Processar OCR"):
            with st.spinner("Analisando..."):
                with tempfile.TemporaryDirectory() as tmp:
                    p = os.path.join(tmp, "t.pdf")
                    with open(p, "wb") as f: f.write(up.getbuffer())
                    kwargs = {'poppler_path': POPPLER_PATH} if POPPLER_PATH else {}
                    imgs = convert_from_path(p, **kwargs)
                    doc = Document()
                    for i in imgs:
                        doc.add_paragraph(pytesseract.image_to_string(i, lang='por'))
                        doc.add_page_break()
                    b = io.BytesIO()
                    doc.save(b)
                    st.download_button("📥 Baixar Word", b.getvalue(), "ocr.docx")

    elif st.session_state.opcao == "Imagem para PDF":
        st.header("📸 Conversor Universal de Imagem -> PDF")
        img_up = st.file_uploader("Selecione a imagem (JPG, PNG, WEBP, BMP, TIFF, GIF)", 
                                 type=["png", "jpg", "jpeg", "webp", "bmp", "tiff", "gif"])
        
        if img_up:
            st.image(img_up, caption="Pré-visualização", width=300)
            
            if st.button("🚀 Converter para PDF"):
                try:
                    im = Image.open(img_up)
                    im_pdf = im.convert('RGB')
                    buf = io.BytesIO()
                    im_pdf.save(buf, format="PDF")
                    st.success("🎯 Conversão concluída com precisão!")
                    st.download_button(
                        label="📥 Baixar PDF",
                        data=buf.getvalue(),
                        file_name="sniper_convertido.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Erro na extração: {e}")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown('<div style="text-align: center; color: #95a5a6; font-size: 0.8rem;">© 2026 - Sniper Lab | Hub de Ferramentas SESMT</div>', unsafe_allow_html=True)