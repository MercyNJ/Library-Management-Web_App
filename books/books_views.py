#!/usr/bin/python3
from flask import Flask, render_template, jsonify
from flask import url_for, request, redirect, abort
from flask_login import login_required
import models
from models.books import Books
from models import storage
from . import books_bp

@books_bp.route('/books', methods=['GET'])
@login_required
def view_books():
    """Handle the request to view the available books."""
    try:
        books = storage.all(Books).values()
        books = sorted(books, key=lambda k: k.id)
        return render_template('view_books.html', books=books)
    except Exception as e:
        error_message = "Error viewing books: {}".format(str(e))
        return error_message, 500



@books_bp.route(
    '/add_book_form', methods=['GET', 'POST'],
    strict_slashes=False)
@login_required
def add_book_form():
    """Handle the request to display and add a book."""
    if request.method == 'POST':
        book_name = request.form.get('book_name')
        book_author = request.form.get('book_author')
        book_original_stock = request.form.get('book_original_stock')
        book_current_stock = request.form.get('book_current_stock')

        try:
            new_book = Books(
                    name=book_name, author=book_author,
                    original_stock=book_original_stock,
                    current_stock=book_current_stock)
            new_book.save()
            return redirect(url_for('books.view_books'))
        except Exception as e:
            pass
    return render_template('add_book_form.html')



@books_bp.route('/update_book_form/<book_id>', methods=['GET', 'POST'])
@login_required
def update_book_form(book_id):
    """Handle the request to update a book record."""
    try:
        book_id = int(book_id)
        book = storage.get(Books, book_id)
        if request.method == 'POST':
            if book:
                book.name = request.form.get('book_name')
                book.author = request.form.get('book_author')
                book.original_stock = request.form.get(
                        'book_original_stock')
                book.current_stock = request.form.get(
                        'book_current_stock')
                book.save()
                return redirect(url_for('books.view_books'))
            else:
                return "Book not found"
        elif request.method == 'GET':
            if book:
                return render_template(
                        'update_book_form.html', book=book)
            else:
                return "Book not found"
    except Exception as e:
        return "Error updating book form: {}".format(str(e))



@books_bp.route('/delete_book/<book_id>', methods=['GET', 'POST'])
@login_required
def delete_book(book_id):
    """Handle the request to delete a book by its ID."""
    try:
        book = storage.get(Books, int(book_id))
        if book:
            storage.delete(book)
            storage.save()
        return redirect(url_for('books.view_books'))
    except Exception as e:
        return "Error deleting the book: {}".format(str(e))
