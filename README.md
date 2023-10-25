# auto-review 
A simple web app for generating short review for a product using YouTube review videos and duckduckgo search utilizing [LangChain](https://github.com/langchain-ai/langchain) and [Streamlit](https://github.com/streamlit/streamlit).

![alt text](https://github.com/ebra44/auto-review/blob/main/answer.png?raw=true)

## How It Works:
It uses langchain tools to first grab transcripts from youtube reviews and then summarize them. After the summary is passed to an agent with access to duckduckgo search tasked with writing the review. This is powered through OpenAI models. 


## Install: 
```
git clone https://github.com/ebra44/auto-review.git
pip install -r requirements.txt
streamlit run auto-review.py
```
remember to either export the api key in the OPENAI_API_KEY environment variable or to load with .env

## To-Do: 
- replace openai with open source models from hugging face.
- find a faster summarization strategy to replace map-reduce.
  
