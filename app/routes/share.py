from flask import Blueprint, render_template, request, redirect, url_for
from . import bp_share

@bp_share.route('/notes/<int:note_id>/share', methods=['POST'])
def generate_share_link(note_id):
    """
    為指定筆記產生一組帶有 UUID token 的共用連結 (設定唯讀或編輯權限)
    """
    pass

@bp_share.route('/share/<string:token>', methods=['GET'])
def access_share_link(token):
    """
    透過 token 存取共用筆記
    驗證通過後，依權限返回唯讀或編輯頁面
    """
    pass

@bp_share.route('/share/<string:token>/save', methods=['POST'])
def save_share_note(token):
    """
    共用者(具有編輯權限)儲存更新後的筆記內容
    """
    pass
