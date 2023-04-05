# LibriS2S
This repo contains scripts and alignment data to create a dataset build further upon [librivoxDeEn](https://www.cl.uni-heidelberg.de/statnlpgroup/librivoxdeen/) such that it contains (German audio, German transcription, English audio, English transcription) quadruplets and can be used for Speech-to-Speech translation research. Because of this, the alignments are released under the same [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/) <div>
 These alignments were collected by downloading the English audiobooks and using [aeneas](https://github.com/readbeyond/aeneas) to align the book chapters to the transcripts. For more information read the original [paper](https://arxiv.org/abs/2204.10593) (Presented at LREC 2022)

### The data
The English/German audio are available in the folder EN/DE respectively and can be downloaded from [this onedrive](https://onedrive.live.com/embed?cid=DCE49ACC2BDA7D8C&resid=DCE49ACC2BDA7D8C%2115663&authkey=ANmUz8gRUoyxmjk) or from [HuggingFace](https://huggingface.co/datasets/PedroDKE/LibriS2S). In case there are any problems with the download, feel free to open an issue <br/>
The repo structure is as follow:
- Alignments : Contains all the alignments for each book and chapter
- DE : Contains the German audio for each chapter per book.
- EN : Contains the English audio for each chapter per book.
- Example : contains example files on for the scraping and aligning explanations that were used to build this dataset.
- LibrivoxDeEn_alignments : Contains the base alignments from the LibrivoxDeEn dataset. <br/>

In case you feel a part of the data is missing, feel free to open an issue!
The full zipfile is about 20 GB of size.

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
**note:** the example folder in this repo already contains the first two chapters from [Undine](https://librivox.org/undine-by-friedrich-de-la-motte-fouque/) scraped from librivox and their transcripts and (modified to only contain the first 2 chapters) tsv table retrieved from LibrivoxDeEn.
Additional data to align can be scraped by using the same file shown previously and combined with the provided data from LibriVoxDeEn

Additionally with this repo the full alignment for the 8 following books with following LibrivoxDeEn id's are also given:
[9](https://librivox.org/the-picture-of-dorian-gray-1891-version-by-oscar-wilde/), [10](https://librivox.org/pandoras-box-by-frank-wedekind/), [13](https://librivox.org/survivors-of-the-chancellor-by-jules-verne/), [18](https://librivox.org/undine-by-friedrich-de-la-motte-fouque/), [23](https://librivox.org/around-the-world-in-80-days-by-jules-verne/), [108](https://librivox.org/elective-affinities-by-johann-wolfgang-von-goethe/), [110](https://librivox.org/candide-by-voltaire-3/), [120](https://librivox.org/the-metamorphosis-by-franz-kafka/).

Other books such as [11](https://librivox.org/the-castle-of-otranto-by-horace-walpole/), [36](https://librivox.org/the-rider-on-the-white-horse-by-theodor-storm/), [67](https://librivox.org/frankenstein-or-the-modern-prometheus-1818-by-mary-wollstonecraft-shelley/) and [54](https://librivox.org/white-nights-other-stories-by-fyodor-dostoyevsky/) are also inside of the librivoxDeEn dataset but the chapters do not correspond in a 1:1 mannner(for example: the German version of book 67 has 27 chapters but the English version has 29 and thus need to be re-aligned before the allignment script in this repo will work). Therefore these alignments are given but might have be different if you scrape them yourselves as the re-alignments might be different for you.
### Metrics on the alignment given in this repo.
Using the alignments given in this repo some metrics were collected and quickly displayed here, for this table and the next figure the books which were manually alligned, although provided in the zip, were not accounted for, but the full table can be found in the original paper.
|  | German | English  |
| :---:   | :-: | :-: |
|number of files  | 18868 | 18868 |
|total time (hh:mm:ss) | 39:11:08 | 40:52:31 |
|Speakers | 41 |22 |

note: the speakers were counted for each book seperatly so some speakers might be counter more than once.

the number of hours for each book aligned in this repo:<br>
<img src="https://user-images.githubusercontent.com/43861296/122250648-1f5f7f80-ceca-11eb-84fd-344a2261bf47.png" width="500">
 
 when using this work, please cite the original paper and the LibrivoxDeEn authors
 ```
@InProceedings{jeuris-niehues:2022:LREC,
  author    = {Jeuris, Pedro  and  Niehues, Jan},
  title     = {LibriS2S: A German-English Speech-to-Speech Translation Corpus},
  booktitle      = {Proceedings of the Language Resources and Evaluation Conference},
  month          = {June},
  year           = {2022},
  address        = {Marseille, France},
  publisher      = {European Language Resources Association},
  pages     = {928--935},
  url       = {https://aclanthology.org/2022.lrec-1.98}
}
 ```
 ```
 @article{beilharz19,
  title = {LibriVoxDeEn: A Corpus for German-to-English Speech Translation and Speech Recognition},
  author = {Beilharz, Benjamin and Sun, Xin and Karimova, Sariya and Riezler, Stefan},
  journal = {Proceedings of the Language Resources and Evaluation Conference},
  journal-abbrev = {LREC},
  year = {2020},
  city = {Marseille, France},
  url = {https://arxiv.org/pdf/1910.07924.pdf}
}
```
 

