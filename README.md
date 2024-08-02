# Contract Understanding Agent

## Objectives

1. Extract key terms from the given terms in JSON format, including terms like budget constraints, types of allowable work, etc.

2. Given a list of tasks and the associated budgets, output whether the task is compliant with the contract and list the reasons for non-compliance, if any.

## Technical Architecture

### Frontend
Built using Streamlit with ability to:
- upload contract and task description files
- view and download the extracted contract terms as a JSON file
- view and download the compliance terms that are violated and reasons for non-compliance (if applicable)

### Backend
Two components built using LangChain to return structured output in JSON mode via OpenAI's GPT-4o:
- Extract the terms of the contract in JSON using GPT-4o
- Predict the contract terms that are violated along with details

## How to run the app



# contract-understanding-agent
