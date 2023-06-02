import requests
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to retrieve web page content
def get_page_content(url):
    response = requests.get(url)
    return response.text

# Function to preprocess text
def preprocess_text(text):
    # Remove HTML tags and special characters
    clean_text = re.sub('<.*?>', '', text)
    clean_text = re.sub(r'[^\w\s]', '', clean_text)
    return clean_text.lower()

# Function to generate shingles from text
def generate_shingles(text, k):
    shingles = set()
    words = text.split()
    for i in range(len(words) - k + 1):
        shingle = ' '.join(words[i:i+k])
        shingles.add(shingle)
    return shingles

# Function to calculate Jaccard similarity
def calculate_jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1) + len(set2) - intersection
    similarity = intersection / union
    return similarity

# Function to check plagiarism using Shingle algorithm
def check_plagiarism_shingle(text, threshold):
    # Retrieve web page content
    page_content = get_page_content(url)
    preprocessed_content = preprocess_text(page_content)
    
    # Generate shingles from the content
    shingles = generate_shingles(preprocessed_content, k)
    
    # Calculate Jaccard similarity with previously stored shingles
    similarity_scores = []
    for stored_shingles in stored_shingles_list:
        similarity = calculate_jaccard_similarity(stored_shingles, shingles)
        similarity_scores.append(similarity)
    
    # Check if any similarity score is above the threshold
    if max(similarity_scores) > threshold:
        return True
    else:
        # Store the shingles for future comparisons
        stored_shingles_list.append(shingles)
        return False

# Function to check plagiarism using TF-IDF and cosine similarity
def check_plagiarism_tfidf(url, threshold=0.8):
    # Retrieve web page content
    page_content = get_page_content(url)
    preprocessed_content = preprocess_text(page_content)
    
    # Calculate TF-IDF vectors
    documents = stored_documents + [preprocessed_content]
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    
    # Calculate cosine similarity with previously stored documents
    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
    
    # Check if any similarity score is above the threshold
    if max(similarity_scores) > threshold:
        return True
    else:
        # Store the document for future comparisons
        stored_documents.append(preprocessed_content)
        return False

# List to store the shingles for comparison
stored_shingles_list = []

# List to store the documents for comparison
stored_documents = []

# Example usage
url = 'https://www.example.com/blog/article'
is_plagiarized_shingle = check_plagiarism_shingle(url)
is_plagiarized_tfidf = check_plagiarism_tfidf(url)

if is_plagiarized
