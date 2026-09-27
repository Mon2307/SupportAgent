from langchain_aws import BedrockEmbeddings


def get_embedding_function():
    return BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")