#!/usr/bin/env python3
"""
Resume Checker Report PDF Generator
 
Reads a structured JSON report and produces a professionally formatted PDF.
 
Usage:
    python generate_report_pdf.py <input_json> <output_pdf>
 
The input JSON should have this structure:
{
    "match_score": 43,
    "summary": "Your strong statistical...",
    "highlights": ["Highlight 1", "Highlight 2", "Highlight 3"],
    "improvements": ["Improvement 1", "Improvement 2", "Improvement 3"],
    "content": {
        "status": "NEEDS WORK",
        "measurable_results": {
            "count": 6,
            "items": [
                {"original": "Maintained automation scripts...", "suggestion": "Maintained 15+ automation scripts..."}
            ]
        },
        "spelling_grammar": {
            "count": 2,
            "items": [
                {"original": "some text", "issue": "description of issue", "fix": "corrected text"}
            ]
        }
    },
    "skills": {
        "status": "NEEDS WORK",
        "hard_skills": [
            {"skill": "PyTorch", "required": true, "in_jd": 1, "in_resume": 0, "matched": false}
        ],
        "soft_skills": [
            {"skill": "Collaboration", "in_jd": 1, "in_resume": 0, "matched": false}
        ],
        "suggestions": ["Suggestion 1", "Suggestion 2"]
    },
    "format": {
        "status": "PASS",
        "date_formatting": {"status": "PASS", "detail": "Consistent formatting"},
        "resume_length": {"status": "PASS", "detail": "One page, appropriate"},
        "bullet_points": {"status": "PASS", "detail": "Clear and action-verb-led"}
    },
    "sections": {
        "status": "NEEDS WORK",
        "items": [
            {"section": "Name", "present": true, "value": "John Doe"},
            {"section": "Job Title", "present": false, "value": null},
            {"section": "Phone Number", "present": true, "value": "123-456-7890"},
            {"section": "Email Address", "present": true, "value": "john@example.com"},
            {"section": "Portfolio or Website Link", "present": false, "value": null},
            {"section": "Summary", "present": true, "value": "..."},
            {"section": "Experience", "present": true, "value": "..."},
            {"section": "Education", "present": true, "value": "..."},
            {"section": "Hard Skills", "present": true, "value": "..."},
            {"section": "Soft Skills", "present": false, "value": null}
        ]
    },
    "style": {
        "status": "NEEDS WORK",
        "voice": {
            "jd_tone": ["professional", "collaborative", "innovative"],
            "findings": ["Finding 1"],
            "count": 1
        },
        "buzzwords": {
            "status": "PASS",
            "items": []
        }
    },
    "rewrites": {
        "summary": {
            "original": "Aspiring analyst...",
            "suggested": "ML engineer with..."
        },
        "bullets": [
            {"original": "Maintained automation scripts...", "suggested": "Maintained 15+ automation scripts...", "reason": "Added quantifiable metric"}
        ]
    }
}
"""
 
import json
import sys
import os
from datetime import datetime
 
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
 
 
# Color palette
GREEN = HexColor("#27ae60")
GREEN_BG = HexColor("#eafaf1")
AMBER = HexColor("#f39c12")
AMBER_BG = HexColor("#fef9e7")
RED = HexColor("#e74c3c")
RED_BG = HexColor("#fdedec")
BLUE = HexColor("#2980b9")
DARK = HexColor("#2c3e50")
LIGHT_GRAY = HexColor("#f5f5f5")
GRAY = HexColor("#95a5a6")
WHITE = HexColor("#ffffff")
 
 
def get_status_color(status):
    status = status.upper()
    if status == "PASS":
        return GREEN
    elif status == "NEEDS WORK":
        return AMBER
    elif status == "MISSING":
        return RED
    return GRAY
 
 
def get_status_bg(status):
    status = status.upper()
    if status == "PASS":
        return GREEN_BG
    elif status == "NEEDS WORK":
        return AMBER_BG
    elif status == "MISSING":
        return RED_BG
    return LIGHT_GRAY
 
 
