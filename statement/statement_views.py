#!/usr/bin/python3
from . import statement_bp
from flask import Flask, render_template, request
from flask import redirect, url_for, Response
from flask_weasyprint import HTML
from flask_login import login_required
from models.statement import Statement
from models.issuance import Issuance
from models.members import Members
from models import storage

@statement_bp.route('/open_issuances', methods=['GET'])
@login_required
def view_open_issuances():
    """Handle the request to view open issuances."""
    try:
        issuances = storage.all(Issuance).values()
        open_issuances = []

        for iss in issuances:
            iss.issuance_status()

            if (iss.return_status == "borrowed" or
                    iss.return_status == "overdue"):
                open_issuances.append(iss)
        outstanding_fee = sum(
            iss.total_fee for iss in open_issuances)
        return render_template(
            'open_issuances.html', open_issuances=open_issuances,
             outstanding_fee= outstanding_fee)
    except Exception as e:
        return "Error viewing open issuances: {}".format(str(e))



@statement_bp.route('/search_open_issuances', methods=['POST'])
@login_required
def search_open_issuances():
    """Handle the search for open issuances by member name or ID."""
    try:
        search_term = request.form.get('search')
        issuances = storage.all(Issuance).values()
        open_issuances = []
        for iss in issuances:
            iss.issuance_status()
            if (iss.return_status == "borrowed" or
                    iss.return_status == "overdue"):
                open_issuances.append(iss)

        member = None
        search_term_lower = search_term.lower()
        if search_term.isdigit():
            member_id = int(search_term)
            member = storage.get(Members, member_id)
        else:
            members = storage.all(Members).values()
            for memb in members:
                if memb.name.lower().split()[0] == search_term_lower:
                    member = memb

        issuances_per_member = []
        if member:
            for member_issuance in open_issuances:
                if (member_issuance.members.name.lower() == member.name
                .lower() or
                member_issuance.members.id == member.id):
                    issuances_per_member.append(member_issuance)
            return render_template(
                'view_member_open_issuances.html',
                member=member, issuances=issuances_per_member)
        else:
            return "Member not found"
    except Exception as e:
        return "Error searching open issuances: {}".format(str(e))



@statement_bp.route('/generate_statement', methods=['GET'])
@login_required
def generate_statement():
    """Generation of statement of a member"""
    try:
        all_issuances = storage.all(Issuance).values()
        member_id = request.args.get('member_id')
        member = storage.get(Members, int(member_id))
        issuances = []
        issuances_per_member = []
        for issuance in all_issuances:
            issuance.issuance_status()
            if (issuance.return_status == "borrowed" or
                    issuance.return_status == "overdue"):
                issuances.append(issuance)

        for iss in issuances:
            if iss.member_id == int(member_id):
                issuances_per_member.append(iss)
        outstanding_fee = sum(i.total_fee for i in issuances_per_member)
        statement = Statement(
                member_name=member.name,
                outstanding_fee= outstanding_fee, issuances=issuances_per_member)
        statement.save()
        return render_template(
                'generate_statement.html', date_created=statement.created_at,
                statement=statement)
    except Exception as e:
        return "Error generating statement: {}".format(str(e))



@statement_bp.route('/download_statement_pdf/<statement_id>')
@login_required
def download_statement_pdf(statement_id):
    """Handle request to download a statement of issuance in PDF format."""
    try:
        statement = storage.get(Statement, int(statement_id))
        if statement is None:
            return "Statement not found", 404
        html = render_template(
                'generate_statement.html', date_created=statement.created_at,
                statement=statement)
        pdf = HTML(string=html).write_pdf()

        response = Response(pdf, content_type='application/pdf')
        response.headers[
                'Content-Disposition'] = (
                        f'attachment; filename=statement_{statement_id}.pdf')

        return response
    except Exception as e:
        return "Error downloading statement PDF: {}".format(str(e))
