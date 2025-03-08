# Password Strength Meter

This project is a **Password Strength Meter** built with **Streamlit** that evaluates password security based on multiple criteria.

## Variants
This repository contains two variants of the project:
1. **Basic Version** (v0.2.0)
2. **Advanced Version** (v0.0.2)

---

## **1. Basic Version** (v0.2.0)
**Description:** The Basic Version evaluates password strength based on length, character variety, and common patterns. It has two iterations, with improvements in validation and UI responsiveness.

### **Features:**
- Login, Registration, and Password Reset functionality
- Password length validation
- Checks for uppercase & lowercase letters
- Requires at least one number
- Requires at least one special character
- Prevents use of common passwords
- Tracks last 10 used passwords to prevent reuse
- All missing requirements/errors displayed at once
- Simple UI for password input

### **Version History:**
- **v0.2.0** - Enhanced validation, improved feedback messages.
- **v0.1.0** - Initial version with basic checks.

---

## **2. Advanced Version** (v0.0.2)
**Description:** The Advanced Version includes all features of the Basic Version with additional security measures, gamified password selection, and enhanced tracking.

### **Features:**
- Everything in the Basic Version
- Password selection follows a game-like approach with multiple mandatory requirements
- Prevents reuse of the last 15 passwords
- Detects consecutive number sequences
- Tracks previously tested passwords to guide user improvement
- Displays number of attempts taken to set a valid password
- Password confirmation step before registration or reset
- Does not include a traditional strength meter

### **Version History:**
- **v0.0.2** - Updated password validation with enhanced game-like requirements.
- **v0.0.1** - Initial advanced implementation with improved password validation and tracking.

---

## **Installation & Setup**
1. Clone the repository:
   ```sh
   git clone https://github.com/muhammadsaadullah/Password-Strength-Meter.git
   cd Password-Strength-Meter
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   streamlit run app.py
   ```

---

## **Usage**
- Enter a password in the input field.
- The system will analyze its strength and display necessary improvements.
- If the password is weak, follow the suggestions and retry.
- The Advanced Version keeps track of previously tested passwords and prevents recent password reuse.

---

## **Contributing**
Feel free to contribute by submitting issues or pull requests. Suggestions for improvements are always welcome!

---

## **License**
This project is licensed under the MIT License.

