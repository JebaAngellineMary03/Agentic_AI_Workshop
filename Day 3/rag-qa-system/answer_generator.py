import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(query, context_chunks):
    context = "\n\n".join([chunk['text'] for chunk in context_chunks])

    prompt = f"""
You are an AI assistant that answers questions using academic text chunks provided below. 
When answering, cite the source chunks using square brackets like [1], [2], etc., matching the numbers assigned in the context.

Question: {query}


Context:
{context}

Answer:"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=500
    )

    return response.choices[0].message.content
