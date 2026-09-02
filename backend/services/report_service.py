import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def generate_report(
    verification,
    user,
    output_path
):

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    document = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title = styles["Title"]
    heading = styles["Heading2"]
    normal = styles["Normal"]

    content = []

    content.append(
        Paragraph(
            "SIGNATURE VERIFICATION REPORT",
            title
        )
    )

    content.append(
        Spacer(
            1,
            20
        )
    )

    content.append(
        Paragraph(
            "AI-Based Signature Verification System",
            heading
        )
    )

    content.append(
        Spacer(
            1,
            15
        )
    )

    data = [
        ["Verification ID", str(verification.id)],
        ["User", user.name],
        ["Email", user.email],
        ["File", verification.filename],
        ["Result", verification.result],
        [
            "Confidence",
            f"{verification.confidence:.2f}%"
        ],
        [
            "Genuine Probability",
            f"{verification.genuine_probability:.2f}%"
        ],
        [
            "Forged Probability",
            f"{verification.forged_probability:.2f}%"
        ],
        [
            "Date",
            verification.created_at.strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        ]
    ]

    table = Table(
        data,
        colWidths=[180, 300]
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#eef1f7")
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                "Helvetica"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8
            )
        ])
    )

    content.append(table)

    content.append(
        Spacer(
            1,
            25
        )
    )

    if (
        verification.image_path
        and os.path.exists(
            verification.image_path
        )
    ):
        content.append(
            Paragraph(
                "Uploaded Signature",
                heading
            )
        )

        content.append(
            Spacer(
                1,
                10
            )
        )

        image = Image(
            verification.image_path,
            width=4 * inch,
            height=2 * inch,
            preserveAspectRatio=True
        )

        content.append(image)

        content.append(
            Spacer(
                1,
                20
            )
        )

    content.append(
        Paragraph(
            "This report was generated automatically by the Signature Verification System.",
            normal
        )
    )

    document.build(content)

    return output_path