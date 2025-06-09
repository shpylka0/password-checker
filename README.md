# 🔐 Password Checker

A simple CLI tool for evaluating the strength of passwords based on multiple criteria, including integration with the [Have I Been Pwned](https://haveibeenpwned.com/) API.

## ✅ Features

- **Password Strength Validation**:
  - Minimum length of 8 characters
  - Contains uppercase and lowercase letters
  - Contains digits
  - Contains special characters
  - Not a common password (basic dictionary check)
  - Not found in known data breaches (via HIBP API)

- **Color Output**:
  - Uses `colorama` for clear, color-coded feedback

- **History Tracking**:
  - Saves password check results to a local JSON file (`password_checks.json`)

## ▶️ How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/shpylka0/password-checker.git
   cd password-checker
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the main checker:

   ```bash
   python src/password_checker.py
   ```

4. View password check history:

   ```bash
   python src/read_history.py
   ```

## 📂 Project Structure

```
password-checker/
├── README.md
├── requirements.txt
├── src/
│   ├── password_checker.py
│   └── read_history.py
├── data/
│   └── password_checks.json  # created automatically
└── .gitignore
```

## ⚠️ Notes

- Do not use this tool to store real user passwords — it's for educational purposes only.
- If the Have I Been Pwned API fails, the tool will still perform local checks.
