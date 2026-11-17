from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.graphics.shapes import Drawing, Circle, Line, String
from reportlab.graphics import renderPDF
from xml.sax.saxutils import escape


def generate_pdf_report(
    file_path,
    case,
    transactions,
    chains,
    high_value_transactions,
    risk_score,
    risk_level
):

    document = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    story = []

    # -----------------------------
    # Title
    # -----------------------------

    story.append(
        Paragraph(
            "CYBERCORE FORENSIC INVESTIGATION REPORT",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    # -----------------------------
    # Case Information
    # -----------------------------

    story.append(
        Paragraph(
            "1. Case Information",
            styles["Heading2"]
        )
    )

    case_data = [
        ["Case ID", str(case.id)],
        ["Case Name", case.name],
        ["Risk Score", f"{risk_score}/10"],
        ["Risk Level", risk_level],
    ]

    case_table = Table(
        case_data,
        colWidths=[1.5 * inch, 4.5 * inch]
    )

    case_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ])
    )

    story.append(case_table)

    story.append(Spacer(1, 20))

    # -----------------------------
    # Investigation Summary
    # -----------------------------

    story.append(
        Paragraph(
            "2. Investigation Summary",
            styles["Heading2"]
        )
    )

    summary_text = (
        f"The investigation contains "
        f"{len(transactions)} transaction(s), "
        f"{len(chains)} transaction chain(s), and "
        f"{len(high_value_transactions)} high-value "
        f"transaction(s). The deterministic forensic engine "
        f"assigned a risk score of {risk_score}/10, classified "
        f"as {risk_level}."
    )

    story.append(
        Paragraph(
            summary_text,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 15))

    # -----------------------------
    # Transactions
    # -----------------------------

    story.append(
        Paragraph(
            "3. Transactions",
            styles["Heading2"]
        )
    )

    transaction_data = [
        [
            "ID",
            "Sender",
            "Receiver",
            "Amount",
            "Timestamp"
        ]
    ]

    for transaction in transactions:

        transaction_data.append([
            transaction.transaction_id,
            transaction.sender,
            transaction.receiver,
            str(transaction.amount),
            str(transaction.timestamp)
        ])

    transaction_table = Table(
        transaction_data,
        repeatRows=1
    )

    transaction_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ])
    )

    story.append(transaction_table)

    story.append(Spacer(1, 20))

    # -----------------------------
    # Transaction Chains
    # -----------------------------

    story.append(
        Paragraph(
            "4. Transaction Chains",
            styles["Heading2"]
        )
    )

    if chains:

        for index, chain in enumerate(chains, start=1):

            chain_text = (
                f"Chain {index}: "
                + " -> ".join(chain["path"])
                + f" (within {chain['duration_hours']}h)"
            )

            story.append(
                Paragraph(
                    chain_text,
                    styles["BodyText"]
                )
            )

            story.append(Spacer(1, 5))

    else:

        story.append(
            Paragraph(
                "No transaction chains detected.",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 20))

    # -----------------------------
    # High Value Transactions
    # -----------------------------

    story.append(
        Paragraph(
            "5. High-Value Transactions",
            styles["Heading2"]
        )
    )

    if high_value_transactions:

        high_value_data = [
            [
                "Transaction ID",
                "Sender",
                "Receiver",
                "Amount"
            ]
        ]

        for item in high_value_transactions:

            high_value_data.append([
                item.transaction_id,
                item.sender,
                item.receiver,
                str(item.amount)
            ])

        high_value_table = Table(
            high_value_data,
            repeatRows=1
        )

        high_value_table.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
            ])
        )

        story.append(high_value_table)

    else:

        story.append(
            Paragraph(
                "No high-value transactions detected.",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 20))

    # -----------------------------
    # Risk Assessment
    # -----------------------------

    story.append(
        Paragraph(
            "6. Risk Assessment",
            styles["Heading2"]
        )
    )

    risk_text = (
        f"Final Risk Score: {risk_score}/10<br/>"
        f"Risk Classification: {risk_level}"
    )

    story.append(
        Paragraph(
            risk_text,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 15))

    # -----------------------------
    # Final Assessment
    # -----------------------------

    story.append(
        Paragraph(
            "7. Final Assessment",
            styles["Heading2"]
        )
    )

    final_text = (
        "This report summarizes findings generated by the "
        "CyberCore deterministic forensic analysis engine. "
        "The identified patterns should be treated as "
        "investigation indicators and not as conclusive "
        "proof of fraudulent activity."
    )

    story.append(
        Paragraph(
            final_text,
            styles["BodyText"]
        )
    )

    document.build(story)