def build_styles():
    styles = getSampleStyleSheet()
 
    styles.add(ParagraphStyle(
        name="ReportTitle",
        fontSize=22,
        leading=28,
        textColor=DARK,
        spaceAfter=6,
        fontName="Helvetica-Bold",
    ))
 
    styles.add(ParagraphStyle(
        name="ScoreDisplay",
        fontSize=36,
        leading=44,
        textColor=BLUE,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
    ))
 
    styles.add(ParagraphStyle(
        name="SectionHeader",
        fontSize=16,
        leading=22,
        textColor=DARK,
        spaceBefore=16,
        spaceAfter=8,
        fontName="Helvetica-Bold",
    ))
 
    styles.add(ParagraphStyle(
        name="SubHeader",
        fontSize=12,
        leading=16,
        textColor=DARK,
        spaceBefore=10,
        spaceAfter=4,
        fontName="Helvetica-Bold",
    ))
 
    styles.add(ParagraphStyle(
        name="BodyText2",
        fontSize=10,
        leading=14,
        textColor=DARK,
        spaceAfter=4,
    ))
 
    styles.add(ParagraphStyle(
        name="Quote",
        fontSize=9,
        leading=13,
        textColor=HexColor("#555555"),
        leftIndent=20,
        spaceAfter=2,
        fontName="Helvetica-Oblique",
    ))
 
    styles.add(ParagraphStyle(
        name="Suggestion",
        fontSize=9,
        leading=13,
        textColor=GREEN,
        leftIndent=20,
        spaceAfter=6,
    ))
 
    styles.add(ParagraphStyle(
        name="BulletItem",
        fontSize=10,
        leading=14,
        textColor=DARK,
        leftIndent=15,
        spaceAfter=3,
        bulletIndent=5,
    ))
 
    styles.add(ParagraphStyle(
        name="TableCell",
        fontSize=9,
        leading=12,
        textColor=DARK,
    ))
 
    styles.add(ParagraphStyle(
        name="TableHeader",
        fontSize=9,
        leading=12,
        textColor=WHITE,
        fontName="Helvetica-Bold",
    ))
 
    return styles
 
 
def make_status_badge(status, styles):
    color = get_status_color(status)
    return Paragraph(
        f'<font color="{color.hexval()}">[{status.upper()}]</font>',
        styles["SubHeader"]
    )
 
 
def build_overview(data, styles):
    elements = []
 
    # Title
    elements.append(Paragraph("Resume Checker Report", styles["ReportTitle"]))
    elements.append(Paragraph(
        f'<font color="{GRAY.hexval()}" size="9">Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}</font>',
        styles["BodyText2"]
    ))
    elements.append(Spacer(1, 12))
 
    # Score
    score = data.get("match_score", 0)
    score_color = GREEN if score >= 70 else AMBER if score >= 40 else RED
    elements.append(Paragraph(
        f'<font color="{DARK.hexval()}" size="12">Match Score:</font>',
        styles["BodyText2"]
    ))
    elements.append(Paragraph(
        f'<font color="{score_color.hexval()}">{score}</font><font color="{GRAY.hexval()}" size="18"> / 100</font>',
        styles["ScoreDisplay"]
    ))
    elements.append(Spacer(1, 8))
 
    # Summary
    elements.append(Paragraph(data.get("summary", ""), styles["BodyText2"]))
    elements.append(Spacer(1, 10))
 
    # Highlights
    highlights = data.get("highlights", [])
    if highlights:
        elements.append(Paragraph("Highlights", styles["SubHeader"]))
        for h in highlights:
            elements.append(Paragraph(
                f'<font color="{GREEN.hexval()}">&#x2714;</font> {h}',
                styles["BulletItem"]
            ))
        elements.append(Spacer(1, 6))
 
    # Improvements
    improvements = data.get("improvements", [])
    if improvements:
        elements.append(Paragraph("Key Improvements", styles["SubHeader"]))
        for imp in improvements:
            elements.append(Paragraph(
                f'<font color="{RED.hexval()}">&#x2716;</font> {imp}',
                styles["BulletItem"]
            ))
 
    elements.append(Spacer(1, 6))
    elements.append(HRFlowable(width="100%", color=LIGHT_GRAY, thickness=1))
    return elements
 
 
