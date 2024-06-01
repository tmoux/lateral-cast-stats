import json 
from dataclasses import dataclass
import matplotlib.pyplot as plt

@dataclass
class Question:
  episode: int
  question: str
  length: int


questions = []
for i in range(1, 85 + 1):
  try:
    with open(f"results/{i}.txt") as file:
      l = json.load(file)
      for j in range(len(l) - 1):
        qlen = l[j+1]["index"] - l[j]["index"]
        questions.append(Question(i, l[j]["question"], qlen))

  except FileNotFoundError:
    pass

questions.sort(key = lambda q: -q.length)

lengths = list(map(lambda q: q.length, questions))

plt.hist(lengths, bins=20, alpha=0.7, color='blue', edgecolor='black')
plt.xlabel('Length')
plt.ylabel('Frequency')
plt.title('Distribution of Question Lengths (in characters)')
plt.show()
