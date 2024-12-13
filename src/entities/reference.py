# pylint: disable=bare-except, redefined-builtin
from sqlalchemy import text

class Reference:
    """Default class for references"""
    type     = "generic_reference"
    table    = ""
    required = []
    optional = []
    special  = {}
    id       = None
    fields   = {}

    def __init__(self, id=None, **kwargs):
        self.id     = id
        self.fields = { **kwargs }

    def validate(self):
        required_fields = all(
            required in self.fields
            for required in self.required
        )

        def can_convert_to(type, field):
            try:
                if field and type(field):
                    pass
            except ValueError:
                return False
            return True

        typed_fields = all(
            can_convert_to(self.special[key], val)
            for key, val in self.fields.items()
            if key in self.special
        )

        return required_fields and typed_fields

    def details(self):
        default   = {key: None for key in self.required + self.optional}
        populated = {key: val or None for key, val in self.fields.items()}
        return {**default, **populated}

    def from_id(self, db):
        sql = f"""
            SELECT * FROM {self.table} WHERE id = :id
        """

        try:
            res = db.session.execute(text(sql), { "id": self.id })
        except:
            return self.__class__()

        row = res.fetchone()
        return self.__class__(**row._asdict()) if row else None

    def get_all(self, db):
        sql = f"""
            SELECT * FROM {self.table}
        """

        try:
            res = db.session.execute(text(sql))
        except:
            return []

        return [self.__class__(**row._asdict()) for row in res.fetchall()]

    def get_like(self, db, query):
        fields = [f"CAST({key} AS TEXT) ILIKE :query" for key in self.required + self.optional]
        sql = f"""
            SELECT *
            FROM {self.table}
            WHERE {" OR ".join(fields)}
        """

        try:
            res = db.session.execute(text(sql), {"query": f"%{query}%"})
            return [self.__class__(**row._asdict()) for row in res.fetchall()]
        except:
            db.session.rollback()
            return []


    def get_by_field(self, db, field, query):
        sql = f"""
            SELECT *
            FROM {self.table}
            WHERE CAST({field} AS TEXT) ILIKE :query
        """

        try:
            res = db.session.execute(text(sql), {"query": f"%{query}%"})
            return [self.__class__(**row._asdict()) for row in res.fetchall()]
        except:
            db.session.rollback()
            return []

    def insert(self, db) -> bool:
        details = self.details()
        fields  = details.keys()
        sql = f"""
            INSERT INTO {self.table} ({", ".join(fields)}) VALUES ({", ".join([f":{key}" for key in fields])})
        """

        try:
            db.session.execute(text(sql), details)
        except:
            db.session.rollback()
            return False

        db.session.commit()
        return True

    def update(self, db) -> bool:
        details = self.details()
        sql = f"""
            UPDATE {self.table}
            SET {", ".join([f"{key}=:{key}" for key in details.keys()])}
            WHERE id = :id
        """

        try:
            db.session.execute(text(sql), {"id": self.id, **details})
        except:
            db.session.rollback()
            return False

        db.session.commit()
        return True

    def delete(self, db) -> bool:
        sql = f"""
            DELETE FROM {self.table} where id=:id
        """

        try:
            db.session.execute(text(sql), {"id": self.id})
        except:
            db.session.rollback()
            return False

        db.session.commit()
        return True

    def generate(self):
        header = f"{self.type}-{self.id}"
        fields = "\n".join([f"\t{key} = {{{val}}}," for key, val in self.fields.items() if val])
        return f"@{self.type}{{{header},\n{fields}\n}}\n"

class Article(Reference):
    """Class for article references"""
    type     = "article"
    table    = "Articles"
    required = ["author", "title", "journal", "year"]
    optional = ["volume", "number", "pages", "month", "note"]
    special  = { "year": int, "volume": int, "number": int }

class Book(Reference):
    """Class for book references"""
    type     = "book"
    table    = "Books"
    required = ["author", "title", "publisher", "year", "address"]
    optional = []
    special  = { "year": int }

class Inproceedings(Reference):
    """Class for inproceedings references"""
    type     = "inproceedings"
    table    = "Inproceedings"
    required = ["author", "title", "booktitle", "year"]
    optional = ["editor", "volume", "number", "series", "pages", "address",
                "month", "organization", "publisher"]
    special  = { "year": int, "volume": int, "number": int }

class Manual(Reference):
    """Class for manuals references"""
    type     = "manual"
    table    = "Manuals"
    required = ["title", "year"]
    optional = ["author", "organization", "address", "edition", "month", "note"]
    special  = { "year": int }
