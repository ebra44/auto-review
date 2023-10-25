import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
from langchain.document_loaders import YoutubeLoader
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools , initialize_agent , AgentType
from langchain.chains.summarize import load_summarize_chain
from langchain.tools import YouTubeSearchTool
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain

llm = ChatOpenAI(temperature=0,streaming=True, model_name="gpt-3.5-turbo-16k")

st.title("Auto Review ⏩")
st.header("Auto review using youtube videos and review articles!")


if device := st.chat_input():
    st.chat_message("user").write(device)


    with st.chat_message("assistant"):
        st.write("checking what youtube has to say ...")
        videos = YouTubeSearchTool().run(f"{device} review, 3")
        l_videos= videos.split(",")
        context = []

        text_spliter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=0)
    
        for link in l_videos:
            link = link.replace("'","").replace("[","").replace("]","").replace(" ","")
            loader = YoutubeLoader.from_youtube_url(link)
            result = loader.load()
            context.extend(text_spliter.split_documents(result))
    
        map_prompt = """
            Write a concise summary of the following:
            "{text}"
            CONCISE SUMMARY:
            """

        combine_prompt = """
        Write a concise summary of the following text delimited by triple backquotes.
        Return your response in bullet points which covers the key points of the text.
        ```{text}```
        BULLET POINT SUMMARY:
        """

        map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])
        combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"])


        s_chain = load_summarize_chain(
                llm=llm,
                chain_type="map_reduce",
                map_prompt=map_prompt_template,
                combine_prompt = combine_prompt_template,
                verbose=False)

        st.write("creating a summry of top youtube reviews ...")
        summrized_information = s_chain.run(context)
        st.write("thinking and writing ...")
        prompt = PromptTemplate(
                input_variables=["device","text"],
                template="You are an expert tech writer. You should write a detalied article review for '{device}' be sure to consult the context and include its main points '{text}'. If you are unsure about any detail you can use Search tool to look up and validate information , be sure to cover technical specs, best parts, worst parts, any problems that come after use, preformance only if information exsists else ignor. give the device a rating on a scale from 1 to 10 where 1 is DON'T BUY and 10 being MUST buy",
        )
        tools = load_tools(["ddg-search"])
        writer_agent = initialize_agent(
                 tools=tools,
                llm=llm,
                agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION
        )

        st_callback = StreamlitCallbackHandler(st.container())
        response = writer_agent.run(prompt.format(device=device,text=summrized_information),callbacks=[st_callback])
        st.write(response)
