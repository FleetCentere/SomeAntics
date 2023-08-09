from ProjectFiles import db

class pressReleases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(250))
    ticker = db.Column(db.String(10))
    link = db.Column(db.String(100))
    datePosted = db.Column(db.DateTime)

    def __repr__(self):
        return "<CompanyPost {}>".format(self.company)