import sqlglot
import torch
import transformers
import logging
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
from text_to_sql.helper import execute_sql_query, extract_schema_info


# Suppress all the unnecessary info/warning logs
logging.getLogger("transformers").setLevel(logging.ERROR)



def load_llm(model_id, optimize='4-bit', device='auto'):
    """
    Load a pre-trained language model and its corresponding tokenizer with 4-bit quantization support, 
    using BitsAndBytesConfig for efficient memory usage.

    Args:
        model_id (str): Model identifier or path to the pre-trained model.
        optimize (str): Model weights optimization {'4-bit', '8-bit', '16-bit', None}.
        device (str): Device to load the model on {'auto', 'cpu' or 'cuda:x' for specific GPU}.

    Returns:
        tuple: A tuple containing the loaded model and tokenizer.
    """
    # Load the tokenizer with left padding and fast mode
    tokenizer = AutoTokenizer.from_pretrained(
        model_id, 
        padding_side='left', 
        use_fast=True
    )
    # Define a mapping for quantization configurations
    quantization_configs = {
        '4-bit': BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",  # "fp4" is also an option
            bnb_4bit_compute_dtype=torch.bfloat16  # Can be torch.float16 or torch.bfloat16
        ),
        '8-bit': BitsAndBytesConfig(
            load_in_8bit=True,
            bnb_8bit_use_double_quant=True,
            bnb_8bit_quant_type="dynamic",  # "static" is also an option
            bnb_8bit_compute_dtype=torch.bfloat16  # Can be torch.float16 or torch.bfloat16
        ),
    }
    # Load the model based on the optimization level
    if optimize in quantization_configs:
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            quantization_config=quantization_configs[optimize],
            device_map=device,
            trust_remote_code=True,
        )
    elif optimize == '16-bit':
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float16,  # Using half precision (16-bit)
            device_map=device,
            trust_remote_code=True,
        )
    elif optimize == None:
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map=device,
            trust_remote_code=True,
        )

    # Initialize the text-generation pipeline with the loaded model and tokenizer
    pipe = pipeline( 
        "text-generation", 
        model=model, 
        tokenizer=tokenizer, 
    )
    return pipe


def get_llm_response(pipe, prompt):
    messages = [{"role": "user", "content": prompt}] 
    # generation_args = {
    #     "max_new_tokens": 500,
    #     "return_full_text": False,
    #     "temperature": 0.1,
    #     "do_sample": True,
    # }
    # output = pipe(messages, **generation_args) 
    output = pipe(messages, max_new_tokens=500)
    response = output[0]['generated_text'][-1]["content"]
    return response


def sql_llm(pipe, db, question, max_try, domain_knowledge=""):
    """
    Generate an SQL query using an LLM and execute it on a database.

    Parameters:
    - db (str): The path to the SQLite database file.
    - question (str): The natural language question to convert to SQL.
    - max_try (int): The maximum number of attempts for generating a valid SQL query.
    - domain_knowledge (str): Additional domain-specific knowledge to guide the query generation.

    Returns:
    - tuple: A tuple containing the generated SQL query and the query results.
    """

    # # Query to extract information about the tables in the database
    # db_info_extraction_query = """
    # SELECT name, sql
    # FROM sqlite_master
    # WHERE type='table';
    # """
    # db_info = execute_sql_query(db_info_extraction_query, db)

    # Extract database information
    db_info = extract_schema_info(db)

    # Define the prompt for the LLM
    prompt = f"""
    You are an expert in converting English questions to SQL query!
    \nThe SQL database details: \n{db_info.strip()}
    \nQuestion: \n{question.strip()}
    \nDomain Knowledge: \n{domain_knowledge.strip()}
    \nGenerate a SQL query based on the provided database details, English question and domain knowledge. Also the sql code should not have ``` in beginning or end and sql word in output.
    """

    prompt = prompt.strip()

    for _ in range(max_try):
        try:
            generated_query = get_llm_response(pipe, prompt)
            generated_query = ' '.join(generated_query.split()) # Convert to a single-line query
            generated_query = generated_query.split("```sql")[-1].split("```")[0].strip() # Cleaning
            sqlglot.transpile(generated_query) # Validate the generated SQL query
            sql_llm_response = execute_sql_query(generated_query, db)
            if len(sql_llm_response) > 0: # Break the loop if you receive any response
                break
        except Exception as e:
            if _ == max_try-1:  # On the final attempt, return an error message
                try:
                    generated_query
                except:
                    generated_query = ""
                sql_llm_response = "I’m having trouble in understanding. Could you please rephrase or simplify your query?"
    return generated_query, sql_llm_response