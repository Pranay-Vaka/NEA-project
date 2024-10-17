import random

def miller_rabin(prime, cycles): # 40 number of cycles to check primes is the optimum to be used here

    r = 0
    s = prime - 1

    while s % 2 == 0:

        r = r + 1
        s = s // 2


    for i in range(cycles):

        a = random.randint(2, prime - 2)

        x = (a ** s) % prime

        if x == 1 or x == prime - 1:

            continue


        for i in range(r - 1):
            x = (x ** 2) % prime

            if x == prime - 1:
                break

        else:
            return False


    return True



def is_prime(n): # This will check if the number is prime using some small prime numbers as well
    # This is a list of low primes from 0 to 1000
    low_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

    for i in low_primes: # This will check if the number is a factor of the primes, returns false if so
        if i == n or n % i == 0:
            return False


    return miller_rabin(n, 40) # If nothing passes then use the miller_rabin method. The optimum here is 40


def generate_large_prime(keysize):

    while True:
        n = random.randint(10 ** keysize, int("9" * (keysize + 1))) # This will create a random integer in the specified range

        if is_prime(n) is True: # This uses the is_prime function to check if it's prime and then repeats the loop if its not prime

            return n


def gcd(p, q): # Will calculate the greatest common divisor for the two prime numbers
# Will find the largest natural number that divides both p and q
    while q:
        p, q = q, p % q

    return p




def egcd(p, q): # Extended eucledian algorithm, this is more efficient and utilises recursion

    if p == 0:
        return q, 0, 1

    else:

        g, y, x = egcd(q % p, p)
        return g, x - (q // p) * y, y



def modular_inv(p, q): # This will return the private key as the public key % phi(n)

    g, x, y = egcd(p, q)
    private_key = x % q
    return private_key


def get_totient(p, q):# Takes the two prime numbers and finds the totient of them

    return (p - 1) * (q - 1)


def generate_keys(keysize = 3):
    # e is the public key
    # d is the private key

    public_key = 0
    private_key = 0
    prime_product = 0

    p = generate_large_prime(keysize) # Gets prime number of a certain length
    q = generate_large_prime(keysize)

    prime_product = p * q # These are then mulitipied together so that we get a value that must be facrotoised by one of the prime numbers to be decrypted
    phi_n = get_totient(p, q) # This will get the totient of the two values

    while True:
        public_key = random.randint(10 ** keysize, int("9" * (keysize + 1)))
        #public_key = random.randint(2 ** (keysize - 1), 2 ** keysize - 1)

        if gcd(public_key, phi_n) == 1: # This will check if they are co prime (they do not have a positive interger to divide each other by other than 1)

            break

    private_key = modular_inv(public_key, phi_n) # This creates the private key which requires the modular inverse method

    return public_key, private_key, prime_product




def encrypt(public_key, prime_product, data):

    encrypted_data = ""

    for char in data: #iterates over the characters in the data
        char_ord = ord(char) #gets the unicode for it
        encrypted_data += str((char_ord ** public_key) % prime_product) + " " #does modular exponation (a^b) % c to get the encrypted data
        #print(str((char_ord ** public_key) % prime_product))
        #print(math.pow(char_ord, public_key, prime_product))


    return encrypted_data



def decrypt(private_key, prime_product, encrypted_data): #this will take the encrypted data and decrypt it

    decrypted_data = ""

    encrypted_data_list = encrypted_data.split() #will split the data into parts that are used by the split function

    for character in encrypted_data_list: # iterates over the encrypted data list
        if character:

            decrypted_data += chr(pow(int(character), private_key, prime_product)) # does modular exponation for the charcter codee, private key and the prime product
            #decrypted_data += chr((int(character) ** private_key) % prime_product)

    return decrypted_data



"""
#public_key, private_key, prime_product = generate_keys()

public_key, private_key, prime_product = 4309, 1014589, 1115111

data = "new test string"

print(public_key, private_key, prime_product)
encrypted_data = encrypt(public_key, prime_product, data)

encrypted_data = "760428 348655 299621 299621 488402"

print(encrypted_data)
decrypted_data = decrypt(private_key, prime_product, encrypted_data)
print(decrypted_data)
"""


