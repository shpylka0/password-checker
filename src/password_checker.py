import re
import json
import requests
from hashlib import sha1
from colorama import Fore, Style, init

# Ініціалізація colorama ( для Windows)
init(autoreset=True)

# Список поширених паролів
COMMON_PASSWORDS = ["123456", "password", "12345678", "qwerty", "abc123", "123456789"]

# Функція перевірки пароля у зламаних базах через API
def is_password_pwned(password):
    try:
        sha1_password = sha1(password.encode('utf-8')).hexdigest().upper()
        prefix = sha1_password[:5]
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
        if response.status_code == 200:
            hashes = response.text.splitlines()
            for line in hashes:
                hash_suffix, count = line.split(":")
                if sha1_password[5:] == hash_suffix:
                    return True
        return False
    except Exception as e:
        print(Fore.YELLOW + "[УВАГА] Не вдалося перевірити пароль через API. Перевірте своє інтернет-з'єднання.")
        return False

# Функція перевірки надійності пароля
def check_password_strength(password):
    """
    Перевіряє надійність пароля.
    Повертає словник з результатами перевірки.
    """
    if not password:
        return None

    strength = {
        "length": len(password) >= 8,
        "uppercase": bool(re.search(r'[A-Z]', password)),
        "lowercase": bool(re.search(r'[a-z]', password)),
        "digits": bool(re.search(r'\d', password)),
        "special_characters": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
        "common_password": password not in COMMON_PASSWORDS,
        "pwned": not is_password_pwned(password)
    }

    return strength

#Рекомендації для покращення пароля
def generate_recommendations(results):
    """Генерує список рекомендацій для покращення пароля."""
    recommendations = []

    if not results["length"]:
        recommendations.append("Зробіть пароль довшим. Рекомендується мінімум 8 символів.")
    if not results["uppercase"]:
        recommendations.append("Додайте хоча б одну велику літеру.")
    if not results["lowercase"]:
        recommendations.append("Додайте хоча б одну малу літеру.")
    if not results["digits"]:
        recommendations.append("Додайте хоча б одну цифру.")
    if not results["special_characters"]:
        recommendations.append("Додайте спеціальний символ, наприклад: !, @, #, $ тощо.")
    if not results["common_password"]:
        recommendations.append("Не використовуйте поширені паролі, наприклад: 123456, password тощо.")
    if not results["pwned"]:
        recommendations.append("Ваш пароль знайдено у базах зламаних паролів. Створіть унікальний пароль.")

    return recommendations

# Запис історії перевірок у файл
def save_history(password, results):
    """Зберігає результати перевірки у файл JSON."""
    history_entry = {
        "password": password,
        "results": results
    }
    try:
        try:
            with open("password_checks.json", "r") as file:
                history = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []

        # Додати новий запис і обмежити історію до 100 записів
        history.append(history_entry)
        history = history[-100:]

        # Оновлена історія
        with open("password_checks.json", "w") as file:
            json.dump(history, file, indent=4)
    except Exception as e:
        print(Fore.YELLOW + "[УВАГА] Не вдалося записати історію перевірки.")

# main
def main():
    print(Fore.CYAN + "Перевірка надійності пароля")
    password = input("Введіть пароль для перевірки: ")

    results = check_password_strength(password)
    if results is None:
        print(Fore.RED + "Пароль не може бути порожнім.")
        return

    score = sum(results.values())

    print("\nРезультати перевірки:")
    for criteria, passed in results.items():
        print(f"{criteria.capitalize()}: {Fore.GREEN if passed else Fore.RED}{'✅' if passed else '❌'}")

    print(f"\nЗагальний бал: {score}/{len(results)}")

    if score < len(results):
        recommendations = generate_recommendations(results)
        print(Fore.YELLOW + "\nРекомендації для покращення пароля:")
        for rec in recommendations:
            print(Fore.YELLOW + f"- {rec}")

    save_history(password, results)

if __name__ == "__main__":
    main()
