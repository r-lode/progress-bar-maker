import json
from PIL import Image, ImageDraw, ImageFont

# File to store progress data
DATA_FILE = 'progress_data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def create_progress_bar(exam_label, goal, current, filename):
    width = 400
    height = 50
    bar_width = int(width * min(current / goal, 1.0))

    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Background bar
    draw.rectangle([0, 0, width, height], fill='lightgrey')

    # Progress
    draw.rectangle([0, 0, bar_width, height], fill='green')

    # Text
    font = ImageFont.load_default()
    text = f"{exam_label}: {current}/{goal} hours"
    draw.text((10, 15), text, fill='black', font=font)

    img.save(filename)

def add_hours(user_name, exam_name, hours):
    data = load_data()

    # Create user entry if it doesn't exist
    if user_name not in data:
        data[user_name] = {}

    # Create exam entry if it doesn't exist
    if exam_name not in data[user_name]:
        goal_hours = int(input(f"Enter total goal hours for {exam_name}: "))
        data[user_name][exam_name] = {"goal_hours": goal_hours, "current_hours": 0}

    # Update progress
    data[user_name][exam_name]['current_hours'] += hours
    save_data(data)

    print(f"Added {hours} hours to {user_name}'s {exam_name}.")

    # Ask if the user wants to generate an image
    generate = input("Would you like to generate the progress bar image? (y/n): ").lower()
    if generate == 'y':
        label = f"{user_name} - {exam_name}"
        filename = f"{user_name}_{exam_name.replace(' ', '_')}.png"
        create_progress_bar(label, data[user_name][exam_name]['goal_hours'], data[user_name][exam_name]['current_hours'], filename)
        print(f"Progress bar updated and saved as '{filename}'.")

def main():
    user = input("Enter your name: ")
    exam = input("Enter exam name: ")
    hours = int(input("Enter hours studied: "))
    add_hours(user, exam, hours)

if __name__ == "__main__":
    main()
