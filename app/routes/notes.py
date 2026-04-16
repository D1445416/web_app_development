from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import bp_notes

@bp_notes.route('/subjects/<int:subject_id>/notes/create', methods=['GET', 'POST'])
def create_note(subject_id):
    """
    建立筆記
    GET: 顯示富文本編輯器
    POST: 儲存筆記內容至指定科目
    """
    pass

@bp_notes.route('/notes/<int:note_id>', methods=['GET'])
def view_note(note_id):
    """
    閱讀單筆筆記
    """
    pass

@bp_notes.route('/notes/<int:note_id>/edit', methods=['GET', 'POST'])
def edit_note(note_id):
    """
    編輯筆記
    GET: 載入內容至編輯器
    POST: 儲存更新的內容
    """
    pass

@bp_notes.route('/notes/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    """
    刪除指定筆記
    """
    pass

@bp_notes.route('/notes/<int:note_id>/tags', methods=['POST'])
def add_note_tag(note_id):
    """
    為筆記增加標籤
    """
    pass
