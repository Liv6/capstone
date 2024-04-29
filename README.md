# capstone

Main Objectives:

1. Build a function that takes user input and a PDF file, converts and cleans the file, then creates a summary using an LLM.

2. Build an interface with gradio that has a chatbox, place to upload files, and prompt examples.

3. Analyze how well the model performs through different tests.


GRadio Permanent Link: https://huggingface.co/spaces/nonacnov/capstone

1 Installing and Importing Libraries: Before we begin, we need to make sure we have all the necessary libraries installed. We need to install gradio to build the interface, groq to access the model, PyPDF2 to extract the PDF text, and nltk to clean the PDF.

2 Groq API: To access the Groq model, I had to get an API key from their website. Originally I was going to use an OpenAI model, but I could not get it to work correctly. I don't think the API was even available when I started planning out the project, but it was super easy to get working.

Here is how it works: 

* there is a function that takes a pdf file and the users prompt
* the function extracts the text from the pdf file
* then the function summarizes the pdf with a Groq model (only using the first 3 pages and last 3 pages)

The interface is built with gradio. At the top there is a place for users to upload pdf files. It is set to only show PDF files when clicked, but someone could still upload non-pdf files it would just send back an error. Under the file box there is a textbox that shows the output from the model. Under that there is example promps users can click to quickly get summaries, or they can type prompts in the textbox below the examples. To call the function, a user must push the send button.

The project was tested using the PDF "Auditing the Use of Language Models to Guide Hiring Decisions." It was tested at every stage of preprocessing. The results are in the ipynb file. All four Groq models were also tested to see the different layouts of the outputs and how well it handles format requests such as number of paragraphs or number of characters. I also tested the runtimes for each model using the pre-made two-paragraph prompt. The results for all the tests are in the ipynb file.
