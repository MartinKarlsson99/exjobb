from audiocraft.models import MusicGen
import numpy as np
from audiocraft.data.audio import audio_write
from audiocraft.modules.conditioners import ConditioningAttributes
import time
from matplotlib import pyplot as plt
import pandas as pd
from msclap import CLAP
import clap_test



musiccaps_path = 'C:/Users/Public/Martins_Exjobb/musiccaps/musiccaps-public.csv'
clap_path='C:/Users/Public/Martins_Exjobb/eval_tools/music_audioset_epoch_15_esc_90.14.pt'
dataset = pd.read_csv(musiccaps_path)
prompts = []
for i in range(4800, 5328):
    prompts.append([dataset.iloc[i].loc['caption']])

sizes = ['300M'] # '1M', '10M', '58M', '200M', , '300M_official'


model_paths = { '1M':'C:/Users/Public/Martins_Exjobb/1M',
                '10M':'C:/Users/Public/Martins_Exjobb/10M_overfit',
                '58M' : 'C:/Users/Public/Martins_Exjobb/2853_test/checkpoints/my_audio_lm',
                '200M' : 'C:/Users/Public/Martins_Exjobb/200M',
                '300M':'C:/Users/Public/Martins_Exjobb/300M',
                '300M_official':'facebook/musicgen-small'}


clap_model = CLAP(version='2023', use_cuda=False)

text_embeddings = []
for prompt in prompts:
    text_embeddings.append(clap_model.get_text_embeddings(prompt))


times = []
all_dot_scores = []

for size in sizes:
    checkpoint_path = model_paths[size]
    model = MusicGen.get_pretrained(checkpoint_path)
    model.set_generation_params(duration=10)  # generate 10 seconds.

    
    generations = []
    count = 0
    
    for prompt in prompts:
        wav = model.generate(descriptions=prompt, progress=True)
        generations.append(wav)
        count+=1

    index=0
    for wav in generations:
        for idx, one_wav in enumerate(wav):
            audio_write(f'{str(size)}_clap_data/{index}', one_wav.cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
            index+=1

clap_test.run_clap_evaluation(4800, 5328)
