from langchain_community.chat_models import ChatVertexAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from utils import config


settings = config.Settings()


llm = ChatVertexAI(
    model_name="chat-bison@002",
    max_output_tokens=2000,
    temperature=0,
    top_p=0.8,
    top_k=1,
    verbose=True,
)
prompt_template = PromptTemplate.from_template(
    # """
    #     Given the details of a product in an e-commerce marketplace.
    #     Summarize the details, keeping only the ones you would give to a customer, as a salesperson.
    #     Never return anything other than the summarized document, as the output will be sent directly to the customer.
    #     The summarized document should have at most 500 tokens.
    #     The sku_config and offer_code are not important fields.
    #     Product details: {document}
    #     Summarized details:
    # """
    f"""
        You are given the details of a product in an e-commerce marketplace.
        Summarize the details, so that the result has at most {settings.summary_word_count} words.
        Keep as many details as possible while respecting the word limit.
        Prioritize retaining the details that you believe are more important for the customer to see.
        Never return anything other than the summarized document, as the output will be sent directly to the customer.
        Make sure to include the product_url in the summarized details.
        Product details: {{document}}
        Summarized details:
    """
)
chain = LLMChain(llm=llm, prompt=prompt_template)


def summarize(content: str) -> str:
    response = chain({"document": content})
    return response["text"]
