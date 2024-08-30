# SQL Query Generation Using LLM

This project demonstrates the generation of SQL queries from real data using a Large Language Model (LLM) downloaded from Hugging Face.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher is installed.
- `pip` is available for package management.

## Setup Instructions

### 1. Create a Virtual Environment

First, create a virtual environment to manage your project dependencies:

```bash
python3 -m venv env
```

### 2. Activate the Virtual Environment

Activate the virtual environment:

- **For Linux/MacOS:**

    ```bash
    source env/bin/activate
    ```

- **For Windows:**

    ```bash
    .\env\Scripts\activate
    ```

### 3. Install Required Packages

Install the necessary packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Generating SQL Queries

### 1. Install Hugging Face CLI

Install the Hugging Face command line interface (CLI) for managing models:

```bash
pip install -U "huggingface_hub[cli]"
```

### 2. Login to Hugging Face

Authenticate to Hugging Face using your access token:

```bash
huggingface-cli login
```

> **Note:** Use your own Hugging Face read token during login.

### 3. Download the Open-Source LLM

Download the LLM from Hugging Face:

```bash
huggingface-cli download meta-llama/Meta-Llama-3.1-8B-Instruct --local-dir Meta-Llama-3.1-8B-Instruct --local-dir-use-symlinks False
```

### 4. Run the Inference Script

Generate SQL queries using the downloaded LLM:

```bash
python inference_llm.py
```

## Evaluating Generated Queries

You can evaluate the efficiency of the generated SQL queries using the evaluation scripts:

- **Evaluation Example 1:**

    ```bash
    sh ./run_evaluation.sh
    ```

    The main evaluation file for this is located at `./evaluation.py`.

- **Evaluation Example 2:**

    ```bash
    sh ./run_evaluation.sh
    ```

    The main evaluation file for this is located at `./evaluation_ves.py`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

