#!/usr/bin/env python3
'''
    Kiri Salij
    27 October 2023

    passwords.py
    Jeff Ondich, 6 May 2022

    Shows how to compute a SHA-256 hash and manipulate the
    relevant Python types.

    Note that when you want to do a new hash, you need to
    call hashlib.sha256() again to get a fresh sha256 object.
'''

import hashlib
import binascii
import random

# computes the hash of a given word and returns it as a hex string
def compute_hash(word):
    encoded_word = word.encode('utf-8')
    hasher = hashlib.sha256(encoded_word)
    digest = hasher.digest()
    digest_as_hex = binascii.hexlify(digest)
    digest_as_hex_string = digest_as_hex.decode('utf-8')

    return digest_as_hex_string

# Part 1 - one-word passwords
def part_1():
    cracked1 = open('cracked1.txt', 'w')

    words = [line.strip().lower() for line in open('words.txt')]
    hash_dict = {}
    hash_count = 0
    cracked_count = 0

    # precompute the hashes
    for word in words:
        hash = compute_hash(word)
        hash_dict[hash] = word
        hash_count+=1

    # finds the hash in the hash_dict and matches it with the password associated with it
    for line in open('passwords1.txt'):
        info = line.split(':')
        if info[1] in hash_dict:
            print(info[0] + ":" + hash_dict[info[1]], file=cracked1)
            cracked_count+=1

    print("Hashes computed: " + str(hash_count))
    print("Passwords Cracked: " + str(cracked_count))

# Part 2 - two-word passwords
def part_2():
    words = [line.strip().lower() for line in open('words.txt')]
    words.append('') #bc jeff's password is just one word (marmot)
    random.shuffle(words)
    user_dict = {}
    hash_count = 0
    cracked_count = 0

    cracked2 = open('cracked2.txt', 'w')

    # data processing
    for line in open('passwords2.txt'):
        info = line.split(':')
        user_dict[info[1]] = info[0] #unlikely (but possible) users were assigned same password so we can do this with the hashes as the keys
    
    num_users = len(user_dict) 

    # iterates through all of the pairs of words and checking if the hash exists in the dictionary
    for word1 in words:
        for word2 in words:
            hash = compute_hash(word1+word2)
            hash_count+=1

            if hash in user_dict:
                user = user_dict[hash]
                print(user + ":" + word1+word2, file=cracked2)
                
                print("Hashes computed: " + str(hash_count))
                print("Passwords Cracked: " + str(cracked_count))
                cracked_count+=1

            if cracked_count >= num_users: 
                break

# Part 3 - one-word salted passwords
def part_3():
    words = [line.strip().lower() for line in open('words.txt')]
    random.shuffle(words)
    hash_count = 0
    cracked_count = 0

    cracked3 = open('cracked3.txt', 'w')
    
    for line in open('passwords3.txt'):
        # data processing
        info = line.split(':')
        salt_info = info[1].split('$')
        user = info[0]
        salt = salt_info[2]
        user_hash = salt_info[3]

        # computes the hash of the salt and each word until hitting the correct hash
        for word in words:
            hash = compute_hash(salt+word)
            hash_count+=1

            if hash == user_hash:
                print(user + ":" + word, file=cracked3)
                cracked_count+=1
                break
            
    print("Hashes computed: " + str(hash_count))
    print("Passwords Cracked: " + str(cracked_count))



# uncomment out the part you want to run
# part_1()
# part_2()
# part_3()