from config import app, db
from sqlalchemy import text

def reset_db():
    print("""Reseting all tables!""")
    with open('sql/reset.sql', 'r', encoding='utf-8') as file:
        sql = text(file.read())
        res = db.session.execute(sql)
        if res:
            db.session.commit()
        else:
            db.session.rollback()

def drop_tables():
    print("""Dropping all tables!""")
    with open('sql/drop.sql', 'r', encoding='utf-8') as file:
        sql = text(file.read())
        res = db.session.execute(sql)
        if res:
            db.session.commit()
        else:
            db.session.rollback()

def create_tables():
    print("""Creating all tables!""")
    with open('sql/schema.sql', 'r', encoding='utf-8') as file:
        sql = text(file.read())
        res = db.session.execute(sql)
        if res:
            db.session.commit()
        else:
            db.session.rollback()

def setup_db():
    drop_tables()
    create_tables()

if __name__ == "__main__":
    with app.app_context():
        setup_db()
