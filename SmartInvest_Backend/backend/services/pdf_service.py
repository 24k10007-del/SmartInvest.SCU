from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer

from datetime import datetime

import os


class PDFService:

    @staticmethod
    def generate(data):

        if not os.path.exists("exports"):
            os.makedirs("exports")

        filename = f"exports/TLKM_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        doc = SimpleDocTemplate(filename)

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "<b>PT Telkom Indonesia (Persero) Tbk</b>",
                styles["Heading1"]
            )
        )

        story.append(Spacer(1,20))

        story.append(
            Paragraph(
                f"Current Price : {data['currentPrice']}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"Recommendation : {data['recommendation']}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"Confidence : {data['confidence']}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"Score : {data['score']}",
                styles["Normal"]
            )
        )

        story.append(Spacer(1,20))

        story.append(
            Paragraph(
                "<b>Technical Analysis</b>",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                f"RSI : {data['RSI14']}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"SMA20 : {data['SMA20']}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"SMA50 : {data['SMA50']}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"EMA20 : {data['EMA20']}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"MACD : {data['MACD']}",
                styles["Normal"]
            )
        )

        story.append(Spacer(1,20))

        story.append(
            Paragraph(
                "<b>Reason</b>",
                styles["Heading2"]
            )
        )

        for reason in data["reason"]:
            story.append(
                Paragraph(
                    f"• {reason}",
                    styles["Normal"]
                )
            )

        doc.build(story)

        return filename