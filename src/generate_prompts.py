import pandas as pd
import numpy as np
import json
import re

unicode_mapping = {
    '\\u201d': '"',  # Right double quotation mark
    '\\u2019': "'",  # Right single quotation mark
    '\\u2013': '-',  # En dash
    '\\u2018': "'",  # Left single quotation mark
    '\\u2026': '...',  # Horizontal ellipsis
    '\\u00a0': ' ',  # Non-breaking space
    '\\u2014': '--',  # Em dash
    '\\u201c': '"',  # Left double quotation mark
}

def load_wvs_section(excel_file_path="data/WVSChatGPT.xlsx", section_idx=0):
    # read the wvs xlsx
    wvs_df = pd.read_excel(excel_file_path, sheet_name=None)
    wvs_sections = pd.ExcelFile(excel_file_path).sheet_names
    prompt_sections = [section for section in wvs_sections if "Prompt" in section]

    # filter for the specific section_idx
    prompt_section = prompt_sections[section_idx]
    section_df = wvs_df[prompt_section]
    section_df.columns = section_df.columns.str.lower()

    return section_df

def replace_unicode(input_string):
    for unicode_char, ascii_char in unicode_mapping.items():
        input_string = input_string.replace(unicode_char, ascii_char)
    return input_string

def get_wvs_prompts_json(excel_file_path="data/WVSChatGPT.xlsx", section_idx=0):
    section_df = load_wvs_section(excel_file_path, section_idx)

    # retrieve shifts, contexts, questions, and option choices
    shifts = list(section_df["shift"])
    contexts = list(section_df["context"])
    questions = list(section_df["question"])
    orig_options = list(section_df["option"])

    options = list()
    for orig_option_choice in orig_options:
        new_option_choice = [ooc.strip() for ooc in orig_option_choice.split(",")]
        options.append(new_option_choice)

    # retrieve list of prompts for given section
    prompts = list()

    shift = None
    context = None
    question_list = None
    option_choices = None

    for i in range(len(shifts)):
        shift = shifts[i]

        if not np.isnan(shift):
            shift = int(shift)
            context = contexts[i]
            question_list = questions[i:i+shift]
            option_choices = options[i]

            prompt_dict = {
                "Context": context,
                "Questions": question_list,
                "Options": option_choices
            }

            prompt = json.dumps(prompt_dict, indent=2)
            prompt = replace_unicode(prompt)
            prompts.append(prompt)

    return prompts

def find_unicode_indices(input_string):
    indices = [match.start() for match in re.finditer(r'\\u', input_string)]
    return indices

def find_all_unicode():
    unicode_chars = list()
    for section_idx in range(8):
        section_prompts = get_wvs_prompts_json(section_idx=section_idx)
        for prompt in section_prompts:
            unicode_indices = find_unicode_indices(prompt)
            prompt_unicode_chars = [prompt[i:i+6] for i in unicode_indices]
            unicode_chars.extend(prompt_unicode_chars)

    unicode_chars = set(unicode_chars)
    print(unicode_chars)

section_prompts = get_wvs_prompts_json(section_idx=0)

for i in range(len(section_prompts)):
    print("=======================\n")
    print(section_prompts[i])