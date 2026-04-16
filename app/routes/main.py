from flask import Blueprint, render_template, request
from . import bp_main

@bp_main.route('/')
def index():
    """
    首頁：顯示所有科目列表
    """
    pass

@bp_main.route('/search', methods=['GET'])
def search():
    """
    全文搜尋筆記
    參數: q (查詢關鍵字)
    """
    pass
