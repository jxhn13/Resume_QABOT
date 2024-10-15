from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.openai import OpenAI
import os
import openai
from flask import request, jsonify

openai.api key

def chat_output():
    file_dir = '/home/anoop/resumepoc/upload/files'
    input = []
    for filename in os.listdir(file_dir):
        file_path = os.path.join(file_dir, filename)
        input.append(file_path)
    
    documents = SimpleDirectoryReader(input_files=input).load_data()
    index = VectorStoreIndex.from_documents(documents)

    data = request.get_json()
    requirements = data.get('requirements')
    
    if not requirements:
        return jsonify({'output': 'No requirements provided'})

    if not index:
        return jsonify({'output': 'No resumes are indexed yet'})

    llm = OpenAI(model='gpt-3.5-turbo')
    query_engine = index.as_query_engine(llm=llm)
    response = query_engine.query(f"Give me a complete list of all people who meet the following requirements: {requirements}. Provide all matches, not just one.")
    print(response)
    return jsonify({'output': str(response)})
