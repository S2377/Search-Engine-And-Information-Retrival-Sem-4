
################################### required module ####################################

import requests
import re
# importing the previous work done for scrapping(assignment-2)
from web_scrapping import*

################################## Helper function #####################################

def hash_word(word):
    p = 53
    m = 2**64
    sum = 0
    for i in range(len(word)):
        sum += ord(word[i])*p**i
        
    hash_code = sum % m
    return hash_code

def hash_to_binary(hashcode):
    if hashcode == 0:
        return "0b" + "0" * 64
    
    binary_representation = ""
    while hashcode > 0:
        remainder = hashcode % 2
        binary_representation = str(remainder) + binary_representation
        hashcode = hashcode // 2

    padding_length = 64 - len(binary_representation)
    binary_representation = "0" * padding_length + binary_representation

    return binary_representation

def calculate_hash_vector(word,frequency, hash_size):
    """Calculates a weighted hash vector for a single word."""
    hash_value = hash_word(word)
    bin_hash = str(hash_to_binary(hash_value))
    vector = [0] * hash_size
    for i in range(hash_size):
        if bin_hash[i] == "0":  
            vector[i] = -1*frequency 
        else:
            vector[i] = 1 * frequency
            
    # print(word ," ",hash_value)
    return vector

def generate_ngrams(input_list, n=5, overlap = 2):
    ngrams = []
    for i in range(0, len(input_list) - n + 1, overlap+1):
        ngram = input_list[i:i + n]
        ngrams.extend(ngram)
    return ngrams


def word_frequency_count(body_content):
    w = body_content.split()
    words = generate_ngrams(w)
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1   
    # print(word_count)
    return word_count

def column_sum(matrix):
    num_rows = len(matrix)
    num_cols = len(matrix[0]) if num_rows > 0 else 0

    if num_cols == 0:
        return []

    column_sums = [0] * num_cols

    for col in range(num_cols):
        for row in range(num_rows):
            column_sums[col] += matrix[row][col]

    return column_sums


################################## Document cleaning  #####################

import string


def percentage(num):
    total = (num*64)//100
    print("percentage similarity :" ,num)
    print("total similar bit :-",total)

def remove_punctuation(text):
    # Remove punctuation from the text
    return ''.join(char for char in text if char not in string.punctuation)

def remove_stopwords(text, stopwords):
    # Tokenize the text and remove stop words
    words = text.split()
    filtered_words = [word.lower() for word in words if word.lower() not in stopwords]
    return ' '.join(filtered_words)

def clean_text(text):
    # Define your own list of stop words
    custom_stopwords = set(["the", "and", "is", "it", "in", "with", "some", "a", "an"])

    # Remove punctuation
    text_no_punct = remove_punctuation(text)

    # Remove stop words
    cleaned_text = remove_stopwords(text_no_punct, custom_stopwords)

    return cleaned_text


################################## Simhash Algorithms ###########################

def simhash(text, hash_size=64):
    """Calculates the Simhash fingerprint of a given document"""
    text = clean_text(text)
    token_counts = word_frequency_count(text) # Count occurrences of each word
    vectors = []
    for token, count in token_counts.items():
        a = calculate_hash_vector(token,count,64)
        vectors.append(a)
        
    # print(vectors)
    final_vector = column_sum(vectors)     
    fingerprint = [0]*64      
    for i in range(64):
        if final_vector[i] > 0:
            fingerprint[i] = 1   
        else:
            fingerprint[i] = 0   
    return fingerprint


######################################### Taking URL from the user ####################
            
# Get HTML content from the first URL
url1 = input("Enter the first URL: ")
html_content1 = get_html_content(url1)
# Extract the body content from the first URL
body_content1 = extract_body(html_content1)

# Compute Simhash for the first document
simhash1 = simhash(body_content1)

# Get HTML content from the second URL
url2 = input("Enter the second URL: ")
html_content2 = get_html_content(url2)

# Extract the body content from the second URL
body_content2 = extract_body(html_content2)

text1 = body_content1
text2 = body_content2
 
hash1 = simhash(text1)
hash2 = simhash(text2)
def binary_form(lst):
    b = ""
    for i in lst:
        b = b + str(i)   
    return b
hash1 = binary_form(hash1)
hash2 = binary_form(hash2)

print(hash1)
print(hash2)

########################################### Comparision of Two simhases #####################

def simhash_comparision(s1,s2):
    a1 = str(s1)
    a2 = str(s2)
    unset_bit = 0
    for i in range(64):
        if a1[i] == "0" and a2[i] == "0":
            unset_bit += 1
    return unset_bit
result = simhash_comparision(hash1,hash2)
percentage(result)








