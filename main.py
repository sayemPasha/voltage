import streamlit as st
import os 
from dotenv import load_dotenv
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.llms import OpenAI
from langchain.sql_database import SQLDatabase
from langchain.chat_models import ChatOpenAI

load_dotenv()



def main():
    st.title("Voltage: A Natural Language Interface to Databases")
    st.write("Upload SQLite database file below.")

    database = st.file_uploader("Upload a SQLITE Database",accept_multiple_files=False)

    if database is not None:
        with open(os.path.join("database",database.name),"wb") as f:
           f.write(database.getbuffer())
        st.success("Saved File")
        dburi=f'sqlite:///../voltage/database/{database.name}'
        db = SQLDatabase.from_uri(dburi)

        if db:
            agent = create_agent(db)
            candidate_query = st.text_area("Insert your query")

            if st.button("Submit Query", type="primary"):
                st.write("You submitted the query:", "<span style='color: blue;'>", candidate_query, "</span>", unsafe_allow_html=True)
                response = agent.run(candidate_query)
                st.markdown(f"<div style='background-color: lightgreen; padding: 10px;'>{response}</div>",
                unsafe_allow_html=True)

                print(response)


def create_agent(db):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(
        llm = llm,
        toolkit=toolkit,
        verbose=True
    )
    return agent_executor


if __name__ == "__main__":
    main()
