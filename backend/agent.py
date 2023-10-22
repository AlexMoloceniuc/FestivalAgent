import os
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from dataloader import create_loader
from vectors import create_search_section
from prompt import CUISINE_PROMPT, LOCATION_PROMPT
from langchain.chains import RetrievalQA
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import SystemMessage
from langchain.callbacks.streaming_stdout_final_only import (
    FinalStreamingStdOutCallbackHandler,
)
from configs import config

# Acess to ChatGPT model
os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY # Use the API key from the config file
llm = ChatOpenAI(streaming=True, callbacks=[FinalStreamingStdOutCallbackHandler(answer_prefix_tokens=['Agent', ':'])], temperature=0)
embeddings = OpenAIEmbeddings()

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create loader instances for each file type
pdf_loader = create_loader('.pdf', 'data/pdf', script_dir)
geoJson_loader = create_loader('.json', 'data/geoJson/fdv_stands20230920.geojson', script_dir)
csv_loader = create_loader('.csv', 'data/csv/export_stands20230922 (1).csv', script_dir)

# Load the files
pdf_documents = pdf_loader.load()
csv_documents = csv_loader.load()
geoJson_documents = geoJson_loader.load()

# History. Urgency, Ticket, Program, Music
faqSearch = create_search_section(pdf_documents, "faqSection", {'chunk_size': 500, 'chunk_overlap': 0}, embeddings)

# Food, Beverage
cuisineSearch = create_search_section(csv_documents, "cuisineSection", {'chunk_size': 500, 'chunk_overlap': 0}, embeddings)

# Location
locationSearch = create_search_section(csv_documents + geoJson_documents, "locationSection", {'chunk_size': 500, 'chunk_overlap': 0}, embeddings)


# Create retrieverQA chain for each topics
faq_retriever = RetrievalQA.from_chain_type(
    llm=llm, chain_type="refine", retriever=faqSearch.as_retriever(search_type="mmr", search_kwargs={'k': 6, 'lambda_mult': 0.25})
)

cuisine_retriever = RetrievalQA.from_chain_type(
    llm=llm, chain_type="refine", retriever=cuisineSearch.as_retriever(search_type="mmr", search_kwargs={'k': 6, 'lambda_mult': 0.25}, chain_type_kwargs={"prompt": CUISINE_PROMPT})
)

location_retriever = RetrievalQA.from_chain_type(
    llm=llm, chain_type="refine", retriever=locationSearch.as_retriever(chain_type_kwargs = {"prompt": LOCATION_PROMPT})
)

tools = [
    Tool(
        name="FAQ",
        func=faq_retriever.run,
        description="useful the questions about the history of the FDV festival, information about ticket, performance(program) schedule, music, artists, lineup, transportation, and emergencey related info",
    ),
    Tool(
        name="Cuisine",
        func=cuisine_retriever.run,
        description="useful for questions about what food, dirnks, the vendor provides and the properties of the provided food",
    ),
    Tool(
        name="Location",
        func=location_retriever.run,
        description="useful for questions about the location of vendor",
    ),
]

system_message = SystemMessage(
    content="You are an AI that work as a friendly customer support agent to provide info for questions"
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent = initialize_agent(tools, llm, 
                         agent=AgentType.OPENAI_FUNCTIONS, 
                         system_message=system_message,
                         agent_kwargs={"system_message": system_message}, 
                         verbose=False, 
                         memory=memory,
                         max_iterations=2,
                         handle_parsing_errors="Check you output and only give final answer")

print(agent.run("hi, who are you ?"))
print()
while True:
    user_input = input("Human: ")
    print(agent.run(user_input))
    print()
    print('-'*50)