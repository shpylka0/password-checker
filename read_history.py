import json

def read_history(file_path="password_checks.json"):
    # Зчитує і виводить історію перевірок паролів
    try:
        with open(file_path, "r") as file:
            history = json.load(file)
            for entry in history:
                print(f"Пароль: {entry['password']}")
                print("Результати перевірки:")
                for criteria, passed in entry["results"].items():
                    status = "✅" if passed else "❌"
                    print(f"  {criteria.capitalize()}: {status}")
                print("-" * 30)
    except FileNotFoundError:
        print("Файл з історією перевірок не знайдено.")
    except json.JSONDecodeError:
        print("Файл з історією перевірок пошкоджено або має неправильний формат.")
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")

read_history()
