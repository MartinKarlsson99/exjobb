import os
import random
import pygame
import time
import json
import re

# Function to initialize pygame mixer
def init_mixer():
    pygame.mixer.init()

# Function to play an audio file
def play_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)

# Function to get two random audio samples from different folders
def get_random_audio_samples(base_dir, num_folders=5):
    folders = [os.path.join(base_dir, f) for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
    selected_folders = random.sample(folders, num_folders)
    audio_files = []
    for folder in selected_folders:
        files = [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'^\d{1,3}\.wav$', f)]
        if files:
            audio_files.append(random.choice(files))
    return random.sample(audio_files, 2)

# Function to present audio samples to the user and get their choice
def present_audio_samples(audio_samples):
    for i, sample in enumerate(audio_samples):
        print(f"Playing audio sample {i+1}: {sample.split('data')[1]}")
        play_audio(sample)
        time.sleep(1)  # Give a small pause between samples

    choice = None
    while choice not in ['1', '2']:
        choice = input("Which audio sample sounds better? Enter 1 or 2: ")
    
    return int(choice) - 1

# Function to store the result in a CSV file
def store_result(dict, audio_samples, chosen_index):
    winner = audio_samples[chosen_index].split('_clap_data')[0].split('./generated')[1].replace('\\', '')
    if winner == audio_samples[0].split('_clap_data')[0].split('./generated')[1].replace('\\', ''):
        loser = audio_samples[1].split('_clap_data')[0].split('./generated')[1].replace('\\', '')
    else:
        loser = audio_samples[0].split('_clap_data')[0].split('./generated')[1].replace('\\', '')
    return winner, loser



# Main function
def main():
    init_mixer()
    base_dir = "./generated"  # Change this to the path where your folders are located
    result_file = "audio_comparison_results.json"
    dict = {'1M' : [0, 0],
            '10M' : [0, 0],
            '58M' : [0, 0],
            '200M' : [0, 0],
            '300M' : [0, 0],
            '300M_official' : [0, 0]}

    file = open(result_file, "r") 
    dict = json.load(file)

    while True:
        audio_samples = get_random_audio_samples(base_dir)
        chosen_index = present_audio_samples(audio_samples)
        print(f"You selected: {audio_samples[chosen_index]}")
        
        # Store the result
        winner, loser = store_result(dict, audio_samples, chosen_index)
        dict[winner][0]+=1
        dict[loser][1]+=1
        
        another_round = input("Do you want to listen to another pair of samples? (y/n): ").strip().lower()
        if another_round != 'y':
            out_file = open(result_file, "w") 
            json.dump(dict, out_file, indent = 6) 
            out_file.close() 
            break

    pygame.mixer.quit()

if __name__ == "__main__":
    main()