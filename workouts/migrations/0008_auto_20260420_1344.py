from django.db import migrations


def load_initial_data(apps, schema_editor):
    Category = apps.get_model('workouts', 'Category')
    Exercise = apps.get_model('workouts', 'Exercise')

    categories_data = [
        "Chest", "Back", "Shoulders", "Biceps", "Triceps", "Quads",
        "Hamstrings", "Calves", "Abs", "Cardio", "Full Body", "Lower Back"
    ]

    category_instances = {}
    for cat_name in categories_data:
        obj, _ = Category.objects.get_or_create(name=cat_name)
        category_instances[cat_name] = obj

    exercises_data = [
        {"name": "Barbell Bench Press",
         "desc": "A classic compound exercise that primarily targets the chest, while also engaging the triceps and shoulders.",
         "cats": ["Chest", "Shoulders", "Triceps"]},
        {"name": "Incline Dumbbell Press",
         "desc": "An upper body strength exercise focused on the upper pectoral muscles.",
         "cats": ["Chest", "Shoulders"]},
        {"name": "Push-ups",
         "desc": "A fundamental bodyweight exercise that builds chest, shoulder, and tricep strength.",
         "cats": ["Chest", "Triceps", "Abs"]},
        {"name": "Pull-ups",
         "desc": "A challenging upper body compound pulling exercise that heavily targets the latissimus dorsi and biceps.",
         "cats": ["Back", "Biceps"]},
        {"name": "Barbell Deadlift",
         "desc": "A powerful full-body movement that builds immense strength in the posterior chain, including the back, glutes, and hamstrings.",
         "cats": ["Back", "Hamstrings", "Full Body", "Lower Back"]},
        {"name": "Lat Pulldown",
         "desc": "A machine-based exercise designed to develop and widen the latissimus dorsi muscle.",
         "cats": ["Back", "Biceps"]},
        {"name": "Barbell Row", "desc": "A staple compound movement for building a thick, strong back.",
         "cats": ["Back", "Biceps", "Lower Back"]},
        {"name": "Overhead Press",
         "desc": "A primary shoulder builder that also requires core stabilization and tricep strength.",
         "cats": ["Shoulders", "Triceps"]},
        {"name": "Lateral Raises",
         "desc": "An isolation exercise perfect for targeting the medial deltoid for wider shoulders.",
         "cats": ["Shoulders"]},
        {"name": "Face Pulls",
         "desc": "Excellent for rear deltoid development and overall shoulder health and posture.",
         "cats": ["Back", "Shoulders"]},
        {"name": "Barbell Curl", "desc": "The standard isolation exercise for building bicep mass and strength.",
         "cats": ["Biceps"]},
        {"name": "Hammer Curls",
         "desc": "A bicep variation that targets the brachialis and brachioradialis, building thicker arms and grip strength.",
         "cats": ["Biceps"]},
        {"name": "Tricep Rope Pushdown",
         "desc": "An isolation movement using a cable machine to effectively target the triceps.", "cats": ["Triceps"]},
        {"name": "Skull Crushers",
         "desc": "A lying tricep extension that focuses heavily on the long head of the tricep.", "cats": ["Triceps"]},
        {"name": "Barbell Squat",
         "desc": "The king of leg exercises, essential for building quad, glute, and overall lower body power.",
         "cats": ["Quads", "Hamstrings", "Full Body"]},
        {"name": "Leg Press",
         "desc": "A machine-based compound exercise that allows for heavy lower body training without stressing the lower back.",
         "cats": ["Quads", "Calves"]},
        {"name": "Romanian Deadlift",
         "desc": "A hip-hinge movement that heavily isolates and strengthens the hamstrings and glutes.",
         "cats": ["Hamstrings", "Full Body", "Lower Back"]},
        {"name": "Standing Calf Raise",
         "desc": "A basic but highly effective isolation exercise for the gastrocnemius muscle.", "cats": ["Calves"]},
        {"name": "Plank",
         "desc": "A static core exercise that builds endurance and stability in the abdominals and lower back.",
         "cats": ["Abs", "Full Body"]},
        {"name": "Hanging Leg Raises",
         "desc": "An advanced core movement that heavily targets the lower abdominals and hip flexors.",
         "cats": ["Abs"]},
        {"name": "Treadmill Running",
         "desc": "A popular cardiovascular exercise for improving endurance and burning calories.", "cats": ["Cardio"]},
        {"name": "Rowing Machine", "desc": "A full-body cardio workout that also engages the back, legs, and arms.",
         "cats": ["Back", "Cardio", "Full Body"]},
        {"name": "Cable Crossover",
         "desc": "A cable machine isolation exercise that provides constant tension on the chest muscles.",
         "cats": ["Chest"]},
        {"name": "Dumbbell Flyes",
         "desc": "An isolation exercise designed to stretch and squeeze the pectoral muscles.", "cats": ["Chest"]},
        {"name": "Decline Bench Press", "desc": "A bench press variation that targets the lower portion of the chest.",
         "cats": ["Chest", "Triceps"]},
        {"name": "Front Squat",
         "desc": "A squat variation with the barbell resting on the front delts, emphasizing the quadriceps and upper back.",
         "cats": ["Quads", "Full Body"]},
        {"name": "Leg Extension", "desc": "A machine isolation exercise specifically for targeting the quadriceps.",
         "cats": ["Quads"]},
        {"name": "Walking Lunges",
         "desc": "A dynamic, unilateral leg exercise that improves balance, coordination, and overall leg strength.",
         "cats": ["Quads", "Hamstrings", "Calves"]},
        {"name": "Seated Leg Curl",
         "desc": "A machine isolation movement for the hamstrings performed in a seated position.",
         "cats": ["Hamstrings"]},
        {"name": "Lying Leg Curl",
         "desc": "A machine isolation exercise that targets the hamstrings from a prone position.",
         "cats": ["Hamstrings"]},
        {"name": "Good Mornings",
         "desc": "A barbell hip-hinge exercise that builds strength in the lower back, glutes, and hamstrings.",
         "cats": ["Hamstrings", "Lower Back"]},
        {"name": "Seated Calf Raise", "desc": "A calf isolation exercise that specifically targets the soleus muscle.",
         "cats": ["Calves"]},
        {"name": "Donkey Calf Raise",
         "desc": "A bent-over calf raise variation that provides a deep stretch in the calf muscles.",
         "cats": ["Calves"]},
        {"name": "Jump Rope",
         "desc": "A highly effective cardiovascular exercise that improves agility, coordination, and footwork.",
         "cats": ["Calves", "Cardio", "Full Body"]},
        {"name": "Crunches", "desc": "A classic bodyweight exercise for isolating the upper abdominal muscles.",
         "cats": ["Abs"]},
        {"name": "Ab Wheel Rollout",
         "desc": "An intense core exercise that challenges the abdominals, obliques, and lower back stability.",
         "cats": ["Abs", "Full Body"]},
        {"name": "Russian Twist",
         "desc": "A rotational core exercise that targets the obliques and improves core stability.", "cats": ["Abs"]},
        {"name": "Stationary Bike",
         "desc": "A low-impact cardiovascular exercise ideal for building leg endurance and burning calories.",
         "cats": ["Cardio"]},
        {"name": "Stairmaster",
         "desc": "A demanding cardio machine that mimics climbing stairs, heavily engaging the quads and glutes.",
         "cats": ["Quads", "Calves", "Cardio"]},
        {"name": "Hyperextension",
         "desc": "A bodyweight or weighted exercise that strengthens the lower back and erector spinae.",
         "cats": ["Hamstrings", "Lower Back"]},
        {"name": "Superman",
         "desc": "A floor-based exercise that targets the lower back, glutes, and shoulders for better posture.",
         "cats": ["Abs", "Lower Back"]},
    ]

    for ex_data in exercises_data:
        exercise, created = Exercise.objects.get_or_create(
            name=ex_data["name"],
            defaults={"description": ex_data["desc"]}
        )
        cats_to_assign = [category_instances[c] for c in ex_data["cats"]]
        exercise.categories.set(cats_to_assign)


class Migration(migrations.Migration):
    dependencies = [
        ('workouts', '0007_alter_workout_date'),
    ]

    operations = [
        migrations.RunPython(load_initial_data, reverse_code=migrations.RunPython.noop),
    ]
