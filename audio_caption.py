from msclap import CLAP
import pandas as pd
import numpy as np
from torch.nn import functional
import matplotlib.pyplot as plt
import spacy


musiccaps_path = '../musiccaps/'
# data_path = 'C:/Users/Public/Martins_Exjobb/musiccaps/2853/edited'
data_paths = ['./300M_official_clap_data'] # './1M_clap_data', './10M_clap_data', './58M_clap_data', './200M_clap_data', './300M_clap_data', 

prompts = pd.read_csv(musiccaps_path + 'musiccaps-public.csv')
prompts = prompts.loc[5001:5002]

keyword_extractor = spacy.load('en_core_web_sm')

clap_model = CLAP(version='2023', use_cuda=False)
clap_cap = CLAP(version='clapcap', use_cuda=False)

scores = []

for j in range(len(data_paths)):
    sum = 0
    idx = 0
    for i in range(len(prompts)-1):
        prompt = prompts.iloc[i].loc['caption']
        yt_id = prompts.iloc[i].loc['ytid']
        text_embeddings = clap_model.get_text_embeddings([prompt])
        audio_embeddings = clap_model.get_audio_embeddings([f'{data_paths[j]}/{idx}.wav'])
        caption = clap_cap.generate_caption([f'{data_paths[j]}/{idx}.wav'])

        print(f"Generated Caption: {caption}")
        print(f'Actual Caption: {prompt}')

        cap_keys = keyword_extractor(caption[0])
        prompt_keys = keyword_extractor(prompt)

        print(f"Generated keywords: {cap_keys}")
        print(f'Actual keywords: {prompt_keys}')

        normalized_text_emb = functional.normalize(text_embeddings)
        normalized_audio_emb = functional.normalize(audio_embeddings)

        dot_prod = np.dot(normalized_text_emb, np.transpose(normalized_audio_emb)) # This achieves the same thing as compute_similarity() but without logit scaling.
        sum += dot_prod[0][0]
        idx += 1

    print(f'score: {round(sum/len(prompts), 2)}')
    scores.append(round(sum/len(prompts), 2))

plt.plot(scores)
plt.show()