from flask import Blueprint, render_template, request,  flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db

import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if not note or len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id) # type: ignore
            db.session.add(new_note) # type: ignore
            db.session.commit() # type: ignore
            flash('Note added!', category='success')
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note_to_delete = Note.query.get(noteId)
    if note_to_delete:
        db.session.delete(note_to_delete)
        db.session.commit()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}
