
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Preformatted,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import mm

import os
import re
import tempfile


# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_MD_FILE = "Maths_Competitive_Exam_Formulae_and_Tricks.md"

DEFAULT_PDF_FILE = "Maths_Competitive_Exam_Formulae_and_Tricks.pdf"


# ============================================================
# STREAMLIT CONFIG
# ============================================================

st.set_page_config(
    page_title="Maths Formulae PDF Converter",
    page_icon="📘",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 35px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }

    .file-box {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">📘 Maths Formulae & Tricks</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Markdown → PDF Converter for Competitive Exam Preparation'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def escape_html(text):
    """
    Escape characters that have special meaning in ReportLab XML.
    """

    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")

    return text


def format_inline_markdown(text):
    """
    Convert basic Markdown formatting into ReportLab formatting.
    """

    text = escape_html(text)

    # Bold
    text = re.sub(
        r"\*\*(.*?)\*\*",
        r"<b>\1</b>",
        text
    )

    # Italic
    text = re.sub(
        r"(?<!\*)\*(.*?)\*(?!\*)",
        r"<i>\1</i>",
        text
    )

    # Inline code
    text = re.sub(
        r"`(.*?)`",
        r"<font name='Courier'>\1</font>",
        text
    )

    return text


# ============================================================
# MARKDOWN → PDF
# ============================================================

def markdown_to_pdf(md_text, output_file):

    styles = getSampleStyleSheet()

    # --------------------------------------------------------
    # Title
    # --------------------------------------------------------

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=20,
        leading=25,
        alignment=TA_CENTER,
        spaceAfter=15,
    )

    # --------------------------------------------------------
    # H1
    # --------------------------------------------------------

    heading1_style = ParagraphStyle(
        "Heading1Custom",
        parent=styles["Heading1"],
        fontSize=16,
        leading=20,
        spaceBefore=14,
        spaceAfter=8,
    )

    # --------------------------------------------------------
    # H2
    # --------------------------------------------------------

    heading2_style = ParagraphStyle(
        "Heading2Custom",
        parent=styles["Heading2"],
        fontSize=13,
        leading=17,
        spaceBefore=10,
        spaceAfter=6,
    )

    # --------------------------------------------------------
    # H3
    # --------------------------------------------------------

    heading3_style = ParagraphStyle(
        "Heading3Custom",
        parent=styles["Heading3"],
        fontSize=11,
        leading=15,
        spaceBefore=8,
        spaceAfter=5,
    )

    # --------------------------------------------------------
    # Normal text
    # --------------------------------------------------------

    normal_style = ParagraphStyle(
        "NormalCustom",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14,
        spaceAfter=5,
    )

    # --------------------------------------------------------
    # Formula / Code
    # --------------------------------------------------------

    formula_style = ParagraphStyle(
        "FormulaCustom",
        parent=styles["Code"],
        fontSize=9,
        leading=13,
        backColor=colors.whitesmoke,
        borderPadding=6,
        spaceBefore=5,
        spaceAfter=7,
    )

    # --------------------------------------------------------
    # Create PDF
    # --------------------------------------------------------

    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,

        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,

        title="Maths Competitive Exam Formulae and Tricks",
        author="Markdown to PDF Converter",
    )

    story = []

    lines = md_text.splitlines()

    in_code_block = False
    code_buffer = []

    # --------------------------------------------------------
    # Process Markdown line-by-line
    # --------------------------------------------------------

    for line in lines:

        # ----------------------------------------------------
        # Code / Formula block
        # ----------------------------------------------------

        if line.strip().startswith("```"):

            if not in_code_block:

                in_code_block = True
                code_buffer = []

            else:

                in_code_block = False

                if code_buffer:

                    code_text = "\n".join(code_buffer)

                    story.append(
                        Preformatted(
                            code_text,
                            formula_style
                        )
                    )

                    story.append(
                        Spacer(1, 5)
                    )

                code_buffer = []

            continue

        # Inside code block
        if in_code_block:

            code_buffer.append(line)

            continue

        # ----------------------------------------------------
        # Empty line
        # ----------------------------------------------------

        if not line.strip():

            story.append(
                Spacer(1, 5)
            )

            continue

        # ----------------------------------------------------
        # H1
        # ----------------------------------------------------

        if line.startswith("# "):

            text = line[2:].strip()

            story.append(
                Paragraph(
                    escape_html(text),
                    title_style
                )
            )

        # ----------------------------------------------------
        # H2
        # ----------------------------------------------------

        elif line.startswith("## "):

            text = line[3:].strip()

            story.append(
                Paragraph(
                    escape_html(text),
                    heading1_style
                )
            )

        # ----------------------------------------------------
        # H3
        # ----------------------------------------------------

        elif line.startswith("### "):

            text = line[4:].strip()

            story.append(
                Paragraph(
                    escape_html(text),
                    heading2_style
                )
            )

        # ----------------------------------------------------
        # H4
        # ----------------------------------------------------

        elif line.startswith("#### "):

            text = line[5:].strip()

            story.append(
                Paragraph(
                    escape_html(text),
                    heading3_style
                )
            )

        # ----------------------------------------------------
        # Bullet list
        # ----------------------------------------------------

        elif line.startswith("- ") or line.startswith("* "):

            text = line[2:].strip()

            text = format_inline_markdown(text)

            story.append(
                Paragraph(
                    "• " + text,
                    normal_style
                )
            )

        # ----------------------------------------------------
        # Numbered list
        # ----------------------------------------------------

        elif re.match(r"^\d+\.\s+", line):

            text = re.sub(
                r"^\d+\.\s+",
                "",
                line
            )

            text = format_inline_markdown(text)

            story.append(
                Paragraph(
                    "• " + text,
                    normal_style
                )
            )

        # ----------------------------------------------------
        # Blockquote
        # ----------------------------------------------------

        elif line.startswith("> "):

            text = line[2:].strip()

            text = format_inline_markdown(text)

            quote_style = ParagraphStyle(
                "Quote",
                parent=normal_style,
                leftIndent=15,
                rightIndent=10,
                borderPadding=5,
                backColor=colors.whitesmoke,
            )

            story.append(
                Paragraph(
                    text,
                    quote_style
                )
            )

        # ----------------------------------------------------
        # Horizontal rule
        # ----------------------------------------------------

        elif line.strip() in ["---", "***", "___"]:

            story.append(
                Spacer(1, 8)
            )

        # ----------------------------------------------------
        # Normal paragraph
        # ----------------------------------------------------

        else:

            text = format_inline_markdown(
                line.strip()
            )

            story.append(
                Paragraph(
                    text,
                    normal_style
                )
            )

    # --------------------------------------------------------
    # Build PDF
    # --------------------------------------------------------

    doc.build(story)


