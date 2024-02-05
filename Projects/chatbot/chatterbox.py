import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import random

def load_json(relative_path):
    """
    Load the JSON data from a file specified by a relative path.

    Args:
        relative_path (str): The relative path to the JSON file.

    Returns:
        dict: A dictionary containing the loaded JSON data.
    """
    with open(relative_path, 'r') as file:
        return json.load(file)

def calculate_age(birthdate_str):
    """
    Calculate the age of the chatbot in a more precise manner.

    Args:
        birthdate_str (str): The birthdate of the chatbot in 'YYYY-MM-DD' format.

    Returns:
        str: The age of the chatbot in years, months, and days.
    """
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
    today = datetime.now()
    age = relativedelta(today, birthdate)
    return f"{age.years} years, {age.months} months, and {age.days} days"

def find_closest_query(user_input, queries):
    """
    Find the closest matching query for the user's input using fuzzy string matching.

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
        for pattern in patterns:
            score = fuzz.token_sort_ratio(user_input, pattern)
            if score > max_score:
                max_score = score
                chosen_query = query

    return chosen_query if max_score >= 50 else None  # Lower the threshold to 50 for broader matching

def chatbot_response(user_input, queries, profile):
    """
    Generate a response from the chatbot based on the user's input.

    Args:
        user_input (str): The user's input string.
        queries (dict): The dictionary containing queries and their responses.
        profile (dict): The chatbot's profile information.

    Returns:
        tuple: A response from the chatbot and a flag indicating if the chat should end.
    """
    query = find_closest_query(user_input, queries)
    if query:
        response = random.choice(queries[query]['responses'])
        response = response.replace("[CALCULATED_AGE]", calculate_age(profile['birthday']))
        end_chat = queries[query].get("end_chat", False)
        return response, end_chat
    else:
        return "I'm not sure how to respond to that. Can you ask something else?", False

def main():
    data = load_json('chatbot/prompts.json')
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
