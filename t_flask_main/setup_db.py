from t_flask import app, db

with app.app_context():
    try:
        db.create_all()
        print("Database created successfully!")
    except Exception as e:
        print(f"Error: {e}")
