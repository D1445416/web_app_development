from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from . import bp_admin

@bp_admin.route('/login', methods=['GET', 'POST'])
def admin_login():
    """
    管理員登入
    GET: 顯示登入表單
    POST: 驗證帳密並下發 session
    """
    pass

@bp_admin.route('/logout', methods=['POST'])
def admin_logout():
    """
    清除 session 並登出，重導回首頁
    """
    pass

@bp_admin.route('/dashboard', methods=['GET'])
def dashboard():
    """
    管理後台首頁
    """
    pass

@bp_admin.route('/notes', methods=['GET'])
def manage_notes():
    """
    列出系統中所有筆記供管理員檢視
    """
    pass

@bp_admin.route('/notes/<int:note_id>/delete', methods=['POST'])
def force_delete_note(note_id):
    """
    管理員強制刪除特定筆記
    """
    pass

@bp_admin.route('/links', methods=['GET'])
def manage_links():
    """
    查看所有被分享的共用連結
    """
    pass

@bp_admin.route('/links/<int:link_id>/revoke', methods=['POST'])
def revoke_link(link_id):
    """
    撤銷(停用/刪除)指定的共用連結
    """
    pass
