# Product Q&A ChatBot

Q&A tool to extract meaningful information from the Google Store reviews.

## Installation

Prerequisite:
- In this case, I use WSL or Ubuntu 22.04.
- Python3.10
- virtualenv

Steps:
- Create and activate the virtualenv.

    ```bash
    virtualenv .venv -p /usr/bin/python3.10
    source .venv/bin/activate
    ```

- Install python packages.

    ```bash
    pip install -r requirements.txt
    ```

## Execution Pipeline

Steps:
- Load the environment variables that contain `OPENAI` and `PINECONE` credentials. Then, fill in your credentials. The example of envars were written in `.env.example` file.
- Edit and fill `.env.example` and rename it to `.env`.
- Load the envars with `export` command.

    ```bash
    export $(grep -v '^#' .env | xargs)
    ```

- Now we can run the execution pipeline by executing the `main.py` file.

    ```bash
    python main.py
    ```

- All the configuration params are saved in `config/config.yml`
- The process will execute the other process in this order:
  - Data ingestion (Automatically download the datasets).
    - The important params:
      - `force_ingest`: set to `True` to replace the current datasets.
  - Upsert the document (Select the useful features (column), Load the CSV as Documents, Chunk the documents, Document embedding, and upsert to the Pinecone database).
    - The important params:
      - `data_length`: to determine the length of the datasets (number of rows as documents). With the value set to `-1` are mean upsert all data to Pinecone.
      - `force_upsert`: set to `True` to replace the current documents in Pinecone.
  - Evaluation (Evaluate the LLMs Performance), *this part is already done in `notebook/10_evaluation.ipynb` but I still need time to implement it as part of the pipeline*.

## Run Application

Steps:
- Load the environment variables that contain `OPENAI` and `PINECONE` credentials. Then, fill in your credentials. The example of envars was written in `.env.example` file.
- Edit and fill `.env.example` and rename it to `.env`.
- Load the envars with `export` command.

    ```bash
    export $(grep -v '^#' .env | xargs)
    ```

- Now we can run the streamlit apps by executing the `app.py`.

    ```bash
    streamlit run app.py
    ```

## Future Works

- Convert `notebook/10_evaluation.ipynb` to pipeline.
- Try more prompt by using [Summarization](https://python.langchain.com/docs/use_cases/summarization) and [Self-Querying](https://python.langchain.com/docs/modules/data_connection/retrievers/self_query/) to improve the ChatBot. Because this is a CSV data and we can use the Metadata as input.
- Spliting Upsert the document pipeline into more detail parts like:
  - Select the useful features (column)
  - Load the CSV as Documents
  - Chunk the documents
  - Document embedding
  - Upsert to the Pinecone database

## Screenshots

<br>
<p align="center" width="100%">
    <img width="80%" src="img/chat_bot.png">
</p>
<br>

## Demo Videos

https://github.com/rohwid/question-and-answer-chatbot/assets/9447439/f0585787-8bc6-4ba0-9b57-e971871b78ea
