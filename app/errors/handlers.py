from flask import render_template, current_app
from app.errors import errors_bp


@errors_bp.app_errorhandler(404)
def not_found_error(error):
    current_app.logger.error('File not found')
    return render_template('errors/404.html'), 404


@errors_bp.app_errorhandler(500)
def internal_error(error):
    current_app.logger.error('server error')
    return render_template('errors/500.html'), 500
