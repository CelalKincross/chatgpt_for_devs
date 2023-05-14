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