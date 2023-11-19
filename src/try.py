from datetime import datetime, timedelta

def get_first_day_of_week(date):
    # Calculate the difference between the current day and Monday (0)
    days_to_monday = date.weekday()

    # Subtract the difference to get the first day of the week
    first_day_of_week = date - timedelta(days=days_to_monday)

    return first_day_of_week.date()

# Example usage
date_obj = datetime(2023, 11, 17)  # Replace with your datetime object
first_day_of_week = get_first_day_of_week(date_obj)

print("Original Date:", date_obj)
print("First Day of the Week:", first_day_of_week)