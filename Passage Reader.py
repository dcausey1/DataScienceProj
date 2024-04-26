import csv
import re
import nltk
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

def calculate_grade_level(text):
    # Tokenize the text into words and sentences
    words = word_tokenize(text)
    sentences = sent_tokenize(text)

    # Remove punctuation and stopwords
    words = [word.lower() for word in words if word.isalnum()]
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Count the number of words, sentences, and syllables
    num_words = len(words)
    num_sentences = len(sentences)
    num_syllables = sum([syllable_count(word) for word in words])

    # Calculate the Flesch-Kincaid Grade Level
    if num_words == 0:
        return 0
    else:
        grade_level = 0.39 * (num_words / num_sentences) + 11.8 * (num_syllables / num_words) - 15.59
        return round(grade_level, 2)

def syllable_count(word):
    vowels = "aeiouy"
    count = 0
    prev_char = ''  # Initialize prev_char to an empty string
    for char in word:
        if char.lower() in vowels and prev_char not in vowels:
            count += 1
        prev_char = char.lower()
    if word.endswith('e'):
        count -= 1
    if count == 0:
        count += 1
    return count

def main():
    # Ask the user for input choice
    choice = input("Do you want to enter a passage manually (type 'manual') or read from CSV (type 'csv')? ").lower()

    grade_levels = []

    if choice == 'manual':
        passage = input("Enter the passage: ")
        grade_level = calculate_grade_level(passage)
        grade_levels.append(grade_level)
        print("Grade Level:", grade_level)
    elif choice == 'csv':
        # Open the CSV file
        with open('passages.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            for row in reader:
                passage = row[1]  # Assuming the passage is in the second column ('excerpt')

                # Skip short or non-text passages
                if len(passage) < 10 or not any(char.isalpha() for char in passage):
                    continue

                grade_level = calculate_grade_level(passage)
                grade_levels.append(grade_level)
                print("Passage:", passage)
                print("Grade Level:", grade_level)
                print()
    else:
        print("Invalid choice.")

    # Plotting the trend
    plt.plot(grade_levels)
    plt.xlabel('Passage Index')
    plt.ylabel('Grade Level')
    plt.title('Grade Level Trend Across Passages')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
