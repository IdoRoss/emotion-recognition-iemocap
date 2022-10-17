import os
import pandas as pd
import argparse
import shutil


def init_directories():
    # remove Data/Audio Directory if exist
    if os.path.exists(os.path.join('./', 'Audio')):
        shutil.rmtree(os.path.join('./', 'Audio'))
    os.mkdir(os.path.join('./', 'Audio'))
    for i in range(1, 6):
        os.mkdir(os.path.join('./', 'Audio', f'Ses0{i}'))


def __main__():
    parser = argparse.ArgumentParser(description="extract database info",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-path', type=str, help="path to iemocap DB", default='./', required=False)
    args = parser.parse_args()
    init_directories()
    labels = ['fru', 'ang', 'hap', 'sad', 'exc']
    iemocap_path = args.path

    df = pd.DataFrame(columns=["audio", "text", "start", "end", "session", "label"])
    for ses_num in range(4, 6):
        session_dir = os.path.join(iemocap_path, f'Session{ses_num}')
        evaluation_dir = os.path.join(session_dir, 'dialog', 'EmoEvaluation')
        transcription_dir = os.path.join(session_dir, 'dialog', 'transcriptions')
        for file_name in os.listdir(evaluation_dir):
            file_name = file_name.strip()
            if file_name.startswith('.') or not file_name.endswith('.txt'):
                continue
            transcription_path = os.path.join(transcription_dir, file_name)
            evaluation_path = os.path.join(evaluation_dir, file_name)
            audio_dir = os.path.join(session_dir, 'sentences', 'wav', file_name.split('.')[0])
            with open(evaluation_path) as eval_file:
                eval_lines = eval_file.readlines()
                eval_lines = [line.rstrip() for line in eval_lines if line.startswith('[')]
                with open(transcription_path) as trans_file:
                    trans_lines = trans_file.readlines()
                    trans_lines = [line.rstrip() for line in trans_lines]
                    for line in eval_lines:
                        info = line.split('\t')
                        label = info[-2]
                        if label not in labels:
                            continue
                        time_stamp = info[0]
                        time_stamp = time_stamp[1:-2]  # remove the '[' and ']' characters
                        start = int(float(time_stamp.split('-')[0].strip()))
                        end = int(float(time_stamp.split('-')[1].strip()))
                        instance_name = info[1].split('.')[0]
                        text = list(
                            filter(
                                lambda l: l.startswith(instance_name),
                                trans_lines
                            )
                        )
                        # to debug
                        if len(text) != 1:
                            print(f'error with {instance_name}')
                        text = text[0].split(':')[-1].strip()
                        origin_audio_path = os.path.join(audio_dir, f'{instance_name}.wav')
                        target_audio_path = os.path.join('Audio', f'Ses0{ses_num}', f'{instance_name}-{label}.wav')
                        shutil.copy(origin_audio_path, target_audio_path)
                        df.loc[len(df.index)] = [instance_name, text, start, end, ses_num, label]
    df.to_csv('./summary.tsv', sep="\t", index=False)


__main__()
