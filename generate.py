import markovify
import pronouncing
import os
import re
import random

input_file = "bb_lyrics.txt"
output_file = "bb_new_song.txt"

def clean_input(txt_file):
    # Remove unnecessary characters from file
    bad_chars = ['(', ')', '[', ']', ',', '-']
    for char in bad_chars:
        txt_file = txt_file.replace(char, '') # removes the bad character
    
    return txt_file

def markov_chain(txt_file):
    text_model = markovify.NewlineText(txt_file)

    return text_model

def intersection(list_of_rhymes, end_words):
    # Gets all words that are in the lyrics and rhyme with the potential word
    return list(set(end_words).intersection(list_of_rhymes))

def generate_stanza(text_model, txt_file):
    finished_stanza = False
    
    # Keep creatin stanzas until one rhymes
    while not finished_stanza:
        found_rhyme = False
        lines = []
        end_words = []
        rhyme_index = -1
        while not found_rhyme:
            # Generate line
            ln = text_model.make_sentence()

            # Take off last word
            try:
                rhyme = ln.split(" ")[-1]
            except AttributeError:
                continue
            
            # See if it rhymes with any other end word
            list_of_rhymes = pronouncing.rhymes(rhyme)
            intersect = intersection(list_of_rhymes, end_words)

            # If theres a rhyme
            if intersect:
                found_rhyme = True
                # Get index of lines
                rhyme_index = end_words.index(intersect[0])

            # Put line and end word into containers
            lines.append(ln)
            end_words.append(rhyme)
        
        finished_stanza = []
        # First Line
        rand = rhyme_index
        while rand == rhyme_index:
            rand = random.randint(0, len(lines) - 1)

        finished_stanza.append(lines[rand])

        # Second Line
        finished_stanza.append(lines[rhyme_index])

        # Third Line
        rand = rhyme_index
        while rand == rhyme_index:
            rand = random.randint(0, len(lines) - 2)
        
        finished_stanza.append(lines[rand])

        # Fourth Line
        finished_stanza.append(lines[len(lines) - 1])

    return finished_stanza


def generate_lyrics(text_model, txt_file):
    fout = open(output_file, 'w')
    num_bars = 8

    for i in range(num_bars):
        lines = generate_stanza(text_model, txt_file)
        for line in lines:
            fout.write(line)
            fout.write('\n')
        fout.write('\n')


def main():
    # Open txt file and lowercases all characters
    txt_file = open(input_file, 'r').read().lower()

    # Clean text from input file
    txt_file = clean_input(txt_file)

    # Create Markov Chain with input txt file
    text_model = markov_chain(txt_file)

    # Line by line generate new song using Markov Chain
    generate_lyrics(text_model, txt_file)

main()