from document import FPDF, DocumentPrefs, Context, Contexts, ContextData, WorkExperience
from document import create_pdf, save_pdf, parse_data, add_text_line, add_paragraph


def create_header(pdf: FPDF, resume: Context):
    title = f'{resume.first_name} {resume.last_name}'
    contact = f'{resume.address}{DocumentPrefs.separator}{resume.phone_number}{DocumentPrefs.separator}{resume.email}{DocumentPrefs.separator}{resume.linked_in}'
    add_text_line(pdf, title.upper(), DocumentPrefs.font_size_title, bold=True)
    pdf.ln(5.0)
    add_text_line(pdf, contact, DocumentPrefs.font_size_reg)
    pdf.ln(DocumentPrefs.margin_section)


def create_professional_summary(pdf: FPDF, resume: Context):
    add_section_title(pdf, 'PROFESSIONAL SUMMARY')
    add_paragraph(pdf, resume.professional_summary)
    pdf.ln(DocumentPrefs.margin_section)


def create_skills(pdf: FPDF, resume: Context):
    sectionWidth = (pdf.w - (DocumentPrefs.margin_side * 2)) / DocumentPrefs.skills_per_line
    add_section_title(pdf, 'SKILLS')
    for idx, skill in enumerate(resume.skills, start=0):
        if idx + 1 == len(resume.skills) or (idx % DocumentPrefs.skills_per_line == DocumentPrefs.skills_per_line - 1) and idx + 1 != len(resume.skills):
            add_text_line(pdf, f' • {skill}', DocumentPrefs.font_size_reg, width=sectionWidth)
        else:
            add_text_line(pdf, f' • {skill}', DocumentPrefs.font_size_reg, width=sectionWidth, br=False)
    pdf.ln(DocumentPrefs.margin_section)


def create_experience(pdf: FPDF, resume: ContextData):
    add_section_title(pdf, 'EXPERIENCE')
    for xp in resume.work_experience:
        will_xp_page_break(pdf, xp)
        pdf.set_font(DocumentPrefs.font_family, 'BI', DocumentPrefs.font_size_reg)
        add_text_line(pdf, xp.title, bold=True, italic=True, width=pdf.get_string_width(xp.title), br=False)
        add_text_line(pdf, f'{DocumentPrefs.separator}{xp.company}', width=pdf.get_string_width(xp.company), br=False)
        add_text_line(pdf, xp.period, bold=True, align='R')
        add_paragraph(pdf, xp.summary)
        for point in xp.points:
            add_text_line(pdf, f'{DocumentPrefs.separator}{point}')
        if not xp is resume.work_experience[-1]:
            pdf.ln(DocumentPrefs.font_size_reg)
    pdf.ln(DocumentPrefs.margin_section)


def create_education(pdf: FPDF, resume: ContextData):
    add_section_title(pdf, 'EDUCATION')
    for ed in resume.education:
        pdf.set_font(DocumentPrefs.font_family, 'BI', DocumentPrefs.font_size_reg)
        add_text_line(pdf, ed.degree, bold=True, italic=True, width=pdf.get_string_width(ed.degree), br=False)
        add_text_line(pdf, f'{DocumentPrefs.separator}{ed.field}', width=pdf.get_string_width(ed.field+DocumentPrefs.separator), br=False)
        add_text_line(pdf, ed.completed, bold=True, align='R')
        add_text_line(pdf, ed.school, width=pdf.get_string_width(ed.school+DocumentPrefs.separator))
        pdf.ln()


def add_section_title(pdf: FPDF, text: str):
    add_text_line(pdf, text, bold=True)


def will_xp_page_break(pdf: FPDF, xp: WorkExperience):
    pdf.set_font(DocumentPrefs.font_family, '', DocumentPrefs.font_size_reg)
    summaryHeight = pdf.get_string_width(xp.summary) / (pdf.w_pt - (DocumentPrefs.margin_side * 2)) * DocumentPrefs.font_size_reg
    bulletPointHeight = len(xp.points) * DocumentPrefs.font_size_reg
    xpHeight = summaryHeight + bulletPointHeight + (DocumentPrefs.font_size_reg * 2)
    remainingHeight = pdf.h - DocumentPrefs.margin_vertical - pdf.get_y()
    if xpHeight > remainingHeight:
        pdf.add_page()


if __name__ == '__main__':
    resume = parse_data(Contexts.resume)
    pdf = create_pdf(resume, Contexts.resume)
    create_header(pdf, resume)
    create_professional_summary(pdf, resume)
    create_skills(pdf, resume)
    create_experience(pdf, resume)
    create_education(pdf, resume)
    save_pdf(pdf, resume, Contexts.resume)