# python src/preprocess/clean_questionaire.py --wvs_fp wvs_data/questionaire/natural_wvs.xlsx --output_fp wvs_data/questionaire/clean_wvs.csv

import argparse
import pandas as pd
from tqdm import tqdm

letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

def create_question(question_template, lower, question_info):
    question_insertion = question_info["QuestionInsertion"]
    left = question_info["Left"]
    right = question_info["Right"]

    if type(question_insertion) == str:
        if lower:
            question_insertion = question_insertion.lower()
        question = question_template.replace("{QUESTION}", question_insertion)  

    else:
        question = question_template   
    
    if type(left) == str:
        question = question.replace("{LEFT}", left)

    if type(right) == str:
        question = question.replace("{RIGHT}", right)

    return question.strip()

def split_string_by_commas(s):
    result = []
    current = ""
    depth = 0

    for char in s:
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1

        if char == ',' and depth == 0:
            result.append(current.strip())
            current = ""
        else:
            current += char

    # Add the remaining part if any
    if current:
        result.append(current.strip())

    return result

def create_answer_choice(question_info):
    answer_choice = question_info["AnswerChoices"]
    left = question_info["Left"]
    right = question_info["Right"]

    if type(left) == str:
        answer_choice = answer_choice.replace("{LEFT}", left)

    if type(right) == str:
        answer_choice = answer_choice.replace("{RIGHT}", right)

    answer_choice = split_string_by_commas(answer_choice)
    answer_choice = [c for c in answer_choice if not c == ""]
    nums = [int(c.split(":")[0].strip()) for c in answer_choice]
    answer_choice = [c.split(":")[1].strip() for c in answer_choice]

    sorted_pairs = sorted(zip(nums, answer_choice), key=lambda x: x[0])
    answer_choice = [pair[1] for pair in sorted_pairs]

    return answer_choice

def create_cleaned_ds(wvs_fp, output_fp):
    wb = pd.ExcelFile(wvs_fp)

    question_ids = list()
    sections = list()
    questions = list()
    answer_choices = list()
    ordinals = list()
    indices = list()

    for section in tqdm(range(1, 9)):
        section_name = f"Section{section}"
        sheet_names = wb.sheet_names
        target_sheet_name = next((name for name in sheet_names if name.startswith(section_name)), None)
        df = pd.read_excel(wvs_fp, sheet_name=target_sheet_name)

        i = 0
        while not i == len(df):
            orig_question_info = dict(df.iloc[i])
            shift = int(orig_question_info["Shift"])
            question_template = orig_question_info["Question"]
            lower = (orig_question_info["Lower"] == 1)
            ordinal = (orig_question_info["Ordinal"] == 1)
            one_index = (orig_question_info["OneIndex"] == 1)

            for j in range(i, i+shift):
                question_info = dict(df.iloc[j])
                question = create_question(question_template, lower, question_info)
                answer_choice = create_answer_choice(question_info)
                answer_choice = answer_choice + [None] * (10 - len(answer_choice))
                
                question_ids.append(question_info["ID"])
                sections.append(section)
                questions.append(question)
                answer_choices.append(answer_choice)
                ordinals.append(ordinal)
                indices.append(one_index)
                
            i = j + 1

    data = {
        'ID': question_ids,
        'Section': sections,
        'Ordinal': ordinals,
        'OneIndex': indices,
        'Question': questions
    }

    for i in range(10):
        answer_choices_i = [ac[i] for ac in answer_choices]
        data[letters[i]] = answer_choices_i
            
    df = pd.DataFrame(data)
    df.to_csv(output_fp, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--wvs_fp", type=str)
    parser.add_argument("--output_fp", type=str)
    args = parser.parse_args()

    create_cleaned_ds(args.wvs_fp, args.output_fp)