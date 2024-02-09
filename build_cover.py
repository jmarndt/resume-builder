import os
import sys
import calendar
from datetime import date
from types import SimpleNamespace

from fpdf import FPDF
from fpdf.enums import XPos, YPos
import markdown_to_json


DocumentPrefs = SimpleNamespace(
    font_family = 'Cabin',
    font_size_reg = 14,
    font_size_title = 24,
    line_spacing = 2,
    separator = '  •  ',
    unit = 'pt',
    page_size = 'Letter',
    margin_vertical = 25,
    margin_side = 25,
    margin_section = 30,
    script_dir = os.path.dirname(os.path.realpath(__file__))
)


def create_pdf(cover):
    pdf = FPDF('P', DocumentPrefs.unit, DocumentPrefs.page_size)
    pdf.add_font(DocumentPrefs.font_family, style="", fname=f'{DocumentPrefs.script_dir}/fonts/{DocumentPrefs.font_family}-Regular.ttf')
    pdf.add_font(DocumentPrefs.font_family, style="b", fname=f'{DocumentPrefs.script_dir}/fonts/{DocumentPrefs.font_family}-Bold.ttf')
    pdf.add_font(DocumentPrefs.font_family, style="i", fname=f'{DocumentPrefs.script_dir}/fonts/{DocumentPrefs.font_family}-Italic.ttf')
    pdf.add_font(DocumentPrefs.font_family, style="bi", fname=f'{DocumentPrefs.script_dir}/fonts/{DocumentPrefs.font_family}-BoldItalic.ttf')
    pdf.set_title(f'{cover.first_name} {cover.last_name} Cover Letter')
    pdf.set_margins(DocumentPrefs.margin_vertical, DocumentPrefs.margin_side)
    pdf.set_auto_page_break(True, DocumentPrefs.margin_vertical)
    pdf.add_page()
    return pdf


def create_header(pdf: FPDF, cover):
    title = f'{cover.first_name} {cover.last_name}'
    contact = f'{cover.phone_number}{DocumentPrefs.separator}{cover.email}{DocumentPrefs.separator}{cover.address}'
    add_text_line(pdf, title.upper(), DocumentPrefs.font_size_reg, bold=True)
    pdf.ln(5.0)
    add_text_line(pdf, contact, DocumentPrefs.font_size_reg)
    pdf.ln(DocumentPrefs.margin_section)


def create_date_stamp(pdf: FPDF):
    today = date.today()
    month = calendar.month_name[today.month]
    day = f'  {today.day}'
    suffix = get_ordinal(today.day)
    year = f',  {today.year}'
    add_text_line(pdf, month, width=pdf.get_string_width(month), br=False)
    add_text_line(pdf, day, width=pdf.get_string_width(day), br=False)
    pdf.char_vpos = "SUP"
    add_text_line(pdf, suffix, width=pdf.get_string_width(suffix), br=False)
    pdf.char_vpos = "LINE"
    add_text_line(pdf, year)
    pdf.ln(DocumentPrefs.margin_section)


def create_greeting(pdf, cover):
    add_paragraph(pdf, cover.greeting)
    pdf.ln()


def create_letter(pdf, cover):
    add_paragraph(pdf, cover.letter)
    pdf.ln()


def create_ending(pdf, cover):
    ending = f'Thank you for your time and consideration,\n{cover.first_name} {cover.last_name}'
    add_paragraph(pdf, ending)


def add_paragraph(pdf: FPDF, text: str):
    pdf.set_font(DocumentPrefs.font_family, '', DocumentPrefs.font_size_reg)
    pdf.multi_cell(0, DocumentPrefs.font_size_reg +DocumentPrefs.line_spacing , text, align='J', new_x='LEFT')
    

def get_ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        return 'th'
    else:
        return ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]


def add_text_line(pdf: FPDF, text: str, size=DocumentPrefs.font_size_reg, cellSize=None, bold=False, underline=False, italic=False, br=True, align='L', width=0, font=DocumentPrefs.font_family):
    style = ''
    if bold: style += 'B'
    if underline: style += 'U'
    if italic: style += 'I'
    pdf.set_font(font, style, size)
    pdf.cell(width, cellSize if cellSize else size + DocumentPrefs.line_spacing, text, align=align, new_x=XPos.LMARGIN if br else XPos.RIGHT, new_y=YPos.NEXT if br else YPos.TOP)


def parse_cover():
    file_name = sys.argv[1] if len(sys.argv) > 1 else 'cover.md'
    with open(file_name, 'r') as cover:
        data =  markdown_to_json.dictify(cover.read())
        return SimpleNamespace(
            first_name = data['First Name'],
            last_name = data['Last Name'],
            email = data['Email'],
            phone_number = data['Phone Number'],
            address = data['Address'],
            greeting = data['Greeting'],
            letter = data['Letter']
        )


if __name__ == '__main__':
    cover = parse_cover()
    pdf = create_pdf(cover)
    create_header(pdf, cover)
    create_date_stamp(pdf)
    create_greeting(pdf, cover)
    create_letter(pdf, cover)
    create_ending(pdf, cover)
    pdf.output(f'{DocumentPrefs.script_dir}/{cover.last_name.lower()}_{cover.first_name.lower()}_cover_letter.pdf')