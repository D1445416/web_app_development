from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.tag import Tag
from . import bp_tags

@bp_tags.route('/', methods=['GET'])
def tag_list():
    """
    管理所有標籤頁面
    """
    tags = Tag.get_all()
    return render_template('tags/list.html', tags=tags)

@bp_tags.route('/create', methods=['POST'])
def create_tag():
    """
    建立自訂標籤 (名稱、顏色)
    """
    name = request.form.get('name', '').strip()
    color = request.form.get('color', '#8b5cf6') # Default to a nice purple if not provided
    if name:
        try:
            Tag.create(name=name, color=color)
            flash('標籤建立成功', 'success')
        except Exception as e:
            flash(f'錯誤: {str(e)}', 'danger')
    else:
        flash('標籤名稱不能留白', 'danger')
    return redirect(url_for('tags.tag_list'))

@bp_tags.route('/<int:tag_id>/notes', methods=['GET'])
def notes_by_tag(tag_id):
    """
    依標籤篩選出相關筆記
    """
    tag = Tag.get_by_id(tag_id)
    if not tag:
        flash('標籤不存在', 'danger')
        return redirect(url_for('tags.tag_list'))
    return render_template('tags/notes_by_tag.html', tag=tag, notes=tag.notes.all())
