from datetime import datetime, timedelta
import publix_db as db

from transformers import pipeline

def categorize_items(items):
    classifier = pipeline("zero-shot-classification")

    labels = ['fruit', 'vegetable', 'dairy', 'meat', 'snack', 
              'household supplies', 'drink', 'breakfast', 'dessert', 
              'kitchen', 'flowers']
    
    for item in items:
        result = classifier(item, labels)
        print(f"{item} is classified as {result['labels'][0]}")

def get_week_range(current_date):
    # Calculate the most recent Thursday
    days_since_thursday = (current_date.weekday() - 3) % 7  # Thursday is weekday 3
    start_of_week = current_date - timedelta(days=days_since_thursday)
    
    # Calculate the upcoming Wednesday
    end_of_week = start_of_week + timedelta(days=6)
    
    # Format the dates as MM/DD for the message
    start_str = start_of_week.strftime("%m/%d")
    end_str = end_of_week.strftime("%m/%d")
    
    return start_str, end_str

def display_bogo_message():
    today = datetime.now()
    
    # Get the current week's date range (Thursday to Wednesday)
    start_str, end_str = get_week_range(today)
    
    # Print the BOGO message for the current week
    print(f"\nBOGO items for the week of {start_str} - {end_str}")


if __name__ == "__main__":
    # categorize_items(bogo_items)
    display_bogo_message()
    db.printItems()