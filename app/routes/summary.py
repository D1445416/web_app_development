from flask import Blueprint, render_template, redirect, url_for, flash
from app.models.subject import Subject
from . import bp_summary

@bp_summary.route('/subjects/<int:subject_id>/summary', methods=['GET'])
def subject_summary(subject_id):
    """
    檢視科目統整摘要
    提取所有筆記並呈現整合視圖
    """
    subject = Subject.get_by_id(subject_id)
    if not subject:
        flash('找不到該科目資訊', 'danger')
        return redirect(url_for('main.index'))
    return render_template('notes/summary.html', subject=subject)
