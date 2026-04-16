from flask import Blueprint, render_template, request, redirect, url_for
from . import bp_tags

@bp_tags.route('/', methods=['GET'])
def tag_list():
    """
    管理所有標籤頁面
    """
    pass

@bp_tags.route('/create', methods=['POST'])
def create_tag():
    """
    建立自訂標籤 (名稱、顏色)
    """
    pass

@bp_tags.route('/<int:tag_id>/notes', methods=['GET'])
def notes_by_tag(tag_id):
    """
    依標籤篩選出相關筆記
    """
    pass
