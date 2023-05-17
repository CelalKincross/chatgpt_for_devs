import openai
import os

from dotenv import load_dotenv, find_dotenv
_= load_dotenv(find_dotenv())

openai.api_key = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model='gpt-3.5-turbo'):
    messages = [{'role': 'user', 'content': prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, #this is the degree of randomness of the model's output
    )
    return response.choices[0].message['content']

###
# Prompting principles
# 1. Write Clear and specific instructions
#
# Tactic 1: Use delimiters to clearly indicate distinct parts of the input
# Delimiters can be anything like: ```, """, < >, <tag> </tag>
###

text = f'''
Yous should express what you want a model to do by \
providing instructions that are as clear and \
specific as you can possibly make them. \
This will guide the model towards the desired output, \
and reduce the chances of receiving irrelevant \
or incorrect responses. Don't confuse writing a \
clear prompt with writing a short prompt. \ 
In many cases, longer prompts provide more clarity \
and context for the model, which can lead to \
more detailed and relevant outputs. 
'''

prompt = f'''
Summarize the text delimited by triple backticks \
into a single sentence.
```{text}```
'''

response = get_completion(prompt)
print(response)

###
# Prompting principles
# 1. Write Clear and specific instructions
#
# Tactic 2: Ask for structured output
###

prompt1 = f'''
Generate a list of three made-up book titles along \ 
with their authors and genres.
Provide them in JSON format with the following keys:
book_id, title, author, genre.
'''

response1 = get_completion(prompt1)

print(response1)

###
# Prompting principles
# 1. Write Clear and specific instructions
#
# Tactic 3: Ask the model to check whether the conditions are satisfied
###

text_1 = f"""
Making a cup of tea is easy! First, you need to get some \ 
water boiling. While that's happening, \ 
grab a cup and put a tea bag in it. Once the water is \ 
hot enough, just pour it over the tea bag. \ 
Let it sit for a bit so the tea can steep. After a \ 
few minutes, take out the tea bag. If you \ 
like, you can add some sugar or milk to taste. \ 
And that's it! You've got yourself a delicious \ 
cup of tea to enjoy.
"""
prompt = f"""
You will be provided with text delimited by triple quotes. 
If it contains a sequence of instructions, \ 
re-write those instructions in the following format:

Step 1 - ...
Step 2 - …
…
Step N - …

If the text does not contain a sequence of instructions, \ 
then simply write \"No steps provided.\"

\"\"\"{text_1}\"\"\"
"""
response = get_completion(prompt)
print("Completion for Text 1:")
print(response)

###
# Prompting principles
# 1. Write Clear and specific instructions
#
# Tactic 4: "Few-Shot" prompting -- give an example of how you want the LLM to respond
###
prompt = f"""
Your task is to answer in a consistent style.

<child>: Teach me about patience.

<grandparent>: The river that carves the deepest \ 
valley flows from a modest spring; the \ 
grandest symphony originates from a single note; \ 
the most intricate tapestry begins with a solitary thread.

<child>: Teach me about resilience.
"""
response = get_completion(prompt)
print(response)

###
# Prompting principles
# 2. Give the model time to think
#
# Tactic 1: Specifiy the steps required to complete the task
###

text = f"""
In a charming village, siblings Jack and Jill set out on \ 
a quest to fetch water from a hilltop \ 
well. As they climbed, singing joyfully, misfortune \ 
struck—Jack tripped on a stone and tumbled \ 
down the hill, with Jill following suit. \ 
Though slightly battered, the pair returned home to \ 
comforting embraces. Despite the mishap, \ 
their adventurous spirits remained undimmed, and they \ 
continued exploring with delight.
"""
# example 1
prompt_1 = f'''
Perform the following actions:
1. Summarize the following text delimited by the triple backticks with 1 sentence
2. Translate the summary into French
3. List each name in the French summary
4. Output a json object that contains the for the following keys: french_summary, num_names.

Separate your answers with line breaks
Text:
```{text}```
'''

response = get_completion(prompt_1)
print("Completion for prompt 1:")
print(response)

###
# Prompting principles
# 2. Give the model time to think
#
# Tactic 2: Instruct the model to work out its own solution before rushing to a conclusion
###

prompt = f"""
Determine if the student's solution is correct or not.

Question:
I'm building a solar power installation and I need \
 help working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost \ 
me a flat $100k per year, and an additional $10 / square \
foot
What is the total cost for the first year of operations 
as a function of the number of square feet.

Student's Solution:
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
"""
response = get_completion(prompt)
print(response)

### Students response is incorrect but the model say sit is correct
### We can fi this by instructing the model to work out its own solution

prompt = f'''
Your task is to determine if the student's solution is correct or not.
To solve the problem do the following:
-First, work out your own solution to the problem
-Then compare your solution with the student's solution and evaluate if the student's solution is correct.
Don't decide if the student's solution is correct until you have done the problem yourself.

Use the following format:
Question:
```
Question here
```
Student's solution:
```
Student's solution here
```
Actual solution:
```
steps to work out the solution here
```
Is the student's solution the same as the actual solution just calcualted:
```
yes or no
```
Student grade:
```
correct or incorrect
```
Question:
```
I'm building a solar power installation and I need help \
working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost \
me a flat $100k per year, and an additional $10 / square \
foot
What is the total cost for the first year of operations \
as a function of the number of square feet.
``` 
Student's solution:
```
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
```
Actual solution:
'''

response = get_completion(prompt)
print(response)

fact_sheet_chair = """
OVERVIEW
- Part of a beautiful family of mid-century inspired office furniture, 
including filing cabinets, desks, bookcases, meeting tables, and more.
- Several options of shell color and base finishes.
- Available with plastic back and front upholstery (SWC-100) 
or full upholstery (SWC-110) in 10 fabric and 6 leather options.
- Base finish options are: stainless steel, matte black, 
gloss white, or chrome.
- Chair is available with or without armrests.
- Suitable for home or business settings.
- Qualified for contract use.

CONSTRUCTION
- 5-wheel plastic coated aluminum base.
- Pneumatic chair adjust for easy raise/lower action.

DIMENSIONS
- WIDTH 53 CM | 20.87”
- DEPTH 51 CM | 20.08”
- HEIGHT 80 CM | 31.50”
- SEAT HEIGHT 44 CM | 17.32”
- SEAT DEPTH 41 CM | 16.14”

OPTIONS
- Soft or hard-floor caster options.
- Two choices of seat foam densities: 
 medium (1.8 lb/ft3) or high (2.8 lb/ft3)
- Armless or 8 position PU armrests 

MATERIALS
SHELL BASE GLIDER
- Cast Aluminum with modified nylon PA6/PA66 coating.
- Shell thickness: 10 mm.
SEAT
- HD36 foam

COUNTRY OF ORIGIN
- Italy
"""


