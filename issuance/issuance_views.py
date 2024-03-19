#!/usr/bin/python3
from flask import Flask, render_template, request
from flask import redirect, url_for, make_response
from flask_weasyprint import HTML, render_pdf
from flask_login import login_required
from models.members import Members
from models.books import Books
from models.issuance import Issuance
from models.issuance_books import IssuanceBooks
import models
from models import storage
from datetime import date
from . import issuance_bp


def check_status():
    """Checks the status of an issuance & calculate late fee"""
    try:
        all_issuances = storage.all(Issuance).values()
        current_date = date.today()
        for issuance in all_issuances:
            if issuance.return_status != "returned" \
                    and issuance.due_date < current_date:
                issuance.return_status = "overdue"
                issuance.calculate_total_fee()
                issuance.save()
            elif issuance.return_status != "returned":
                issuance.return_status = "borrowed"
                issuance.calculate_total_fee()
                issuance.save()
    except Exception as e:
        return "Error: {}" .format(str(e))


@issuance_bp.route('/issuances', methods=['GET'])
@login_required
def view_issuances():
    """list all issuances"""
    try:
        check_status()
        issuances = storage.all(Issuance).values()
        issuances = sorted(issuances, key=lambda k: k.id)
        return render_template('view_issuances_form.html', issuances=issuances)
    except Exception as e:
        return "Error: {}".format(str(e))



@issuance_bp.route('/create_issuance', methods=['GET', 'POST'])
@login_required
def create_issuance():
    """creates an issuance based
    on data given in the form"""
    if request.method == 'POST':
        try:
            member_id = int(request.form.get('member'))
            book_ids = request.form.getlist('book')
            orders = request.form.getlist('quantity')
            total_fee = float(request.form.get('total_fee', 0.0))

            member = models.storage.get(Members, member_id)
            if not member:
                return "Member not found."
            if not member.can_make_issuance():
                return "Member is not eligible for issuance."

            books = []
            quantities = []
            for book_id, order in zip(book_ids, orders):
                book = models.storage.get(Books, int(book_id))
                if book:
                    if book.reduce_stock(int(order)):
                        books.append(book)
                        quantities.append(order)
                    else:
                        return "Book is not available "\
                            "in the required quantity."
                else:
                    return "Book not found"
            quantities_cpy = quantities.copy()
            books_borrowed = 0
            for q in quantities_cpy:
                books_borrowed += int(q)
            new_issuance = Issuance(
                member_id=member.id, books=books,
                contact_number=member.contact,
                total_fee=total_fee, books_borrowed=books_borrowed,
                due_date=request.form.get('due_date'))
            new_issuance.save()

            # Create the corresponding issuancebook
            for book_id, order in zip(book_ids, orders):
                book = models.storage.get(Books, int(book_id))
                if book:
                    new_issuance_book = IssuanceBooks(
                        issuance_id=new_issuance.id, books_id=book.id,
                        quantity=int(order))
                    new_issuance_book.save()
            return redirect(url_for(
                'issuance.issuance_template',
                issuance_id=new_issuance.id,
                quantities=quantities))
        except Exception as e:
            return "Error: {}".format(str(e))

    # Fetch members and books for dropdown lists
    members = models.storage.all(Members).values()
    books = models.storage.all(Books).values()

    return render_template(
        'create_issuance.html', members=members,
        books=books)



@issuance_bp.route('/issuance_template/<issuance_id>', methods=['GET'])
@login_required
def issuance_template(issuance_id):
    """return an issuance template based on
    the data given in issuance creation"""
    try:
        issuance_id = int(issuance_id)
        issuance = storage.get(Issuance, issuance_id)
        total_fee = issuance.total_fee
        if issuance:
            member_name = issuance.members.name
            books = issuance.books
            quantities = [int(q) for q in request.args.getlist('quantities')]
            total_books = 0
            for quantity in quantities:
                total_books += quantity
            return render_template(
                'issuance_template.html', issuance=issuance,
                member_name=member_name, books=books,
                quantities=quantities, total_books=total_books, total_fee=total_fee)
        else:
            return "Issunce not Found"
    except Exception as e:
        return "Error: {}".format(str(e))



