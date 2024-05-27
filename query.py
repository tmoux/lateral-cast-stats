#!/usr/bin/env python

import sys
from openai import OpenAI
from os import getenv

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=getenv("OPENROUTER_API_KEY"),
)

def query(id):
  with open(f'transcripts/{id}.txt', 'r') as file:
      content = ''.join(file.read().splitlines())

  # prompt = """
  # This is a transcript of a trivia podcast that has the following format: 
  # 1. Asking a short "bonus question" and introducing the guests.
  # 2. A sequence of questions. One person will read the question twice, and then the other guests will work together to find the answer. 
  # 3. Conclusion and answering the "bonus question" quickly.

  # Please identify each of these trivia questions that are being asked, including the "bonus question".
  # Usually, there will be six questions, plus the bonuus question answered at the end.

  # Format your response with each question on a newline, EXACTLY as they are written in the transcript.
  # For the bonus question, write it like it is written at the END of the transcript, not the beginning.
  # Do not include answers or any other text, or questions like "What next question do you have for us?"
  # Do NOT use a numbered list or punctuation.
  # """

  prompt = """
  This is a transcript of a trivia podcast that has the following format: 
  1. Asking a short "bonus question" and introducing the guests.
  2. A sequence of questions. One person will read the question twice, and then the other guests will work together to find the answer. 
  3. Conclusion and answering the "bonus question" quickly.

  Please identify each of these trivia questions that are being asked.
  Usually, there will be seven questions, including a bonus question.

  Format your response with each question on a newline, EXACTLY as they are written in the transcript.
  For the bonus question, write it like it is written at the END of the transcript, not the beginning.
  Do not include answers or any other text, or questions like "What next question do you have for us?"
  Do NOT write questions multiple times.
  Do NOT use a numbered list or punctuation.
  """

  chat_prompt = content + prompt

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
with open(f'questions/{id}.txt', 'w') as file:
  questions = query(id)
  print(questions)
  file.write(questions + '\n')