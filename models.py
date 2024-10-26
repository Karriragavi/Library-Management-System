from datetime import datetime

class Book:
    def __init__(self, book_id, title, author, available=True):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.available = available

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

class BorrowRecord:
    def __init__(self, record_id, book_id, user_id, borrow_date, return_date=None):
        self.record_id = record_id
        self.book_id = book_id
        self.user_id = user_id
        self.borrow_date = borrow_date
        self.return_date = return_date
