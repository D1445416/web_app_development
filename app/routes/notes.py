from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.subject import Subject
from app.models.note import Note
from app.models.tag import Tag
from app.models.note_tag import NoteTag
from . import bp_notes

@bp_notes.route('/subjects/<int:subject_id>/notes/create', methods=['GET', 'POST'])
def create_note(subject_id):
    """
    建立筆記
    GET: 顯示富文本編輯器
    POST: 儲存筆記內容至指定科目
    """
    subject = Subject.get_by_id(subject_id)
    if not subject:
        flash('科目不存在', 'danger')
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '')
        if not title:
            flash('標題為必填項目', 'danger')
            return redirect(url_for('notes.create_note', subject_id=subject.id))
        try:
            note = Note.create(subject_id=subject.id, title=title, content=content)
            flash('筆記新增成功', 'success')
            return redirect(url_for('notes.view_note', note_id=note.id))
        except Exception as e:
            flash(f'建立失敗: {str(e)}', 'danger')
            
    return render_template('notes/create.html', subject=subject)

@bp_notes.route('/notes/<int:note_id>', methods=['GET'])
def view_note(note_id):
    """
    閱讀單筆筆記
    """
    note = Note.get_by_id(note_id)
    if not note:
        flash('找不到筆記', 'danger')
        return redirect(url_for('main.index'))
    tags = Tag.get_all() # 用於顯示新增標籤的選單
    return render_template('notes/view.html', note=note, all_tags=tags)

@bp_notes.route('/notes/<int:note_id>/edit', methods=['GET', 'POST'])
def edit_note(note_id):
    """
    編輯筆記
    GET: 載入內容至編輯器
    POST: 儲存更新的內容
    """
    note = Note.get_by_id(note_id)
    if not note:
        flash('找不到筆記', 'danger')
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '')
        if not title:
            flash('標題為必填項目', 'danger')
            return redirect(url_for('notes.edit_note', note_id=note.id))
        try:
            note.update(title=title, content=content)
            flash('編輯保存成功', 'success')
            return redirect(url_for('notes.view_note', note_id=note.id))
        except Exception as e:
            flash(f'保存失敗: {str(e)}', 'danger')
            
    return render_template('notes/edit.html', note=note)

@bp_notes.route('/notes/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    """
    刪除指定筆記
    """
    note = Note.get_by_id(note_id)
    if note:
        subject_id = note.subject_id
        try:
            note.delete()
            flash('刪除成功', 'success')
        except Exception as e:
            flash(f'刪除失敗: {str(e)}', 'danger')
        return redirect(url_for('subjects.subject_detail', subject_id=subject_id))
    flash('筆記不存在', 'danger')
    return redirect(url_for('main.index'))

@bp_notes.route('/notes/<int:note_id>/tags', methods=['POST'])
def add_note_tag(note_id):
    """
    為筆記增加標籤
    """
    note = Note.get_by_id(note_id)
    tag_id = request.form.get('tag_id')
    if note and tag_id:
        try:
            NoteTag.create(note_id=note.id, tag_id=int(tag_id))
            flash('標籤貼上成功', 'success')
        except BaseException:
            flash('標籤已存在或錯誤', 'danger')
    return redirect(url_for('notes.view_note', note_id=note_id))
