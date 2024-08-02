from langchain_openai import ChatOpenAI
from typing import Annotated


def extract_contract_terms(contract_text):
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    structured_llm = model.with_structured_output(method="json_mode")
    prompt_prefix = """
    You will be provided with a contract text containing various terms and constraints for work execution (e.g., budget constraints, types of allowable work, etc.).
	Your task is to extract the list of all key terms from the contract and structure them in a JSON format.
    Terms may be related to different sections and subsections of the contract, which should be reflected in your JSON.
    """
    terms = structured_llm.invoke(f"{prompt_prefix} Contract Text: {contract_text}")
    return terms


class ViolatedTerms:
    term: Annotated[str, "The specific contract term that is violated."]
    violation: Annotated[str, "Detailed explanation of the violation."]


class TaskCompliance:
    compliant: Annotated[
        bool, "True if the task is compliant with the contract terms, False otherwise."
    ]
    violated_terms: Annotated[
        list[ViolatedTerms],
        "If the task is not compliant, the specific terms that are violated along with detailed explanation.",
    ]


def predict_task_compliance(task, amount, contract_terms):
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    structured_llm = model.with_structured_output(TaskCompliance, method="json_mode")
    prompt_prefix = """
    You will be provided with a task description and an amount of money allocated for that task.
    Your task is to predict in JSON format with the following fields: 
    (1) "compliant": whether the task is compliant with the contract terms.
    (2) "violated_terms": if not compliant, which specific contract terms are violated. This should be 
    a list of dictionaries containg fields for:
        (a) term - the term that was violated.
        (b) violation - detailed description of the violation.
    
    The contract terms are structured in a JSON format with different sections and subsections.
    """
    task_compliance = structured_llm.invoke(
        f"{prompt_prefix} Task Description: {task} Amount: {amount} Contract Terms: {contract_terms}"
    )
    return task_compliance