def build_content_section(data, styles):
    elements = []
    content = data.get("content", {})
    status = content.get("status", "PASS")
 
    elements.append(Paragraph("1. Content", styles["SectionHeader"]))
    elements.append(make_status_badge(status, styles))
 
    # Measurable Results
    mr = content.get("measurable_results", {})
    count = mr.get("count", 0)
    elements.append(Paragraph("Measurable Results", styles["SubHeader"]))
    if count > 0:
        elements.append(Paragraph(
            f'<font color="{AMBER.hexval()}">!</font> {count} bullet point(s) lack quantifiable impact.',
            styles["BodyText2"]
        ))
        for item in mr.get("items", []):
            elements.append(Paragraph(f'"{item["original"]}"', styles["Quote"]))
            if item.get("suggestion"):
                elements.append(Paragraph(f'&#x2192; {item["suggestion"]}', styles["Suggestion"]))
    else:
        elements.append(Paragraph(
            f'<font color="{GREEN.hexval()}">&#x2714;</font> All bullet points include measurable results.',
            styles["BodyText2"]
        ))
 
    # Spelling & Grammar
    sg = content.get("spelling_grammar", {})
    sg_count = sg.get("count", 0)
    elements.append(Paragraph("Spelling &amp; Grammar", styles["SubHeader"]))
    if sg_count > 0:
        elements.append(Paragraph(
            f'<font color="{AMBER.hexval()}">!</font> {sg_count} issue(s) found.',
            styles["BodyText2"]
        ))
        for item in sg.get("items", []):
            elements.append(Paragraph(f'"{item["original"]}"', styles["Quote"]))
            elements.append(Paragraph(
                f'&#x2192; {item.get("issue", "")} Fix: {item.get("fix", "")}',
                styles["Suggestion"]
            ))
    else:
        elements.append(Paragraph(
            f'<font color="{GREEN.hexval()}">&#x2714;</font> No spelling or grammar issues found.',
            styles["BodyText2"]
        ))
 
    elements.append(Spacer(1, 6))
    elements.append(HRFlowable(width="100%", color=LIGHT_GRAY, thickness=1))
    return elements
 
 
