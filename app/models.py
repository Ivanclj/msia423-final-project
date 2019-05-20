from app import db


class Churn_Prediction(db.Model):
    """Create a data model for the database to be set up for capturing customers """

    __tablename__ = 'churn_prediction'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    activeMember = db.Column(db.Integer, unique=False, nullable=False)
    numProducts = db.Column(db.Integer, unique=False, nullable=False)
    fromGermany = db.Column(db.Integer, unique=False, nullable=False)
    gender = db.Column(db.Integer, unique=False, nullable=False)
    balance = db.Column(db.Float, unique=False, nullable=False)
    hasCrCard = db.Column(db.Integer, unique=False, nullable=False)
    tenure = db.Column(db.Float, unique=False, nullable=False)
    predicted_score = db.Column(db.String(100), unique=False, nullable=False)

    def __repr__(self):
        return '<Customer %r>' % self.id
