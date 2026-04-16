from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.note import Note
from app.models.share_link import ShareLink
from . import bp_share

@bp_share.route('/notes/<int:note_id>/share', methods=['POST'])
def generate_share_link(note_id):
    """
    為指定筆記產生一組帶有 UUID token 的共用連結 (設定唯讀或編輯權限)
    """
    note = Note.get_by_id(note_id)
    if not note:
        flash('找不到該筆記', 'danger')
        return redirect(url_for('main.index'))
        
    permission = request.form.get('permission', 'read')
    if permission not in ['read', 'edit']:
        permission = 'read'
        
    try:
        link = ShareLink.create(note_id=note.id, permission=permission)
        flash(f'已建立共用連結，權限為 {permission}', 'success')
    except Exception as e:
        flash(f'建立連結時失敗: {str(e)}', 'danger')
        
    return redirect(url_for('notes.view_note', note_id=note.id))

@bp_share.route('/share/<string:token>', methods=['GET'])
def access_share_link(token):
    """
    透過 token 存取共用筆記
    驗證通過後，依權限返回唯讀或編輯頁面
    """
    link = ShareLink.get_by_token(token)
    if not link:
        # 可以設計一個通用錯誤頁面
        return render_template('error.html', message='此共用連結無效或已過期。'), 404
        
    note = Note.get_by_id(link.note_id)
    if not note:
        return render_template('error.html', message='原始筆記不存在。'), 404
        
    if link.permission == 'edit':
        return render_template('notes/share_edit.html', note=note, token=token)
    else:
        return render_template('notes/share_view.html', note=note)

@bp_share.route('/share/<string:token>/save', methods=['POST'])
def save_share_note(token):
    """
    共用者(具有編輯權限)儲存更新後的筆記內容
    """
    link = ShareLink.get_by_token(token)
    if not link or link.permission != 'edit':
        return render_template('error.html', message='這個連結不具備編輯權限。'), 403
        
    note = Note.get_by_id(link.note_id)
    if not note:
        return render_template('error.html', message='原始筆記不存在。'), 404
        
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '')
    
    if title:
        try:
            note.update(title=title, content=content)
            flash('您已成功更新筆記內容', 'success')
        except Exception as e:
            flash(f'保存更新失敗: {str(e)}', 'danger')
    else:
        flash('標題為必填項目', 'danger')
        
    return redirect(url_for('share.access_share_link', token=token))
