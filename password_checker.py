import re
import hashlib
import requests
import json
from colorama import Fore, Style, init

# Ініціалізація colorama (потрібно для Windows)
init(autoreset=True)

# Список найбільш поширених паролів
common_passwords = [
    "123456", "password", "123456789", "12345", "12345678", "qwerty", "abc123", "1234", "password1", "123123"
]


def check_password_strength(password):
    """
    Перевіряє надійність пароля.
    Повертає словник з результатами перевірки.
    """
    strength = {
        "length": len(password) >= 8,
        "uppercase": bool(re.search(r'[A-Z]', password)),
        "lowercase": bool(re.search(r'[a-z]', password)),
        "digits": bool(re.search(r'\d', password)),
        "special_characters": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
        "common": password.lower() in common_passwords
    }

    return strength


def calculate_strength_score(results):
    """
    Обчислює загальний бал надійності пароля.
    """
    return sum(results.values())


def check_password_in_pwned(password):
    """
    Перевіряє, чи є пароль у базах зламаних паролів через API Have I Been Pwned.
    """
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_password[:5]
    suffix = sha1_password[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    if response.status_code != 200:
        print(Fore.RED + "Помилка при перевірці паролю через API.")
        return False

    hashes = response.text.splitlines()
    for line in hashes:
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            print(Fore.RED + f"Ваш пароль було зламано {count} разів. Змініть його!")
            return True

    return False


def save_check_history(password, result, score):
    """
    Зберігає історію перевірок у JSON файл.
    """
    try:
        with open("password_checks.json", "r") as file:
            history = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    history.append({"password": password, "result": result, "score": score})

    with open("password_checks.json", "w") as file:
        json.dump(history, file, indent=4)


def main():
    print(Fore.CYAN + "Перевірка надійності пароля")

    password = input("Введіть пароль для перевірки: ").strip()

    if not password:
        print(Fore.RED + "Пароль не може бути порожнім!")
        return

    # Перевірка на надійність
    results = check_password_strength(password)
    score = calculate_strength_score(results)

    # Перевірка на зламаний пароль
    is_pwned = check_password_in_pwned(password)

    print(Fore.GREEN + "\nРезультати перевірки:")
    for criteria, passed in results.items():
        color = Fore.GREEN if passed else Fore.RED
        print(f"{color}{criteria.capitalize()}: {'✅' if passed else '❌'}")

    print(Fore.YELLOW + f"\nЗагальний бал: {score}/6")
    if score < 3 or is_pwned:
        print(Fore.RED + "Пароль дуже слабкий або знайдений у зламаних базах даних. Змініть його!")
    elif score < 5:
        print(Fore.YELLOW + "Пароль середньої надійності.")
    else:
        print(Fore.GREEN + "Ваш пароль надійний!")

    # Зберігання результатів перевірки
    save_check_history(password, "Проведено перевірку", score)


if __name__ == "__main__":
    main()