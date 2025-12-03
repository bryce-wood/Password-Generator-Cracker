import itertools
import string
import time
import hashlib
from zxcvbn import zxcvbn
from typing import Optional, List, Tuple

HASH_ALGORITHM = 'sha256'

# Common passwords (short list for demo)
COMMON_PASSWORDS = {
    "password", "letmein", "123456", "123456789", "qwerty",
    "iloveyou", "admin", "welcome", "dragon",
    "football", "guest"
}

def mutate_words(words: List[str]) -> set:
    """Generates common password mutations (leet, suffixes, capitalization)."""
    mutations = set()

    for w in words:
        base = w.strip()
        if not base:
            continue

        # Basic variants
        mutations.add(base)
        mutations.add(base.lower())
        mutations.add(base.upper())
        mutations.add(base.capitalize())
        mutations.add(base[::-1])

        # Simple suffix additions
        for suffix in ["1", "123", "!", "!!", "2025", "1!"]:
            mutations.add(base + suffix)

        # prefix additions
        for prefix in ["!", "1", "2025"]:
            mutations.add(prefix + base)

        # Leetspeak variants
        leet = (
            base.replace("a", "@")
                .replace("i", "1")
                .replace("e", "3")
                .replace("o", "0")
                .replace("s", "$")
        )
        mutations.add(leet)
        mutations.add(leet + "1")
        mutations.add(leet + "!")
        mutations.add(leet + "123")
        mutations.add(leet + "123!")

    return mutations

def hash_guess(guess: str, algorithm: str = HASH_ALGORITHM) -> str:
    """Hashes the guess using the specified algorithm."""
    h = hashlib.new(algorithm)
    h.update(guess.encode())
    return h.hexdigest()

def analyze_with_zxcvbn(password: str, context_words: List[str]):
    """Prints the password strength analysis using zxcvbn."""
    print("==================================")
    print("PASSWORD ANALYSIS (Strength Estimation)")
    print("==================================")
    analysis = zxcvbn(password, user_inputs=context_words)
    print("\n  Score (0-4):", analysis["score"])
    print("  Estimated Crack Times:", analysis["crack_times_display"]["offline_fast_hashing_1e10_per_second"])

def hash_cracker(
    target_hash: str,
    target_password: str,
    context_words: Optional[List[str]] = None,
    max_brute_length: int = 5
) -> Tuple[Optional[str], int, float, float]:
    """
    Attempts to crack a target hash using a dictionary attack and limited brute force.
    
    Returns: (cracked_password, attempts, elapsed_time, speed_hashes_per_sec)
    """
    if context_words is None:
        context_words = []

    analyze_with_zxcvbn(target_password, context_words)

    print(f"\n========== {HASH_ALGORITHM.upper()} HASH CRACKER DEMO ==========\n")
    print("Target Password:", target_password)
    print("Target Hash:", target_hash)
    
    attempts = 0
    start_time = time.time()
    
    # Generate Master Dictionary
    master_dictionary = set()
    master_dictionary.update(COMMON_PASSWORDS)
    master_dictionary.update(mutate_words(context_words))

    print("\nTrying dictionary candidates...")

    for guess in master_dictionary:
        attempts += 1
        guess_hash = hash_guess(guess)
        
        if guess_hash == target_hash:
            elapsed = time.time() - start_time
            if elapsed != 0:
                speed = attempts / elapsed
            else:
                speed = float('inf')
            print("\nFOUND via Dictionary Attack!\n")
            return guess, attempts, elapsed, speed
    
    print("Dictionary failed. Falling back to limited Brute Force...")

    # brute force fallback
    charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$%^&*()-_=+[]{}|\\;:'\",<.>/?`~"
    print(f"Charset Size: {len(charset)}")
    print(f"Trying Brute Force up to length {max_brute_length}...")
    
    for length in range(1, max_brute_length + 1):
        print(f"  - Trying length {length}...")
        
        # Estimate combinations for progress
        count = len(charset) ** length
        print(f"    ~ {count:,} combinations...")

        for combo in itertools.product(charset, repeat=length):
            attempts += 1
            guess = ''.join(combo)
            guess_hash = hash_guess(guess)

            if guess_hash == target_hash:
                elapsed = time.time() - start_time
                speed = attempts / elapsed
                print(f"\nFOUND via Brute Force Fallback (Attempt {attempts})!")
                return guess, attempts, elapsed, speed
            

    elapsed = time.time() - start_time
    speed = attempts / elapsed if elapsed else 0
    print("\nFAILED to crack the hash within the search space.")
    return None, attempts, elapsed, speed


# demo
def demo(password: str = "H0lbr00k123!"):
    DEMO_PASSWORD = password
    TARGET_HASH = hash_guess(DEMO_PASSWORD)

    result = hash_cracker(
        target_hash=TARGET_HASH,
        target_password=DEMO_PASSWORD,
        context_words=["Zac", "Holbrook", "2004"],
        max_brute_length=12
    )

    cracked_pwd, total_attempts, total_time, hash_speed = result
    print("==================")
    print(f"RESULT SUMMARY:")
    print("==================")
    print(f"\n  Target Hash: {TARGET_HASH}")
    print(f"\n  Cracked Password: {cracked_pwd}")
    print(f"\n  Total Attempts: {total_attempts:,}")
    print(f"\n  Time Elapsed: {total_time:.4f} seconds")
    print(f"\n  Hash Speed: {hash_speed:.0f} hashes/second")
