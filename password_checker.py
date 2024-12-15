import re

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
        "special_characters": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    }

    return strength


def calculate_strength_score(results):
    """
    Обчислює загальний бал надійності пароля.
    """
    return sum(results.values())


def main():
    print("Перевірка надійності пароля")
    password = input("Введіть пароль для перевірки: ")

    results = check_password_strength(password)
    score = calculate_strength_score(results)

    print("\nРезультати перевірки:")
    for criteria, passed in results.items():
        print(f"{criteria.capitalize()}: {'✅' if passed else '❌'}")

    print(f"\nЗагальний бал: {score}/5")
    if score < 3:
        print("Пароль дуже слабкий.")
    elif score < 5:
        print("Пароль середньої надійності.")
    else:
        print("Ваш пароль надійний!")

if __name__ == "__main__":
    main()
