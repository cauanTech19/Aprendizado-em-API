from app import create_app
import os
from models import db


if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        db.create_all()

    if __name__ == '__main__':    
        app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False) 
    