def generate_complete_pdf_report(file_path, report):
    document = SimpleDocTemplate(file_path, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    styles["BodyText"].leading = 13

    def paragraph(value):
        return Paragraph(escape(str(value)).replace("\n", "<br/>") , styles["BodyText"])

    def table(rows, widths=None):
        result = Table(rows, colWidths=widths, repeatRows=1)
        result.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#8b9aaa")),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dce7f0")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#102b46")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6)
        ]))
        return result

    case = report["case"]
    summary = report["summary"]
    evidence = report.get("evidence", [])
    findings = report.get("findings", [])
    timeline = report.get("timeline", [])
    entities = report.get("entities", [])
    graph = report.get("unified_graph", {})
    story = [
        Paragraph("CYBERCORE FORENSIC INVESTIGATION REPORT", styles["Title"]),
        paragraph(f"Human-readable report for {case['case_number']}"),
        Spacer(1, 12),
        Paragraph("1. Case Identification", styles["Heading2"]),
        table([
            ["Field", "Value"],
            ["Case number", case["case_number"]],
            ["Case name", case["name"]],
            ["Status", case["status"]],
            ["Created", case["created_at"]],
            ["Risk", f"{summary['risk_score']}/10 ({summary['risk_level']})"]
        ], [1.5 * inch, 4.8 * inch]),
        Spacer(1, 12),
        Paragraph("2. Investigation Summary", styles["Heading2"]),
        paragraph(
            f"The investigation contains {len(evidence)} evidence item(s), "
            f"{summary['total_entities']} entity/entities, "
            f"{summary['total_connections']} graph connection(s), "
            f"{len(timeline)} timeline event(s), and {len(findings)} finding(s)."
        ),
        Spacer(1, 10),
        Paragraph("3. Related Evidence", styles["Heading2"]),
        table(
            [["Type", "File", "SHA-256"]] + [
                [item.get("kind", "evidence"), item.get("filename", ""), item.get("sha256", "")]
                for item in evidence
            ] or [["-", "No evidence recorded", "-"]],
            [1.2 * inch, 2.2 * inch, 2.9 * inch]
        ),
        Spacer(1, 12),
        Paragraph("4. Findings", styles["Heading2"]),
        table(
            [["Type", "Severity", "Explanation"]] + [
                [item.get("type", ""), item.get("severity", ""), item.get("description", "")]
                for item in findings
            ] or [["-", "-", "No findings recorded"]],
            [1.5 * inch, 1.0 * inch, 3.8 * inch]
        ),
        Spacer(1, 12),
        Paragraph("5. Investigation Timeline", styles["Heading2"]),
        table(
            [["Timestamp", "Type", "Event", "Reference"]] + [
                [item.get("timestamp", ""), item.get("type", ""), item.get("description", ""), item.get("reference", "")]
                for item in timeline
            ] or [["-", "-", "No timeline events recorded", "-"]],
            [1.25 * inch, .8 * inch, 3.45 * inch, .8 * inch]
        ),
        Spacer(1, 12),
        Paragraph("6. Entities", styles["Heading2"]),
        table([["Entity", "Role"]] + [[node.get("id", ""), "Connected investigation entity"] for node in entities] or [["-", "No entities recorded"]], [2.5 * inch, 3.8 * inch]),
        Spacer(1, 12),
        Paragraph("7. Unified Evidence Graph", styles["Heading2"]),
        paragraph("The graph below connects entities discovered across financial, device, email, and other related evidence."),
        _build_graph_drawing(graph),
        Spacer(1, 12),
        Paragraph("8. Assessment", styles["Heading2"]),
        paragraph(
            f"The final deterministic risk assessment is {summary['risk_score']}/10, "
            f"classified as {summary['risk_level']}. Findings are investigation indicators "
            "and should be reviewed alongside the original evidence."
        )
    ]
    document.build(story)


def _build_graph_drawing(graph):
    width, height = 500, 260
    drawing = Drawing(width, height)
    nodes = graph.get("nodes", [])[:24]
    edges = graph.get("edges", [])
    if not nodes:
        drawing.add(String(10, height / 2, "No graph entities were generated.", fontSize=10, fillColor=colors.grey))
        return drawing

    positions = {}
    columns = min(4, max(1, len(nodes)))
    rows = (len(nodes) + columns - 1) // columns
    for index, node in enumerate(nodes):
        column = index % columns
        row = index // columns
        x = 55 + column * ((width - 110) / max(1, columns - 1)) if columns > 1 else width / 2
        y = height - 45 - row * (min(70, (height - 80) / max(1, rows - 1))) if rows > 1 else height / 2
        positions[str(node.get("id"))] = (x, y)

    for edge in edges:
        source = positions.get(str(edge.get("source")))
        target = positions.get(str(edge.get("target")))
        if source and target:
            drawing.add(Line(source[0], source[1], target[0], target[1], strokeColor=colors.HexColor("#6d91aa"), strokeWidth=1))

    for node in nodes:
        node_id = str(node.get("id"))
        x, y = positions[node_id]
        drawing.add(Circle(x, y, 15, fillColor=colors.HexColor("#123b5a"), strokeColor=colors.HexColor("#39b9d4"), strokeWidth=1.2))
        label = node_id if len(node_id) <= 15 else f"{node_id[:12]}..."
        drawing.add(String(x, y - 28, label, textAnchor="middle", fontSize=7, fillColor=colors.HexColor("#1f3344")))
    return drawing