from flask import Flask, render_template, request, redirect, url_for
from utils import load_all_words, next_possible_steps, convert_step_to_page_name, convert_step_to_display_name, is_step_choosable, get_all_options, finishing_steps, tense_choosable_steps, get_singular_nouns, get_plural_nouns, get_base_verb, get_present_verb

app = Flask(__name__, static_folder='static', template_folder='templates')

all_words = load_all_words()

chosen_options = {}

@app.route('/')
def home():
    chosen_options.clear()
    return render_template('home.html')

@app.route('/step/<step>', methods=['GET', 'POST'])
def step(step):
    if request.method == 'POST':
        chosen_options[step] = request.form['option']

        if step in tense_choosable_steps:
            chosen_options["tense"] = request.form['tense']

        return redirect(url_for('steps', step=step))
    
    possible_options = get_all_options(all_words, step)
    page_name = convert_step_to_page_name(step)
    return render_template(f'{page_name}.html', step=step, options=possible_options)

@app.route('/steps', methods=['GET', 'POST'])
def steps():
    if request.method == 'POST':
        selected_step = request.form['step']

        if selected_step in finishing_steps:
            return redirect(url_for('result'))
        
        if is_step_choosable(selected_step):
            return redirect(url_for('step', step=selected_step))
        else:
            return redirect(url_for('steps', step=selected_step))

    step = request.args.get('step', 'start')
    next_steps = map(lambda val: { "display_name": convert_step_to_display_name(val), "step": val }, get_next_steps(step))
    return render_template('next.html', current_step=step, possible_steps=next_steps)

@app.route('/result')
def result():
    sentence = build_sentence()
    chosen_options.clear()
    return render_template('result.html', sentence=sentence)

def get_next_steps(current_step):
    next_steps = next_possible_steps.get(current_step)
    return next_steps

def build_sentence():
    elements = []

    chosen_tense = chosen_options.get("tense")
    chosen_type_of_sentence = chosen_options.get("sentence type")

    if chosen_tense == "present":
        if chosen_options.get("pronoun") in ["he", "she", "it"] or chosen_options.get("noun") in get_singular_nouns(all_words):
            if chosen_type_of_sentence == "statement":
                chosen_options["verb"] = get_present_verb(all_words, chosen_options["verb"])
            elif chosen_type_of_sentence == "question":
                chosen_options["question"] = "Does "
            elif chosen_type_of_sentence == "negation":
                chosen_options["verb"] = "doesn't " + chosen_options["verb"]
        elif chosen_options.get("pronoun") in ["we", "you", "they"] or chosen_options.get("noun") in get_plural_nouns(all_words):
            if chosen_type_of_sentence == "question":
                chosen_options["question"] = "Do "
            elif chosen_type_of_sentence == "negation":
                chosen_options["verb"] = "don't " + chosen_options["verb"]
    elif chosen_tense == "past":
        if chosen_type_of_sentence == "question":
            chosen_options["question"] = "Did "
            chosen_options["verb"] = get_base_verb(all_words, chosen_options["verb"])
        elif chosen_type_of_sentence == "negation":
            chosen_options["verb"] = "didn't " + chosen_options["verb"]
    elif chosen_tense == "perfect":
        if chosen_type_of_sentence == "statement":
            chosen_options["verb"] = "had " + chosen_options["verb"]
        elif chosen_type_of_sentence == "question":
            chosen_options["question"] = "Had "
        elif chosen_type_of_sentence == "negation":
            chosen_options["verb"] = "hadn't " + chosen_options["verb"]
    elif chosen_tense == "continuous":
        if chosen_options.get("pronoun") == "I":
            if chosen_type_of_sentence == "statement":
                chosen_options["verb"] = "am " + chosen_options["verb"]
            elif chosen_type_of_sentence == "question":
                chosen_options["question"] = "Am "
            elif chosen_type_of_sentence == "negation":
                chosen_options["verb"] = "am not " + chosen_options["verb"]
        elif chosen_options.get("pronoun") in ["he", "she", "it"] or chosen_options.get("noun") in get_singular_nouns(all_words):
            if chosen_type_of_sentence == "statement":
                chosen_options["verb"] = "is " + chosen_options["verb"]
            elif chosen_type_of_sentence == "question":
                chosen_options["question"] = "Is "
            elif chosen_type_of_sentence == "negation":
                chosen_options["verb"] = "isn't " + chosen_options["verb"]
        elif chosen_options.get("pronoun") in ["we", "you", "they"] or chosen_options.get("noun") in get_plural_nouns(all_words):
            if chosen_type_of_sentence == "statement":
                chosen_options["verb"] = "are " + chosen_options["verb"]
            elif chosen_type_of_sentence == "question":
                chosen_options["question"] = "Are "
            elif chosen_type_of_sentence == "negation":
                chosen_options["verb"] = "aren't " + chosen_options["verb"]

    for k, v in chosen_options.items():
        elements.append({"key": k, "option": v})

    elements.append({"key": "ending", "option": "?" if chosen_type_of_sentence == "question" else ""})

    reordered_elements = swap_elements(elements, ["question", "determiner", "adjective", "noun", "pronoun", 
    "verb", "preposition", "adjective after verb", "noun after verb", "adverb", "ending"])
        
    return ' '.join(map(lambda val: val["option"], reordered_elements))

def swap_elements(elements, sentence_order):
    reordered_elements = []

    for key in sentence_order:
        matching_element = next((element for element in elements if element["key"] == key), None)
        if matching_element:
            reordered_elements.append(matching_element)
    
    return reordered_elements

if __name__ == '__main__':
    app.run(debug=True)
