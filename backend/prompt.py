from langchain.prompts import PromptTemplate

prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Answer:
"""

# customized prompt for cusine related info
cuisine_context = """So you are going to search the information of vendors list in CSV file, which has following columns:
place_number : the id for searcing vendor's location
booking_weezpay_account:the booking account number of the vendors
stall_name: name of the vendors
drink_categories: available drink from the vendors
food_types: available food from vendors
"""
CUISINE_PROMPT = PromptTemplate(
    template=prompt_template, input_variables=[cuisine_context, "question"]
)

# customized prompt for location related info
location_context = """So you are going to search the information of vendors location, which has following information:
when user ask where is the vendor, you need to follow following step:
1. find the place_number 
2. use the place_number to find corrsponded properties has same numero value.
3. return the whole properties information, including centerpoint.
"""
LOCATION_PROMPT = PromptTemplate(
    template=prompt_template, input_variables=[location_context, "question"]
)