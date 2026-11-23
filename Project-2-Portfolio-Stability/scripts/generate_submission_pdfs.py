"""Generate static PDF submission companions from validated Project 2 evidence."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS = PROJECT_ROOT / "docs"


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("Title", parent=base["Title"], fontName="Helvetica-Bold", fontSize=14, leading=16, alignment=TA_CENTER, spaceAfter=6),
        "subtitle": ParagraphStyle("Subtitle", parent=base["Normal"], fontName="Helvetica", fontSize=8, leading=10, alignment=TA_CENTER, spaceAfter=8),
        "heading": ParagraphStyle("Heading", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=9, leading=11, spaceBefore=5, spaceAfter=2),
        "body": ParagraphStyle("Body", parent=base["BodyText"], fontName="Helvetica", fontSize=7.4, leading=9.1, spaceAfter=3),
        "small": ParagraphStyle("Small", parent=base["BodyText"], fontName="Helvetica", fontSize=6.8, leading=8.1, spaceAfter=2),
    }


def footer(canvas, document) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.drawString(0.5 * inch, 0.35 * inch, "FIN 439 Project 2 - Meridian Foundation Reserve - Educational coursework only")
    canvas.drawRightString(8.0 * inch, 0.35 * inch, f"Page {document.page}")
    canvas.restoreState()


def add_table(story, rows, widths, style_map) -> None:
    table = Table(rows, colWidths=widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 6.4),
                ("LEADING", (0, 0), (-1, -1), 7.5),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#B7C9D6")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 4))


def p(text: str, style: str, style_map) -> Paragraph:
    return Paragraph(text, style_map[style])


def build_decision_memo() -> None:
    style_map = styles()
    output = DOCS / "Decision-Memo.pdf"
    document = SimpleDocTemplate(str(output), pagesize=letter, leftMargin=0.45 * inch, rightMargin=0.45 * inch, topMargin=0.42 * inch, bottomMargin=0.52 * inch)
    story = [
        p("Meridian Foundation Reserve - Committee Decision Memo", "title", style_map),
        p("FIN 439 Project 2 | 2026-11-23 | Educational coursework, not investment advice", "subtitle", style_map),
        p("AI use: OpenAI Codex assisted with planning, code structure, testing, documentation formatting, and app development. Student ownership: the analysis and decision are the student's own; this is educational coursework, not personalized investment advice.", "body", style_map),
        p("Recommendation", "heading", style_map),
        p("<b>REJECT live allocation or process deployment now; allocation range 0%.</b> This rejects capital deployment, not further research. A future conditional 0%-5% pilot is a student-proposed discussion range only after evidence gates close, committee definitions are approved, and a fresh cold run passes.", "body", style_map),
        p("Mandate and data boundary", "heading", style_map),
        p("Fictional Meridian has a seven-year horizon, annual rebalance, CPI + 4% net rolling-five-year objective, BIL/IEF/LQD/VT implementation universe, and 60% VT / 40% LQD benchmark. Approved input is 60 completed Yahoo adjusted-close source labels from 2021-10-01 to 2026-09-01 (59 returns). The preserved legacy price file is quarantined because it carried an incomplete October 2026 observation. Labels are not guaranteed executable prices; results are gross historical analytics.", "body", style_map),
        p("Three-portfolio comparison", "heading", style_map),
    ]
    rows = [
        ["Portfolio", "Allocation", "Gross ann. return", "Ann. vol.", "Max DD", "Turnover", "Status"],
        ["Equal weight", "25% each", "2.87%", "7.52%", "-15.49%", "50.00%", "FAIL turnover"],
        ["60/40 benchmark", "0/0/40/60", "5.73%", "12.35%", "-23.81%", "3.31%", "Not decision-ready"],
        ["Constrained", "25/0/40/35", "4.23%", "8.70%", "-17.31%", "25.00%", "Not decision-ready"],
    ]
    add_table(story, rows, [1.0 * inch, 0.85 * inch, 0.8 * inch, 0.6 * inch, 0.6 * inch, 0.6 * inch, 1.1 * inch], style_map)
    story += [
        p("Equal weight is a required baseline but is infeasible under the 25% initial hypothetical turnover cap. The constrained allocation minimizes realized annual-rebalance-path volatility only among feasible 5% grid candidates; it is not a recommendation.", "body", style_map),
        p("Stress and locked evidence", "heading", style_map),
        p("The committed-before-run locked window test changed 59 returns to 36. Predicted constrained volatility was 8.15%; actual was 6.703604%, -1.446396 percentage points from prediction and -2.000461 from the 59-return baseline. Allocation remained 25% BIL / 0% IEF / 40% LQD / 35% VT, and no modeled turnover event exceeded 25%. Independent sample-volatility arithmetic matched the emitted return path.", "body", style_map),
        p("Non-locked -10 bps monthly return, 1.25x risk, 25 bps hypothetical cost, 20% turnover, and 10% BIL scenario cases all returned STOP_UNVERIFIED_MANDATE_EVIDENCE. The 20% turnover case selected 20% BIL / 0% IEF / 40% LQD / 40% VT. The 10% BIL scenario did not bind because base BIL is 25%. Hypothetical costs are not sourced costs.", "body", style_map),
        p("Evidence gates, monitoring, and committee ask", "heading", style_map),
        p("Do not allocate until CPI release/vintage and net-cost methodology, dated trading costs, reserve eligibility, redemption definition, issuer look-through, calendar-loss definition, and ALFRED signal rule are evidenced and approved. Stop on data-integrity failure, infeasibility, missing required evidence, or a verified hard-rule breach. For any future approved pilot, pause/unwind on a verified hard-rule breach, turnover cap breach without approval, or approved loss/signal trigger. <b>Committee ask: approve no live allocation and authorize only evidence collection and governance-definition work.</b>", "body", style_map),
    ]
    document.build(story, onFirstPage=footer, onLaterPages=footer)


def build_validation_record() -> None:
    style_map = styles()
    output = DOCS / "Validation-and-AI-Use.pdf"
    document = SimpleDocTemplate(str(output), pagesize=letter, leftMargin=0.5 * inch, rightMargin=0.5 * inch, topMargin=0.48 * inch, bottomMargin=0.52 * inch)
    story = [
        p("Meridian Foundation Reserve - Validation and AI Use", "title", style_map),
        p("FIN 439 Project 2 | 2026-11-23 | Educational coursework, not investment advice", "subtitle", style_map),
        p("AI use: OpenAI Codex (model/version not exposed in the workspace interface) assisted on 2026-11-23 with planning, code structure, testing, documentation formatting, debugging, and Streamlit implementation. Student ownership: the analysis and decision are the student's own; this is educational coursework, not personalized investment advice.", "body", style_map),
        p("Sources, as-of boundary, and known-answer checks", "heading", style_map),
        p("Approved prices span 2021-10-01 through 2026-09-01. The October 2026 retrieval-month defect was quarantined after raw-to-lineage checks. Tests cover parsing, completed-month selection, lineage, numerical integrity, deterministic output, portfolio known answers, turnover/drift, infeasibility, CPI publication cutoffs, signal-vintage cutoffs, and cost-evidence gates. Results remain gross adjusted-close analytics, not executable-price or net-return claims.", "body", style_map),
        p("Manual Streamlit checks and corrections", "heading", style_map),
        p("The Reset to base control initially raised a Streamlit state exception after checkbox instantiation; it was corrected with a pre-widget on_click callback and tested through enable-reset-enable interaction. Relative documentation links did not load local Markdown; they were replaced with an in-app trusted-document viewer and rendered-heading regression test. The app also has a tested on-demand non-locked stress panel.", "body", style_map),
        p("Locked Changed-Input Record", "heading", style_map),
    ]
    rows = [
        ["Item", "Record"],
        ["Prediction commit", "0f1c1da43b7958be8ae82e8e5b3f8b2712aebdbc on origin/main"],
        ["AI-off prediction", "8.15% annualized sample volatility; 59 returns to 36 returns"],
        ["Execution", "Retry at 2026-11-23T13:22:22-05:00 after PATH failure documented before calculation"],
        ["Actual", "6.703604%; -1.446396 percentage points from prediction"],
        ["Independent check", "Sample formula on 36 emitted returns: 0.067036042519"],
        ["Decision effect", "Lower observed history did not close evidence gates; 0% live allocation remains."],
    ]
    add_table(story, rows, [1.35 * inch, 6.1 * inch], style_map)
    story += [
        p("Stress, limitations, and remaining work", "heading", style_map),
        p("One-input window, return, risk, hypothetical-cost, turnover, and BIL scenario tests are implemented. All approved-data stress cases returned STOP_UNVERIFIED_MANDATE_EVIDENCE. Hypothetical costs are not sourced. CPI release/vintage evidence, ALFRED vintages/action rule, reserve and redemption evidence, issuer look-through, calendar-loss definition, and dated transaction costs remain unresolved. A clean clone passed the pipeline, 42 tests, and headless app check. Videos, transcripts, Brightspace attachments, and final access checks remain student tasks.", "body", style_map),
        p("Test result", "heading", style_map),
        p("The latest full regression suite reported 42 passed, 0 failed, 0 errors. Streamlit's bare-mode test warning did not produce a page exception. See the repository Markdown validation record for full methodology and evidence paths.", "body", style_map),
    ]
    document.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build_decision_memo()
    build_validation_record()
