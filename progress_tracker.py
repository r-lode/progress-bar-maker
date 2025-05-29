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
    # Overall image dimensions
    bar_width = 100
    bar_height = 400
    label_height = 40
    total_height = label_height + bar_height
    radius = 15

    # Calculate progress height
    progress_height = int(bar_height * min(current / goal, 1.0))
    progress_top = label_height + bar_height - progress_height

    # Create base image with transparent background
    img = Image.new('RGBA', (bar_width, total_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    bg_color = '#FFFFFF'      # White for unfilled
    progress_color = '#001f3f' # Navy for filled
    border_color = '#333333'   # Dark border
    label_color = '#FFFFFF'    # White title label

    # Create mask for rounded corners
    full_mask = Image.new('L', (bar_width, total_height), 0)
    mask_draw = ImageDraw.Draw(full_mask)
    mask_draw.rounded_rectangle([0, 0, bar_width, total_height], radius, fill=255)

    # Draw unfilled background
    draw.rounded_rectangle([0, label_height, bar_width, total_height], radius, fill=bg_color, outline=border_color, width=2)

    # Draw progress fill
    progress_img = Image.new('RGBA', (bar_width, bar_height), (0, 0, 0, 0))
    progress_draw = ImageDraw.Draw(progress_img)
    progress_draw.rectangle([0, bar_height - progress_height, bar_width, bar_height], fill=progress_color)
    img.paste(progress_img, (0, label_height), progress_img)

    # Draw tick marks and labels dynamically colored
    font = ImageFont.load_default()
    tick_spacing = 50
    label_padding = 5
    for tick in range(0, goal + 1, tick_spacing):
        y = label_height + bar_height - int(bar_height * tick / goal)
        y = min(max(label_height + label_padding, y), label_height + bar_height - label_padding)

        # Determine tick color: white if in progress area, black otherwise
        tick_color = '#FFFFFF' if y >= progress_top else '#000000'

        # Draw tick line
        draw.line([(label_padding, y), (20, y)], fill=tick_color, width=2)

        # Draw tick label
        draw.text((25, y - 6), f"{tick}", fill=tick_color, font=font)

    # Draw the exam label text at top in white, with dark outline for readability
    label_bbox = draw.textbbox((0, 0), exam_label, font=font)
    label_width = label_bbox[2] - label_bbox[0]
    label_x = (bar_width - label_width) // 2
    label_y = (label_height - (label_bbox[3] - label_bbox[1])) // 2

    outline_color = '#000000'
    for offset in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
        draw.text((label_x + offset[0], label_y + offset[1]), exam_label, fill=outline_color, font=font)

    draw.text((label_x, label_y), exam_label, fill=label_color, font=font)


    # Apply rounded corner mask
    img.putalpha(full_mask)

    # Save final image
    img.convert('RGB').save(filename)

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
