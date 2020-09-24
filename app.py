# -*- coding: utf-8 -*-
"""P-Bert.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Z-SpJjKC58CaNlL8l5wTKyIURLgaQo1y
"""

import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer

#Model
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

#Tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

def tokenize(question, paragraph):
  encoding = tokenizer.encode_plus(text=question,text_pair=paragraph, add_special=True, verbose=False)
  inputs = encoding['input_ids']  #Token embeddings
  sentence_embedding = encoding['token_type_ids']  #Segment embeddings
  tokens = tokenizer.convert_ids_to_tokens(inputs) #input tokens
  return tokens, sentence_embedding, inputs

def correctedAnswer(answer):
  corrected_answer = ''
  for word in answer.split():
      #If it's a subword token
      if word[0:2] == '##':
          corrected_answer += word[2:]
      else:
          corrected_answer += ' ' + word
  return corrected_answer

def findAnswer(question, paragraph):
  tokens, sentence_embedding, inputs = tokenize(question, paragraph)
  start_scores, end_scores = model(input_ids=torch.tensor([inputs]), token_type_ids=torch.tensor([sentence_embedding]))
  start_index = torch.argmax(start_scores)
  end_index = torch.argmax(end_scores)
  answer = ' '.join(tokens[start_index:end_index+1])
  return correctedAnswer(answer)

findAnswer(question, paragraph)

# Interface
import gradio as gr
def qa_func(question, paragraph):
    return findAnswer(question, paragraph)
gr.Interface(qa_func, 
    [
        gr.inputs.Textbox(lines=7, label="Context"), 
        gr.inputs.Textbox(label="Question"), 
    ], 
gr.outputs.Textbox(label="Answer"),
title="Question Answer",
description="BERT-SQuAD is a question answering model that takes 2 inputs: a paragraph that provides context and a question that should be answered. Takes around 6s to run.").launch()

