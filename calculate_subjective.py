import pandas as pd

result_file = 'audio_comparison_results.json'
data = pd.read_json(result_file)

ranking = data.to_dict()

for col in data:
    wins = data[col].loc[0]
    losses = data[col].loc[1]
    ranking[col] = wins - losses

print(ranking)


