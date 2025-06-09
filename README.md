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

