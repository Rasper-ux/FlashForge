# pylint: disable=redefined-builtin
from config import db
from entities.reference import Article, Book, Inproceedings, Manual

def add_reference(ref):
    return ref.insert(db)

def edit_ref(ref):
    return ref.update(db)

def delete_reference(ref):
    return ref.delete(db)

def get_all_articles():
    return Article().get_all(db)

def get_all_books():
    return Book().get_all(db)

def get_all_inproceedings():
    return Inproceedings().get_all(db)

def get_all_manuals():
    return Manual().get_all(db)

def get_all_references():
    return [
        *get_all_articles(),
        *get_all_books(),
        *get_all_inproceedings(),
        *get_all_manuals(),
    ]

def ref_from_id(ref_type, id):
    match ref_type:
        case Article.type:
            ref = Article
        case Book.type:
            ref = Book
        case Inproceedings.type:
            ref = Inproceedings
        case Manual.type:
            ref = Manual

        case _:
            return None

    return ref(id=id).from_id(db)

def search_result(query):
    return [
        *Article().get_like(db, query),
        *Book().get_like(db, query),
        *Inproceedings().get_like(db, query),
        *Manual().get_like(db, query),
    ]

def order_references(order):
    match order:
        case "old_to_new":
            return sorted(get_all_references(), key=lambda ref: ref.details().get("year") or "")
        case "new_to_old":
            return order_references("old_to_new")[::-1]
        case "author_a_to_z":
            return sorted(get_all_references(), key=lambda ref: ref.details().get("author") or "")
        case "author_z_to_a":
            return order_references("author_a_to_z")[::-1]

        case _:
            return get_all_references()

def advanced_search_result(field, query):
    if field == "all_fields":
        return search_result(query)

    return [
        *Article().get_by_field(db, field, query),
        *Book().get_by_field(db, field, query),
        *Inproceedings().get_by_field(db, field, query),
        *Manual().get_by_field(db, field, query),
    ]
