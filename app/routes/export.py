from flask import Blueprint, send_file, Response, redirect, url_for, flash
from app.models.note import Note
from . import bp_export

@bp_export.route('/notes/<int:note_id>/export/pdf', methods=['GET'])
def export_pdf(note_id):
    """
    將筆記匯出為 PDF 檔案下載
    (MVP: 退回瀏覽器端使用 JavaScript 列印輸出)
    """
    from flask import render_template
    note = Note.get_by_id(note_id)
    if not note:
        flash('找不到筆記', 'danger')
        return redirect(url_for('main.index'))
    # 返回一個適合被直接列印 (window.print()) 成 PDF 的樣板
    return render_template('notes/export_print.html', note=note)

@bp_export.route('/notes/<int:note_id>/export/md', methods=['GET'])
def export_md(note_id):
    """
    將筆記匯出為 Markdown 檔案下載
    """
    note = Note.get_by_id(note_id)
    if not note:
        flash('找不到筆記', 'danger')
        return redirect(url_for('main.index'))
        
    # 將標題跟原始內容整合為簡單格式 (以 MVP 作為考量)
    md_content = f"# {note.title}\n\n"
    if note.content:
        # 在正式轉換時，HTML -> Markdown 可以使用 HTML2Text 取代，此處以原始匯出替代
        md_content += str(note.content).replace('<h1>', '# ').replace('</h1>', '\n').replace('<p>', '').replace('</p>', '\n\n')
        
    return Response(
        md_content,
        mimetype="text/markdown",
        headers={"Content-disposition": f"attachment; filename=note-{note.id}.md"}
    )
