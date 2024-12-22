# -*- coding: utf-8 -*-

import nltk
from nltk.corpus import mac_morpho
from nltk.probability import FreqDist
import matplotlib.pyplot as plt

nltk.download('mac_morpho')

import spacy
from collections import defaultdict

nlp = spacy.load("pt_core_news_sm")

def extract_verbs(doc):
    grouped_verbs = defaultdict(set)
    for token in doc:
        if token.pos_ == "VERB":
            if token.i + 1 < len(doc) and doc[token.i + 1].pos_ == "NOUN":
                grouped_verbs[token.lemma_].add(doc[token.i + 1].text)
            if token.i + 2 < len(doc) and doc[token.i + 2].pos_ == "NOUN":
                grouped_verbs[token.lemma_].add(doc[token.i + 2].text)
    return grouped_verbs

sentences = mac_morpho.sents()[:10000]

all_grouped_verbs = defaultdict(set)

for sentence in sentences:
    doc = nlp(" ".join(sentence))
    grouped_verbs = extract_verbs(doc)
    for verb, nouns in grouped_verbs.items():
        all_grouped_verbs[verb].update(nouns)

# for verb, nouns in all_grouped_verbs.items():
#     print(f"Verb: {verb}: {len(nouns)}")

# num_verbs = len(all_grouped_verbs)
# num_relations = sum(len(nouns) for nouns in all_grouped_verbs.values())

# all_nouns = set()
# for nouns in all_grouped_verbs.values():
#     all_nouns.update(nouns)
# num_unique_nouns = len(all_nouns)

# most_relations_verb = max(all_grouped_verbs, key=lambda verb: len(all_grouped_verbs[verb]))
# most_relations_count = len(all_grouped_verbs[most_relations_verb])

# least_relations_verb = min(all_grouped_verbs, key=lambda verb: len(all_grouped_verbs[verb]))
# least_relations_count = len(all_grouped_verbs[least_relations_verb])

# verbs_more_than_10 = len([verb for verb in all_grouped_verbs if len(all_grouped_verbs[verb]) > 10])
# verbs_more_than_50 = len([verb for verb in all_grouped_verbs if len(all_grouped_verbs[verb]) > 50])

# lexeme_relation_counts = {verb: len(nouns) for verb, nouns in all_grouped_verbs.items()}

# print(f"Liczba czasowników: {num_verbs}")
# print(f"Liczba relacji (czasownik -> rzeczownik): {num_relations}")
# print(f"Liczba unikalnych rzeczowników: {num_unique_nouns}")
# print(f"Czasownik z największą liczbą relacji: {most_relations_verb} ({most_relations_count} relacji)")
# print(f"Czasownik z najmniejszą liczbą relacji: {least_relations_verb} ({least_relations_count} relacji)")
# print(f"Liczba czasowników z więcej niż 10 relacjami: {verbs_more_than_10}")
# print(f"Liczba czasowników z więcej niż 50 relacjami: {verbs_more_than_50}")
# print("\nPogrupowanie po lematyzach (liczba relacji dla każdego czasownika):")
# for verb, count in lexeme_relation_counts.items():
#     print(f"{verb}: {count} relacji")

# def top_verb_relations(all_grouped_verbs, top_n=50):
#     verb_relations = []
#     for verb, nouns in all_grouped_verbs.items():
#         verb_relations.append((verb, len(nouns), len(set(nouns))))
#     verb_relations.sort(key=lambda x: x[1], reverse=True)
#     top_verbs = verb_relations[:top_n]
#     return top_verbs

# top_50_verbs = top_verb_relations(all_grouped_verbs)

# print("Top 50 czasowników z największą liczbą relacji:")
# for verb, relation_count, unique_nouns in top_50_verbs:
#     print(f"Czasownik: {verb}, Liczba relacji: {relation_count}, Liczba unikalnych rzeczowników: {unique_nouns}")

# def process_verbs(doc):
#     grouped_verbs = defaultdict(lambda: defaultdict(set))
#     for token in doc:
#         if token.pos_ == "VERB":
#             if token.i + 1 < len(doc) and doc[token.i + 1].pos_ == "NOUN":
#                 grouped_verbs[token.lemma_][token.text].add(doc[token.i + 1].text)
#             if token.i + 2 < len(doc) and doc[token.i + 2].pos_ == "NOUN":
#                 grouped_verbs[token.lemma_][token.text].add(doc[token.i + 2].text)
#     return grouped_verbs

# def process_sentences(sentences):
#     all_grouped_verbs = defaultdict(lambda: defaultdict(set))

#     for sentence in sentences:
#         doc = nlp(" ".join(sentence))
#         grouped_verbs = process_verbs(doc)

#         for lexem, verb_dict in grouped_verbs.items():
#             for verb, nouns in verb_dict.items():
#                 all_grouped_verbs[lexem][verb].update(nouns)

#     return all_grouped_verbs

# result = process_sentences(mac_morpho.sents()[:10000])
# print(result)

# sorted_lexems = sorted(result.items(), key=lambda x: sum(len(v) for v in x[1].values()), reverse=True)

# for i, (lexem, verb_dict) in enumerate(sorted_lexems[:50]):
#     print(f"Lexem: {lexem}")
#     for verb, nouns in verb_dict.items():
#         print(f"  Czasownik: {verb} -> Rzeczowniki: {', '.join(nouns)}")
#     print("-" * 50)

# def find_common_nouns(lexem1, lexem2, all_grouped_verbs):
#     nouns_lexem1 = set()
#     nouns_lexem2 = set()

#     if lexem1 in all_grouped_verbs:
#         for verb, nouns in all_grouped_verbs[lexem1].items():
#             nouns_lexem1.update(nouns)

#     if lexem2 in all_grouped_verbs:
#         for verb, nouns in all_grouped_verbs[lexem2].items():
#             nouns_lexem2.update(nouns)

#     common_nouns = nouns_lexem1.intersection(nouns_lexem2)
#     return common_nouns

# lexem1 = "ter"
# lexem2 = "fazer"
# common_nouns = find_common_nouns(lexem1, lexem2, result)

# print(f"Wspólne rzeczowniki dla lexemów '{lexem1}' i '{lexem2}': {common_nouns}")