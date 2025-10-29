from app import create_app, db

# Create Flask app
app = create_app()

# Create all tables
with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Tables created successfully!")
    
    # List all tables
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"Created tables: {tables}")