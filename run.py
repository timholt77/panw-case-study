from app.app import app
from app.db import init_db, seed_db_from_json

if __name__ == '__main__':
    init_db()
    seed_db_from_json()
    app.run(debug=True)
