from library_facade import LibraryFacade
from observers import LibraryEventLogger, EmailNotificationObserver, StatisticsObserver
from commands import BorrowBookCommand, ReturnBookCommand, AddBookCommand, CommandInvoker


class LibraryCLI:
    def __init__(self):
        self.library = LibraryFacade()
        self.command_invoker = CommandInvoker()
        self._setup_observers()
        self._setup_sample_data()

    def _setup_observers(self):
        """Setup all observers"""
        self.library.add_observer(LibraryEventLogger())
        self.library.add_observer(EmailNotificationObserver())
        self.library.add_observer(StatisticsObserver())

    def _setup_sample_data(self):
        """Template method for initializing sample data"""
        self.library.add_book("The Great Gatsby", "F. Scott Fitzgerald",
                              "9780743273565", "Fiction")
        self.library.add_book("To Kill a Mockingbird", "Harper Lee",
                              "9780061120084", "Fiction")
        self.library.add_book("1984", "George Orwell",
                              "9780451524935", "Dystopian")
        self.library.add_book("Pride and Prejudice", "Jane Austen",
                              "9780141439518", "Romance")
        self.library.add_book("The Catcher in the Rye", "J.D. Salinger",
                              "9780316769174", "Fiction")

        self.library.register_user("John Doe", "john@example.com", "123 Main St")
        self.library.register_user("Jane Smith", "jane@example.com", "456 Oak Ave")

    def run(self):
        """Main CLI loop"""
        print("Welcome to the Library Management System!")
        while True:
            self._display_menu()
            choice = input("\nEnter your choice: ").strip()

            if choice == '0':
                print("Thank you for using the Library Management System. Goodbye!")
                break

            self._handle_choice(choice)

    def _display_menu(self):
        """Display the main menu"""
        print("\n" + "=" * 50)
        print("LIBRARY MANAGEMENT SYSTEM")
        print("=" * 50)
        print("1.  Add a book")
        print("2.  Search for books")
        print("3.  View all books")
        print("4.  Register a user")
        print("5.  View all users")
        print("6.  Borrow a book")
        print("7.  Return a book")
        print("8.  View borrowed books")
        print("9.  Generate report")
        print("10. Save data")
        print("11. Load data")
        print("12. Delete book")
        print("13. View configuration")
        print("14. Update configuration")
        print("15. Undo last command")
        print("0.  Exit")
        print("=" * 50)

    def _handle_choice(self, choice: str):
        """Handle user choice"""
        handlers = {
            '1': self._add_book,
            '2': self._search_books,
            '3': self._view_all_books,
            '4': self._register_user,
            '5': self._view_all_users,
            '6': self._borrow_book,
            '7': self._return_book,
            '8': self._view_borrowed_books,
            '9': self._generate_report,
            '10': self._save_data,
            '11': self._load_data,
            '12': self._delete_book,
            '13': self._view_config,
            '14': self._update_config,
            '15': self._undo_last_command
        }

        handler = handlers.get(choice)
        if handler:
            try:
                handler()
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Invalid choice. Please try again.")

    def _add_book(self):
        print("\n--- Add New Book ---")
        title = input("Enter title: ").strip()
        author = input("Enter author: ").strip()
        isbn = input("Enter ISBN: ").strip()
        genre = input("Enter genre: ").strip()

        if not all([title, author, isbn, genre]):
            print("All fields are required!")
            return

        command = AddBookCommand(self.library, title, author, isbn, genre)
        book_id = self.command_invoker.execute_command(command)
        print(f"✓ Book added successfully with ID: {book_id}")

    def _search_books(self):
        print("\n--- Search Books ---")
        keyword = input("Enter search keyword: ").strip()
        if not keyword:
            print("Please enter a search keyword!")
            return

        print("\nSearch strategies:")
        print("1. Title search")
        print("2. Author search")
        print("3. Genre search")
        print("4. Composite search (default)")

        strategy_choice = input("Choose search strategy (1-4, default: 4): ").strip()
        strategy_map = {'1': 'title', '2': 'author', '3': 'genre', '4': 'composite'}
        strategy = strategy_map.get(strategy_choice, 'composite')

        results = self.library.search_books(keyword, strategy)
        self._display_books(results, f"Search Results for '{keyword}'")

    def _view_all_books(self):
        books = self.library.get_all_books()
        self._display_books(books, "All Books")

    def _register_user(self):
        print("\n--- Register New User ---")
        name = input("Enter name: ").strip()
        email = input("Enter email: ").strip()
        address = input("Enter address: ").strip()

        if not all([name, email, address]):
            print("All fields are required!")
            return

        user_id = self.library.register_user(name, email, address)
        print(f"✓ User registered successfully with ID: {user_id}")

    def _view_all_users(self):
        users = self.library.get_all_users()
        if not users:
            print("\nNo users registered.")
            return

        print(f"\n--- All Users ({len(users)}) ---")
        for user in users:
            status = "Active" if user.active else "Inactive"
            print(f"ID: {user.id:2d} | Name: {user.name:25s} | Email: {user.email:25s} | Status: {status}")

    def _borrow_book(self):
        print("\n--- Borrow Book ---")
        try:
            user_id = int(input("Enter user ID: "))
            book_id = int(input("Enter book ID: "))

            command = BorrowBookCommand(self.library, user_id, book_id)
            success = self.command_invoker.execute_command(command)

            if success:
                print("✓ Book borrowed successfully!")
            else:
                print("✗ Failed to borrow book. Check if book is available and user exists.")
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

    def _return_book(self):
        print("\n--- Return Book ---")
        try:
            user_id = int(input("Enter user ID: "))
            book_id = int(input("Enter book ID: "))

            command = ReturnBookCommand(self.library, user_id, book_id)
            success = self.command_invoker.execute_command(command)

            if success:
                print("✓ Book returned successfully!")
            else:
                print("✗ Failed to return book. Check if the book was borrowed by this user.")
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

    def _view_borrowed_books(self):
        print("\n--- View Borrowed Books ---")
        try:
            user_id = int(input("Enter user ID: "))
            user = self.library.get_user(user_id)
            if not user:
                print("User not found!")
                return

            books = self.library.get_borrowed_books(user_id)
            if not books:
                print(f"No books borrowed by {user.name}.")
                return

            self._display_books(books, f"Books borrowed by {user.name}")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def _generate_report(self):
        report = self.library.generate_report()
        print("\n" + "=" * 40)
        print("LIBRARY REPORT")
        print("=" * 40)
        print(f"Total Books:      {report.total_books:4d}")
        print(f"Available Books:  {report.available_books:4d}")
        print(f"Borrowed Books:   {report.borrowed_books:4d}")
        print(f"Total Users:      {report.total_users:4d}")
        print(f"Active Borrowers: {report.active_borrowers:4d}")
        print("=" * 40)

    def _save_data(self):
        print("\n--- Save Data ---")
        filename = input("Enter filename to save (default: library_data.json): ").strip()
        filename = filename or "library_data.json"

        success = self.library.save_data(filename)
        if success:
            print(f"✓ Data saved successfully to {filename}")
        else:
            print("✗ Failed to save data")

    def _load_data(self):
        print("\n--- Load Data ---")
        filename = input("Enter filename to load (default: library_data.json): ").strip()
        filename = filename or "library_data.json"

        success = self.library.load_data(filename)
        if success:
            print(f"✓ Data loaded successfully from {filename}")
        else:
            print("✗ Failed to load data")

    def _delete_book(self):
        print("\n--- Delete Book ---")
        try:
            book_id = int(input("Enter book ID to delete: "))
            book = self.library.get_book(book_id)
            if not book:
                print("Book not found!")
                return

            confirm = input(f"Are you sure you want to delete '{book.title}' by {book.author}? (y/N): ").strip().lower()
            if confirm == 'y':
                success = self.library.remove_book(book_id)
                if success:
                    print("✓ Book deleted successfully")
                else:
                    print("✗ Failed to delete book")
            else:
                print("Deletion cancelled")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def _view_config(self):
        config = self.library.get_config()
        print("\n" + "=" * 50)
        print("LIBRARY CONFIGURATION")
        print("=" * 50)
        for key, value in config.items():
            print(f"{key.replace('_', ' ').title():30s}: {value}")
        print("=" * 50)

    def _update_config(self):
        print("\n--- Update Configuration ---")
        print("Available settings:")
        print("1. max_books_per_user")
        print("2. default_search_strategy")
        print("3. max_borrow_days")
        print("4. fine_per_day")
        print("5. email_notifications_enabled")

        setting = input("Enter setting name: ").strip()
        if not setting:
            print("Setting name is required!")
            return

        value = input(f"Enter new value for {setting}: ").strip()
        if not value:
            print("Value is required!")
            return

        try:
            # Convert to appropriate type
            if setting in ['max_books_per_user', 'max_borrow_days', 'backup_interval_minutes']:
                value = int(value)
            elif setting == 'fine_per_day':
                value = float(value)
            elif setting in ['email_notifications_enabled', 'auto_save_enabled']:
                value = value.lower() in ['true', '1', 'yes', 'on']

            self.library.update_config(**{setting: value})
            print(f"✓ Configuration updated: {setting} = {value}")
        except Exception as e:
            print(f"✗ Failed to update configuration: {e}")

    def _undo_last_command(self):
        print("\n--- Undo Last Command ---")
        success = self.command_invoker.undo_last_command()
        if success:
            print("✓ Last command undone successfully")
        else:
            print("✗ No command to undo or undo failed")

    def _display_books(self, books, title):
        """Helper method to display books in a formatted table"""
        if not books:
            print(f"\n{title}: No books found.")
            return

        print(f"\n--- {title} ({len(books)}) ---")
        print(f"{'ID':3s} | {'Title':30s} | {'Author':20s} | {'Genre':15s} | {'Status':10s}")
        print("-" * 85)

        for book in books:
            status = "Available" if book.available else "Borrowed"
            print(f"{book.id:3d} | {book.title[:30]:30s} | {book.author[:20]:20s} | "
                  f"{book.genre[:15]:15s} | {status:10s}")


# Main execution
if __name__ == "__main__":
    cli = LibraryCLI()
    cli.run()