# Contract Understanding Agent

## Objectives

1. Extract key terms from the given terms in JSON format, including terms like budget constraints, types of allowable work, etc.

2. Given a list of tasks and the associated budgets, output whether the task is compliant with the contract and list the reasons for non-compliance, if any.

## Technical Details

### Frontend

Built using Streamlit with ability to:

- upload contract and task description files
- view and download the extracted contract terms as a JSON file
- view and download the compliance terms that are violated and reasons for non-compliance (if applicable)

### Backend

Two components built using LangChain to return structured output in JSON mode via OpenAI's GPT-4o:

- Extract the terms of the contract in JSON using GPT-4o
- Predict the contract terms that are violated along with details

## Public URL of the app hosted on Streamlit Cloud

## How to run the app locally

- Create an env file with the OPENAI_API_KEY set to a valid one (say, `.env`)
- Build a docker image like so:
  `docker build -t contract-app:0.1 .`
- Run a docker container using the image like so:
  `docker run --env-file .env -p 8501:8501 contract-app:0.1`
- Visit http://localhost:8501 to view the app
