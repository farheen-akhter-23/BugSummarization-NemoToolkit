from langchain.llms import HuggingFaceHub
from langchain.chains.summarize import load_summarize_chain
# from nemo_guardrails import Guardrails

# Initialize Hugging Face LLM
def initialize_llm():
    # Replace 'huggingface/llm-model-name' with the desired model from Hugging Face
    llm = HuggingFaceHub(
        model="nvidia/Mistral-NeMo-Minitron-8B-Instruct", 
        api_key="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"
    )
    return llm

# Function to generate a summary with Guardrails
def generate_summary(text):
    llm = initialize_llm()
    # Initialize summarization chain
    summarize_chain = load_summarize_chain(llm)
    summary = summarize_chain(text)
    return summary