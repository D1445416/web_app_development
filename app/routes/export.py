from flask import Blueprint, send_file
from . import bp_export

@bp_export.route('/notes/<int:note_id>/export/pdf', methods=['GET'])
def export_pdf(note_id):
    """
    將筆記匯出為 PDF 檔案下載
    """
    pass

@bp_export.route('/notes/<int:note_id>/export/md', methods=['GET'])
def export_md(note_id):
    """
    將筆記匯出為 Markdown 檔案下載
    """
    pass
