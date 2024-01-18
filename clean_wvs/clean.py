from clean_utils import *
import argparse
import pandas as pd
from tqdm import tqdm

letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

def create_cleaned_ds(wvs_fp, output_fp):
    wb = pd.ExcelFile(wvs_fp)

    question_ids = list()
    sections = list()
    questions = list()
    answer_choices = list()

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

            for j in range(i, i+shift):
                question_info = dict(df.iloc[j])
                question = create_question(question_template, lower, question_info)
                answer_choice = create_answer_choice(question_info)
                answer_choice = answer_choice + [None] * (10 - len(answer_choice))
                
                question_ids.append(question_info["ID"])
                sections.append(section)
                questions.append(question)
                answer_choices.append(answer_choice)
                
            i = j + 1

    data = {
        'ID': question_ids,
        'Section': sections,
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