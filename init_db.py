from app import create_app
import app
app = create_app()
db=app.config['qmdb']
db.create_all()
