import re
from pytube import YouTube

# Define your function_patterns
function_patterns = [
    r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&.*?\|\|\s*([a-z]+)',
    r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
    r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
]

# Example YouTube video URL
video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

# Create a YouTube object
yt = YouTube(video_url)

# Get the current title
original_title = yt.title

# Loop through each pattern and apply replacement
for pattern in function_patterns:
    regex = re.compile(pattern)
    modified_title = regex.sub('replacement_string', original_title)

# Set the modified title back to the YouTube object
yt.title = modified_title

# Print the modified title
print("Modified Title:", yt.title)