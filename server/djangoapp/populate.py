from .models import CarMake, CarModel


def initiate():
    car_make_data = [
        {"name": "NISSAN", "description": "Japanese technology"},
        {"name": "Mercedes", "description": "German technology"},
        {"name": "Audi", "description": "German technology"},
        {"name": "Kia", "description": "Korean technology"},
        {"name": "Toyota", "description": "Japanese technology"},
    ]

    car_make_instances = {}

    for data in car_make_data:
        make, created = CarMake.objects.get_or_create(
            name=data["name"],
            defaults={"description": data["description"]}
        )
        car_make_instances[data["name"]] = make

    car_model_data = [
        ("NISSAN", "Pathfinder"),
        ("NISSAN", "Qashqai"),
        ("NISSAN", "XTRAIL"),
        ("Mercedes", "A-Class"),
        ("Mercedes", "C-Class"),
        ("Mercedes", "E-Class"),
        ("Audi", "A4"),
        ("Audi", "A5"),
        ("Audi", "A6"),
        ("Kia", "Sorrento"),
        ("Kia", "Carnival"),
        ("Kia", "Cerato"),
        ("Toyota", "Corolla"),
        ("Toyota", "Camry"),
        ("Toyota", "Kluger"),
    ]

    for make_name, model_name in car_model_data:
        CarModel.objects.get_or_create(
            car_make=car_make_instances[make_name],
            name=model_name,
            defaults={
                "type": "SUV",
                "year": 2023
            }
        )
