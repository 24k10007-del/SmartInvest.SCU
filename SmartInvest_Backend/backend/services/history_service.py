from database import db
from models.history import History


class HistoryService:

    @staticmethod
    def save(data):

        history = History(

            symbol=data["symbol"],

            price=data["currentPrice"],

            recommendation=data["recommendation"],

            score=data["score"],

            confidence=data["confidence"]

        )

        db.session.add(history)

        db.session.commit()

        return history


    @staticmethod
    def get_all():

        histories = History.query.order_by(

            History.created_at.desc()

        ).all()

        result = []

        for item in histories:

            result.append({

                "id": item.id,

                "symbol": item.symbol,

                "price": item.price,

                "recommendation": item.recommendation,

                "score": item.score,

                "confidence": item.confidence,

                "created_at": item.created_at

            })

        return result