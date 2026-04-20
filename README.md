# Gym Tracker 🏋️‍♂️

Gym Tracker is a Django web app for logging workouts and tracking gym progress. I built this as my main portfolio project during a Python Developer bootcamp. Before jumping into IT, I studied Automation and Robotics, which gave me a solid technical foundation for programming.

## 🚀 Features

* **User Accounts:** Standard registration and login functionality.
* **Workout Management:** Creating, editing, and deleting workouts (adding specific exercises, sets, reps, and weights).
* **Exercise History:** You can click on a specific exercise to see exactly when and how you performed it in the past.
* **Search & Filtering:** Filtering exercises by categories (e.g., Chest, Back, Cardio) and searching through past workouts.
* **Pre-loaded Database:** The app comes with 12 muscle categories and 41 default exercises out of the box. I used custom Django Data Migrations (`RunPython`) to seed this data automatically instead of relying on standard JSON fixtures.
* **UI:** Clean, responsive interface built with HTML, CSS, and Bootstrap.

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Database:** SQLite
* **Frontend:** HTML, CSS, Bootstrap

## 📸 Snapshot

![Home Page](docs/home_page.jpg)

## ⚙️ How to run locally

**1. Clone the repository and navigate to the project directory:**
```bash
git clone [https://github.com/Darmi555/gym-tracker](https://github.com/Darmi555/gym-tracker)
cd gym-tracker
```

**2. Create and activate a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Run migrations (This automatically populates Categories and Exercises):**
```bash
python manage.py migrate
```

**5. Load test user data (Includes a user with 25 pre-generated workouts for testing):**
```bash
python manage.py loaddata seed_data.json
```
*Note: You can log in using the credentials: `testuser` / `testpass123`*

**6. Create an admin account (Optional):**
```bash
python manage.py createsuperuser
```

**7. Run the development server:**
```bash
python manage.py runserver
```
*Navigate to `http://127.0.0.1:8000` in your browser.*