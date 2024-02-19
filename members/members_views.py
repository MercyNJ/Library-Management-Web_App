#!/usr/bin/python3
from . import members_bp
from flask import Flask, render_template, jsonify, url_for, request, redirect
from flask_login import login_required
import models
from models.members import Members
from models.issuance import Issuance
from models import storage

@members_bp.route('/members', methods=['GET'])
def view_members():
    """list all the library members in database"""
    try:
        members = storage.all(Members).values()
        members = sorted(members, key=lambda k: k.id)
        return render_template(
            'view_members.html', members=members)
    except Exception as e:
        return "Error fetching member data: {}".format(str(e))

@members_bp.route(
    '/add_members_form', methods=['GET', 'POST'],
    strict_slashes=False)
@login_required
def add_members_form():
    """allows the librarian to add member to the record"""
    if request.method == 'POST':
        try:
            members_name = request.form.get('members_name')
            members_email = request.form.get('members_email')
            members_contact = request.form.get('members_contact')
            new_member = Members(
                name=members_name, email=members_email,
                contact=members_contact)
            new_member.save()
            return redirect(url_for('members.view_members'))
        except Exception as e:
            return "Error: {}".format(str(e))
    return render_template('add_members_form.html')



@members_bp.route(
    '/update_members_form/<members_id>',
    methods=['GET', 'POST'])
@login_required
def update_members_form(members_id):
    """allow update of member already existing data"""
    members_id = int(members_id)
    member = storage.get(Members, members_id)
    if request.method == 'POST':
        try:
            if member:
                member.name = request.form.get('members_name')
                member.email = request.form.get('members_email')
                member.contact = request.form.get('members_contact')
                member.save()
                return redirect(url_for('members.view_members'))
            else:
                return "Member not found"
        except Exception as e:
            return "Error: {}".format(str(e))
    elif request.method == 'GET':
        if member:
            return render_template(
                'update_members_form.html', member=member)
        else:
            return "Member not found"



@members_bp.route('/delete_member/<member_id>', methods=['GET', 'POST'])
@login_required
def delete_member(member_id):
    """deletes a record of a member"""
    try:
        member = storage.get(Members, int(member_id))
        if member:
            storage.delete(member)
            storage.save()
        return redirect(url_for('members.view_members'))
    except Exception as e:
        return "Error: {}".format(str(e))

