import pandas as pd
import xml.etree.ElementTree as ET
from pathlib import Path

def parse_file(file: Path):
    parsed_xml = ET.parse(file)
    root = parsed_xml.getroot()
    
    question = root.find("questionText").text
    reference_answer_elements = root.find("referenceAnswers").findall("referenceAnswer")
    reference_answers = [] 
    for ref_answer in reference_answer_elements:
        if ref_answer.attrib["category"] == "BEST":
            reference_answers.append(ref_answer.text)

    student_answer_elements = root.find("studentAnswers").findall("studentAnswer")
    
    entries = []
    for student_answer in student_answer_elements:
        entry = {
                "question": question,
                "student_answer": student_answer.text,
                "accuracy": student_answer.attrib["accuracy"],
                "file_name": file.stem
            }
        for index, reference_answer in enumerate(reference_answers):
            entry[f"reference_answer{index}"] = reference_answer
        entries.append(entry)
    return entries

def convert_accuracy_to_grade(accuracy):
    if accuracy == "non_domain" or accuracy == "irrelevant":
        return 0
    if accuracy == "contradictory":
        return 1
    if accuracy == "partially_correct_incomplete":
        return 2
    if accuracy == "correct":
        return 3
    
    raise f"Unexpected accuracy type encountered: {accuracy}"

def load_beetle(xml_folder_path = Path("../../data/original/semeval-5way/beetle/train/Core")) -> pd.DataFrame:
    xml_files = xml_folder_path.glob("*.xml")
    
    entries = []
    for file in xml_files:
        entries += parse_file(file)

    df = pd.DataFrame(entries)
    df['grade'] = df['accuracy'].apply(convert_accuracy_to_grade)
    return df

def rename_beetle(beetle: pd.DataFrame) -> pd.DataFrame:
    return beetle.rename(columns={
        "reference_answer0": "reference_answer",
        "student_answer": "provided_answer",
    })

