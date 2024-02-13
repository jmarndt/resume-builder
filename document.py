import os
import sys
import calendar
from typing import List
from datetime import date

from fpdf import FPDF
from fpdf.enums import XPos, YPos
import markdown_to_json


class DocumentPrefs():
    font_family = 'Cabin'
    font_size_reg = 14
    font_size_title = 24
    line_spacing = 2
    skills_per_line = 3
    separator = '  •  '
    unit = 'pt'
    format = 'Letter'
    margin_vertical = 25
    margin_side = 25
    margin_section = 30
    script_dir = os.path.dirname(os.path.realpath(__file__))


class Context():
    def __init__(self, proper_name: str, simple_name: str, file_name: str):
        self.proper_name = proper_name
        self.simple_name = simple_name
        self.file_name = file_name


class Contexts():
    resume = Context(proper_name = 'Résumé', simple_name='resume', file_name = 'résumé')
    cover_letter = Context(proper_name = 'Cover Letter', simple_name='cover', file_name = 'cover_letter')
    resignation = Context(proper_name = 'Resignation', simple_name='resignation', file_name = 'resignation')


class WorkExperience():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    company: str
    title: str
    period: str
    summary: str
    points: List[str]


class Education():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    degree: str
    field: str
    school: str
    completed: str


class ContextData():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        if kwargs.get('work_experience'):
            self.work_experience = [WorkExperience(**work_experience) for work_experience in kwargs['work_experience'].values()]
        if kwargs.get('education'):
            self.education = [Education(**education) for education in kwargs['education'].values()]
    first_name: str
    last_name: str
    email: str
    phone_number: str
    address: str
    linked_in: str
    professional_summary: str
    skills: List[str]
    work_experience: List[WorkExperience]
    education = List[Education]
    cover_letter: str
    resignation_letter: str


def create_pdf(context_data, context: Context):
    pdf = FPDF(unit=DocumentPrefs.unit, format=DocumentPrefs.format)
    pdf.add_font(DocumentPrefs.font_family, style="", fname=f'{DocumentPrefs.script_dir}/fonts/{DocumentPrefs.font_family}-Regular.ttf')
    pdf.add_font(DocumentPrefs.font_family, style="b", fname=f'{DocumentPrefs.script_dir}/fonts/{DocumentPrefs.font_family}-Bold.ttf')
    pdf.add_font(DocumentPrefs.font_family, style="i", fname=f'{DocumentPrefs.script_dir}/fonts/{DocumentPrefs.font_family}-Italic.ttf')
    pdf.add_font(DocumentPrefs.font_family, style="bi", fname=f'{DocumentPrefs.script_dir}/fonts/{DocumentPrefs.font_family}-BoldItalic.ttf')
    pdf.set_title(f'{context_data.first_name} {context_data.last_name} {context.proper_name}')
    pdf.set_margins(DocumentPrefs.margin_vertical, DocumentPrefs.margin_side)
    pdf.set_auto_page_break(True, DocumentPrefs.margin_vertical)
    pdf.add_page()
    return pdf


def save_pdf(pdf: FPDF, context_data, context: Context):
    pdf.output(f'{DocumentPrefs.script_dir}/{context_data.last_name.lower()}_{context_data.first_name.lower()}_{context.file_name}.pdf')


def parse_data(context: Context):
    file_name = sys.argv[1] if len(sys.argv) > 1 else f'{context.simple_name}.md'
    with open(file_name, 'r') as data_file:
        data =  markdown_to_json.dictify(data_file.read())
        return ContextData(**data)


def add_text_line(pdf: FPDF, text: str, size=DocumentPrefs.font_size_reg, cellSize=None, bold=False, underline=False, italic=False, br=True, align='L', width=0, font=DocumentPrefs.font_family):
    style = 'BI' if bold and italic else 'B' if bold else 'I' if italic else ''
    pdf.set_font(font, style, size)
    pdf.cell(width, cellSize if cellSize else size + DocumentPrefs.line_spacing, text, align=align, new_x=XPos.LMARGIN if br else XPos.RIGHT, new_y=YPos.NEXT if br else YPos.TOP)


def add_paragraph(pdf: FPDF, text: str):
    pdf.set_font(DocumentPrefs.font_family, '', DocumentPrefs.font_size_reg)
    pdf.multi_cell(0, DocumentPrefs.font_size_reg +DocumentPrefs.line_spacing , text, align='J', new_x='LEFT')


def add_line(pdf: FPDF):
    pdf.line(DocumentPrefs.margin_side, pdf.get_y(), pdf.w_pt - DocumentPrefs.margin_side, pdf.get_y())


def add_date_stamp(pdf: FPDF):
    pdf.set_font(DocumentPrefs.font_family, '', DocumentPrefs.font_size_reg)
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


def get_ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        return 'th'
    else:
        return ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]