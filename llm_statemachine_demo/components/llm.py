import os
from langchain_openai import ChatOpenAI

ModelName = "llama3-70b-8192"
llm = ChatOpenAI(
    openai_api_base=os.environ["LLM_PROXY_BASE_URL"],
    openai_api_key=os.environ["LLM_PROXY_KEY"],
    model=ModelName,
)


if __name__ == "__main__":
    print(os.environ["LLM_PROXY_KEY"], os.environ["LLM_PROXY_BASE_URL"])
    for d in llm.stream([("user", "Hello, write a quick sort for me")]):
        print(d.content, end="")
