from document import FPDF, DocumentPrefs, Contexts, ContextData
from document import create_pdf, save_pdf, parse_data, add_text_line, add_paragraph, add_date_stamp


def create_header(pdf: FPDF, cover: ContextData):
    title = f'{cover.first_name} {cover.last_name}'
    contact = f'{cover.address}{DocumentPrefs.separator}{cover.phone_number}{DocumentPrefs.separator}{cover.email}{DocumentPrefs.separator}{cover.linked_in}'
    add_text_line(pdf, title.upper(), DocumentPrefs.font_size_reg, bold=True)
    pdf.ln(5.0)
    add_text_line(pdf, contact, DocumentPrefs.font_size_reg)
    pdf.ln(DocumentPrefs.margin_section)


def create_letter(pdf: FPDF, cover: ContextData):
    add_paragraph(pdf, cover.cover_letter)
    pdf.ln()


def create_ending(pdf: FPDF, cover: ContextData):
    ending = f'Thank you for your time and consideration,\n{cover.first_name} {cover.last_name}'
    add_paragraph(pdf, ending)


if __name__ == '__main__':
    cover = parse_data(Contexts.cover_letter)
    pdf = create_pdf(cover, Contexts.cover_letter)
    create_header(pdf, cover)
    add_date_stamp(pdf)
    create_letter(pdf, cover)
    create_ending(pdf, cover)
    save_pdf(pdf, cover, Contexts.cover_letter)