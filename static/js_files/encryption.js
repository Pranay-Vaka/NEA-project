function get_rand_int(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);

    return Math.floor(Math.random() * (max - min + 1) + min); // Thsi will be inclusive of both the min and the max value
}

/*function miller_rabin(prime, cycles) {
    let r = 0;
    let s = prime - 1;

    while (s % 2 == 0) {
        r = r + 1
        s = Math.floor(s / 2)
    }


    for (let i = 0; i < cycles; i++) {
        let a = get_rand_int(2, prime - 2)
        let x = (a ** s) % prime

        if (x == 1 || x == prime - 1) { continue }

        for (let i = 0; i < r - 1; i++) {

            x = (x ** 2) % prime

            if (x == prime - 1) { break }

        }

        else { return false }


    }

    return true

}*/


function is_prime(n) { // This will check if the number is prime using some small prime numbers as well

    let low_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

    for (let i in low_primes) {
        if (i == n || n % i == 0) { return false }
    }

    if (n % 2 == 0) { return false }


    //miller_rabin(n, 40)
}


function generate_large_prime(keysize) {

    while (true) {
        let max_size = ""

        for (let i = 0; i < keysize + 1; i++) {
            max_size = max_size + "9"
        }

        max_size = parseInt(max_size)

        let n = get_rand_int(10 ** keysize, max_size)

        if (is_prime(n) == true) { return n }

    }
}

function gcd(p, q) { // Will calculate the greatest common divisor for the two prime numbers

    while (q == true) {
        p, q = q, p % q
    }
    return p
}

function egcd(a, b) {

    if (a == 0) {
        return b, 0, 1
    }

    else {
        let g = 0
        let y = 0
        let x = 0

        g, y, x = egcd(b % a, a)
        return g, x - Math.floor(b / a) * y, y

    }
}


function modular_inv(a, b) { // This will return the private key as the public key % phi(n)

    let x = 0
    let g = 0
    let y = 0

    g, x, y = egcd(a, b)
    let private_key = x % b
    return private_key
}

function get_totient(p, q) { //Takes the two prime numbers and finds the totient of them

    return (p - 1) * (q - 1)
}

function generate_keys(keysize = 4) {
    // e is the public key
    // d is the private key

    let public_key = 0
    let private_key = 0
    let prime_product = 0

    let p = generate_large_prime(keysize) // Gets prime number of a certain length
    let q = generate_large_prime(keysize)

    prime_product = p * q // These are then mulitipied together so that we get a value that must be facrotoised by one of the prime numbers to be decrypted
    let phi_n = get_totient(p, q) // This will get the totient of the two values

    while (true) {
        //e = random.randrange(10 ** keysize, int("9" * (keysize + 1)))
        public_key = get_rand_int(2 ** (keysize - 1), 2 ** keysize - 1)

        if (gcd(public_key, phi_n) == 1) {// This will check if they are co prime (they do not have a positive interger to divide each other by other than 1)
            break
        }

    }

    private_key = modular_inv(public_key, phi_n) // This creates the private key which requires the modular inverse method

    return public_key, private_key, prime_product
}


function modular_exponentiation(base, exponent, modulus) { // This will find the modular exponation within the bounds of a javascript integer

    if (modulus == 1) { // If the modulus is one then it will be perfectly divisible and so would always return 0
        return 0
    }

    let result = 1
    base %= modulus

    while (exponent > 0) { // The exponent must be positive for this to work
        if (exponent % 2 == 1) // This will check if the exponent is an odd number
            result = (result * base) % modulus
        exponent >>= 1 // This will divide the exponent by 2 by right shifitng it once
        base = (base ** 2) % modulus // squares the base and finds the exponential modulus
    }
    return result
}



function encrypt(public_key, prime_product, data) {

    let encrypted_data = ""

    for (let i of data) { //iterates over the characters in the data
        let char_ord = i.charCodeAt(0) // gets the unicode for it

        let new_char = (modular_exponentiation(char_ord, public_key, prime_product)).toString() // does modular exponation (a^b) % c to get the encrypted data

        encrypted_data += new_char + " " // will add it to the encrypted data
    }

    return encrypted_data

}


function decrypt(private_key, prime_product, encrypted_data) { // this will take the encrypted data and decrypt it

    let decrypted_data = ""

    let encrypted_data_list = encrypted_data.split(" ") // will split the data into parts that are used by the split function

    for (let character of encrypted_data_list) { // iterates over the encrypted data list

        if (character) {
            decrypted_data += String.fromCharCode(modular_exponentiation(parseInt(character), private_key, prime_product)) // does modular exponation for the charcter codee, private key and the prime product 
        }
    }

    return decrypted_data
}

/*
let e = 4309
let d = 1014589
let N = 1115111

let string = "hello"


let data = encrypt(e, N, string)
console.log(data)
let decrypted_data = decrypt(d, N, data)
console.log(decrypted_data)
*/


