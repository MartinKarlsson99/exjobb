from msclap import CLAP
import pandas as pd
import numpy as np
from torch.nn import functional
import matplotlib.pyplot as plt

def run_clap_evaluation(start_index, stop_index):
    musiccaps_path = '../musiccaps/'
    # data_path = 'C:/Users/Public/Martins_Exjobb/musiccaps/2853/edited'
    data_paths = ['./1M_clap_data', './10M_clap_data', './58M_clap_data', './200M_clap_data', './300M_clap_data', './300M_official_clap_data']

    prompts = pd.read_csv(musiccaps_path + 'musiccaps-public.csv')
    prompts = prompts.loc[start_index:stop_index]


    clap_model = CLAP(version='2023', use_cuda=False)

    scores = []

    for j in range(len(data_paths)):
        sum = 0
        yt_id = 0
        for i in range(len(prompts)-1):
            prompt = prompts.iloc[i].loc['caption']
            # yt_id = prompts.iloc[i].loc['ytid']
            text_embeddings = clap_model.get_text_embeddings([prompt])
            audio_embeddings = clap_model.get_audio_embeddings([f'{data_paths[j]}/{yt_id}.wav'])

            normalized_text_emb = functional.normalize(text_embeddings)
            normalized_audio_emb = functional.normalize(audio_embeddings)

            dot_prod = np.dot(normalized_text_emb, np.transpose(normalized_audio_emb)) # This achieves the same thing as compute_similarity() but without logit scaling.
            sum += dot_prod[0][0]
            yt_id += 1

        print(f'score: {round(sum/len(prompts), 2)}')
        scores.append(round(sum/len(prompts), 2))

    sizes = ['1M', '10M', '58M', '200M', '300M', '300M_official']
    all_dot_scores = scores

    plt.bar(sizes, all_dot_scores)

    plt.suptitle('CLAP scores')
    plt.show()

run_clap_evaluation(4800, 5328)