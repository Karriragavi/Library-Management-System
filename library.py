# library_management.py
import sqlite3
from datetime import datetime

# Database functions
def create_connection():
    return sqlite3.connect("library.db")

def create_tables():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            available BOOLEAN NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrow_records (
            record_id INTEGER PRIMARY KEY,
            book_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            borrow_date TEXT NOT NULL,
            return_date TEXT
        )
        """)

        # Insert default books if the table is empty
        cursor.execute("SELECT COUNT(*) FROM books")
        if cursor.fetchone()[0] == 0:
            default_books = [
                (1, "To Kill a Mockingbird", "Harper Lee"),
                (2, "1984", "George Orwell"),
                (3, "The Great Gatsby", "F. Scott Fitzgerald"),
                (4, "The Catcher in the Rye", "J.D. Salinger"),
                (5, "Pride and Prejudice", "Jane Austen")
            ]
            for book_id, title, author in default_books:
                cursor.execute("INSERT INTO books (book_id, title, author, available) VALUES (?, ?, ?, ?)", (book_id, title, author, True))
            conn.commit()

        # Insert default users if the table is empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            default_users = [
                (1, "John Doe"),
                (2, "Jane Smith"),
                (3, "Alice Johnson"),
                (4, "Bob Brown")
            ]
            cursor.executemany("INSERT INTO users (user_id, name) VALUES (?, ?)", default_users)
            conn.commit()

def add_book(title, author):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, available) VALUES (?, ?, ?)", (title, author, True))
        book_id = cursor.lastrowid
        conn.commit()
        print(f"Added book '{title}' with ID {book_id}")
        return book_id

def add_user(name):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
        user_id = cursor.lastrowid
        conn.commit()
        print(f"Added user '{name}' with ID {user_id}")
        return user_id

def book_exists(book_id):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM books WHERE book_id = ?", (book_id,))
        return cursor.fetchone()[0] > 0

def user_exists(user_id):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()[0] > 0

def borrow_book(book_id, user_id):
    if not book_exists(book_id):
        print("Invalid book ID. Please try again.")
        return False
    if not user_exists(user_id):
        print("No user found with this ID. Please try again.")
        return False

    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT available FROM books WHERE book_id = ?", (book_id,))
        available = cursor.fetchone()[0]
        if available:
            cursor.execute("UPDATE books SET available = ? WHERE book_id = ?", (False, book_id))
            cursor.execute("INSERT INTO borrow_records (book_id, user_id, borrow_date) VALUES (?, ?, ?)",
                           (book_id, user_id, datetime.now().isoformat()))
            conn.commit()
            print(f"Book with ID {book_id} borrowed by user with ID {user_id}")
            return True
        else:
            print(f"Book with ID {book_id} is not available")
            return False

def return_book(record_id):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT book_id FROM borrow_records WHERE record_id = ?", (record_id,))
        book_id = cursor.fetchone()
        if not book_id:
            print("Invalid record ID. Please try again.")
            return

        book_id = book_id[0]
        cursor.execute("UPDATE borrow_records SET return_date = ? WHERE record_id = ?", (datetime.now().isoformat(), record_id))
        cursor.execute("UPDATE books SET available = ? WHERE book_id = ?", (True, book_id))
        conn.commit()
        print(f"Book with ID {book_id} has been returned")

# Main function
def main():
    create_tables()

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Add User")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            add_book(title, author)

        elif choice == "2":
            name = input("Enter user name: ")
            add_user(name)

        elif choice == "3":
            while True:
                try:
                    book_id = int(input("Enter book ID to borrow: "))
                    user_id = int(input("Enter user ID: "))
                    if borrow_book(book_id, user_id):
                        break
                except ValueError:
                    print("Invalid input. Please enter numeric IDs.")

        elif choice == "4":
            while True:
                try:
                    record_id = int(input("Enter borrow record ID to return: "))
                    return_book(record_id)
                    break
                except ValueError:
                    print("Invalid input. Please enter a numeric record ID.")

        elif choice == "5":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
