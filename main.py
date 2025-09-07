# DVA 09/07/25
import requests
import random
import string
import threading
import time
from colorama import Fore, Style, init

init(autoreset=True)

# Banner
print(Fore.CYAN + r"""
███╗   ██╗ ███╗   ███╗ █████╗ ███╗   ██╗ ██████╗ ███╗   ██╗
████╗  ██║ ████╗ ████║██╔══██╗████╗  ██║██╔═══██╗████╗  ██║
██╔██╗ ██║ ██╔████╔██║███████║██╔██╗ ██║██║   ██║██╔██╗ ██║
██║╚██╗██║ ██║╚██╔╝██║██╔══██║██║╚██╗██║██║   ██║██║╚██╗██║
██║ ╚████║ ██║ ╚═╝ ██║██║  ██║██║ ╚████║╚██████╔╝██║ ╚████║
╚═╝  ╚═══╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝
""")
print(Fore.MAGENTA + ".wat3rfr on dc - NAMEGEN\n" + Style.RESET_ALL)

# Reset logs
open("success.txt", "w").close()
open("invalid.txt", "w").close()

# User inputs
length_choice = input("Pick 3, 4, or 5 letter usernames: ").strip()
while length_choice not in ["3", "4", "5"]:
    length_choice = input("Invalid choice. Pick 3, 4, or 5: ").strip()
length_choice = int(length_choice)

mode_choice = input("Pick mode: (1) Random Letters/Numbers (2) Dictionary Words): ").strip()
while mode_choice not in ["1", "2"]:
    mode_choice = input("Invalid choice. Pick 1 or 2: ").strip()
mode_choice = int(mode_choice)

use_webhook = input("Webhook yes or no: ").strip().lower()
webhook_url = input("Enter your webhook: ").strip() if use_webhook == "yes" else ""

threads_count = int(input("How many threads (0 = infinite): ").strip())

print(Fore.YELLOW + "\nStarting generation...\nType Ctrl+C to stop safely.\n" + Style.RESET_ALL)

# Dictionary APIs
DICTIONARY_APIS = [
    "https://random-word-api.herokuapp.com/word?number=1&length={n}",
    "https://random-word-form.herokuapp.com/random/noun?count=1",
    "https://api.datamuse.com/words?sp={pattern}",
    "https://random-word.ryanrk.com/api/en/word/random"
]

# Globals
successes = []
invalids = 0
retries = 0
lock = threading.Lock()

# Random username
def random_username(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# Dictionary username (improved)
def dictionary_username(length):
    while True:
        for api in DICTIONARY_APIS:
            try:
                if "random-word-api" in api:
                    r = requests.get(api.format(n=length), timeout=5)
                    if r.ok:
                        word = r.json()[0]
                        if len(word) == length:
                            return word
                elif "random-word-form" in api:
                    r = requests.get(api, timeout=5)
                    if r.ok:
                        word = r.json()[0]
                        if len(word) == length:
                            return word
                elif "datamuse" in api:
                    pattern = "?" * length
                    r = requests.get(api.format(pattern=pattern), timeout=5)
                    if r.ok:
                        data = r.json()
                        if data:
                            return random.choice(data)["word"]
                elif "ryanrk" in api:
                    r = requests.get(api, timeout=5)
                    if r.ok:
                        word = r.json()[0]
                        if len(word) == length:
                            return word
            except Exception as e:
                print(Fore.YELLOW + f"[!] API failed: {api} | {e}")
                continue
        print(Fore.YELLOW + "[!] All dictionary APIs unavailable. Retrying in 5 seconds...")
        time.sleep(5)

# Store success
def store_success(username):
    global successes
    with lock:
        successes.append(username)
        with open("success.txt", "a") as f:
            f.write(username + "\n")
    if use_webhook == "yes" and webhook_url:
        try:
            requests.post(webhook_url, json={"content": f"✅ Success: {username}"}, timeout=5)
        except:
            pass

# Store invalid
def store_invalid(username):
    global invalids
    with lock:
        invalids += 1
        with open("invalid.txt", "a") as f:
            f.write(username + "\n")

# Check username
def check_username(username):
    global retries
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code in [204, 404]:
            print(Fore.GREEN + f"✅ Success {username}")
            store_success(username)
        elif r.status_code == 200:
            print(Fore.RED + f"❌ Invalid {username}")
            store_invalid(username)
        else:
            print(Fore.YELLOW + f"[!] Mojang response {r.status_code} for {username}")
            retries += 1
    except requests.exceptions.RequestException:
        print(Fore.YELLOW + "[!] Rate limited or connection issue. Retrying...")
        retries += 1
        time.sleep(0.5)

# Worker
def worker():
    while True:
        if mode_choice == 1:
            username = random_username(length_choice)
        else:
            username = dictionary_username(length_choice)
        check_username(username)
        time.sleep(0.5)

# Start threads
threads = []
for _ in range(threads_count if threads_count > 0 else 1):
    t = threading.Thread(target=worker, daemon=True)
    threads.append(t)
    t.start()

# Ctrl+C handling
try:
    for t in threads:
        t.join()
except KeyboardInterrupt:
    print(Fore.YELLOW + "\n[!] Stopped by user")
    if use_webhook == "yes" and webhook_url:
        try:
            with open("success.txt", "rb") as s_file, open("invalid.txt", "rb") as i_file:
                files = {"success": s_file, "invalid": i_file}
                requests.post(webhook_url, data={
                    "content": f"✅ NAMEGEN finished.\nSuccesses: {len(successes)}\nInvalids: {invalids}\nRetries: {retries}"
                }, files=files, timeout=10)
                print(Fore.GREEN + "[!] Final webhook sent!")
        except Exception as e:
            print(Fore.RED + f"[!] Failed to send final webhook: {e}")
    print(Fore.GREEN + f"\n✅ Finished. Successes: {len(successes)}, Invalids: {invalids}, Retries: {retries}")
