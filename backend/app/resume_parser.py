# app/resume_parser.py
import pdfplumber
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ''.join([page.extract_text() or '' for page in pdf.pages])
    return text

def extract_entities(text):
    doc = nlp(text)
    entities = {"PERSON": [], "ORG": [], "EMAIL": [], "PHONE": [], "SKILLS": []}
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG"]:
            entities[ent.label_].append(ent.text)
    return entities
