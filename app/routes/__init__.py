from flask import Blueprint

# 初始化所有 Blueprint
bp_main = Blueprint('main', __name__)
bp_subjects = Blueprint('subjects', __name__, url_prefix='/subjects')
bp_notes = Blueprint('notes', __name__)
bp_summary = Blueprint('summary', __name__)
bp_export = Blueprint('export', __name__)
bp_tags = Blueprint('tags', __name__, url_prefix='/tags')
bp_share = Blueprint('share', __name__)
bp_admin = Blueprint('admin', __name__, url_prefix='/admin')

def init_app(app):
    # import routes sequentially to ensure execution of decorators
    from . import main, subjects, notes, summary, export, tags, share, admin
    
    app.register_blueprint(bp_main)
    app.register_blueprint(bp_subjects)
    app.register_blueprint(bp_notes)
    app.register_blueprint(bp_summary)
    app.register_blueprint(bp_export)
    app.register_blueprint(bp_tags)
    app.register_blueprint(bp_share)
    app.register_blueprint(bp_admin)
