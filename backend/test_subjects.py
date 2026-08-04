from app import app
from models.subject import Subject

with app.app_context():

    print("=" * 40)

    for subject in Subject.query.all():
        print(subject.subject_code)

    print("=" * 40)