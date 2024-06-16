from earningscall import get_company
from openai import OpenAI

# Place your OpenAI API key in a file called .openai-api-key
with open(".openai-api-key", "r") as fd:
    api_key = fd.read().strip()
client = OpenAI(api_key=api_key)


def generate_summary_and_sentiment(input_text: str):
    summarization_prompt = f"""Summarize the following text:

{input_text}

Summary:
    """
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that is able to read a piece of text and summarize it.",
            },
            {
                "role": "user",
                "content": summarization_prompt,
            }
        ]
    )
    summary_text = " ".join([choice.message.content for choice in completion.choices])
    return summary_text


company = get_company("aapl")  # Lookup Apple, Inc by its ticker symbol, "AAPL"

transcript = company.get_transcript(year=2024, quarter=1)
print(f"Input Transcript Text :  {company} Q1 2024 Transcript Text: \"{transcript.text[:100]}...\"\n")
result = generate_summary_and_sentiment(transcript.text)
print(f"Generated Summary : \"{result}\"")
