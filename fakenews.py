# -*- coding: utf-8 -*-
"""FakeNews.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1a0gLs-thLYtsjZfL8gOlpCYE_8lh5JwJ
"""

!pip install datasets

from datasets import load_dataset

# Load the train dataset
train_dataset = load_dataset("mohammadjavadpirhadi/fake-news-detection-dataset-english", "main", split="train")

# Load the test dataset
test_dataset = load_dataset("mohammadjavadpirhadi/fake-news-detection-dataset-english", "main", split="test")

# You can access the text and label columns as follows:
x_train = train_dataset['text']
y_train = train_dataset['label']
x_test = test_dataset['text']
y_test = test_dataset['label']

# Encode labels into integers (0 for fake, 1 for real)
y_train = [0 if label == "FAKE" else 1 for label in y_train]
y_test = [0 if label == "FAKE" else 1 for label in y_test]

# Now you can proceed with the rest of your classification code as previously discussed.

# Assuming you have already loaded the dataset
from datasets import load_dataset

# Load the train dataset
train_dataset = load_dataset("mohammadjavadpirhadi/fake-news-detection-dataset-english", "main", split="train")

# Access the text and label columns
x_train = train_dataset['text']
y_train = train_dataset['label']

# Print all examples in the training dataset with real/fake labels
for i in range(len(x_train)):
    real_or_fake = "Real" if y_train[i] == 1 else "Fake"
    print(f"Text: {x_train[i]}")
    print(f"Label: {y_train[i]} ({real_or_fake})\n")

from sklearn.feature_extraction.text import TfidfVectorizer

# Create a TF-IDF vectorizer
vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7)

# Convert list elements to strings
x_train_str = [str(x) for x in x_train]
x_test_str = [str(x) for x in x_test]

# Vectorize the training data
x_train_vectorized = vectorizer.fit_transform(x_train_str)

# Vectorize the test data
x_test_vectorized = vectorizer.transform(x_test_str)

from sklearn.svm import LinearSVC

# Create and train a LinearSVC classifier
clf = LinearSVC()
clf.fit(x_train_vectorized, y_train)

# Calculate accuracy on the testing set
accuracy = clf.score(x_test_vectorized, y_test)
print(f"Accuracy on the testing set: {accuracy * 100:.2f}%")

# Make predictions for a new text
new_text = "This is a new text that you want to classify."
vectorized_text = vectorizer.transform([new_text])
predicted_label = clf.predict(vectorized_text)

# Convert the predicted label to human-readable form (Real or Fake)
predicted_label_human_readable = "Real" if predicted_label == 1 else "Fake"

print(f"Predicted Label: {predicted_label[0]} ({predicted_label_human_readable})")

import re
import math

def tokenize(text):
    """Converts a text string into a list of tokens (words)."""
    text = text.lower()
    tokens = re.findall(r'\b\w+\b', text)
    return set(tokens)

def jaccard_similarity(text1, text2):
    """Calculates the Jaccard similarity coefficient between two sets of tokens."""
    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    return len(intersection) / len(union)

def cosine_similarity(text1, text2):
    """Calculates the cosine similarity between two texts."""
    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)

    # Create a set of all unique words in both texts
    all_words = tokens1.union(tokens2)

    # Create vectors of word frequencies for each text
    vector1 = [list(tokens1).count(word) for word in all_words]
    vector2 = [list(tokens2).count(word) for word in all_words]

    # Calculate the dot product and magnitudes of the vectors
    dot_product = sum([vector1[i] * vector2[i] for i in range(len(vector1))])
    magnitude1 = math.sqrt(sum([count**2 for count in vector1]))
    magnitude2 = math.sqrt(sum([count**2 for count in vector2]))

    # Calculate the cosine similarity between the vectors
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    else:
        return dot_product / (magnitude1 * magnitude2)

def is_fake_news(text, threshold=0.1):
    # Load some example real news articles for comparison
    real_news_articles = x_train  # Assuming x_train contains real news articles

    # Calculate Jaccard and cosine similarities between the input text and each real news article
    jaccard_similarities = [jaccard_similarity(text, article) for article in real_news_articles]
    cosine_similarities = [cosine_similarity(text, article) for article in real_news_articles]

    # Determine whether the input text is more similar to fake news or real news
    avg_jaccard_similarity = sum(jaccard_similarities) / len(jaccard_similarities)
    avg_cosine_similarity = sum(cosine_similarities) / len(cosine_similarities)

    if avg_jaccard_similarity <= threshold:
        print("Jaccard similarity score: ", avg_jaccard_similarity)
        print("This news is likely fake according to Jaccard similarity!")
    else:
        print("Jaccard similarity score: ", avg_jaccard_similarity)
        print("This news seems to be legitimate according to Jaccard similarity.")

    if avg_cosine_similarity <= threshold:
        print()
        print("Cosine similarity score: ", avg_cosine_similarity)
        print("This news is likely fake according to Cosine similarity!")
    else:
        print()
        print("Cosine similarity score: ", avg_cosine_similarity)
        print("This news seems to be legitimate according to Cosine similarity.")

