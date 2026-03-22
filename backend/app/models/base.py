from sqlalchemy.orm import declarative_base

# Single shared Base for ALL SQLAlchemy models.
# Import this Base in every model file and in Alembic's env.py
# so that all tables are discovered during migrations.
Base = declarative_base()
