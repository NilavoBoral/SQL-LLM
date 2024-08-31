### Download the model (Meta-Llama-3.1-8B-Instruct)

- **I. Install Hugging Face CLI**

Install the Hugging Face command line interface (CLI) for managing models:

```bash
pip install -U "huggingface_hub[cli]"
```

- **II. Login to Hugging Face**

Authenticate to Hugging Face using your access token:

```bash
huggingface-cli login
```

> **Note:** Use your own Hugging Face read token during login. You can find your access token by going to [Hugging Face Tokens](https://huggingface.co/settings/tokens).

- **III. Download the LLM from Hugging Face:**

```bash
huggingface-cli download meta-llama/Meta-Llama-3.1-8B-Instruct --local-dir Meta-Llama-3.1-8B-Instruct --local-dir-use-symlinks False
```