import sys
print("Python version:", sys.version)

try:
    import flask
    print("Flask version:", flask.__version__)
except ImportError as e:
    print("Flask import error:", e)

try:
    import flask_sqlalchemy
    print("Flask-SQLAlchemy imported successfully")
except ImportError as e:
    print("Flask-SQLAlchemy import error:", e)

try:
    import flask_restful
    print("Flask-RESTful imported successfully")
except ImportError as e:
    print("Flask-RESTful import error:", e)