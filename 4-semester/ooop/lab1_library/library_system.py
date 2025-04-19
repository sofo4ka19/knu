class Library:
    def __init__(self):
        self.books = []
        self.users = []
        self.borrowed_books = {}  # user_id -> [book_ids]

    def add_book(self, title, author, isbn, genre):
        book = {
            'id': len(self.books) + 1,
            'title': title,
            'author': author,
            'isbn': isbn,
            'genre': genre,
            'available': True
        }
        self.books.append(book)
        return book['id']

    def remove_book(self, book_id):
        for i, book in enumerate(self.books):
            if book['id'] == book_id:
                del self.books[i]
                return True
        return False

    def search_books(self, keyword):
        results = []
        for book in self.books:
            if (keyword.lower() in book['title'].lower() or
                    keyword.lower() in book['author'].lower() or
                    keyword.lower() in book['genre'].lower()):
                results.append(book)
        return results

    def register_user(self, name, email, address):
        user = {
            'id': len(self.users) + 1,
            'name': name,
            'email': email,
            'address': address,
            'active': True
        }
        self.users.append(user)
        return user['id']

    def get_user(self, user_id):
        for user in self.users:
            if user['id'] == user_id:
                return user
        return None

    def get_book(self, book_id):
        for book in self.books:
            if book['id'] == book_id:
                return book
        return None

    def borrow_book(self, user_id, book_id):
        user = self.get_user(user_id)
        book = self.get_book(book_id)

        if not user or not book:
            return False

        if not book['available']:
            return False

        if user_id not in self.borrowed_books:
            self.borrowed_books[user_id] = []

        self.borrowed_books[user_id].append(book_id)
        book['available'] = False
        return True

    def return_book(self, user_id, book_id):
        if user_id not in self.borrowed_books or book_id not in self.borrowed_books[user_id]:
            return False

        book = self.get_book(book_id)
        if not book:
            return False

        self.borrowed_books[user_id].remove(book_id)
        book['available'] = True
        return True

    def get_borrowed_books(self, user_id):
        if user_id not in self.borrowed_books:
            return []

        borrowed_books = []
        for book_id in self.borrowed_books[user_id]:
            book = self.get_book(book_id)
            if book:
                borrowed_books.append(book)

        return borrowed_books

    def generate_report(self):
        total_books = len(self.books)
        available_books = sum(1 for book in self.books if book['available'])
        borrowed_books = total_books - available_books
        total_users = len(self.users)

        active_borrowers = sum(1 for user_id in self.borrowed_books if self.borrowed_books[user_id])

        report = {
            'total_books': total_books,
            'available_books': available_books,
            'borrowed_books': borrowed_books,
            'total_users': total_users,
            'active_borrowers': active_borrowers
        }

        return report

    def save_data(self, filename):
        import json
        data = {
            'books': self.books,
            'users': self.users,
            'borrowed_books': self.borrowed_books
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_data(self, filename):
        import json
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.books = data['books']
                self.users = data['users']
                self.borrowed_books = data['borrowed_books']
            return True
        except:
            return False


# CLI interface for the library system
if __name__ == "__main__":
    library = Library()

    # Add some sample data
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", "Fiction")
    library.add_book("To Kill a Mockingbird", "Harper Lee", "9780061120084", "Fiction")
    library.add_book("1984", "George Orwell", "9780451524935", "Dystopian")
    user_id = library.register_user("John Doe", "john@example.com", "123 Main St")

    while True:
        print("\nLibrary Management System")
        print("1. Add a book")
        print("2. Search for books")
        print("3. Register a user")
        print("4. Borrow a book")
        print("5. Return a book")
        print("6. View borrowed books")
        print("7. Generate report")
        print("8. Save data")
        print("9. Load data")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter title: ")
            author = input("Enter author: ")
            isbn = input("Enter ISBN: ")
            genre = input("Enter genre: ")
            book_id = library.add_book(title, author, isbn, genre)
            print(f"Book added with ID: {book_id}")

        elif choice == '2':
            keyword = input("Enter search keyword: ")
            results = library.search_books(keyword)
            print("\nSearch Results:")
            for book in results:
                status = "Available" if book['available'] else "Borrowed"
                print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}, Status: {status}")

        elif choice == '3':
            name = input("Enter name: ")
            email = input("Enter email: ")
            address = input("Enter address: ")
            user_id = library.register_user(name, email, address)
            print(f"User registered with ID: {user_id}")

        elif choice == '4':
            user_id = int(input("Enter user ID: "))
            book_id = int(input("Enter book ID: "))
            success = library.borrow_book(user_id, book_id)
            if success:
                print("Book borrowed successfully")
            else:
                print("Failed to borrow book")

        elif choice == '5':
            user_id = int(input("Enter user ID: "))
            book_id = int(input("Enter book ID: "))
            success = library.return_book(user_id, book_id)
            if success:
                print("Book returned successfully")
            else:
                print("Failed to return book")

        elif choice == '6':
            user_id = int(input("Enter user ID: "))
            books = library.get_borrowed_books(user_id)
            print("\nBorrowed Books:")
            for book in books:
                print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}")

        elif choice == '7':
            report = library.generate_report()
            print("\nLibrary Report:")
            print(f"Total Books: {report['total_books']}")
            print(f"Available Books: {report['available_books']}")
            print(f"Borrowed Books: {report['borrowed_books']}")
            print(f"Total Users: {report['total_users']}")
            print(f"Active Borrowers: {report['active_borrowers']}")

        elif choice == '8':
            filename = input("Enter filename to save: ")
            library.save_data(filename)
            print("Data saved successfully")

        elif choice == '9':
            filename = input("Enter filename to load: ")
            success = library.load_data(filename)
            if success:
                print("Data loaded successfully")
            else:
                print("Failed to load data")

        elif choice == '0':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")