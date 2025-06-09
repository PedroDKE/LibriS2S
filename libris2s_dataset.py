import os
import torch
import pandas as pd
import torchaudio
from torch.utils.data import Dataset
from typing import List, Optional

class Libris2sDataset(torch.utils.data.Dataset):
    def __init__(self, data_dir: str, split: str, transform=None, book_ids: Optional[List[str]]=None):
        """
        Initialize the LibriS2S dataset.
        
        Args:
            data_dir (str): Root directory containing the dataset
            split (str): Path to the CSV file containing alignments
            transform (callable, optional): Optional transform to be applied on the audio
            book_ids (List[str], optional): List of book IDs to include. If None, includes all books.
                                          Example: ['9', '10', '11'] will only load these books.
        """
        self.data_dir = data_dir
        self.transform = transform
        self.book_ids = set(book_ids) if book_ids is not None else None
        
        # Load alignment CSV file
        self.alignments = pd.read_csv(split)
        
        # Create lists to store paths and metadata
        self.de_audio_paths = []
        self.en_audio_paths = []
        self.de_transcripts = []
        self.en_transcripts = []
        self.alignment_scores = []
        
        # Process each entry in the alignments
        for _, row in self.alignments.iterrows():
            # Get book ID from the path
            book_id = str(row['book_id'])
            
            # Skip if book_id is not in the filtered set
            if self.book_ids is not None and book_id not in self.book_ids:
                continue
            
            # Get full paths from CSV
            de_audio = os.path.join(data_dir, row['DE_audio'])
            en_audio = os.path.join(data_dir, row['EN_audio'])
            
            # Only add if both audio files exist
            if os.path.exists(de_audio) and os.path.exists(en_audio):
                self.de_audio_paths.append(de_audio)
                self.en_audio_paths.append(en_audio)
                self.de_transcripts.append(row['DE_transcript'])
                self.en_transcripts.append(row['EN_transcript'])
                self.alignment_scores.append(float(row['score']))
            else:
                print(f"Skipping {de_audio} or {en_audio} because they don't exist")

    def __len__(self):
        """Return the number of items in the dataset."""
        return len(self.de_audio_paths)

    def __getitem__(self, idx):
        """
        Get a single item from the dataset.
        
        Args:
            idx (int): Index of the item to get
            
        Returns:
            dict: A dictionary containing:
                - de_audio: German audio waveform
                - de_sample_rate: German audio sample rate
                - en_audio: English audio waveform
                - en_sample_rate: English audio sample rate
                - de_transcript: German transcript
                - en_transcript: English transcript
                - alignment_score: Alignment score between the pair
        """
        # Load audio files
        de_audio, de_sr = torchaudio.load(self.de_audio_paths[idx])
        en_audio, en_sr = torchaudio.load(self.en_audio_paths[idx])
        
        # Apply transforms if specified
        if self.transform:
            de_audio = self.transform(de_audio)
            en_audio = self.transform(en_audio)
        
        return {
            'de_audio': de_audio,
            'de_sample_rate': de_sr,
            'en_audio': en_audio,
            'en_sample_rate': en_sr,
            'de_transcript': self.de_transcripts[idx],
            'en_transcript': self.en_transcripts[idx],
            'alignment_score': self.alignment_scores[idx]
        }