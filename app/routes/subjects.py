from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.subject import Subject
from . import bp_subjects

@bp_subjects.route('/create', methods=['GET', 'POST'])
def create_subject():
    """
    建立科目
    GET: 顯示表單
    POST: 接收資料並存入資料庫
    """
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            flash('科目名稱為必填項目', 'danger')
            return redirect(url_for('subjects.create_subject'))
        try:
            Subject.create(name=name)
            flash('新增科目成功', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            flash(f'發生錯誤: {str(e)}', 'danger')
    return render_template('subjects/create.html')

@bp_subjects.route('/<int:subject_id>', methods=['GET'])
def subject_detail(subject_id):
    """
    科目詳細頁：顯示該科目下所有的筆記清單
    """
    subject = Subject.get_by_id(subject_id)
    if not subject:
        flash('找不到該科目', 'danger')
        return redirect(url_for('main.index'))
    return render_template('subjects/detail.html', subject=subject)

@bp_subjects.route('/<int:subject_id>/delete', methods=['POST'])
def delete_subject(subject_id):
    """
    刪除科目及其所有相關筆記
    """
    subject = Subject.get_by_id(subject_id)
    if subject:
        try:
            subject.delete()
            flash('科目刪除成功', 'success')
        except Exception as e:
            flash(f'刪除時發生錯誤: {str(e)}', 'danger')
    else:
        flash('找不到該科目', 'danger')
    return redirect(url_for('main.index'))
