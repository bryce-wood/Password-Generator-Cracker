import itertools
import string
import time

def brute_force_crack(
    target: str,
    charset: str = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$%^&*()-_=+[]{};:,.<>?/",
    max_length: int = 10
):
    start_time = time.time()
    attempts = 0

    for length in range(1, max_length + 1):
        for combo in itertools.product(charset, repeat=length):
            attempts += 1
            guess = ''.join(combo)

            if guess == target:
                elapsed = time.time() - start_time
                speed = attempts // elapsed

                return guess, attempts, elapsed, speed
            
        elapsed = time.time() - start_time
        if elapsed != 0:
            speed = attempts // elapsed

    return None, attempts, elapsed, speed

def demo(password: str = "Zac1"):
    target_password = password # Zac12 took almost 100x longer, i'd assume Zac123 takes 10,000x longer, so we will use Zac1 for demo
    print("====================")
    print(f"Target Password: {target_password}")
    print("====================")

    cracked_password, total_attempts, total_time, hash_rate = brute_force_crack(target_password)

    if cracked_password:
        print(f"\nCRACKED! Password: {cracked_password}")
        print(f"\nTotal Attempts: {total_attempts}")
        print(f"\nTotal Time: {total_time:.2f} seconds")
        print(f"\nHash Rate: {hash_rate} attempts/second")
    else:
        print("\nFAILED to crack the password within the search space.")