# auto-review
A smiple web app for generating short review for a product using YouTube review videos and duckduckgo search utilizing [LangChain](https://github.com/langchain-ai/langchain) and [Streamlit](https://github.com/streamlit/streamlit).


## How It Wroks:
It uses langchain tools to first grab transcripts from youtube reviews and then summrize them. After the summary is passed to an agent with accsses to duckduckgo search tasked with writting the review. This is powered through OpenAI models. 

## Install: 


## To-Do: 
- replace openai with opensource models from huggingface.
- find a faster summrization startgery other than map-reduce.
- 
