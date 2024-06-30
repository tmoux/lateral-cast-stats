#!/usr/bin/env python

import sys
import json
from openai import OpenAI
from os import getenv

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=getenv("OPENROUTER_API_KEY"),
)

def query_all(id):
  with open(f'transcripts/{id}.txt', 'r') as file:
      transcript = ''.join(file.read().splitlines())

  with open(f'results/{id}.txt', 'r') as file:
      questions = json.load(file)

  for question in questions:
    response = query(transcript, question['question'])
    question['answer'] = response
  
  return questions

def query(transcript, question):
  prompt = """
  This is a transcript of a trivia podcast.
  Explain the answer to the following question that was discussed.
  Be concise but provide all information needed to understand the answer:

  """

  chat_prompt = transcript + prompt + question

  completion = client.chat.completions.create(
    # model= "microsoft/phi-3-medium-128k-instruct:free",
    model = "mistralai/mistral-7b-instruct:free",
    messages = [
      {
        "role": "user",
        "content": chat_prompt
      },
    ],
  )
  return completion.choices[0].message.content

id = int(sys.argv[1])
answers = query_all(id)
for d in answers:
  print(d['question'])
  print(d['answer'])
  print('')
with open(f"answers/{id}.txt", 'w', encoding='utf8') as outfile:
  json.dump(answers, outfile, ensure_ascii=False)
