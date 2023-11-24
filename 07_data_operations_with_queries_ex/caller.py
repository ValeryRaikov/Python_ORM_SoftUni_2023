import os
import django

from django.db.models import QuerySet, F

from db_fill_data import populate_model_with_data

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character

# Create queries within functions


def create_pet(name: str, species: str) -> str:
    pet = Pet.objects.create(
        name=name,
        species=species,
    )

    # pet = Pet(
    #     name=name,
    #     species=species,
    # )
    #
    # pet.save()

    return f"{pet.name} is a very cute {pet.species}!"

# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool) -> str:
    artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical,
    )

    return f"The artifact {artifact.name} is {artifact.age} years old!"


def delete_all_artifacts() -> None:
    Artifact.objects.all().delete()

# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))
#
# print(create_artifact('Crystal Amulet', 'Mystic Forest', 300, 'A magical amulet believed to bring good fortune', True))


def show_all_locations() -> str:
    locations = Location.objects.all().order_by('-id')

    return '\n'.join(str(l) for l in locations)


def new_capital() -> None:
    # curr_location = Location.objects.first()
    # curr_location.is_capital = True
    # curr_location.save()

    Location.objects.filter(pk=1).update(is_capital=True)


def get_capitals() -> QuerySet:
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location() -> None:
    Location.objects.first().delete()


# populate_model_with_data(Location, 20)

# print(show_all_locations())
# print(new_capital())
# print(get_capitals())


def apply_discount() -> None:
    all_cars = Car.objects.all()

    for car in all_cars:
        percentage_off = sum(int(x) for x in str(car.year)) / 100
        discount = float(car.price) * percentage_off
        car.price_with_discount = float(car.price) - discount
        # car.save()

    Car.objects.bulk_update(all_cars, ['price_with_discount'])


def get_recent_cars() -> QuerySet:
    return Car.objects.filter(year__gte=2020).values('model', 'price_with_discount')


def delete_last_car() -> None:
    Car.objects.last().delete()


# populate_model_with_data(Car, 10)

# apply_discount()
# print(get_recent_cars())


def show_unfinished_tasks() -> str:
    unfinished_tasks = Task.objects.filter(is_finished=False).values('title', 'due_date')

    return '\n'.join(str(x) for x in unfinished_tasks)


def complete_odd_tasks() -> None:
    all_tasks = Task.objects.all()

    for task in all_tasks:
        if task.id % 2 != 0:
            task.is_finished = True
            # task.save()

    Task.objects.bulk_update(all_tasks, ['is_finished'])


def encode_and_replace(text: str, task_title: str) -> None:
    CONST_MOVE = -3

    decoded_text = ''.join(chr(ord(x) + CONST_MOVE) for x in text)
    # Task.objects.filter(title=task_title).update(description=decoded_text)

    task_that_match = Task.objects.filter(title=task_title)
    for task in task_that_match:
        task.description = decoded_text
        # task.save()

    Task.objects.bulk_update(task_that_match, ['description'])


# populate_model_with_data(Task, 10)

# encode_and_replace("Zdvk#wkh#glvkhv$", "Simple Task")
# print(Task.objects.get(title='Simple Task') .description)


def get_deluxe_rooms() -> str:
    deluxe_rooms = HotelRoom.objects.filter(room_type='Deluxe')
    even_id_deluxe_rooms = []

    for d_room in deluxe_rooms:
        if d_room.id % 2 == 0:
            even_id_deluxe_rooms.append(d_room)

    return '\n'.join(str(d_room) for d_room in deluxe_rooms)


def increase_room_capacity() -> None:
    all_rooms = HotelRoom.objects.all().order_by("id")

    previous_room_capacity = None

    for room in all_rooms:
        if not room.is_reserved:
            continue

        if previous_room_capacity:
            room.capacity += previous_room_capacity
        else:
            room.capacity += room.id

        previous_room_capacity = room.capacity

        room.save()


def reserve_first_room() -> None:
    HotelRoom.objects.filter(pk=1).update(is_reserved=True)

    # first_room = HotelRoom.objects.first()
    # first_room.is_reserved = True
    # first_room.save()


def delete_last_room() -> None:
    HotelRoom.objects.filter(is_reserved=True).last().delete()

    # last_room = HotelRoom.objects.last()
    #
    # if last_room.is_reserved:
    #     last_room.delete()


# populate_model_with_data(HotelRoom, 10)

# print(get_deluxe_rooms())
# reserve_first_room()
# print(HotelRoom.objects.get(room_number=20).is_reserved)


def update_characters() -> None:
    Character.objects.filter(class_name='Mage').update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7,
    )

    Character.objects.filter(class_name='Warrior').update(
        hitpoints=F('hit_points') / 2,
        dexterity=F('dexterity') + 4,
    )

    Character.objects.filter(class_name__in=['Assassin', 'Scout']).update(
        inventory='The inventory is empty',
    )


def fuse_characters(first_character: Character, second_character: Character) -> None:
    fusion_name = first_character.name + " " + second_character.name
    fusion_class = 'Fusion'
    fusion_level = (first_character.level + second_character.level) // 2
    fusion_strength = (first_character.strength + second_character.strength) * 1.2
    fusion_dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    fusion_intelligence = (first_character.intelligence + second_character.intelligence) * 1.5
    fusion_hit_points = (first_character.hit_points + second_character.hit_points)

    if first_character.class_name in ['Mage', 'Scout']:
        fusion_inventory = 'Bow of the Elven Lords, Amulet of Eternal Wisdom'
    else:
        fusion_inventory = 'Dragon Scale Armor, Excalibur'

    Character.objects.create(
        name=fusion_name,
        class_name=fusion_class,
        level=fusion_level,
        strength=fusion_strength,
        dexterity=fusion_dexterity,
        intelligence=fusion_intelligence,
        hit_points=fusion_hit_points,
        inventory=fusion_inventory,
    )

    first_character.delete()
    second_character.delete()


def grand_dexterity() -> None:
    Character.objects.update(dexterity=30)


def grand_intelligence() -> None:
    Character.objects.update(intelligence=40)


def grand_strength() -> None:
    Character.objects.update(strength=50)


def delete_characters() -> None:
    Character.objects.filter(inventory='The inventory is empty').delete()


# populate_model_with_data(Character, 10)

# character1 = Character.objects.create(
#     name="Gandalf",
#     class_name="Mage",
#     level=10,
#     strength=15,
#     dexterity=20,
#     intelligence=25,
#     hit_points=100,
#     inventory="Staff of Magic, Spellbook",
# )
#
# character2 = Character.objects.create(
#     name="Hector",
#     class_name="Warrior",
#     level=12,
#     strength=30,
#     dexterity=15,
#     intelligence=10,
#     hit_points=150,
#     inventory="Sword of Troy, Shield of Protection",
# )
#
# fuse_characters(character1, character2)
# fusion = Character.objects.filter(class_name='Fusion').get()
#
# print(fusion.name)
# print(fusion.class_name)
# print(fusion.level)
# print(fusion.intelligence)
# print(fusion.inventory)
