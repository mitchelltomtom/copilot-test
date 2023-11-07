import openai
import PyPDF2
import tiktoken

MAX_TOKENS = 150
MODEL_TOKEN_SIZE = 4097
def openai_summarise(api_key: str, text_contents: str, model_engine: str, prompt_question:str = 'Please summarize the following text:'):
    openai.api_key = api_key
    prompt = f"{prompt_question}:\n{text_contents}"
    completions = openai.ChatCompletion.create(
        model=model_engine,
        messages = [{"role": "user", "content": prompt}],
        max_tokens=MAX_TOKENS,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return completions

def summarise_pdf(pdf_path: str, api_key: str, model_engine: str) -> str:
    """
    Summarises the text contents of a PDF file using the OpenAI API.

    Args:
        pdf_path (str): The path to the PDF file to summarize.
        api_key (str): The API key for the OpenAI API.
        model_engine (str): The name of the OpenAI model engine to use for summarization.

    Returns:
        str: The summary of the text contents of the PDF file.
    """
    # Step 1: Configure a tokenizer using the TikToken library
    encoding = tiktoken.encoding_for_model(model_engine)

    # Step 2: Read the PDF file using PyPDF2 and extract the text contents
    batch_size = MODEL_TOKEN_SIZE - MAX_TOKENS - 100
    batches_text = ['']
    batch_iterator = 0
    summaries = []

    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            new_text = page.extract_text()
            len_new_tokens = len(encoding.encode(new_text))
            len_tokens = len(encoding.encode(batches_text[batch_iterator]))
            if len_new_tokens + len_tokens > batch_size:
                batch_iterator += 1
                batches_text.append('')
            batches_text[batch_iterator] += new_text

    # Step 3: Use the OpenAI API to generate a summary of the text contents
    i: int  = 1
    for batch in batches_text:
        print(f'Processing batch {i} of {len(batches_text)}')
        i+=1
        summary = openai_summarise( api_key, batch, model_engine)
        summaries.append(summary)

    

    # Step 4: Return the summary
    return [summary.choices[0].text.strip() for summary in summaries]
