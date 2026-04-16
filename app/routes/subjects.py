from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import bp_subjects

@bp_subjects.route('/create', methods=['GET', 'POST'])
def create_subject():
    """
    建立科目
    GET: 顯示表單
    POST: 接收資料並存入資料庫
    """
    pass

@bp_subjects.route('/<int:subject_id>', methods=['GET'])
def subject_detail(subject_id):
    """
    科目詳細頁：顯示該科目下所有的筆記清單
    """
    pass

@bp_subjects.route('/<int:subject_id>/delete', methods=['POST'])
def delete_subject(subject_id):
    """
    刪除科目及其所有相關筆記
    """
    pass
