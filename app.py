from flask import Flask, logging, render_template
import os
from dotenv import load_dotenv
from blueprints.user.routes import user_bp
from blueprints.blog.routes import blog_bp
from blueprints.errors.routes import error_bp
from extensions import db, migrate, ckeditor
from models import Post, login_manager
import psycopg2

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG')
    
    if not app.debug:
        app.logger.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(error_bp)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    ckeditor.init_app(app)

    app.logger.info('Flask app created and initialized')      
    return app

app = create_app()

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run()
    
