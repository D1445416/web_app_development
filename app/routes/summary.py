from flask import Blueprint, render_template
from . import bp_summary

@bp_summary.route('/subjects/<int:subject_id>/summary', methods=['GET'])
def subject_summary(subject_id):
    """
    檢視科目統整摘要
    提取所有筆記並呈現整合視圖
    """
    pass
