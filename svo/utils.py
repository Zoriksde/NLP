import sqlite3

loaded_data_cache = {}

finishing_steps = ["end"]
tense_choosable_steps = ["verb"]

next_possible_steps = {
    "start": ["pronoun", "noun"],
    "pronoun": ["verb", "adverb"],
    "noun": ["adjective", "verb", "adverb", "determiner", "preposition"],
    "adjective": ["verb", "adverb", "determiner", "preposition"],
    "adverb": ["verb"],
    "determiner": ["verb"],
    "preposition": ["verb"],
    "verb": ["sentence type", "noun after verb"],
    "noun after verb": ["adjective after verb", "sentence type"],
    "adjective after verb": ["sentence type"],
    "sentence type": ["end"],
    "end": []
}

steps_to_display_name = {
    "start": "Start",
    "pronoun": "Choose pronoun",
    "noun": "Choose noun",
    "adjective": "Choose adjective",
    "adverb": "Choose adverb",
    "determiner": "Choose determiner",
    "preposition": "Choose preposition",
    "verb": "Choose verb",
    "noun after verb": "Choose noun after verb",
    "adjective after verb": "Choose adjective after verb",
    "sentence type": "Choose sentence type",
    "end": "End"
}

table_names = ["nouns", "adjectives", "pronouns", "adverbs", "determiners", "prepositions", "verbs"]

simple_steps_to_table_name = {
    "adjective after verb": "adjectives",
    "adjective": "adjectives",
    "pronoun": "pronouns",
    "adverb": "adverbs",
    "determiner": "determiners",
    "preposition": "prepositions",
}

steps_to_page = {
    "pronoun": "step",
    "noun": "noun",
    "adjective": "step",
    "adverb": "step",
    "determiner": "step",
    "preposition": "step",
    "verb": "verb",
    "noun after verb": "noun",
    "adjective after verb": "step",
    "sentence type": "step"
}

steps_to_choosable = {
    "start": False,
    "pronoun": True,
    "noun": True,
    "adjective": True,
    "adverb": True,
    "determiner": True,
    "preposition": True,
    "verb": True,
    "noun after verb": True,
    "adjective after verb": True,
    "sentence type": True,
    "end": False,
}

def is_step_choosable(step):
    return steps_to_choosable.get(step)

def convert_step_to_display_name(step):
    return steps_to_display_name.get(step)

def convert_step_to_table_name(step):
    return simple_steps_to_table_name.get(step)

def convert_step_to_page_name(step):
    return steps_to_page.get(step)

def get_word_options(table_name):
    if table_name in loaded_data_cache:
        return loaded_data_cache[table_name]

    conn = sqlite3.connect('./db/words.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    column_names = [description[0] for description in cursor.description]
    
    options = [
        {column_names[i]: row[i] for i in range(len(column_names))}
        for row in cursor.fetchall()
    ]

    conn.close()
    loaded_data_cache[table_name] = options
    return options

def load_all_words():
    for table_name in table_names:
        get_word_options(table_name)
    
    return loaded_data_cache

def get_singular_nouns(all_words):
    return map(lambda val: val["singular"], all_words["nouns"]) 

def get_plural_nouns(all_words):
    return map(lambda val: val["plural"], all_words["nouns"]) 

def get_base_verb(all_words, verb):
    verb_dict = {}

    for current_verb in all_words["verbs"]:
        verb_dict[current_verb["present"]] = current_verb["base"]
        verb_dict[current_verb["past"]] = current_verb["base"]
        verb_dict[current_verb["perfect"]] = current_verb["base"]
        verb_dict[current_verb["continuous"]] = current_verb["base"]

    return verb_dict.get(verb) 

def get_present_verb(all_words, verb):
    verb_dict = {}

    for current_verb in all_words["verbs"]:
        verb_dict[current_verb["base"]] = current_verb["present"]
        verb_dict[current_verb["past"]] = current_verb["present"]
        verb_dict[current_verb["perfect"]] = current_verb["present"]
        verb_dict[current_verb["continuous"]] = current_verb["present"]

    return verb_dict.get(verb) 

def get_all_options(all_words, step):
    if step in ["noun", "noun after verb"]:
        return { 
            "singular": map(lambda val: { "id": val["id"], "word": val["singular"] }, all_words["nouns"]), 
            "plural": map(lambda val: { "id": val["id"], "word": val["plural"] }, all_words["nouns"])}
    if step in ["verb"]:
        return { 
            "present": map(lambda val: { "id": val["id"], "word": val["base"] }, all_words["verbs"]), 
            "past": map(lambda val: { "id": val["id"], "word": val["past"] }, all_words["verbs"]),
            "perfect": map(lambda val: { "id": val["id"], "word": val["perfect"] }, all_words["verbs"]),
            "continuous": map(lambda val: { "id": val["id"], "word": val["continuous"] }, all_words["verbs"])}
    if step in ["sentence type"]:
        return [{"id": 1, "word": "statement"}, {"id": 2, "word": "question"}, {"id": 3, "word": "negation"}]

    table_name = convert_step_to_table_name(step)
    return all_words[table_name]