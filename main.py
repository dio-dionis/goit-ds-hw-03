from pymongo import MongoClient, errors
from bson.objectid import ObjectId

# Підключення до MongoDB
try:
    client = MongoClient("mongodb+srv://dio-di:x9bvogsf@dio-di.ruhxhoa.mongodb.net/?appName=Dio-di")
    db = client['cat_database']  # Назва бази даних
    cats_collection = db['cats']  # Колекція
    print("Підключення до MongoDB успішне!")
except errors.ConnectionFailure as e:
    print("Не вдалося підключитися до MongoDB:", e)


# ================================
# ФУНКЦІЇ CRUD
# ================================

# --- CREATE ---
def add_cat(name: str, age: int, features: list):
    """Додає нового кота до колекції"""
    try:
        cat = {"name": name, "age": age, "features": features}
        result = cats_collection.insert_one(cat)
        print(f"Кота додано з _id: {result.inserted_id}")
    except errors.PyMongoError as e:
        print("Помилка при додаванні кота:", e)


# --- READ ---
def show_all_cats():
    """Виводить всіх котів із колекції"""
    try:
        cats = cats_collection.find()
        for cat in cats:
            print(cat)
    except errors.PyMongoError as e:
        print("Помилка при читанні котів:", e)


def show_cat_by_name(name: str):
    """Виводить інформацію про кота за іменем"""
    try:
        cat = cats_collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"Кіт з ім'ям '{name}' не знайдений.")
    except errors.PyMongoError as e:
        print("Помилка при пошуку кота:", e)


# --- UPDATE ---
def update_cat_age(name: str, new_age: int):
    """Оновлює вік кота за іменем"""
    try:
        result = cats_collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count > 0:
            print(f"Вік кота '{name}' оновлено на {new_age}.")
        else:
            print(f"Кота '{name}' не знайдено або вік вже оновлено.")
    except errors.PyMongoError as e:
        print("Помилка при оновленні віку кота:", e)


def add_feature_to_cat(name: str, feature: str):
    """Додає нову характеристику коту"""
    try:
        result = cats_collection.update_one({"name": name}, {"$push": {"features": feature}})
        if result.modified_count > 0:
            print(f"Характеристика '{feature}' додана коту '{name}'.")
        else:
            print(f"Кота '{name}' не знайдено.")
    except errors.PyMongoError as e:
        print("Помилка при додаванні характеристики:", e)


# --- DELETE ---
def delete_cat_by_name(name: str):
    """Видаляє кота за ім'ям"""
    try:
        result = cats_collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Кіт '{name}' видалений.")
        else:
            print(f"Кота '{name}' не знайдено.")
    except errors.PyMongoError as e:
        print("Помилка при видаленні кота:", e)


def delete_all_cats():
    """Видаляє всіх котів із колекції"""
    try:
        result = cats_collection.delete_many({})
        print(f"Видалено {result.deleted_count} котів.")
    except errors.PyMongoError as e:
        print("Помилка при видаленні всіх котів:", e)


# ================================
# ПРИКЛАД ВИКОРИСТАННЯ
# ================================
if __name__ == "__main__":
    # Додати кота
    add_cat("Barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    
    # Показати всіх котів
    show_all_cats()
    
    # Пошук кота за ім'ям
    show_cat_by_name("Barsik")
    
    # Оновлення віку
    update_cat_age("Barsik", 4)
    
    # Додати характеристику
    add_feature_to_cat("Barsik", "любить гратися з мотузкою")
    
    # Видалити кота
    # delete_cat_by_name("Barsik")
    
    # Видалити всіх котів
    # delete_all_cats()
