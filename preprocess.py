import re

import pandas as pd

# Load the scraped data
df = pd.read_csv('telegram_data.csv')

# Function to clean and normalize Amharic text
def clean_text(text):
    if not isinstance(text, str):
        return ""
    # Remove emojis, Latin characters, special characters except Amharic punctuation
    text = re.sub(r"[^\u1200-\u137F\u1380-\u139F\u2D80-\u2DDFA-Za-z0-9፡።\s]", "", text)
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    return text.strip()

# Apply cleaning to the Message column
df['cleaned_message'] = df['Message'].apply(clean_text)

# Optional: Filter out empty messages after cleaning
df = df[df['cleaned_message'].str.len() > 0]

# Optional: Filter out messages that don't look like product listings (e.g., must contain 'ብር' or 'ዋጋ')
keywords = ['ብር', 'ዋጋ', 'የሽያጭ', 'እቃ', 'ምርት']
df = df[df['cleaned_message'].apply(lambda msg: any(keyword in msg for keyword in keywords))]

# Save the result to a new file
df.to_csv('preprocessed_data.csv', index=False, encoding='utf-8')

print(f"✅ Preprocessing complete. {len(df)} messages saved to preprocessed_data.csv")
