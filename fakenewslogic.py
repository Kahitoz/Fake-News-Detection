import re
import math
from datasets import load_dataset

# Load the train dataset
train_dataset = load_dataset("mohammadjavadpirhadi/fake-news-detection-dataset-english", "main", split="train")

# Load the test dataset
test_dataset = load_dataset("mohammadjavadpirhadi/fake-news-detection-dataset-english", "main", split="test")


x_train = train_dataset['text']
y_train = train_dataset['label']
x_test = test_dataset['text']
y_test = test_dataset['label']

# Encode labels into integers (0 for fake, 1 for real)
y_train = [0 if label == "FAKE" else 1 for label in y_train]
y_test = [0 if label == "FAKE" else 1 for label in y_test]

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

    response_data = {
        "score_1": avg_jaccard_similarity,
        "score_2": avg_cosine_similarity,
        "remark_1": "This news is likely fake according to Jaccard similarity!"
        if avg_jaccard_similarity <= threshold
        else "This news seems to be legitimate according to Jaccard similarity.",
        "remark_2": "This news is likely fake according to Cosine similarity!"
        if avg_cosine_similarity <= threshold
        else "This news seems to be legitimate according to Cosine similarity.",
    }

    print("Jaccard similarity score:", avg_jaccard_similarity)
    print(response_data["remark_1"])

    print("Cosine similarity score:", avg_cosine_similarity)
    print(response_data["remark_2"])

    return response_data

# Example usage:
text = "FBI agents say the bureau is alarmed over Director James Comey s decision to not suggest that the Justice Department prosecute Hillary Clinton over her mishandling of classified information.According to an interview transcript given to The Daily Caller, provided by an intermediary who spoke to two federal agents with the bureau last Friday, agents are frustrated by Comey s leadership. This is a textbook case where a grand jury should have been convened, but was not. That is appalling,  an FBI special agent who has worked public corruption and criminal cases said of the decision.  We talk about it in the office and don t know how Comey can keep going. The agent was also surprised that the bureau did not bother to search Clinton s house during the investigation. We didn t search their house. We always search the house. The search should not just have been for private electronics, which contained classified material, but even for printouts of such material,  he said. There should have been a complete search of their residence,  the agent pointed out.  That the FBI did not seize devices is unbelievable. The FBI even seizes devices that have been set on fire. Another special agent for the bureau who worked counter-terrorism and criminal cases said he is offended by Comey s saying:  we  and  I ve been an investigator. After graduating from law school, Comey became a law clerk to a U.S. District Judge in Manhattan and later became an associate in a law firm in the city. After becoming a U.S. Attorney in the Southern District of New York, Comey s career moved through the U.S. Attorney s Office until he became Deputy Attorney General during the George W. Bush administration.After Bush left office, Comey entered the private sector and became general counsel and Senior Vice President for Lockheed Martin, among other private sector posts. President Barack Obama appointed him to FBI director in 2013 replacing out going-director Robert Mueller. Comey was never an investigator or special agent. The special agents are trained investigators and they are insulted that Comey included them in  collective we  statements in his testimony to imply that the SAs agreed that there was nothing there to prosecute,  the second agent said.  All the trained investigators agree that there is a lot to prosecuted but he stood in the way. He added,  The idea that [the Clinton/e-mail case] didn t go to a grand jury is ridiculous. According to Washington D.C. attorney Joe DiGenova, more FBI agents will be talking about the problems at bureau and specifically the handling of the Clinton case by Comey when Congress comes back into session and decides to force them to testify by subpoena.DiGenova told WMAL radio s Drive at Five last week,  People are starting to talk. They re calling their former friends outside the bureau asking for help. We were asked today to provide legal representation to people inside the bureau and agreed to do so and to former agents who want to come forward and talk. Comey thought this was going to go away."

# is_fake_news(text)
