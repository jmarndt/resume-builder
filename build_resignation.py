from document import FPDF, DocumentPrefs, Contexts, ContextData
from document import create_pdf, save_pdf, parse_data, add_text_line, add_paragraph, add_date_stamp, add_line


def create_header(pdf: FPDF):
    title = f'FORMAL RESIGNATION LETTER'
    add_text_line(pdf, title, DocumentPrefs.font_size_title, bold=True, align='C')
    add_line(pdf)
    pdf.ln(DocumentPrefs.font_size_reg)


def create_letter(pdf, resignation: ContextData):
    add_paragraph(pdf, resignation.resignation_letter)
    pdf.ln(DocumentPrefs.margin_section)


def create_signature(pdf, resignation: ContextData):
    add_text_line(pdf, 'Sincerly,')
    pdf.image(f'{DocumentPrefs.script_dir}/SignatureTransparentBackground.png', x=DocumentPrefs.margin_side, w=pdf.epw/3)
    add_text_line(pdf, f'{resignation.first_name} {resignation.last_name}')


if __name__ == '__main__':
    resignation = parse_data(Contexts.resignation)
    pdf = create_pdf(resignation, Contexts.resignation)
    create_header(pdf)
    add_date_stamp(pdf)
    create_letter(pdf, resignation)
    create_signature(pdf, resignation)
    save_pdf(pdf, resignation, Contexts.resignation)