#!/usr/bin/env python

import sys
import json

class ProcessingException(Exception):
    def __init__(self, question, message):
        super().__init__(message)
        self.message = message
        self.question = question

    def __str__(self):
        return f"Question: {self.question}: {self.message}"

# Find longest prefix of question that appears 1-3 times
def find_index(transcript: str, question: str):
  for i in range(len(question), 0, -1):
     prefix = question[:i]
     prefix_count = transcript.count(prefix)
     if 1 <= prefix_count <= 3:
        return transcript.rfind(prefix)
  raise ProcessingException(question, "No occurence of 1-3 times")

def process_transcript(transcript: str, questions: list[str]):
  transcript_lower = transcript.lower()
  def build_info(question):
    question_lower = question.lower()
    index = find_index(transcript_lower, question_lower)
    return {
    "question": question,
    "index": index
    }

  results = [build_info(question) for question in questions]
  return sorted(results, key = lambda x: x["index"])

def read_transcript(id):
   with open(f"transcripts/{id}.txt", 'r') as file:
    return ''.join(file.read().splitlines())


def build_results(id):
  transcript = read_transcript(id)
  with open(f"questions/{id}.txt", 'r') as file:
    questions = list(map(str.strip, filter(None, file.read().splitlines())))
  results = process_transcript(transcript, questions)

  ds = []
  for res in results:
     print(f'{res["index"]:5} {res["question"]}')
     ds.append(res["index"])
  dds = [ds[i] - ds[i - 1] for i in range(1, len(ds))] 
  print(dds)
  with open(f"results/{id}.txt", 'w', encoding='utf8') as outfile:
    json.dump(results, outfile, ensure_ascii=False)
  
id = int(sys.argv[1])
build_results(id)