@issuance_bp.route('/update_issuance_form/<issuance_id>', methods=['GET', 'POST'])
@login_required
def update_issuance_form(issuance_id):
    try:
        issuance_id = int(issuance_id)
        issuance = storage.get(Issuance, issuance_id)

        if request.method == 'POST':
            if issuance:
                # Retrieve updated values from the form
                return_status = request.form.get('return_status')
                member_id = int(request.form.get('member'))
                book_ids = request.form.getlist('book')
                orders = request.form.getlist('quantity')
                total_fee = request.form.get('total_fee') or 0

                # Fetch the member for the issuance
                member = models.storage.get(Members, member_id)

                # Calculate books borrowed
                total_quantity = 0
                for book_id, order in zip(book_ids, orders):
                    book = models.storage.get(Books, int(book_id))
                    if book:

                        total_quantity += int(order)
                    else:
                        return "Book not found"

                # Update issuance details
                issuance.return_status = return_status
                issuance.member_id = member.id
                issuance.books = [models.storage.get(Books, int(book_id)) for book_id in book_ids]
                issuance.contact_number = member.contact
                issuance.total_fee = total_fee
                issuance.due_date = request.form.get('due_date')
                issuance.books_borrowed = total_quantity
                issuance.save()

                # Update associated IssuanceBooks records
                for issuance_book in issuance.issued_books:
                    models.storage.delete(issuance_book)
                    
    
                for book_id, order in zip(book_ids, orders):
                    book = models.storage.get(Books, int(book_id))
                    if book:
                        list_books = issuance.issued_books
                        old_quantity = next((ib.quantity for ib in list_books if ib.books_id == int(book_id)), 0)
                        quantity_difference = int(order) - old_quantity
                        new_issuance_book = IssuanceBooks(
                            issuance_id=issuance.id, books_id=book.id,
                            quantity=int(order))
                        new_issuance_book.save()
                        
                        book.reduce_stock(quantity_difference)
                        models.storage.save()

                # Update current stock after a book return
                if issuance.return_status == "returned":
                    for book_id, order in zip(book_ids, orders):
                        book = models.storage.get(Books, int(book_id))
                        if book:
                            book.current_stock += int(order)
                            models.storage.save()

                return redirect(url_for('issuance.view_issuances'))
            else:
                return "Issuance not found"

        elif request.method == 'GET':
            if issuance:
                # Fetch members and books for dropdown lists
                members = models.storage.all(Members).values()
                books = models.storage.all(Books).values()

                # Fetch quantities and books for the existing issuance
                quantities = [issuance_book.quantity for issuance_book in issuance.issued_books]
                list_books = issuance.issued_books

                return render_template(
                    'update_issuance_form.html', issuance=issuance,
                    members=members, books=books,
                    list_books=list_books, quantities=quantities)
            else:
                return "Issuance not found"

    except Exception as e:
        return "Error: {}".format(str(e))



@issuance_bp.route('/view_issuance_template/<issuance_id>', methods=['GET', 'POST'])
@login_required
def view_issuance_template(issuance_id):
    """displays issuance template of an already
    existing issuance"""
    quantities = []
    list_books = []
    issuance = storage.get(Issuance, int(issuance_id))
    issuance_issued_books = storage.all(IssuanceBooks).values()
    for issuance_book in issuance_issued_books:
        if issuance_book.issuance_id == int(issuance_id):
            quantities.append(issuance_book.quantity)
            list_books.append(issuance_book)
    return render_template('view_issuance_template.html', list_books=list_books, issuance=issuance, quantities=quantities)



@issuance_bp.route(
    '/delete_issuance/<issuance_id>', methods=['GET', 'POST'])
@login_required
def delete_issuance(issuance_id):
    """allows librarian to delete a record
    of an issuance"""
    try:
        issuance = storage.get(Issuance, int(issuance_id))
        if issuance:
            storage.delete(issuance)
            storage.save()
        return redirect(url_for('issuance.view_issuances'))
    except Exception as e:
        return "Error: {}".format(str(e))



@issuance_bp.route(
    '/download_issuance_pdf/<issuance_id>', methods=['GET'])
@login_required
def download_issuance_pdf(issuance_id):
    """allows for the downloading of an issuance"""
    try:
        issuance_id = int(issuance_id)
        issuance = storage.get(Issuance, issuance_id)
        quantities_param = request.args.getlist('quantities')
        if issuance:
            if quantities_param:
                quantities = [int(q) for q in quantities_param]
            else:
                quantities = []
            rendered_template = render_template(
                'issuance_template.html', issuance=issuance,
                books=issuance.books, quantities=quantities,
                total_books=request.args.get('total_books'), total_fee=request.args.get('total_fee'))

            pdf = HTML(string=rendered_template).write_pdf()
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = f'inline; '\
                'filename=issuance_{issuance_id}.pdf'

            return response

        else:
            return "Issuance not found"
    except Exception as e:
        return "Error: {}".format(str(e))
