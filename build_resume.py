import os
import sys
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


def create_pdf(resume):
    pdf = FPDF('P', DocumentPrefs.unit, DocumentPrefs.page_size)
    pdf.add_font(DocumentPrefs.font_family, style="", fname=f'{DocumentPrefs.script_dir}/fonts/{DocumentPrefs.font_family}-Regular.ttf')
    pdf.add_font(DocumentPrefs.font_family, style="b", fname=f'{DocumentPrefs.script_dir}/fonts/{DocumentPrefs.font_family}-Bold.ttf')
    pdf.add_font(DocumentPrefs.font_family, style="i", fname=f'{DocumentPrefs.script_dir}/fonts/{DocumentPrefs.font_family}-Italic.ttf')
    pdf.add_font(DocumentPrefs.font_family, style="bi", fname=f'{DocumentPrefs.script_dir}/fonts/{DocumentPrefs.font_family}-BoldItalic.ttf')
    pdf.set_title(f'{resume.personal_info.first_name} {resume.personal_info.last_name} Résumé')
    pdf.set_margins(DocumentPrefs.margin_vertical, DocumentPrefs.margin_side)
    pdf.set_auto_page_break(True, DocumentPrefs.margin_vertical)
    pdf.add_page()
    return pdf


def create_header(pdf: FPDF, resume):
    title = f'{resume.personal_info.first_name} {resume.personal_info.last_name}'
    contact = f'{resume.personal_info.email}{DocumentPrefs.separator}{resume.personal_info.phone_number}'
    add_text_line(pdf, title.upper(), DocumentPrefs.font_size_title, bold=True)
    pdf.ln(5.0)
    add_text_line(pdf, contact, DocumentPrefs.font_size_reg)
    pdf.ln(DocumentPrefs.margin_section)


def create_professional_summary(pdf: FPDF, resume):
    add_section_title(pdf, 'PROFESSIONAL SUMMARY')
    add_paragraph(pdf, resume.professional_summary)
    pdf.ln(DocumentPrefs.margin_section)


def create_skills(pdf: FPDF, resume):
    skillsPerLine = 3
    sectionWidth = (pdf.w - (DocumentPrefs.margin_side * 2)) / skillsPerLine
    add_section_title(pdf, 'SKILLS')
    for idx, skill in enumerate(resume.skills, start=0):
        if idx + 1 == len(resume.skills) or (idx % skillsPerLine == skillsPerLine - 1) and idx + 1 != len(resume.skills):
            add_text_line(pdf, f' • {skill}', DocumentPrefs.font_size_reg, width=sectionWidth)
        else:
            add_text_line(pdf, f' • {skill}', DocumentPrefs.font_size_reg, width=sectionWidth, br=False)
    pdf.ln(DocumentPrefs.margin_section)


def create_experience(pdf: FPDF, resume):
    add_section_title(pdf, 'EXPERIENCE')
    for xp in resume.work_exp:
        will_xp_page_break(pdf, xp)
        pdf.set_font(DocumentPrefs.font_family, 'BI', DocumentPrefs.font_size_reg)
        add_text_line(pdf, xp.title, bold=True, italic=True, width=pdf.get_string_width(xp.title), br=False)
        add_text_line(pdf, f'{DocumentPrefs.separator}{xp.company}', width=pdf.get_string_width(xp.company), br=False)
        add_text_line(pdf, xp.period, bold=True, align='R')
        add_paragraph(pdf, xp.summary)
        for point in xp.points:
            add_text_line(pdf, f'{DocumentPrefs.separator}{point}')
        pdf.ln(DocumentPrefs.font_size_reg)
    pdf.ln(DocumentPrefs.margin_section)


def create_education(pdf: FPDF, resume):
    add_section_title(pdf, 'EDUCATION')
    for ed in resume.education:
        pdf.set_font(DocumentPrefs.font_family, 'BI', DocumentPrefs.font_size_reg)
        add_text_line(pdf, ed.degree, bold=True, italic=True, width=pdf.get_string_width(ed.degree), br=False)
        add_text_line(pdf, f'{DocumentPrefs.separator}{ed.field}', width=pdf.get_string_width(ed.field+DocumentPrefs.separator), br=False)
        add_text_line(pdf, f'{DocumentPrefs.separator}{ed.school}', width=pdf.get_string_width(ed.school+DocumentPrefs.separator), br=False)
        add_text_line(pdf, ed.completed, bold=True, align='R')


def add_section_title(pdf: FPDF, text: str):
    add_text_line(pdf, text, bold=True)


def add_paragraph(pdf: FPDF, text: str):
    pdf.set_font(DocumentPrefs.font_family, '', DocumentPrefs.font_size_reg)
    pdf.multi_cell(0, DocumentPrefs.font_size_reg +DocumentPrefs.line_spacing , text, align='J', new_x='LEFT')


def add_text_line(pdf: FPDF, text: str, size=DocumentPrefs.font_size_reg, cellSize=None, bold=False, underline=False, italic=False, br=True, align='L', width=0, font=DocumentPrefs.font_family):
    style = ''
    if bold: style += 'B'
    if underline: style += 'U'
    if italic: style += 'I'
    pdf.set_font(font, style, size)
    pdf.cell(width, cellSize if cellSize else size + DocumentPrefs.line_spacing, text, align=align, new_x=XPos.LMARGIN if br else XPos.RIGHT, new_y=YPos.NEXT if br else YPos.TOP)


def will_xp_page_break(pdf: FPDF, xp):
    pdf.set_font(DocumentPrefs.font_family, '', DocumentPrefs.font_size_reg)
    summaryHeight = pdf.get_string_width(xp.summary) / (pdf.w_pt - (DocumentPrefs.margin_side * 2)) * DocumentPrefs.font_size_reg
    bulletPointHeight = len(xp.points) * DocumentPrefs.font_size_reg
    xpHeight = summaryHeight + bulletPointHeight + (DocumentPrefs.font_size_reg * 2)
    remainingHeight = pdf.h - DocumentPrefs.margin_vertical - pdf.get_y()
    if xpHeight > remainingHeight:
        pdf.add_page()


def parse_resume():
    file_name = sys.argv[1] if len(sys.argv) > 1 else 'resume.md'
    with open(file_name, 'r') as rusume:
        data =  markdown_to_json.dictify(rusume.read())
        return SimpleNamespace(
            personal_info = SimpleNamespace(
                first_name = data['Personal Info']['First Name'],
                last_name = data['Personal Info']['Last Name'],
                email = data['Personal Info']['Email'],
                phone_number = data['Personal Info']['Phone Number'],
                address = data['Personal Info']['Address']
            ),
            professional_summary = data['Professional Summary'],
            skills = data['Skills'],
            work_exp = [SimpleNamespace(company = det['Company'], title = det['Title'], period = det['Period'], summary = det['Summary'], points = det['Points']) for det in data['Work Experience'].values()],
            education = [SimpleNamespace(degree = det['Degree'], field = det['Field'], school = det['School'], completed = det['Completed']) for det in data['Education'].values()]
        )


if __name__ == '__main__':
    resume = parse_resume()
    pdf = create_pdf(resume)
    create_header(pdf, resume)
    create_professional_summary(pdf, resume)
    create_skills(pdf, resume)
    create_experience(pdf, resume)
    create_education(pdf, resume)
    pdf.output(f'{DocumentPrefs.script_dir}/{resume.personal_info.last_name.lower()}_{resume.personal_info.first_name.lower()}_résumé.pdf')