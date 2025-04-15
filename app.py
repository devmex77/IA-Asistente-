#librerias
from flask import Flask, render_template, request, jsonify
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from conocimientos import info

app = Flask(__name__)

template = """

Respuesta  a la pregunta debajo:
Conocimientos:
{conocimientos}

aqui esta el contexto de la conversacion:
{context}

Pregunta: {question}

Respuesta: 
"""

model = OllamaLLM(model = "llama3.2:1b")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    #recibiendo mensaje de navegador
    question = request.json.get("message")
    print(question)
    if not question:  
            return jsonify({"response": "No entendí tu mensaje."})


    print("Generando respuesta...")
    context = ""
    while  True:
        #question = input("Tu: ")
        if question == "stop":
            break
        
        #respuesta del chatbot
        result = chain.invoke({"conocimientos":info, "context":context, "question": question})
        #imprimiendo respuesta por consola
        print("Bot:", result)
        context += f"Bot: {result}\nTu: {question}\n"
        return jsonify({"response": result})
    

if __name__ == "__main__":
    app.run(debug=True)
    chat()