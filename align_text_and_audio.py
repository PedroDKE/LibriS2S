# -*- coding: utf-8 -*-
import aeneas.globalconstants as gc
import pandas as pd
import os
import argparse

from aeneas.executetask import ExecuteTask
from aeneas.language import Language
from aeneas.syncmap import SyncMapFormat
from aeneas.task import Task
from aeneas.task import TaskConfiguration
from aeneas.textfile import TextFileFormat
from pydub import AudioSegment


parser = argparse.ArgumentParser(description='A program to download all the chapters in a given librivox URL.')
parser.add_argument("--text_dir",
                    help='Directory containing the txt files to allign the audio to',
                    required=True,
                    type=str)
parser.add_argument("--audio_path",
                    help="path to the chapter which are to be aligned.",
                    required=True,
                    type=str)
parser.add_argument("--aeneas_path",
                    help="path to save the allignments from aeneas",
                    required=True,
                    type=str)
parser.add_argument("--en_audio_export_path",
                    help="path to save the english audio fragments",
                    required=True,
                    type=str)
parser.add_argument("--total_alignment_path",
                    help="path to save the english audio fragments",
                    required=True,
                    type=str)
parser.add_argument("--librivoxdeen_alignment",
                    help="path to TSV file provided by LibriVoxDeEn for this particular book",
                    required=True,
                    type=str)
parser.add_argument("--aeneas_head_max",
                    help="max value (s) of the head for the aeneas alignment, depending on the book to be alligned this has to be tuned",
                    default = 0,
                    required=False,
                    type=int)
parser.add_argument("--aeneas_tail_min",
                    help="min value (s) of the tail for the aeneas alignment, depending on the book to be alligned this has to be tuned",
                    default = 0,
                    required=False,
                    type=int)
args = parser.parse_args()

#variables
number_files = len(os.listdir(args.text_dir))
txt_files = os.listdir(args.text_dir)
txt_files.sort()

audio_files = os.listdir(args.audio_path)
audio_files.sort()

EN_AUDIO_EXPORT_NAME = '000{}-{}.wav' # path where to store the english fragments
EN_ALIGNED_CSV = '000{}-undine_map.csv' #name to store the aeneas mapping
TOTAL_ALIGNMENT_NAME = '000{}-undine_map_DeEn.csv' #path to store the english and german mapping

GE_AUDIO_NAME_TEMPLATE = '000{}-undine_{}.flac' #name of german audio file
#aeneas arguments
tsv_audio_template = "000{}" #template of audio files in tsv file

#count the number of total missing files unaligned
total_missing = 0
total = 0


if not os.path.exists(args.aeneas_path):
    os.makedirs(args.aeneas_path)
    print('made new directory at:',args.aeneas_path)
if not os.path.exists(args.en_audio_export_path):
    os.makedirs(args.en_audio_export_path)
    print('made new directory at:',args.en_audio_export_path)
if not os.path.exists(args.total_alignment_path):
    os.makedirs(args.total_alignment_path)
    print('made new directory at:',args.total_alignment_path)



for chap in range(1 ,number_files+1):

    abs_path = args.text_dir+txt_files[chap-1]
    str_chap = str(chap)
    str_chap = str(chap).zfill(2)

    print('start alignent for chap: {}'.format(chap))

    # create Task object
    config = TaskConfiguration()
    config[gc.PPN_TASK_LANGUAGE] = Language.ENG
    config[gc.PPN_TASK_IS_TEXT_FILE_FORMAT] = TextFileFormat.PLAIN
    config[gc.PPN_TASK_OS_FILE_FORMAT] = SyncMapFormat.CSV
    config[gc.PPN_TASK_OS_FILE_NAME] = EN_ALIGNED_CSV.format(str_chap)
    config[gc.PPN_TASK_IS_AUDIO_FILE_DETECT_HEAD_MAX] = args.aeneas_head_max
    config[gc.PPN_TASK_IS_AUDIO_FILE_DETECT_TAIL_MIN] = args.aeneas_tail_min
    config[gc.PPN_TASK_OS_FILE_HEAD_TAIL_FORMAT] = 'hidden'

    task = Task()
    task.configuration = config
    task.text_file_path_absolute = abs_path
    task.audio_file_path_absolute = args.audio_path+'/'+audio_files[chap-1]
    task.sync_map_file_path = EN_ALIGNED_CSV.format(str_chap)

    # process Task
    ExecuteTask(task).execute()

    task.output_sync_map_file(os.getcwd()+args.aeneas_path[1:])

    # print(task.sync_map)
    print('alignent done for chap: {}'.format(chap))

    # -------- read csv and cut audio -----------
    print('cutting audio for chap: {}'.format(chap))

    en_alignment = pd.read_csv(args.aeneas_path+EN_ALIGNED_CSV.format(str_chap), header = None)

    original = AudioSegment.from_file(args.audio_path+'/'+audio_files[chap-1])
    for Name, Start, End, Text in zip(en_alignment.iloc[:,0], en_alignment.iloc[:,1], en_alignment.iloc[:,2], en_alignment.iloc[:,3]):
        extract = original[Start*1000:End*1000]
        extract.export(args.en_audio_export_path+EN_AUDIO_EXPORT_NAME.format(str_chap,Name), format="wav")

    print('done cutting audio for chap: {}'.format(chap))
    # ------- create CSV file with concatenated data ------
    print('create CSV for chap: {}'.format(chap))

    new = pd.DataFrame(columns=['book', 'DE_audio', 'EN_audio', 'score', 'DE_transcript', 'EN_transcript'])

    # open German TSV
    ge_alignment = pd.read_table(args.librivoxdeen_alignment)

    # all german audio names
    # restrict german to only the current chapter
    ge_alignment = ge_alignment[ge_alignment['audio'].str.contains(tsv_audio_template.format(str_chap))==True]
    ge_audio_names = []

    for i in range(ge_alignment.shape[0]+1):
        ge_audio_names.append(GE_AUDIO_NAME_TEMPLATE.format(str_chap,i))

    for name in ge_audio_names:
        ge_index = ge_alignment[ge_alignment['audio']==name].index
        if len(ge_index) > 0:
            en_translation = ge_alignment['en_sentence'][ge_index[0]].replace('<MERGE> ', '').strip()
            en_index = en_alignment[en_alignment.iloc[:, 3] == en_translation.replace('~', '')].index
            if len(en_index) > 0:
                ind = ge_index[0]
                new = new.append({'book': ge_alignment['book'][ind],
                                  'DE_audio': ge_alignment['audio'][ind],
                                  'EN_audio':'000{}-'.format(str_chap)+en_alignment.iloc[en_index[0],0]+'.wav',
                                  'score':ge_alignment['score'][ind],
                                  'DE_transcript':ge_alignment['de_sentence'][ind],
                                  'EN_transcript': ge_alignment['en_sentence'][ind]},
                                 ignore_index=True)
                new.to_csv(args.total_alignment_path+'/'+TOTAL_ALIGNMENT_NAME.format(str_chap),index=False)

    print('files in the DeEn csv: ' + str(new.shape))
    print('files in the EN alignment'+str(en_alignment.shape))
    print('files in the original DE csv: ' + str(ge_alignment.shape))
    missing = ge_alignment.shape[0]-new.shape[0]
    total_missing += missing
    print('number of unaligned audio files: '+str(missing))
    print('done creating CSV for chap: {}'.format(chap))
    total += ge_alignment.shape[0]
print('missing: '+str(total_missing)+' out of '+str(total)+' GE files')