# ============================================================
# FIND DEFAULT MARKDOWN FILE
# ============================================================

# Get the folder where app.py is located
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

default_md_path = os.path.join(
    BASE_DIR,
    DEFAULT_MD_FILE
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ Options")

st.sidebar.markdown(
    "### Markdown Source"
)

st.sidebar.write(
    "The application automatically loads:"
)

st.sidebar.code(
    DEFAULT_MD_FILE
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Upload another Markdown file below "
    "to replace the default file."
)


# ============================================================
# FILE UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "📂 Upload another Markdown file (optional)",
    type=["md", "markdown"],
    help="If no file is uploaded, the default Markdown file in the project folder will be used."
)


# ============================================================
# SELECT MARKDOWN SOURCE
# ============================================================

md_content = None
source_name = None


# ------------------------------------------------------------
# OPTION 1: Uploaded file
# ------------------------------------------------------------

if uploaded_file is not None:

    md_content = uploaded_file.getvalue().decode(
        "utf-8",
        errors="ignore"
    )

    source_name = uploaded_file.name

    st.success(
        f"📤 Using uploaded file: `{source_name}`"
    )


# ------------------------------------------------------------
# OPTION 2: Default project file
# ------------------------------------------------------------

elif os.path.exists(default_md_path):

    with open(
        default_md_path,
        "r",
        encoding="utf-8"
    ) as file:

        md_content = file.read()

    source_name = DEFAULT_MD_FILE

    st.success(
        f"📘 Automatically loaded: `{DEFAULT_MD_FILE}`"
    )


# ------------------------------------------------------------
# File doesn't exist
# ------------------------------------------------------------

else:

    st.error(
        f"❌ Default Markdown file was not found:\n\n"
        f"`{default_md_path}`"
    )

    st.warning(
        "Please place the Markdown file in the same folder "
        "as `app.py`, or upload a Markdown file above."
    )

    st.stop()


# ============================================================
# FILE INFORMATION
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Source File",
        source_name
    )

with col2:

    st.metric(
        "Characters",
        f"{len(md_content):,}"
    )

with col3:

    st.metric(
        "Lines",
        f"{len(md_content.splitlines()):,}"
    )


# ============================================================
# MARKDOWN PREVIEW
# ============================================================

st.markdown("---")

st.subheader("📖 Markdown Preview")

preview_col, raw_col = st.columns(2)


# ------------------------------------------------------------
# Rendered Markdown
# ------------------------------------------------------------

with preview_col:

    st.markdown(
        md_content
    )


# ------------------------------------------------------------
# Raw Markdown
# ------------------------------------------------------------

with raw_col:

    with st.expander(
        "View Raw Markdown"
    ):

        st.code(
            md_content,
            language="markdown"
        )


# ============================================================
# PDF CONVERSION
# ============================================================

st.markdown("---")

st.subheader("📄 PDF Conversion")


if st.button(
    "🔄 Convert Markdown → PDF",
    type="primary",
    use_container_width=True
):

    with st.spinner(
        "Generating PDF..."
    ):

        try:

            # Temporary directory
            temp_dir = tempfile.gettempdir()

            output_path = os.path.join(
                temp_dir,
                DEFAULT_PDF_FILE
            )

            # Convert Markdown
            markdown_to_pdf(
                md_content,
                output_path
            )

            # Read PDF
            with open(
                output_path,
                "rb"
            ) as pdf_file:

                pdf_bytes = pdf_file.read()

            st.success(
                "✅ PDF generated successfully!"
            )

            # ------------------------------------------------
            # Download
            # ------------------------------------------------

            st.download_button(
                label="⬇️ Download PDF",
                data=pdf_bytes,
                file_name=DEFAULT_PDF_FILE,
                mime="application/pdf",
                use_container_width=True
            )

            # ------------------------------------------------
            # PDF size
            # ------------------------------------------------

            st.caption(
                f"PDF size: "
                f"{len(pdf_bytes) / 1024:.2f} KB"
            )

        except Exception as e:

            st.error(
                "❌ Error while generating PDF"
            )

            st.exception(e)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "📘 Maths Competitive Exam Formulae & Tricks • "
    "Markdown → PDF Converter"
)