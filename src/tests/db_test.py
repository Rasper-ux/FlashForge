import unittest
from tests import db_helper
from modules import database
from config import app, db

from entities.reference import Article, Book, Inproceedings, Manual

# pylint: disable=too-many-public-methods
class TestDatabase(unittest.TestCase):
    """Class for testing the database"""

    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.context = cls.app.app_context()

        with cls.context:
            db_helper.setup_db()

    def setUp(self):
        self.article_ref = Article(
             author   = 'Article Author',
             title    = 'Article Title',
             journal  = 'Article Journal',
             year     = 2024
        )
        self.book_ref = Book(
            author    = 'Book Author',
            title     = 'Book Title',
            publisher = 'Book Publisher',
            year      = 2022,
            address   = 'Book Address'
        )
        self.inproceedings_ref = Inproceedings(
            author    = 'Inproceedings Author',
            title     = 'Inproceedings Title',
            booktitle = 'Inproceedings Booktitle',
            year      = 2023,
        )
        self.manual_ref = Manual(
            title     = 'Manual Title',
            year      = 2021,
        )

    def tearDown(self):
        with self.context:
            db_helper.reset_db()

    def test_database_add_article(self):
        with self.context:
            self.assertTrue(self.article_ref.insert(db))

    def test_database_query(self):
        with self.context:
            self.assertTrue(self.article_ref.insert(db))
            self.assertTrue(self.book_ref.insert(db))
            self.assertTrue(self.inproceedings_ref.insert(db))
            self.assertTrue(self.manual_ref.insert(db))

            res = database.get_all_articles()
            self.article_ref.id = res[0].id
            self.assertEqual([val.details() for val in res], [self.article_ref.details()])

            res = database.get_all_books()
            self.book_ref.id = res[0].id
            self.assertEqual([val.details() for val in res], [self.book_ref.details()])

            res = database.get_all_inproceedings()
            self.inproceedings_ref.id = res[0].id
            self.assertEqual([val.details() for val in res], [self.inproceedings_ref.details()])

            res = database.get_all_manuals()
            self.manual_ref.id = res[0].id
            self.assertEqual([val.details() for val in res], [self.manual_ref.details()])

    def test_database_add_duplicate_article(self):
        with self.context:
            self.assertTrue(self.article_ref.insert(db))
            self.assertFalse(self.article_ref.insert(db))

    def test_database_valid_search(self):
        with self.context:
            self.assertTrue(self.article_ref.insert(db))
            res = database.search_result('Au')

            expected = self.article_ref.details()
            self.assertEqual([val.details() for val in res], [expected])

            res = database.search_result('thor')
            self.assertEqual([val.details() for val in res], [expected])

            res = database.search_result('2024')
            self.assertEqual([val.details() for val in res], [expected])

    def test_database_invalid_search(self):
        with self.context:
            self.assertTrue(self.article_ref.insert(db))

            res = database.search_result('Invalid')
            self.assertEqual(res, [])

            res = database.search_result('1999')
            self.assertEqual(res, [])

    def test_database_edit_article(self):
        with self.context:
            self.assertTrue(self.article_ref.insert(db))
            res = database.get_all_articles()
            self.article_ref.id = res[0].id

            self.assertTrue(database.edit_ref(self.article_ref))
            res = database.ref_from_id(self.article_ref.type, self.article_ref.id)
            self.assertEqual(res.details(), self.article_ref.details())

    def test_database_edit_book(self):
        with self.context:
            self.assertTrue(self.book_ref.insert(db))
            res = database.get_all_books()
            self.book_ref.id = res[0].id

            self.assertTrue(database.edit_ref(self.book_ref))
            res = database.ref_from_id(self.book_ref.type, self.book_ref.id)
            self.assertEqual(res.details(), self.book_ref.details())

    def test_database_edit_inproceedings(self):
        with self.context:
            self.assertTrue(self.inproceedings_ref.insert(db))
            res = database.get_all_inproceedings()
            self.inproceedings_ref.id = res[0].id

            self.assertTrue(database.edit_ref(self.inproceedings_ref))
            res = database.ref_from_id(self.inproceedings_ref.type, self.inproceedings_ref.id)
            self.assertEqual(res.details(), self.inproceedings_ref.details())

    def test_database_edit_manual(self):
        with self.context:
            self.assertTrue(self.manual_ref.insert(db))
            res = database.get_all_manuals()
            self.manual_ref.id = res[0].id

            self.assertTrue(database.edit_ref(self.manual_ref))
            res = database.ref_from_id(self.manual_ref.type, self.manual_ref.id)
            self.assertEqual(res.details(), self.manual_ref.details())

    def test_database_edit_invalid(self):
        with self.context:
            self.manual_ref.id = 0
            self.assertTrue(database.edit_ref(self.manual_ref))
            res = database.ref_from_id("invalid", self.manual_ref.id)
            self.assertEqual(res, None)

    def test_database_delete_article(self):
        with self.context:
            self.assertTrue(self.article_ref.insert(db))
            res = database.get_all_articles()
            self.assertTrue(database.delete_reference(res[0]))
            res = database.get_all_articles()
            self.assertEqual(res, [])

    def test_database_add_book(self):
        with self.context:
            self.assertTrue(self.book_ref.insert(db))

    def test_database_add_duplicate_book(self):
        with self.context:
            self.assertTrue(self.book_ref.insert(db))
            self.assertFalse(self.book_ref.insert(db))

    def test_database_add_inproceedings(self):
        with self.context:
            self.assertTrue(self.inproceedings_ref.insert(db))

    def test_database_add_duplicate_inproceedings(self):
        with self.context:
            self.assertTrue(self.inproceedings_ref.insert(db))
            self.assertFalse(self.inproceedings_ref.insert(db))

    def test_database_add_manual(self):
        with self.context:
            self.assertTrue(self.manual_ref.insert(db))

    def test_database_add_duplicate_manual(self):
        with self.context:
            self.assertTrue(self.manual_ref.insert(db))
            self.assertFalse(self.manual_ref.insert(db))

    def test_advanced_search(self):
        with self.context:
            self.assertTrue(database.add_reference(self.article_ref))

            res = database.advanced_search_result('author', 'au')
            self.assertEqual([val.details() for val in res], [self.article_ref.details()])

            res = database.advanced_search_result('title', 'tle')
            self.assertEqual([val.details() for val in res], [self.article_ref.details()])

            res = database.advanced_search_result('journal', 'rnal')
            self.assertEqual([val.details() for val in res], [self.article_ref.details()])

            res = database.advanced_search_result('year', '1999')
            self.assertEqual([val.details() for val in res], [])

            res = database.advanced_search_result('all_fields', 'au')
            self.assertEqual([val.details() for val in res], [self.article_ref.details()])

    def test_order_references_by_year(self):
        with self.context:
            self.assertTrue(database.add_reference(self.article_ref))
            self.assertTrue(database.add_reference(self.book_ref))

            res = database.order_references('old_to_new')
            self.assertEqual(res[0].details().get("author"), self.book_ref.details().get("author"))

            res = database.order_references('new_to_old')
            self.assertEqual(res[0].details().get("author"), self.article_ref.details().get("author"))

    def test_order_references_by_author(self):
        with self.context:
            self.assertTrue(database.add_reference(self.article_ref))
            self.assertTrue(database.add_reference(self.book_ref))

            res = database.order_references('author_a_to_z')
            self.assertEqual(res[0].details().get("author"), self.article_ref.details().get("author"))

            res = database.order_references('author_z_to_a')
            self.assertEqual(res[0].details().get("author"), self.book_ref.details().get("author"))

    def test_order_references_by_invalid(self):
        with self.context:
            self.assertTrue(database.add_reference(self.article_ref))
            self.assertEqual([
                val.details() for val in database.order_references('invalid')
            ], [
                val.details() for val in database.get_all_references()
            ])
