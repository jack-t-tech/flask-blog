from flask import Blueprint, render_template

error_bp = Blueprint('error', __name__, template_folder='templates')

# Error Handling


@error_bp.app_errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html', error=e), 500

@error_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html', error=e), 404