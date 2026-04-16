from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.admin import Admin
from app.models.note import Note
from app.models.share_link import ShareLink
from . import bp_admin
import functools

def admin_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('需具備管理員權限', 'warning')
            return redirect(url_for('admin.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@bp_admin.route('/login', methods=['GET', 'POST'])
def admin_login():
    """
    管理員登入
    GET: 顯示登入表單
    POST: 驗證帳密並下發 session
    """
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        admin_user = Admin.get_by_username(username)
        if admin_user and admin_user.check_password(password):
            session['is_admin'] = True
            flash('管理者已登入', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('帳號或登入密碼不正確', 'danger')
            
    return render_template('admin/login.html')

@bp_admin.route('/logout', methods=['POST'])
def admin_logout():
    """
    清除 session 並登出，重導回首頁
    """
    session.pop('is_admin', None)
    flash('管理系統登出完畢', 'success')
    return redirect(url_for('main.index'))

@bp_admin.route('/dashboard', methods=['GET'])
@admin_required
def dashboard():
    """
    管理後台首頁
    """
    note_count = Note.query.count()
    link_count = ShareLink.query.count()
    return render_template('admin/dashboard.html', note_count=note_count, link_count=link_count)

@bp_admin.route('/notes', methods=['GET'])
@admin_required
def manage_notes():
    """
    列出系統中所有筆記供管理員檢視
    """
    notes = Note.get_all()
    return render_template('admin/notes.html', notes=notes)

@bp_admin.route('/notes/<int:note_id>/delete', methods=['POST'])
@admin_required
def force_delete_note(note_id):
    """
    管理員強制刪除特定筆記
    """
    note = Note.get_by_id(note_id)
    if note:
        try:
            note.delete()
            flash('強力抹除筆記成功', 'success')
        except Exception as e:
            flash(f'刪除發生錯誤: {str(e)}', 'danger')
    return redirect(url_for('admin.manage_notes'))

@bp_admin.route('/links', methods=['GET'])
@admin_required
def manage_links():
    """
    查看所有被分享的共用連結
    """
    links = ShareLink.get_all()
    return render_template('admin/links.html', links=links)

@bp_admin.route('/links/<int:link_id>/revoke', methods=['POST'])
@admin_required
def revoke_link(link_id):
    """
    撤銷(停用/刪除)指定的共用連結
    """
    link = ShareLink.query.get(link_id)
    if link:
        try:
            link.delete()
            flash('授權連結已撤銷失效', 'success')
        except Exception as e:
            flash(f'操作失敗: {str(e)}', 'danger')
    return redirect(url_for('admin.manage_links'))