# Example usage:
text = "FBI agents say the bureau is alarmed over Director James Comey s decision to not suggest that the Justice Department prosecute Hillary Clinton over her mishandling of classified information.According to an interview transcript given to The Daily Caller, provided by an intermediary who spoke to two federal agents with the bureau last Friday, agents are frustrated by Comey s leadership. This is a textbook case where a grand jury should have been convened, but was not. That is appalling,  an FBI special agent who has worked public corruption and criminal cases said of the decision.  We talk about it in the office and don t know how Comey can keep going. The agent was also surprised that the bureau did not bother to search Clinton s house during the investigation. We didn t search their house. We always search the house. The search should not just have been for private electronics, which contained classified material, but even for printouts of such material,  he said. There should have been a complete search of their residence,  the agent pointed out.  That the FBI did not seize devices is unbelievable. The FBI even seizes devices that have been set on fire. Another special agent for the bureau who worked counter-terrorism and criminal cases said he is offended by Comey s saying:  we  and  I ve been an investigator. After graduating from law school, Comey became a law clerk to a U.S. District Judge in Manhattan and later became an associate in a law firm in the city. After becoming a U.S. Attorney in the Southern District of New York, Comey s career moved through the U.S. Attorney s Office until he became Deputy Attorney General during the George W. Bush administration.After Bush left office, Comey entered the private sector and became general counsel and Senior Vice President for Lockheed Martin, among other private sector posts. President Barack Obama appointed him to FBI director in 2013 replacing out going-director Robert Mueller. Comey was never an investigator or special agent. The special agents are trained investigators and they are insulted that Comey included them in  collective we  statements in his testimony to imply that the SAs agreed that there was nothing there to prosecute,  the second agent said.  All the trained investigators agree that there is a lot to prosecuted but he stood in the way. He added,  The idea that [the Clinton/e-mail case] didn t go to a grand jury is ridiculous. According to Washington D.C. attorney Joe DiGenova, more FBI agents will be talking about the problems at bureau and specifically the handling of the Clinton case by Comey when Congress comes back into session and decides to force them to testify by subpoena.DiGenova told WMAL radio s Drive at Five last week,  People are starting to talk. They re calling their former friends outside the bureau asking for help. We were asked today to provide legal representation to people inside the bureau and agreed to do so and to former agents who want to come forward and talk. Comey thought this was going to go away."

is_fake_news(text)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Create a TfidfVectorizer object
vectorizer = TfidfVectorizer(stop_words='english')

# Fit and transform the training data for cosine similarity
x_train_vectorized = vectorizer.fit_transform(x_train)

def cosine_similarity_score(news1, news2):
    # Transform news articles
    news1_vectorized = vectorizer.transform([news1])
    news2_vectorized = vectorizer.transform([news2])

    # Calculate cosine similarity
    similarity = cosine_similarity(news1_vectorized, news2_vectorized)[0][0]

    return similarity

# Example usage
news1 = "The moon landing was faked by the government."
news2 = "NASA successfully landed on the moon in 1969."

threshold = 0.6
similarity_score = cosine_similarity_score(news1, news2)

if similarity_score < threshold:
    print("The news articles are likely fake.")
else:
    print("The news articles are likely genuine.")

import re

def tokenize(text):
    """Converts a text string into a list of tokens (words)."""
    text = text.lower()
    tokens = re.findall(r'\b\w+\b', text)
    return set(tokens)

def jaccard_similarity(text1, text2):
    """Calculates the Jaccard similarity coefficient between two sets of tokens."""
    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    return len(intersection) / len(union)

def is_fake_news(text, threshold=0.5):
    # Load some example real news articles for comparison
    real_news_articles = x_train  # Assuming x_train contains real news articles

    # Calculate Jaccard similarity between the input text and each real news article
    similarities = [jaccard_similarity(text, article) for article in real_news_articles]

    # Determine whether the input text is more similar to fake news or real news
    avg_similarity = sum(similarities) / len(similarities)
    return avg_similarity <= threshold

# Example usage:
text = "The Prime Minister of India, Narendra Modi visits Punjab today (April 24, 2023)."

if is_fake_news(text):
    print("This news is likely fake!")
else:
    print("This news seems to be legitimate.")