import unittest
from library_system import Library


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.book_id = self.library.add_book("Test Book", "Test Author", "1234567890", "Test Genre")
        self.user_id = self.library.register_user("Test User", "test@example.com", "Test Address")

    def test_add_book(self):
        book_id = self.library.add_book("New Book", "New Author", "0987654321", "New Genre")
        self.assertEqual(len(self.library.books), 2)
        book = self.library.get_book(book_id)
        self.assertEqual(book['title'], "New Book")
        self.assertEqual(book['author'], "New Author")
        self.assertEqual(book['isbn'], "0987654321")
        self.assertEqual(book['genre'], "New Genre")
        self.assertTrue(book['available'])

    def test_remove_book(self):
        self.assertTrue(self.library.remove_book(self.book_id))
        self.assertEqual(len(self.library.books), 0)
        self.assertFalse(self.library.remove_book(999))

    def test_search_books(self):
        # Add more books for search testing
        self.library.add_book("Python Programming", "John Smith", "1111111111", "Programming")
        self.library.add_book("Python for Beginners", "Jane Doe", "2222222222", "Programming")
        self.library.add_book("Java Basics", "John Doe", "3333333333", "Programming")

        # Test search by title
        results = self.library.search_books("Python")
        self.assertEqual(len(results), 2)

        # Test search by author
        results = self.library.search_books("John")
        self.assertEqual(len(results), 2)

        # Test search by genre
        results = self.library.search_books("Programming")
        self.assertEqual(len(results), 3)

        # Test case insensitivity
        results = self.library.search_books("python")
        self.assertEqual(len(results), 2)

    def test_register_user(self):
        user_id = self.library.register_user("New User", "new@example.com", "New Address")
        self.assertEqual(len(self.library.users), 2)
        user = self.library.get_user(user_id)
        self.assertEqual(user['name'], "New User")
        self.assertEqual(user['email'], "new@example.com")
        self.assertEqual(user['address'], "New Address")
        self.assertTrue(user['active'])

    def test_borrow_return_book(self):
        # Test borrowing
        self.assertTrue(self.library.borrow_book(self.user_id, self.book_id))
        book = self.library.get_book(self.book_id)
        self.assertFalse(book['available'])

        # Test borrowing an already borrowed book
        self.assertFalse(self.library.borrow_book(self.user_id, self.book_id))

        # Test returning
        self.assertTrue(self.library.return_book(self.user_id, self.book_id))
        book = self.library.get_book(self.book_id)
        self.assertTrue(book['available'])

        # Test returning a book that wasn't borrowed
        self.assertFalse(self.library.return_book(self.user_id, self.book_id))

    def test_get_borrowed_books(self):
        self.library.borrow_book(self.user_id, self.book_id)
        borrowed_books = self.library.get_borrowed_books(self.user_id)
        self.assertEqual(len(borrowed_books), 1)
        self.assertEqual(borrowed_books[0]['id'], self.book_id)

        # Test for user with no borrowed books
        new_user_id = self.library.register_user("Another User", "another@example.com", "Another Address")
        borrowed_books = self.library.get_borrowed_books(new_user_id)
        self.assertEqual(len(borrowed_books), 0)

    def test_generate_report(self):
        self.library.borrow_book(self.user_id, self.book_id)
        report = self.library.generate_report()
        self.assertEqual(report['total_books'], 1)
        self.assertEqual(report['available_books'], 0)
        self.assertEqual(report['borrowed_books'], 1)
        self.assertEqual(report['total_users'], 1)
        self.assertEqual(report['active_borrowers'], 1)

    def test_save_load_data(self):
        # Add data
        book_id = self.library.add_book("Save Test Book", "Save Test Author", "5555555555", "Test Genre")
        self.library.borrow_book(self.user_id, book_id)

        # Save data
        filename = "test_library_data.json"
        self.library.save_data(filename)

        # Create a new library instance and load data
        new_library = Library()
        self.assertTrue(new_library.load_data(filename))

        # Verify the data was loaded
        self.assertEqual(len(new_library.books), 2)
        self.assertEqual(len(new_library.users), 1)
        self.assertEqual(len(new_library.borrowed_books[str(self.user_id)]), 1)

        # Test loading with invalid filename
        self.assertFalse(new_library.load_data("invalid_filename.json"))


if __name__ == '__main__':
    unittest.main()