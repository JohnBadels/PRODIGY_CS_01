import string
import time
import os
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize colorama

def caesar_cipher(text, shift, mode='encrypt'):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            if mode == 'encrypt':
                shifted = (ord(char) - ascii_offset + shift) % 26
            else:  # decrypt
                shifted = (ord(char) - ascii_offset - shift) % 26
            result += chr(shifted + ascii_offset)
        else:
            result += char
    return result

def progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█', print_end="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    if iteration == total:
        print()

def process_with_progress(text, shift, mode):
    result = ""
    for i, char in enumerate(text):
        result += caesar_cipher(char, shift, mode)
        progress_bar(i + 1, len(text), prefix=f'{mode.capitalize()}ing:', suffix='Complete', length=30)
        time.sleep(0.01)  # Slow down for visual effect
    return result

def save_to_file(text, filename):
    try:
        with open(filename, 'w') as f:
            f.write(text)
        print(f"{Fore.GREEN}File saved successfully: {filename}")
    except IOError as e:
        print(f"{Fore.RED}Error saving file: {e}")

def read_from_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"{Fore.RED}File not found: {filename}")
    except IOError as e:
        raise IOError(f"{Fore.RED}Error reading file: {e}")

def get_valid_shift():
    while True:
        try:
            shift = int(input(f"{Fore.GREEN}Enter the shift value (0-25): "))
            if 0 <= shift <= 25:
                return shift
            else:
                print(f"{Fore.RED}Shift must be between 0 and 25. Please try again.")
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a number between 0 and 25.")

def get_input_method():
    while True:
        choice = input(f"{Fore.GREEN}Enter 'F' to read from file, or 'M' for manual input: ").upper()
        if choice in ['F', 'M']:
            return choice
        print(f"{Fore.RED}Invalid choice. Please enter 'F' or 'M'.")

def get_message(mode):
    while True:
        message = input(f"{Fore.GREEN}Enter the message to {mode}: ")
        if message.strip():
            return message
        print(f"{Fore.RED}Error: Message cannot be empty. Please try again.")

def get_save_choice():
    while True:
        choice = input(f"{Fore.GREEN}Do you want to save the result to a file? (Y/N): ").upper()
        if choice in ['Y', 'N']:
            return choice
        print(f"{Fore.RED}Invalid choice. Please enter 'Y' or 'N'.")

def main():
    while True:
        try:
            print(f"\n{Fore.CYAN}=== Caesar Cipher ===")
            print(f"{Fore.YELLOW}1. Encrypt")
            print(f"{Fore.YELLOW}2. Decrypt")
            print(f"{Fore.YELLOW}3. Exit")
            
            choice = input(f"{Fore.GREEN}Enter your choice: ")
            
            if choice == '3':
                print(f"{Fore.MAGENTA}Thank you for using the Caesar Cipher program.")
                break
            
            if choice not in ['1', '2']:
                print(f"{Fore.RED}Invalid choice. Please enter 1, 2, or 3.")
                continue
            
            mode = 'encrypt' if choice == '1' else 'decrypt'
            
            input_choice = get_input_method()
            if input_choice == 'F':
                filename = input("Enter the input filename: ")
                try:
                    message = read_from_file(filename)
                    print(f"{Fore.GREEN}File read successfully.")
                except (FileNotFoundError, IOError) as e:
                    print(e)
                    continue
            else:
                message = get_message(mode)
            
            shift = get_valid_shift()
            
            result = process_with_progress(message, shift, mode)
            
            print(f"\n{Fore.CYAN}Result: {Style.RESET_ALL}{result}")
            
            save_choice = get_save_choice()
            if save_choice == 'Y':
                filename = input("Enter the output filename: ")
                save_to_file(result, filename)
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Operation cancelled by user.")
        except Exception as e:
            print(f"{Fore.RED}An unexpected error occurred: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()