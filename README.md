# LibrivoxDeEn-English-Allignments
This repo contains tools and allignment data to create a dataset build further upon [librivoxDeEn](https://www.cl.uni-heidelberg.de/statnlpgroup/librivoxdeen/) that contains (german audio, german transcription, english audio, english transcription) quadruplets
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
--aeneas_head_max 120 \
--aeneas_tail_min 5 \
```
**note:** the example folder in this repo already contains the first two chapters from [Undine](https://librivox.org/undine-by-friedrich-de-la-motte-fouque/) scraped from librivox and their transcripts and (modified) tsv table retrieved from LibrivoxDeEn .
Additional data to align can be scraped by using the same file shown previously and combined with the provided data from LibriVoxDeEn

Additionally with this repo the full allignment for the 8 following books with folowwing LibrivoxDeEn id's are also given:
[9](https://librivox.org/the-picture-of-dorian-gray-1891-version-by-oscar-wilde/), [10](https://librivox.org/pandoras-box-by-frank-wedekind/), [13](https://librivox.org/survivors-of-the-chancellor-by-jules-verne/), [18](https://librivox.org/undine-by-friedrich-de-la-motte-fouque/), [23](https://librivox.org/around-the-world-in-80-days-by-jules-verne/), [108](https://librivox.org/elective-affinities-by-johann-wolfgang-von-goethe/), [110](https://librivox.org/candide-by-voltaire-3/), [120](https://librivox.org/the-metamorphosis-by-franz-kafka/).

Other books such as [11](https://librivox.org/the-castle-of-otranto-by-horace-walpole/), [36](https://librivox.org/the-rider-on-the-white-horse-by-theodor-storm/), [67](https://librivox.org/frankenstein-or-the-modern-prometheus-1818-by-mary-wollstonecraft-shelley/) are also inside of the librivoxDeEn dataset but the chapters do not correspond in a 1:1 mannner(for example: the German version of book 67 has 27 chapters but the English version has 29 and thus need to be re-aligned before the allignment script in this repo will work.). Therefore these alignments are not given since they could be different depending on the cutting points. 

### Metrics on the alignment given in this repo.
Using the allignments given in this repo some metrics were collected and quickly displayed here
|  | German | English  |
| :---:   | :-: | :-: |
|number of files  | 18868 | 18868 |
|total time (hh:mm:ss) | 39:11:08 | 40:52:31 |
|Speakers | 41 |22 |

note: the speakers were counter for each book seperatly so some speakers might be counter more than once.

the number of hours for each book alligned in this repo:<br>
<img src="https://user-images.githubusercontent.com/43861296/122250648-1f5f7f80-ceca-11eb-84fd-344a2261bf47.png" width="500">

