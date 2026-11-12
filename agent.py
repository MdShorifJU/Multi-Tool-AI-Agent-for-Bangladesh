
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq


from tools.restaurants_tool import (
    RestaurantsDBTool,
    get_restaurants_schema
)

from tools.hospitals_tool import (
    HospitalsDBTool,
    get_hospitals_schema
)

from tools.instituations_tool import (
    InstitutionsDBTool,
    get_institutions_schema
)


load_dotenv()


# Initialize Groq LLM
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.2,
    api_key=os.getenv("GROQ_API_KEY")
)


DATABASES = {
    "RESTAURANTS": {
        "schema": get_restaurants_schema,
        "tool": RestaurantsDBTool,
        "description": "Restaurant names, cuisines, ratings, addresses and food."
    },

    "HOSPITALS": {
        "schema": get_hospitals_schema,
        "tool": HospitalsDBTool,
        "description": "Hospital names, locations, facilities and healthcare information."
    },

    "INSTITUTIONS": {
        "schema": get_institutions_schema,
        "tool": InstitutionsDBTool,
        "description": "Educational, government and other institutional information."
    }
}


# Step 1: Database Decision


def select_database(question):

    decision_prompt = f"""
You are an intelligent query classification assistant.

Your task is to identify whether the user's question
requires information from one of the available Bangladesh
databases or is a general question.

Available Databases:

1. RESTAURANTS:
   {DATABASES["RESTAURANTS"]["description"]}

2. HOSPITALS:
   {DATABASES["HOSPITALS"]["description"]}

3. INSTITUTIONS:
   {DATABASES["INSTITUTIONS"]["description"]}

4. GENERAL:
   Any question asking for general knowledge, explanations,
   advice, guidance, suggestions, tutorials, career planning,
   study abroad guidance, or information unrelated to the
   specific records in the three Bangladesh databases.

IMPORTANT CLASSIFICATION RULES:

- Select RESTAURANTS only when the user asks for restaurant
  records, ratings, cuisines, locations, or related data.

- Select HOSPITALS only when the user asks for hospital
  records, locations, facilities, or related data.

- Select INSTITUTIONS only when the user asks for specific
  institution records available in the Bangladesh institutions
  database.

- Select GENERAL when the user asks for advice, guidance,
  explanations, or general information about a topic.

- Mentioning words like university, hospital, education,
  restaurant, or institution does NOT automatically mean
  the question belongs to a database.

- If the question is not asking for specific records from
  the available databases, always select GENERAL.

EXAMPLES:

Question: Find the top 5 highest-rated restaurants in Bangladesh.
Category: RESTAURANTS

Question: Find hospitals in Dhaka.
Category: HOSPITALS

Question: List public universities in Bangladesh.
Category: INSTITUTIONS

Question: What can I do to pursue a PhD in the USA?
Category: GENERAL

Question: How can I get a scholarship for studying abroad?
Category: GENERAL

Question: Explain Artificial Intelligence.
Category: GENERAL

Question: Which programming language should I learn?
Category: GENERAL

Question: What are the admission requirements for MIT?
Category: GENERAL

Question: Find universities in Bangladesh from the database.
Category: INSTITUTIONS

User Question:
{question}

Return ONLY one exact label:

RESTAURANTS
HOSPITALS
INSTITUTIONS
GENERAL
"""

    response = llm.invoke(decision_prompt)

    selected_database = response.content.strip().upper()

    valid_categories = list(DATABASES.keys()) + ["GENERAL"]

    if selected_database not in valid_categories:
        return "GENERAL"

    return selected_database

# Step 2: Generate SQL Query
def generate_sql(question, schema):

    sql_prompt = f"""
You are an expert SQLite query generator.

Database Schema:
{schema}

User Question:
{question}

Instructions:
- Generate a valid SQLite SELECT query.
- Use only the available table and column names.
- Do not generate INSERT, UPDATE, DELETE or DROP queries.
- Do not explain anything.
- Return only the SQL query.
"""

    response = llm.invoke(sql_prompt)

    sql_query = response.content.strip()

    # Remove Markdown SQL formatting if present
    if sql_query.startswith("```"):
        sql_query = sql_query.split("\n", 1)[1]
        sql_query = sql_query.rsplit("```", 1)[0].strip()

    return sql_query


# Step 3: Execute Selected Database Tool
def execute_database_tool(database_name, sql_query):

    selected_tool = DATABASES[database_name]["tool"]

    result = selected_tool.invoke({
        "sql_query": sql_query
    })

    return result


# Step 4: Generate Natural Language Answer
def generate_answer(question, database_name, db_result):

    answer_prompt = f"""
You are a helpful Bangladesh information assistant.

User Question:
{question}

Selected Database:
{database_name}

Database Result:
{db_result}

Instructions:
- Analyze the database result carefully.
- Answer according to the user's question.
- Show all available relevant records.
- Present information clearly using bullet points.
- Never invent information.
- Never provide information that is not available in the database.
- If no matching records are found, clearly explain that.
- Answer in English.
"""

    response = llm.invoke(answer_prompt)

    return response.content

# Main AI Agent Workflow
def run_agent(question):

    question = question.strip()

    if not question:
        return "Please enter a valid question."

    print("\nUser:", question)

    try:

        # Step 1: Questions type selection
        print("\n[Step 1] Selecting Database/Category...")
        database_name = select_database(question)

        # Part 1
        if database_name == "GENERAL":

            print("\nCategory: GENERAL")

            response = llm.invoke(question)

            print("\nAssistant:")
            print(response.content)

            return response.content

        # or Part 2
        print("\n[Step 2] Getting Database Schema...")

        schema = DATABASES[database_name]["schema"]()

        if schema.startswith(
            ("Database not found:", "Table '", "Database error:")
        ):
            print(schema)
            return ""

        print(schema)

        print("\n[Step 3] Generating SQL Query...")

        sql_query = generate_sql(question, schema)

        print("\nGenerated SQL:")
        print(sql_query)

        print("\n[Step 4] Executing Database Tool...")

        db_result = execute_database_tool(
            database_name,
            sql_query
        )

        print("\nDatabase Result:")
        print(db_result)

        print("\n[Step 5] Final Answer from database...")

        final_answer = generate_answer(
            question,
            database_name,
            db_result
        )

        print("\nAI:")
        print(final_answer)
        return final_answer

    except Exception as e:

        print("\nAgent Error:", str(e))

        return (
            "Sorry! Service is not available right now. "
            "Please try after sometime."
        )

# Run Agent
if __name__ == "__main__":
    run_agent()
