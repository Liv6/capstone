import os
from groq import Groq
import gradio as gr
from PyPDF2 import PdfReader 
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

os.environ['GROQ_API_KEY'] = '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'
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def summarize(file, prompt):

    #preprocess PDF file
    #extracting text from all pages
    reader = PdfReader(file)
    num_pages = len(reader.pages)

    all_text = []

    #extract text from the first three pages
    for page_number in range(min(3, num_pages)):
        page = reader.pages[page_number]
        text = page.extract_text()
        all_text.append(text)

    #extract text from the last three pages
    for page_number in range(max(0, num_pages - 3), num_pages):
        page = reader.pages[page_number]
        text = page.extract_text()
        all_text.append(text)
        
    full_text = ' '.join(all_text)
    
    #tokenization
    tokens = full_text.split()

    #removing punctuation after tokenization
    cleaned_tokens = [re.sub(r'[^\w\s]', '', token) for token in tokens]

    #removing empty tokens
    cleaned_tokens = [token for token in cleaned_tokens if token]
    
    #removing stopwords
    stop_words = set(stopwords.words('english'))
    cleaned_tokens = [token for token in cleaned_tokens if token.lower() not in stop_words]
    
    #concatenate prompt and text
    input_text = prompt + " " + full_text

    #summarize using groq model
    chat_completion = client.chat.completions.create(
    messages=[{
        "role": "user",
        "content": input_text}],
        model="Mixtral-8x7b-32768")

    summarize = chat_completion.choices[0].message.content
    return summarize

#have to define prompt box first to have it under the examples
prompt = gr.Textbox(placeholder="Pick one of the examples or type your prompt...", label = "Prompt Input", lines=8)

with gr.Blocks(theme=gr.themes.Soft(primary_hue="purple")) as iface:
    #place to upload files; I have it to only show pdfs files, but someone could still upload non-PDF files it would just send back an error
    file = gr.File(label="Upload PDF", file_types=["pdf"])

    #box for the output
    sum_box = gr.Textbox(placeholder="Your summary will appear here...", label = "Summary Output", lines=8, interactive= False)

    #examples for users to use, when clicked it fills in the prompt textbox
    examples = gr.Examples(examples=[
        "Write a two-paragraph summary of this PDF document, emphasizing the key points and conclusions"
      , "Write a one-paragraph summary of the key findings or arguments presented in this PDF"
      , "Provide a bullet-point outline of the key insights from this PDF"
      , "Write a summary tweet (280 characters) based on the main points of this PDF"], inputs=[prompt])

    #showing prompt textbox and making button to submit
    prompt.render()
    send = gr.Button("Send")

    #I could not figure out how to align the github link to the right and it bugs me
    with gr.Row():
        gr.Markdown("Made by Olivia VonCanon")
        link = "[View on Github](https://github.com/Liv6)"
        gr.Markdown(link)

    #calling the function if user pushes send button
    send.click(fn=summarize, inputs=[file, prompt], outputs=sum_box)
    
iface.launch()
