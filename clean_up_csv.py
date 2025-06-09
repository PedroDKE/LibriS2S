import pandas as pd
import os
from pathlib import Path

# Read the original CSV
alignment = pd.read_csv("alignments/all_de_en_alligned.csv", index_col=0)

# Create mapping of book numbers to English folder names
en_folder_map = {}
for folder in os.listdir("EN"):
    book_id = folder.split('.')[0]
    en_folder_map[book_id] = folder

# Function to construct full German audio path
def get_de_path(row):
    if "67" in row['book']:
        return os.path.join("DE","67.frankenstein_de_1211_librivox_newly_alligned", "sentence_level_audio", row['DE_audio'])
    return os.path.join("DE", row['book'], "sentence_level_audio", row['DE_audio'])

# Function to construct full English audio path
def get_en_path(row):
    book_id = str(row['book_id'])
    if book_id in en_folder_map:
        return os.path.join("EN", en_folder_map[book_id], "sentence_level_audio", row['EN_audio'] + ".wav")
    return None

# Update paths in the DataFrame
alignment['DE_audio'] = alignment.apply(lambda row: Path(get_de_path(row)).as_posix(), axis=1)
alignment['EN_audio'] = alignment.apply(lambda row: Path(get_en_path(row)).as_posix(), axis=1)

# Drop the 'book' column since paths are now complete
alignment = alignment.drop('book', axis=1)

# Drop rows where EN_audio path couldn't be constructed (book_id not found)
alignment = alignment.dropna(subset=['EN_audio'])

# Save the cleaned up csv
alignment.to_csv("alignments/all_de_en_alligned_cleaned.csv", index=False)

print(f"Saved cleaned CSV with {len(alignment)} rows")
print("\nFirst few rows of cleaned CSV:")
print(alignment.head())

