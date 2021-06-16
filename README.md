# LibrivoxDeEn-English-Allignments
### Scraping a book from Librivox
To download all chapters from a librivox url the following command can be used:
```
python scrape_audio_from_librivox.py \
--url https://librivox.org/undine-by-friedrich-de-la-motte-fouque/ \
--save_dir ./examples
```

### Allign a book from Librivox with the text from LibrivoxDeEn
To allign the previously downloaded book with the txt files and tsv tables provided by LibrivoxDeEn the following command, based on the example provided with this repo, can be used:
```
python align_text_and_audio.py \
--text_dir ./example/en_text/ \
--audio_path ./example/audio_chapters/ \
--aeneas_path ./example/aeneas/ \
--en_audio_export_path ./example/sentence_level_audio/ \
--total_alignment_path ./example/bi-lingual-alignment/ \
--librivoxdeen_alignment ./example/undine_data.tsv \
```
**note:** the example folder in this repo already contains the first two chapters from [Undine](https://librivox.org/undine-by-friedrich-de-la-motte-fouque/) scraped from librivox and their transcripts and (modified) tsv table retrieved from [librivoxDeEn](https://www.cl.uni-heidelberg.de/statnlpgroup/librivoxdeen/).
Additional data to align can be scraped by using the same file shown previously and combined with the provided data from LibriVoxDeEn

Additionally with this repo the full allignment for 9 other books are given
