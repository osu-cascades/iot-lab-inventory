from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

tags = db.Table('tags',
    db.Column('page_id', db.Integer, db.ForeignKey('page.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('pages', lazy='dynamic'))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)

if __name__ == '__main__':

    db.drop_all()
    db.create_all()

    page1 = Page()
    page2 = Page()

    tag1 = Tag()
    tag2 = Tag()
    tag3 = Tag()

    page1.tags = [tag1, tag3]
    page2.tags = [tag1, tag2, tag3]

    db.session.add(page1)
    db.session.add(page2)
    db.session.commit()

    page = Page.query.filter_by(id=1).first()
    for t in page.tags:
        print page.id, t.id

    page = Page.query.filter_by(id=2).first()
    for t in page.tags:
        print page.id, t.id