def build_skills_section(data, styles):
    elements = []
    skills = data.get("skills", {})
    status = skills.get("status", "PASS")
 
    elements.append(Paragraph("2. Skills", styles["SectionHeader"]))
    elements.append(make_status_badge(status, styles))
 
    # Hard Skills table
    hard = skills.get("hard_skills", [])
    if hard:
        elements.append(Paragraph("Hard Skills", styles["SubHeader"]))
 
        header = [
            Paragraph("", styles["TableHeader"]),
            Paragraph("Skill", styles["TableHeader"]),
            Paragraph("Required/Preferred", styles["TableHeader"]),
            Paragraph("In JD", styles["TableHeader"]),
            Paragraph("In Resume", styles["TableHeader"]),
        ]
        rows = [header]
        for s in hard:
            icon = f'<font color="{GREEN.hexval()}">&#x2714;</font>' if s["matched"] else f'<font color="{RED.hexval()}">&#x2716;</font>'
            req = "Required" if s.get("required") else "Preferred"
            rows.append([
                Paragraph(icon, styles["TableCell"]),
                Paragraph(f'<b>{s["skill"]}</b> <font color="{GRAY.hexval()}" size="7">({req.lower()})</font>', styles["TableCell"]),
                Paragraph(req, styles["TableCell"]),
                Paragraph(str(s.get("in_jd", 1)), styles["TableCell"]),
                Paragraph(str(s.get("in_resume", 0)), styles["TableCell"]),
            ])
 
        t = Table(rows, colWidths=[0.3*inch, 2.5*inch, 1.2*inch, 0.8*inch, 0.8*inch])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), DARK),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
            ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#dddddd")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 8))
 
    # Soft Skills table
    soft = skills.get("soft_skills", [])
    if soft:
        elements.append(Paragraph("Soft Skills", styles["SubHeader"]))
        header = [
            Paragraph("", styles["TableHeader"]),
            Paragraph("Skill", styles["TableHeader"]),
            Paragraph("In JD", styles["TableHeader"]),
            Paragraph("In Resume", styles["TableHeader"]),
        ]
        rows = [header]
        for s in soft:
            icon = f'<font color="{GREEN.hexval()}">&#x2714;</font>' if s["matched"] else f'<font color="{RED.hexval()}">&#x2716;</font>'
            rows.append([
                Paragraph(icon, styles["TableCell"]),
                Paragraph(f'<b>{s["skill"]}</b>', styles["TableCell"]),
                Paragraph(str(s.get("in_jd", 1)), styles["TableCell"]),
                Paragraph(str(s.get("in_resume", 0)), styles["TableCell"]),
            ])
        t = Table(rows, colWidths=[0.3*inch, 3.0*inch, 0.8*inch, 0.8*inch])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), DARK),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
            ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#dddddd")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 8))
 
    # Suggestions
    for sug in skills.get("suggestions", []):
        elements.append(Paragraph(f'&#x2192; {sug}', styles["Suggestion"]))
 
    elements.append(Spacer(1, 6))
    elements.append(HRFlowable(width="100%", color=LIGHT_GRAY, thickness=1))
    return elements
 
 
def build_format_section(data, styles):
    elements = []
    fmt = data.get("format", {})
    status = fmt.get("status", "PASS")
 
    elements.append(Paragraph("3. Format", styles["SectionHeader"]))
    elements.append(make_status_badge(status, styles))
 
    for key, label in [("date_formatting", "Date Formatting"), ("resume_length", "Resume Length"), ("bullet_points", "Bullet Points")]:
        item = fmt.get(key, {})
        s = item.get("status", "PASS")
        color = get_status_color(s)
        elements.append(Paragraph(
            f'<font color="{color.hexval()}">{"&#x2714;" if s == "PASS" else "&#x2716;"}</font> <b>{label}:</b> {item.get("detail", "")}',
            styles["BodyText2"]
        ))
 
    elements.append(Spacer(1, 6))
    elements.append(HRFlowable(width="100%", color=LIGHT_GRAY, thickness=1))
    return elements
 
 
def build_sections_section(data, styles):
    elements = []
    sec = data.get("sections", {})
    status = sec.get("status", "PASS")
 
    elements.append(Paragraph("4. Sections", styles["SectionHeader"]))
    elements.append(make_status_badge(status, styles))
 
    for item in sec.get("items", []):
        present = item.get("present", False)
        icon = f'<font color="{GREEN.hexval()}">&#x2714;</font>' if present else f'<font color="{RED.hexval()}">&#x2716;</font>'
        value_str = ""
        if item.get("value"):
            val = str(item["value"])
            if len(val) > 80:
                val = val[:77] + "..."
            value_str = f' - <font color="{GRAY.hexval()}" size="8">{val}</font>'
        elements.append(Paragraph(
            f'{icon} <b>{item["section"]}</b>{value_str}',
            styles["BulletItem"]
        ))
 
    elements.append(Spacer(1, 6))
    elements.append(HRFlowable(width="100%", color=LIGHT_GRAY, thickness=1))
    return elements
 
 
