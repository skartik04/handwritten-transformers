# Handwritten Transformers

By [Kartik Sharma](https://skartik04.github.io/) · [X](https://x.com/s_kartik04)

[Try the models and read the blog](https://skartik04.github.io/blog/handwritten-transformers/)

## Run a chatbot

Python 3.10+:

```bash
git clone https://github.com/skartik04/handwritten-transformers.git
cd handwritten-transformers
python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python code/chat.py --experiment general-chat --writer astra
```

Choose `general-chat` or `sycophantic`, and `astra` or `sol`.
Add `--question "hello !"` for a single question.

## Run the Codex writer

Requires Linux, `bwrap`, and an authenticated Codex CLI with access to the chosen model. The recorded flags depend on your CLI version.

```bash
python code/run_writer.py --experiment general-chat --writer astra --out local-output/astra-new
```

This runs three passes. Use `--writer sol` for Sol, or add `--dry-run` to print the command without calling the model. Each run needs a fresh output directory.
