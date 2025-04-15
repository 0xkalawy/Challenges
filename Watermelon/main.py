from PIL import Image
from sys import argv

if len(argv)!=3:
    print(f"Usage: {argv[0]} <Top-Image> <Bottom-Image>")
    exit()
# Load the two images
top_image_path = argv[1]
bottom_image_path = argv[2]

top_image = Image.open(top_image_path)
bottom_image = Image.open(bottom_image_path)

# Resize the bottom image to match the top image's width
bottom_image_resized = bottom_image.resize((top_image.width, int(bottom_image.height * (top_image.width / bottom_image.width))))

# Create a new image with height = sum of both images
merged_height = top_image.height + bottom_image_resized.height
merged_image = Image.new("RGB", (top_image.width, merged_height))

# Paste the images
merged_image.paste(top_image, (0, 0))
merged_image.paste(bottom_image_resized, (0, top_image.height))

# Save the result
merged_image_path = "/home/wego/test/challenges/Watermelon/gaza/merged.jpg"
merged_image.save(merged_image_path)

merged_image_path
