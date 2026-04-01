from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    HRFlowable, Table, TableStyle
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import io
from datetime import datetime


BRAND_DARK  = colors.HexColor("#0f3460")
BRAND_MID   = colors.HexColor("#1D9E75")
GRAY_LIGHT  = colors.HexColor("#f8fafc")
GRAY_BORDER = colors.HexColor("#e2e8f0")
TEXT_MUTED  = colors.HexColor("#718096")
TEXT_DARK   = colors.HexColor("#1a1a2e")
WARNING_BG  = colors.HexColor("#FAEEDA")
WARNING_FG  = colors.HexColor("#854F0B")


def build_pdf(visit_data: dict) -> bytes:
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm,
    )

    styles = getSampleStyleSheet()

    heading1 = ParagraphStyle(
        "heading1",
        fontSize=18,
        fontName="Helvetica-Bold",
        textColor=BRAND_DARK,
        spaceAfter=4,
    )
    heading2 = ParagraphStyle(
        "heading2",
        fontSize=11,
        fontName="Helvetica-Bold",
        textColor=BRAND_DARK,
        spaceBefore=12,
        spaceAfter=4,
    )
    body = ParagraphStyle(
        "body",
        fontSize=10,
        fontName="Helvetica",
        textColor=TEXT_DARK,
        leading=16,
        spaceAfter=4,
    )
    muted = ParagraphStyle(
        "muted",
        fontSize=9,
        fontName="Helvetica",
        textColor=TEXT_MUTED,
        spaceAfter=2,
    )
    disclaimer = ParagraphStyle(
        "disclaimer",
        fontSize=8,
        fontName="Helvetica-Oblique",
        textColor=TEXT_MUTED,
        alignment=TA_CENTER,
        spaceBefore=8,
    )

    story = []

    story.append(Paragraph("Marz", heading1))
    story.append(Paragraph(
        "Edge AI Clinical Intelligence System", muted
    ))
    story.append(Spacer(1, 4*mm))
    story.append(HRFlowable(
        width="100%", thickness=2,
        color=BRAND_DARK, spaceAfter=6
    ))

    now = datetime.now().strftime("%d %B %Y, %H:%M")
    meta_data = [
        ["Report generated", now],
        ["Visit ID", f"#{visit_data.get('visit_id', '—')}"],
    ]
    meta_table = Table(meta_data, colWidths=[45*mm, 120*mm])
    meta_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (0, -1), TEXT_MUTED),
        ("TEXTCOLOR", (1, 0), (1, -1), TEXT_DARK),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6*mm))

    story.append(Paragraph("Patient information", heading2))
    story.append(HRFlowable(
        width="100%", thickness=0.5,
        color=GRAY_BORDER, spaceAfter=4
    ))

    patient_data = [
        ["Name", visit_data.get("patient_name", "—")],
        ["Age",  str(visit_data.get("age", "—")) + " years"],
        ["Gender", visit_data.get("gender", "Not recorded")],
    ]
    patient_table = Table(patient_data, colWidths=[45*mm, 120*mm])
    patient_table.setStyle(TableStyle([
        ("FONTNAME",    (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE",    (0, 0), (-1, -1), 10),
        ("TEXTCOLOR",   (0, 0), (0, -1),  TEXT_MUTED),
        ("TEXTCOLOR",   (1, 0), (1, -1),  TEXT_DARK),
        ("FONTNAME",    (1, 0), (1, 0),   "Helvetica-Bold"),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("ROWBACKGROUNDS", (0,0), (-1,-1),
         [GRAY_LIGHT, colors.white]),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("Clinical details", heading2))
    story.append(HRFlowable(
        width="100%", thickness=0.5,
        color=GRAY_BORDER, spaceAfter=4
    ))

    def field_block(label, value):
        story.append(Paragraph(label, muted))
        story.append(Paragraph(value or "Not provided", body))
        story.append(Spacer(1, 2*mm))

    field_block("Symptoms",            visit_data.get("symptoms"))
    field_block("Doctor observations", visit_data.get("observations"))
    field_block("Lab results",         visit_data.get("lab_results"))

    story.append(Paragraph("AI-generated diagnosis report", heading2))
    story.append(HRFlowable(
        width="100%", thickness=0.5,
        color=BRAND_MID, spaceAfter=4
    ))

    diagnosis = visit_data.get("diagnosis", "No diagnosis generated.")
    for line in diagnosis.split("\n"):
        line = line.strip()
        if not line:
            story.append(Spacer(1, 2*mm))
            continue
        if line.startswith("**") and line.endswith("**"):
            story.append(Paragraph(
                line.replace("**", ""),
                ParagraphStyle(
                    "bold_line",
                    fontSize=10,
                    fontName="Helvetica-Bold",
                    textColor=BRAND_DARK,
                    spaceAfter=2,
                )
            ))
        elif line.startswith("* ") or line.startswith("- "):
            story.append(Paragraph(
                "• " + line[2:], body
            ))
        else:
            story.append(Paragraph(line, body))

    outcome = visit_data.get("outcome")
    if outcome and outcome.get("treatment_success"):
        story.append(Spacer(1, 5*mm))
        story.append(Paragraph("Treatment outcome", heading2))
        story.append(HRFlowable(
            width="100%", thickness=0.5,
            color=GRAY_BORDER, spaceAfter=4
        ))

        outcome_colors = {
            "success": colors.HexColor("#1D9E75"),
            "partial": colors.HexColor("#EF9F27"),
            "failed":  colors.HexColor("#E24B4A"),
        }
        oc = outcome["treatment_success"]
        oc_color = outcome_colors.get(oc, TEXT_MUTED)

        outcome_table = Table(
            [["Outcome", oc.capitalize()],
             ["Notes",   outcome.get("recovery_notes") or "—"]],
            colWidths=[45*mm, 120*mm]
        )
        outcome_table.setStyle(TableStyle([
            ("FONTNAME",  (0,0), (-1,-1), "Helvetica"),
            ("FONTSIZE",  (0,0), (-1,-1), 10),
            ("TEXTCOLOR", (0,0), (0,-1),  TEXT_MUTED),
            ("TEXTCOLOR", (1,0), (1,0),   oc_color),
            ("FONTNAME",  (1,0), (1,0),   "Helvetica-Bold"),
            ("TEXTCOLOR", (1,1), (1,1),   TEXT_DARK),
            ("BOTTOMPADDING", (0,0), (-1,-1), 4),
            ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ]))
        story.append(outcome_table)

    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(
        width="100%", thickness=0.5,
        color=GRAY_BORDER, spaceAfter=4
    ))
    story.append(Paragraph(
        "This report was generated by Marz, an AI clinical decision support "
        "system. It is intended to assist qualified healthcare professionals "
        "and does not replace clinical judgement. Always verify AI-generated "
        "content before acting on it.",
        disclaimer
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()