import argparse
import torch
import re
import time
from transformers import pipeline
import sqlite3

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_structure(data_path): #1 Extracts the database structure
    """ Extract structure from SQLite database.

    Args:
        data_path: path to SQLite data file.

    Returns:
        text description of database structure.
    """
    with sqlite3.connect(data_path) as connection:
        cursor = connection.cursor()
        cursor.execute("select sql from sqlite_master where type = 'table';")
        table_rows = cursor.fetchall()
        table_ddls = [r[0] for r in table_rows]
    return '\n'.join(table_ddls)

def create_prompt(description, question): #2 Creates a prompt for translation
    """ Generate prompt to translate a question into an SQL query.

    Args:
        description: text description of database structure.
        question: question about data in natural language.

    Returns:
        prompt for question translation.
    """
    parts = []
    parts += ['Database:']
    parts += [description]
    parts += ['Translate this question into SQL query:']
    parts += [question]
    return '\n'.join(parts)

def call_llm(prompt): #3 Invokes the language model
    """ Query large language model and return answer.

    Args:
        prompt: input prompt for language model.

    Returns:
        Answer by language model.
    """
    pipe = pipeline("text-generation", model="Qwen/Qwen2-1.5B-Instruct", max_length=900, device=device, truncation=True)
    
    for nr_retries in range(1, 4):
        try:
            response = pipe(prompt, max_length=900)
            return response[0]['generated_text']
        except:
            time.sleep(nr_retries * 2)
    raise Exception('Cannot query model!')

def process_query(data_path, query): #4 Processes a query on a database
    """ Processes SQL query and returns result.

    Args:
        data_path: path to SQLite data file.
        query: process this query on database.

    Returns:
        query result.
    """
    with sqlite3.connect(data_path) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        table_rows = cursor.fetchall()
        table_strings = [str(r) for r in table_rows]
        return '\n'.join(table_strings)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dbpath', type=str, help='Path to SQLite data')
    args = parser.parse_args()
    
    data_structure = get_structure(args.dbpath) #5 Reads data structure
    while True: #6  Answers questions until the user quits
        user_input = input('Enter question:')
        if user_input == 'quit':
            break
        prompt = create_prompt(data_structure, user_input)
        answer = call_llm(prompt)
        query = re.findall('```sql(.*)```', answer, re.DOTALL)[0]
        print(f'SQL: {query}')

        try: #7  Processes query on the database
            result = process_query(args.data_path, query)
            print(f'Result: {result}')
        except:
            print('Error processing query! Try to reformulate.')
