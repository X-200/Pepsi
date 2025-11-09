#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from docx import Document
import re

# Read the DOCX file
doc = Document('/vercel/sandbox/uploads/MCQs on systematic مختصرة.docx')

# Extract all text
full_text = []
for para in doc.paragraphs:
    text = para.text.strip()
    if text:
        full_text.append(text)

# Parse MCQs
mcqs = []
current_question = None
current_choices = []
i = 0

while i < len(full_text):
    line = full_text[i].strip()
    
    # Check if it's a section header (all caps, no numbers)
    if line.isupper() and not re.match(r'^\d+[.-]', line) and not re.match(r'^[A-D][\s.]', line):
        # This is a section header, skip it
        i += 1
        continue
    
    # Check if it's a question (starts with number)
    question_match = re.match(r'^(\d+)[.-]\s*(.+)', line)
    if question_match:
        # Save previous question if exists
        if current_question:
            mcqs.append({
                'number': current_question['number'],
                'question': current_question['text'],
                'choices': current_choices.copy()
            })
        
        # Start new question
        current_question = {
            'number': question_match.group(1),
            'text': question_match.group(2)
        }
        current_choices = []
        i += 1
        continue
    
    # Check if it's a choice (starts with A, B, C, D)
    choice_match = re.match(r'^([A-D])[\s.]\s*(.+)', line)
    if choice_match and current_question:
        current_choices.append({
            'letter': choice_match.group(1),
            'text': choice_match.group(2)
        })
        i += 1
        continue
    
    # If it's continuation of question or choice
    if current_question and line:
        if current_choices:
            # Continuation of last choice
            current_choices[-1]['text'] += ' ' + line
        else:
            # Continuation of question
            current_question['text'] += ' ' + line
    
    i += 1

# Add last question
if current_question:
    mcqs.append({
        'number': current_question['number'],
        'question': current_question['text'],
        'choices': current_choices.copy()
    })

print(f"Total MCQs found: {len(mcqs)}")
print("\n=== First 5 MCQs ===")
for mcq in mcqs[:5]:
    print(f"\nQ{mcq['number']}: {mcq['question']}")
    for choice in mcq['choices']:
        print(f"  {choice['letter']}. {choice['text']}")
