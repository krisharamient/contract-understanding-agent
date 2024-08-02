import streamlit as st
import docx
from llm_utils import extract_contract_terms, predict_task_compliance
import json
import pandas as pd
from copy import deepcopy

# ensure that environment variable OPENAI_API_KEY is set

st.title("Contract Understanding Agent")


@st.cache_data
def get_contract_terms(uploaded_contract):
    # read docx contents
    doc = docx.Document(uploaded_contract)
    paragraphs = [p.text for p in doc.paragraphs]
    doc_text = "\n".join(paragraphs)
    json_data = extract_contract_terms(doc_text)
    return json_data


@st.cache_data
def get_task_compliance(uploaded_tasks, json_data):
    df = pd.read_excel(uploaded_tasks, index_col=False)
    for i, row in df.iterrows():
        task = row["Task Description"]
        amount = row["Amount"]
        compliance_prediction = predict_task_compliance(task, amount, json_data)

        # ensure that the output has the required keys
        # (LLM output may not always be consistent)
        if "compliant" in compliance_prediction:
            df.at[i, "Compliant?"] = compliance_prediction["compliant"]
        else:
            df.at[i, "Compliant?"] = "Unknown"

        violated_terms = ""
        if "violated_terms" in compliance_prediction:
            # ensuring that output is neatly displayed as a list inside a dataframe cell
            violated_terms = "<br><br>".join(
                [
                    f"({idx + 1}) {compliance_prediction['violated_terms'][idx]['term']}<br>{compliance_prediction['violated_terms'][idx]['violation']} "
                    for idx in range(len(compliance_prediction["violated_terms"]))
                ]
            )
        df.at[i, "Violated Terms (if applicable)"] = violated_terms
    return df


# Extract contract terms from uploaded docx file of the contract
uploaded_contract = st.file_uploader(
    "Upload your contract (only docx format is accepted)"
)
if uploaded_contract is not None:
    json_data = get_contract_terms(uploaded_contract)
    json_string = json.dumps(json_data)
    st.json(json_string)
    st.download_button(
        label="Download JSON",
        file_name="contract.json",
        mime="application/json",
        data=json_string,
    )

    uploaded_tasks = st.file_uploader(
        "Upload your tasks (only xlsx format is accepted)"
    )
    if uploaded_tasks is not None:
        task_compliance_data = get_task_compliance(uploaded_tasks, json_data)
        # display as HTML so that the list of violated terms is displayed as a neat list
        st.markdown(task_compliance_data.to_html(escape=False), unsafe_allow_html=True)
