from flask import Blueprint, render_template, request, flash
from app.models.subject import Subject
from app.models.note import Note
from . import bp_main

@bp_main.route('/')
def index():
    """
    首頁：顯示所有科目列表
    """
    subjects = Subject.get_all()
    return render_template('index.html', subjects=subjects)

@bp_main.route('/search', methods=['GET'])
def search():
    """
    全文搜尋筆記
    參數: q (查詢關鍵字)
    """
    q = request.args.get('q', '').strip()
    notes = []
    if q:
        notes = Note.query.filter(
            (Note.title.ilike(f'%{q}%')) | (Note.content.ilike(f'%{q}%'))
        ).order_by(Note.created_at.desc()).all()
    return render_template('search.html', notes=notes, q=q)
