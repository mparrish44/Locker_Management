from app import db, create_app
from app.models import HomePageContent, Building, Locker, User
from datetime import datetime
import random

app = create_app()

with app.app_context():
    print("Seeding database...")

    # --- Seed HomePageContent ---
    welcome_section = HomePageContent(
        title="Welcome",
        content="""
        <h1>Walker-Parrish Locker Registration</h1>
        <p>Manage locker assignments, scheduling, and more with simplicity and ease.</p>
        <a href='/register_student' class='btn btn-primary mt-4'>Get Started</a>
        """
    )

    features_section = HomePageContent(
        title="Features",
        content="""
        <div class='row text-center'>
            <div class='col-md-4 mb-4'>
                <div class='card p-4 border-0 shadow-sm'>
                    <i class='bi bi-lock-fill text-primary mb-3' style='font-size: 3rem;'></i>
                    <h4>Secure Lockers</h4>
                    <p>Efficient and reliable security features ensure your lockers remain safe at all times.</p>
                </div>
            </div>
            <div class='col-md-4 mb-4'>
                <div class='card p-4 border-0 shadow-sm'>
                    <i class='bi bi-calendar-check-fill text-primary mb-3' style='font-size: 3rem;'></i>
                    <h4>Easy Scheduling</h4>
                    <p>Quickly register and manage locker schedules to keep your belongings organized.</p>
                </div>
            </div>
            <div class='col-md-4 mb-4'>
                <div class='card p-4 border-0 shadow-sm'>
                    <i class='bi bi-people-fill text-primary mb-3' style='font-size: 3rem;'></i>
                    <h4>User-Friendly Design</h4>
                    <p>An intuitive interface ensures you spend less time navigating and more time achieving.</p>
                </div>
            </div>
        </div>
        """
    )

    future_section = HomePageContent(
        title="What’s Next?",
        content="""
        <h2>What’s Next?</h2>
        <p>Stay tuned for upcoming features and exciting updates to enhance your locker management experience!</p>
        """
    )

    db.session.add(welcome_section)
    db.session.add(features_section)
    db.session.add(future_section)
    db.session.commit()
    print("HomePageContent seeded.")

    # --- Seed Buildings ---
    buildings_data = ["Main Hall", "Science Building", "Arts Center", "Gymnasium"]
    for name in buildings_data:
        if not Building.query.filter_by(name=name).first():
            building = Building(name=name)
            db.session.add(building)
    db.session.commit()
    buildings = Building.query.all()
    print("Buildings seeded.")

    # --- Seed Lockers ---
    for building in buildings:
        for floor in range(1, 4):
            for section in ["A", "B"]:
                for i in range(1, 11):
                    locker_number = f"{i:02d}"
                    if not Locker.query.filter_by(building_id=building.id, floor=str(floor), locker_number=locker_number, section=section).first():
                        locker = Locker(building_id=building.id, floor=str(floor), locker_number=locker_number, section=section)
                        db.session.add(locker)
    db.session.commit()
    print("Lockers seeded.")

    # --- Seed Students ---
    for i in range(1, 21):
        first_name = f"Student{i}"
        last_name = "Test"
        email = f"student{i}@example.com"
        if not User.query.filter_by(email=email).first():
            student = User(first_name=first_name, last_name=last_name, email=email, password='password', is_admin=False)
            db.session.add(student)
    db.session.commit()
    students = User.query.filter_by(is_admin=False).all()
    lockers = Locker.query.all()
    print("Students seeded.")

    # --- Seed Teachers (Example - You can adjust the number) ---
    teacher = User(first_name="Admin", last_name="User", email="admin@example.com", password='admin', is_admin=True)
    if not User.query.filter_by(email="admin@example.com").first():
        db.session.add(teacher)
        db.session.commit()
        print("Admin teacher seeded.")

    # --- Assign Some Lockers ---
    available_lockers = list(Locker.query.filter_by(assigned_user_id=None).all())
    random.shuffle(students)
    num_to_assign = min(len(students), len(available_lockers))

    for i in range(num_to_assign):
        if available_lockers:  # Ensure there are still available lockers
            locker_to_assign = available_lockers.pop() # Get and remove a locker
            student_to_assign = students[i % len(students)] # Cycle through students if needed
            locker_to_assign.assigned_user_id = student_to_assign.id
            locker_to_assign.assignment_date = datetime.utcnow()
    db.session.commit()
    print(f"{num_to_assign} lockers assigned.")

    print("Database seeding complete.")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        pass