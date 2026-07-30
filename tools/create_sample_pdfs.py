from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "downloads"
OUT.mkdir(parents=True, exist_ok=True)

INK = colors.HexColor("#152622")
ACCENT = colors.HexColor("#D96B38")
MUTED = colors.HexColor("#63716D")
PAPER = colors.HexColor("#F7F6F1")

styles = getSampleStyleSheet()
name_style = ParagraphStyle("Name", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=25, leading=28, textColor=INK, spaceAfter=4)
title_style = ParagraphStyle("Title", parent=styles["Normal"], fontName="Helvetica", fontSize=10, leading=14, textColor=ACCENT, spaceAfter=12)
section_style = ParagraphStyle("Section", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=ACCENT, spaceBefore=13, spaceAfter=6, uppercase=True)
job_style = ParagraphStyle("Job", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=INK, spaceAfter=2)
body_style = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.8, leading=13, textColor=INK, spaceAfter=4)
small_style = ParagraphStyle("Small", parent=body_style, fontSize=7.6, leading=10, textColor=MUTED)
right_style = ParagraphStyle("Right", parent=small_style, alignment=TA_RIGHT)

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D7D7D0"))
    canvas.line(0.65 * inch, 0.48 * inch, 7.85 * inch, 0.48 * inch)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.65 * inch, 0.32 * inch, "SAMPLE CONTENT - Replace with Luke F. Miller's final document")
    canvas.drawRightString(7.85 * inch, 0.32 * inch, f"Page {doc.page}")
    canvas.restoreState()

def make_resume():
    path = OUT / "luke-f-miller-sample-resume.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=LETTER, rightMargin=.65*inch, leftMargin=.65*inch, topMargin=.58*inch, bottomMargin=.62*inch,
                            title="Luke F. Miller - Sample Resume", author="Luke F. Miller")
    story = [
        Table([[Paragraph("LUKE F. MILLER", name_style), Paragraph("Honolulu, Hawai'i<br/>lukefm@hawaii.edu<br/>(412) 807-8570", right_style)]], colWidths=[4.7*inch, 2.5*inch]),
        Paragraph("RESEARCH · ANALYSIS · PUBLIC IMPACT", title_style),
        HRFlowable(width="100%", thickness=1.2, color=INK),
        Paragraph("PROFESSIONAL SUMMARY", section_style),
        Paragraph("Analyst and researcher focused on rigorous methods, reproducible data systems, and clear communication for public decision-making. This text is sample content and should be replaced with a final professional summary.", body_style),
        Paragraph("EXPERIENCE", section_style),
        Table([[Paragraph("Research & Data Analyst", job_style), Paragraph("Current", right_style)]], colWidths=[5.6*inch, 1.6*inch]),
        Paragraph("Organization name · Honolulu, Hawai'i", small_style),
        Paragraph("• Develop reproducible analytical workflows using R and public data.<br/>• Translate complex findings into clear reports and visual products.<br/>• Collaborate with technical and nontechnical partners to support decisions.", body_style),
        Spacer(1, 5),
        Table([[Paragraph("Program & Policy Analyst", job_style), Paragraph("Previous", right_style)]], colWidths=[5.6*inch, 1.6*inch]),
        Paragraph("Organization name · Location", small_style),
        Paragraph("• Conducted policy research and synthesized qualitative and quantitative evidence.<br/>• Managed project deliverables and communicated progress to stakeholders.<br/>• Improved documentation and repeatability of recurring reporting.", body_style),
        Paragraph("EDUCATION", section_style),
        Table([[Paragraph("Degree and field of study", job_style), Paragraph("Year", right_style)]], colWidths=[5.6*inch, 1.6*inch]),
        Paragraph("University name · Location", small_style),
        Paragraph("SELECTED SKILLS", section_style),
        Paragraph("<b>Analysis:</b> R, statistical analysis, data validation, reproducible research<br/><b>Communication:</b> Technical writing, visualization, presentations, stakeholder engagement<br/><b>Tools:</b> GitHub, GitHub Actions, spreadsheets, document production", body_style),
        Paragraph("PROFESSIONAL LINKS", section_style),
        Paragraph("LinkedIn: linkedin.com/in/luke-miller-283258127/ &nbsp;&nbsp; ORCID: 0009-0008-2932-1568", body_style),
    ]
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return path

def make_report():
    path = OUT / "sample-project-report.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=LETTER, rightMargin=.75*inch, leftMargin=.75*inch, topMargin=.7*inch, bottomMargin=.65*inch,
                            title="Sample Analytical Project", author="Luke F. Miller")
    story = [
        Paragraph("SAMPLE ANALYTICAL PROJECT", name_style),
        Paragraph("A placeholder report demonstrating downloadable project materials", title_style),
        HRFlowable(width="100%", thickness=1.2, color=INK),
        Spacer(1, 12),
        Paragraph("Purpose", section_style),
        Paragraph("This sample PDF confirms that project reports can be displayed and downloaded from the portfolio. Replace it with a finished report when the project library is populated.", body_style),
        Paragraph("Suggested project structure", section_style),
        Paragraph("<b>Question</b> — State the decision or research question.<br/><br/><b>Data</b> — Identify sources, dates, limitations, and update frequency.<br/><br/><b>Methods</b> — Explain processing, validation, analysis, and visualization choices.<br/><br/><b>Results</b> — Present findings in clear language, supported by tables and figures.<br/><br/><b>Reproducibility</b> — Link the code, processed data, and technical documentation.", body_style),
        Paragraph("Files this portfolio can distribute", section_style),
        Table([["Format", "Example use"], ["PDF", "Reports and publications"], ["DOCX", "Editable writing samples"], ["XLSX / CSV", "Data and calculations"], ["R / PY", "Analysis scripts"], ["ZIP", "Complete project packages"]], colWidths=[1.4*inch, 5.5*inch], style=TableStyle([
            ("BACKGROUND", (0,0), (-1,0), INK), ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
            ("FONTSIZE", (0,0), (-1,-1), 8.5), ("GRID", (0,0), (-1,-1), .5, colors.HexColor("#D7D7D0")),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, PAPER]), ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ])),
    ]
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return path

if __name__ == "__main__":
    for item in (make_resume(), make_report()):
        print(item)
