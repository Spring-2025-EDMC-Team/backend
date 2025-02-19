import re
import argparse
from typing import Tuple

# Common passwords list (expand as needed)
COMMON_PASSWORDS = [
    'password', '123456', 'qwerty', '12345678', 'abc123',
    'letmein', 'admin', 'welcome', 'monkey', 'password1', 'password2'
]

SPECIAL_CHARS = r'[!@#$%^&*(),.?":{}|<>_\-+=~`\[\]/]'

def validate_password(password: str) -> Tuple[bool, str]:
    """
    Validates a password against security requirements.
    
    Returns:
        Tuple: (is_valid: bool, message: str)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(SPECIAL_CHARS, password):
        return False, "Password must contain at least one special character"
    
    if password.lower() in COMMON_PASSWORDS:
        return False, "Password is too common. Please choose a more unique password."
    
    return True, "Password is strong and valid"

def password_strength(password: str) -> int:
    """
    Calculates password strength as a percentage based on met criteria.
    """
    strength = 0
    criteria = [
        len(password) >= 8,
        re.search(r'[A-Z]', password) is not None,
        re.search(r'[a-z]', password) is not None,
        re.search(r'\d', password) is not None,
        re.search(SPECIAL_CHARS, password) is not None,
        password.lower() not in COMMON_PASSWORDS
    ]
    
    # Each met criterion adds ~16.67% (100/6)
    strength = sum(criteria) * 100 // 6
    return min(max(strength, 0), 100)

def interactive_mode():
    """Handles interactive password creation flow"""
    print("\n🔐 Secure Password Creation Tool 🔐")
    
    while True:
        password = input("\nEnter your password (or 'quit' to exit): ")
        if password.lower() == 'quit':
            break
            
        is_valid, validation_message = validate_password(password)
        strength = password_strength(password)
        
        print(f"\nValidation: {validation_message}")
        print(f"Strength: {strength}%")
        
        if is_valid:
            confirm = input("Use this password? (yes/no): ")
            if confirm.lower() in ['yes', 'y']:
                print("Password accepted! 🎉")
                return password
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Password Validator and Strength Checker",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-p', '--password',
        help='Test a password directly from command line'
    )
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Launch interactive password creation wizard'
    )
    
    args = parser.parse_args()
    
    if args.password:
        is_valid, message = validate_password(args.password)
        strength = password_strength(args.password)
        print(f"Password: {args.password}")
        print(f"Valid: {is_valid}")
        print(f"Message: {message}")
        print(f"Strength: {strength}%")
    elif args.interactive:
        interactive_mode()
    else:
        parser.print_help()