def build_style_section(data, styles):
    elements = []
    style = data.get("style", {})
    status = style.get("status", "PASS")
 
    elements.append(Paragraph("5. Style", styles["SectionHeader"]))
    elements.append(make_status_badge(status, styles))
 
    # Voice
    voice = style.get("voice", {})
    elements.append(Paragraph("Voice", styles["SubHeader"]))
    tones = voice.get("jd_tone", [])
    if tones:
        tone_tags = " ".join([f'<font color="{BLUE.hexval()}">#{t}</font>' for t in tones])
        elements.append(Paragraph(f'JD tone: {tone_tags}', styles["BodyText2"]))
    for finding in voice.get("findings", []):
        elements.append(Paragraph(f'&#x2192; {finding}', styles["Suggestion"]))
 
    # Buzzwords
    bw = style.get("buzzwords", {})
    elements.append(Paragraph("Buzzwords &amp; Cliches", styles["SubHeader"]))
    if bw.get("status") == "PASS":
        elements.append(Paragraph(
            f'<font color="{GREEN.hexval()}">&#x2714;</font> Your resume is free from generic buzzwords and cliches.',
            styles["BodyText2"]
        ))
    else:
        for item in bw.get("items", []):
            elements.append(Paragraph(f'&#x2716; "{item}"', styles["Quote"]))
 
    elements.append(Spacer(1, 6))
    elements.append(HRFlowable(width="100%", color=LIGHT_GRAY, thickness=1))
    return elements
 
 
def build_rewrites_section(data, styles):
    elements = []
    rewrites = data.get("rewrites", {})
 
    elements.append(Paragraph("Rewrite Suggestions", styles["SectionHeader"]))
 
    # Summary rewrite
    summary = rewrites.get("summary", {})
    if summary:
        elements.append(Paragraph("Summary / Objective", styles["SubHeader"]))
        elements.append(Paragraph(f'<b>Original:</b> {summary.get("original", "")}', styles["BodyText2"]))
        elements.append(Paragraph(
            f'<b>Suggested:</b> <font color="{GREEN.hexval()}">{summary.get("suggested", "")}</font>',
            styles["BodyText2"]
        ))
        elements.append(Spacer(1, 8))
 
    # Bullet rewrites
    bullets = rewrites.get("bullets", [])
    if bullets:
        elements.append(Paragraph("Bullet Point Rewrites", styles["SubHeader"]))
 
        header = [
            Paragraph("#", styles["TableHeader"]),
            Paragraph("Original", styles["TableHeader"]),
            Paragraph("Suggested Rewrite", styles["TableHeader"]),
            Paragraph("Why", styles["TableHeader"]),
        ]
        rows = [header]
        for i, b in enumerate(bullets, 1):
            rows.append([
                Paragraph(str(i), styles["TableCell"]),
                Paragraph(b.get("original", ""), styles["TableCell"]),
                Paragraph(b.get("suggested", ""), styles["TableCell"]),
                Paragraph(b.get("reason", ""), styles["TableCell"]),
            ])
 
        t = Table(rows, colWidths=[0.3*inch, 2.0*inch, 2.3*inch, 1.5*inch])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), DARK),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
            ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#dddddd")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(t)
 
    return elements
 
 
def generate_pdf(input_json_path, output_pdf_path):
    with open(input_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
 
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
    )
 
    styles = build_styles()
    elements = []
 
    elements.extend(build_overview(data, styles))
    elements.extend(build_content_section(data, styles))
    elements.extend(build_skills_section(data, styles))
    elements.extend(build_format_section(data, styles))
    elements.extend(build_sections_section(data, styles))
    elements.extend(build_style_section(data, styles))
    elements.extend(build_rewrites_section(data, styles))
 
    doc.build(elements)
    print(f"PDF report generated: {output_pdf_path}")
 
 
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_report_pdf.py <input.json> <output.pdf>")
        sys.exit(1)
 
    generate_pdf(sys.argv[1], sys.argv[2])
