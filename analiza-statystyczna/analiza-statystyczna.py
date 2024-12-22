# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import mac_morpho
from nltk.probability import FreqDist
import matplotlib.pyplot as plt

nltk.download('mac_morpho')

import matplotlib.pyplot as plt
from nltk.probability import FreqDist
import numpy as np

sentences = mac_morpho.sents()
words = mac_morpho.words()

words_alnum = [word for word in words if word.isalpha()]

num_sentences = len(sentences)
unique_words = set(words_alnum)

num_words = len(unique_words)
avg_word_length = sum(len(word) for word in unique_words) / num_words
avg_sentence_length = sum(len(sentence) for sentence in sentences) / num_sentences

print("Statystyki korpusu Mac-Morpho:")
print(f"Liczba zdań: {num_sentences}")
print(f"Liczba unikalnych słów (tylko alfabetyczne): {num_words}")
print(f"Średnia długość słowa (w znakach): {avg_word_length:.2f}")
print(f"Średnia długość zdania (w słowach): {avg_sentence_length:.2f}")

freq_dist = FreqDist(words_alnum)

top_25_words = freq_dist.most_common(25)

words_top_25 = [word for word, _ in top_25_words]
freq_top_25 = [freq for _, freq in top_25_words]

plt.figure(figsize=(10, 6))
ax1 = plt.gca()

ax1.bar(words_top_25, freq_top_25, color='green', label='Częstotliwość występowania słowa', alpha=0.5)
ax1.tick_params(axis='y', labelsize=10, labelcolor='green')
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0e}'))
ax1.set_ylabel("Częstotliwość występowania słowa", color='green', fontsize=10)
ax1.set_yticks(np.arange(0, max(freq_top_25) + 10000, 10000))

ax2 = ax1.twinx()
cumulative = np.cumsum(freq_top_25)
ax2.plot(words_top_25, cumulative, color='black', label='Częstotliwość skumulowana', linewidth=1, alpha=0.7)
ax2.tick_params(axis='y', labelsize=10, labelcolor='black')
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0e}'))
ax2.set_ylabel("Częstotliwość skumulowana", color='black', fontsize=10)

plt.title('Częstotliwość występowania 25 najbardziej popularnych słów', fontsize=10)
plt.xticks(rotation=45, fontsize=10)

ax1.set_xlabel("Słowa", fontsize=10)

plt.tight_layout()
plt.show()

word_lengths = [len(word) for word in unique_words]

plt.figure(figsize=(10, 6))
plt.hist(word_lengths, bins=range(1, max(word_lengths) + 2), edgecolor='black', alpha=0.5)
plt.title('Rozkład długości słów', fontsize=10)
plt.xlabel('Długość słowa (liczba znaków)', fontsize=10)
plt.ylabel('Częstotliwość', fontsize=10)
plt.xticks(range(1, max(word_lengths) + 1))
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

import pandas as pd

ranks = np.arange(1, len(words_top_25) + 1)

zipf_table = pd.DataFrame({
    'Rank': ranks,
    'Word': words_top_25,
    'Frequency': freq_top_25,
    'Zipf Value': ranks * freq_top_25
})

print(zipf_table)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

freq_words = list(sorted(freq_dist.items(), key=lambda x: x[1], reverse=True))

words_all = [word for word, _ in freq_words]
freq_all = [freq for _, freq in freq_words]

ranks = np.arange(1, len(words_all) + 1)
zipf_values = ranks * freq_all

plt.figure(figsize=(12, 6))

plt.xscale('log')
plt.yscale('log')

plt.scatter(ranks, freq_all, c=zipf_values, cmap='viridis', s=25, edgecolors='none', alpha=0.7)

plt.title('Relacja między rangą statystyczną a częstotliwością występowania słów, wraz ze stałą Zipfa', fontsize=10)
plt.xlabel('Ranga', fontsize=10)
plt.ylabel('Częstotliwość występowania', fontsize=10)
cbar = plt.colorbar()
cbar.set_label('Stała Zipfa', fontsize=10)

plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
plt.hist(zipf_values, bins=50, color='skyblue', edgecolor='black', alpha=0.7)

plt.title("Rozkład stałych Zipf'a", fontsize=10)
plt.xlabel("Stała Zipf'a", fontsize=10)
plt.ylabel('Częstotliwość występowania', fontsize=10)

plt.tight_layout()
plt.show()

from scipy import stats

mean = np.mean(zipf_values)
variance = np.var(zipf_values)
std_dev = np.std(zipf_values)
median = np.median(zipf_values)
mode = stats.mode(zipf_values, keepdims=True)

print(f"Średnia: {mean}")
print(f"Wariancja: {variance}")
print(f"Odchylenie standardowe: {std_dev}")
print(f"Mediana: {median}")
print(f"Dominanta (moda): {mode.mode[0]}, liczba wystąpień: {mode.count[0]}")

import networkx as nx
from collections import Counter
from itertools import combinations

filtered_sentences = [[word for word in sentence if word.isalpha()] for sentence in sentences]

def get_neighbours(sentence):
    neighbours = {}
    for i in range(len(sentence) - 1):
        word = sentence[i]
        if word in neighbours:
            neighbours[word].append(sentence[i + 1])
        else:
            neighbours[word] = [sentence[i + 1]]

    unique_neighbors = {k: list(set(v)) for k, v in neighbours.items()}
    return dict(sorted(unique_neighbors.items(), key=lambda x: len(x[1])))

co_occurrences = Counter()

for sentence in filtered_sentences:
    neighbours = get_neighbours(sentence)
    for word, neighbor_list in neighbours.items():
        for neighbor in neighbor_list:
            if word == neighbor:
              continue
            co_occurrences[(word, neighbor)] += 1

G = nx.Graph()
for (word1, word2), weight in co_occurrences.items():
    G.add_edge(word1, word2, weight=weight)

top_nodes = sorted(G.degree, key=lambda x: x[1], reverse=True)[:100]
top_words = {node for node, degree in top_nodes}


edges = [[k, len(G[k])] for k in top_words]
edges_sorted = sorted(edges, key=lambda x: x[1], reverse=True)

print(edges_sorted)

subgraph = G.subgraph(top_words)

plt.figure(figsize=(8, 4))
pos = nx.spring_layout(subgraph, seed=21)
nx.draw(
    subgraph,
    pos,
    node_size=25,
    node_color="black",
    font_size=10,
    edge_color="green",
    alpha=0.5
)

plt.title("Sieć semantyczna dla 100 wierzchołków", fontsize=10)
plt.tight_layout()
plt.show()

def percentage_of_language(freq):
    number_of_words = sum(freq.values())
    percentage_of_words = {k: v / number_of_words for k, v in freq.items()}
    final_percentage = {i * 10: [] for i in range(1, 11)}
    val = 0
    for k, v in percentage_of_words.items():
        for i, j in final_percentage.items():
            if i / 100 > val:
                final_percentage[i].append(k)
        val += v

    return {
      k: {
          "mean": np.mean([freq_dist[word] for word in v]),
          "std": np.std([freq_dist[word] for word in v])
      } for k, v in final_percentage.items()
    }

percentage_of_language(freq_dist)