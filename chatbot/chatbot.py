import json
import random
from fuzzywuzzy import process
from datetime import datetime

def load_json(file_path):
    """
    Load the JSON data from the specified file path.

    Args:
    file_path (str): The path to the JSON file.

    Returns:
    dict: A dictionary containing the loaded JSON data.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def calculate_age(birthdate_str):
    """
    Calculate the chatbot's age based on its birthdate.

    Args:
    birthdate_str (str): The birthdate of the chatbot in 'YYYY-MM-DD' format.

    Returns:
    str: The age of the chatbot in years, months, and days.
    """
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
    today = datetime.now()
    age = today - birthdate
    years = age.days // 365
    months = (age.days % 365) // 30
    days = (age.days % 365) % 30
    return f"{years} years, {months} months, and {days} days"

def find_closest_query(user_input, queries):
    """
    Find the closest matching query for the user's input.

    Args:
    user_input (str): The user's input string.
    queries (dict): The dictionary containing queries and their patterns.

    Returns:
    str: The key of the closest matching query, or None if no match is found.
    """
    max_score = 0
    chosen_query = None

    for query, data in queries.items():
        patterns = data['patterns']
        highest = process.extractOne(user_input, patterns)[1]
        if highest > max_score:
            max_score = highest
            chosen_query = query

    return chosen_query if max_score > 60 else None

def chatbot_response(user_input, queries, profile):
    """
    Generate a response from the chatbot based on the user's input.

    Args:
    user_input (str): The user's input string.
    queries (dict): The dictionary containing queries and their responses.
    profile (dict): The chatbot's profile information.

    Returns:
    str: A response from the chatbot.
    """
    query = find_closest_query(user_input, queries['queries'])
    if query:
        response = random.choice(queries['queries'][query]['responses'])

        # Replace placeholders with dynamic content
        if "[CALCULATED_AGE]" in response:
            response = response.replace("[CALCULATED_AGE]", calculate_age(profile['birthday']))

        # Check if the conversation should end
        end_chat = queries['queries'][query].get("end_chat", False)
        return response, end_chat
    else:
        return "I'm not sure how to respond to that. Can you ask something else?", False

def main():
    data = load_json('prompts.json')
    queries = data['queries']
    profile = data['chatbot_profile']

    print(f"Hi, I'm {profile['name']}, your friendly chatbot. I was born on {profile['birthday']}. How can I assist you today?")

    while True:
        user_input = input("You: ").lower()
        response, end_chat = chatbot_response(user_input, queries, profile)
        print(f"{profile['name']}:", response)
        if end_chat:
            break

if __name__ == "__main__":
    main()
