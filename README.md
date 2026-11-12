# Multi-Tool AI Agent for Bangladesh

An AI-powered assistant built with **LangChain** that answers Bangladesh-related questions using three structured SQLite databases and a Tavily Web Search tool.

## Features

- **InstitutionsDBTool:** Retrieves information about universities, colleges, and government institutions.
- **HospitalsDBTool:** Retrieves hospital information, including location, bed capacity, and facilities.
- **RestaurantsDBTool:** Retrieves restaurant information, including ratings, cuisine, and addresses.
- **WebSearchTool:** Uses Tavily Search API to answer general knowledge questions.
- **Main AI Agent:** Intelligently selects the appropriate tool based on the user's query.

## Architecture

```text
HuggingFace Datasets
        |
        v
     CSV Files
        |
        v
  SQLite Databases
        |
        |---------------------------|
        |            |              |
        v            v              v
  Institutions   Hospitals     Restaurants
    DB Tool       DB Tool        DB Tool
        |            |              |
        |------------|--------------|
                     |
              Tavily Web Search
                     |
                     v
                 Main Agent
                     |
                     v
            Natural Language Response
```

## Datasets

1. [Institutional Information of Bangladesh](https://huggingface.co/datasets/Mahadih534/Institutional-Information-of-Bangladesh)
2. [All Bangladeshi Hospitals](https://huggingface.co/datasets/Mahadih534/all-bangladeshi-hospitals)
3. [Bangladeshi Restaurant Data](https://huggingface.co/datasets/Mahadih534/Bangladeshi-Restaurant-Data)

## Tech Stack

- Python
- LangChain
- SQLite
- Tavily Search API
- HuggingFace Datasets
- Groq LLM

## Workflow

1. Download datasets from HuggingFace in CSV format.
2. Convert CSV files into three SQLite databases.
3. Create three database-specific LangChain tools.
4. Integrate Tavily Web Search for general knowledge queries.
5. Build a Main AI Agent using LangChain Agent Executor.
6. Execute user queries using appropriate tools and return natural language responses.

## Example Queries

- How many hospitals are there in Dhaka?
- Find the top 10 highest-rated restaurants in Bangladesh.
- Which universities offer medical degrees in Bangladesh?
- What is the role of DGHS in Bangladesh?
- Find restaurants in Chattogram serving biryani.

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## Installation and Usage

```bash
git clone https://github.com/your-username/multi-tool-ai-agent-bangladesh.git

cd multi-tool-ai-agent-bangladesh

pip install -r requirements.txt

python main.py
```

## Project Goal

To build an intelligent multi-tool AI agent that combines structured Bangladeshi datasets with web search to provide accurate, relevant, and natural language answers.

---

**Developed by Md. Shorif**  
IIT, Jahangirnagar University
