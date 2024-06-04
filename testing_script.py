from audiocraft.models import MusicGen
import numpy as np
from audiocraft.data.audio import audio_write
from audiocraft.modules.conditioners import ConditioningAttributes
import time
from matplotlib import pyplot as plt
import pandas as pd
from torch.nn import functional
from msclap import CLAP



musiccaps_path = 'C:/Users/Public/Martins_Exjobb/musiccaps/musiccaps-public.csv'
clap_path='C:/Users/Public/Martins_Exjobb/eval_tools/music_audioset_epoch_15_esc_90.14.pt'
dataset = pd.read_csv(musiccaps_path)
prompts = []
for i in range(4800, 4801):
    prompts.append([dataset.iloc[i].loc['caption']])

sizes = ['1M', '10M', '58M', '200M','300M', '300M_official'] 


model_paths = { '1M':'C:/Users/Public/Martins_Exjobb/1M',
                '10M':'C:/Users/Public/Martins_Exjobb/10M_overfit',
                '58M' : 'C:/Users/Public/Martins_Exjobb/2853_test/checkpoints/my_audio_lm',
                '200M' : 'C:/Users/Public/Martins_Exjobb/200M',
                '300M':'C:/Users/Public/Martins_Exjobb/audiocraft/musicgen-small',
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
    
    start = time.time() # Generation process
    for prompt in prompts:
        wav = model.generate(descriptions=prompt, progress=True)
        generations.append(wav)
        count+=1
    duration = round(time.time() - start, 2)
    times.append(round(duration/len(prompts), 2))

    index=0
    for wav in generations:
        for idx, one_wav in enumerate(wav):
            audio_write(f'{str(size)}_clap_data/{index}', one_wav.cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
            index+=1

    
    audio_embeddings = []
    for i in range(len(prompts)):
        audio_embeddings.append(clap_model.get_audio_embeddings([f'./{size}_clap_data/{i}.wav']))

    


    dot_scores = []
    for i in range(len(prompts)):
        normalized_audio_emb = functional.normalize(audio_embeddings[i][0])
        normalized_text_emb = functional.normalize(text_embeddings[i][0])
        dot_score = np.dot(audio_embeddings[i], np.transpose(text_embeddings[i]))
        print(f'dot score = {dot_score}')
        dot_scores.append(dot_score)
    

    dot_sum = 0
    for i in range(len(dot_scores)):
        dot_sum += dot_scores[i][0]

    print(f'{dot_sum}/{len(dot_scores)}')
    print(dot_scores)

    avg = dot_sum/len(dot_scores)
    print(f'avg CLAP score: {avg}')
    all_dot_scores.append(avg)
    print(f"Took {round(duration/len(prompts),2)}s to generate")



