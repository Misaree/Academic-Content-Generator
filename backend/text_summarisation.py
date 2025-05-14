from transformers import pipeline, AutoTokenizer

def summarize_text(input_text):
    """
    Summarize the input text using BART model
    Args:
        input_text: The text to be summarized
    Returns:
        str: The summarized text
    """
    try:
        # Load the BART summarization pipeline and tokenizer
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")

        # Function to split text into chunks
        def split_text_into_chunks(text, chunk_size=500):
            words = text.split()
            chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
            return chunks

        # Ensure text is not empty
        if not input_text or not input_text.strip():
            raise ValueError("Input text is empty")

        text_chunks = split_text_into_chunks(input_text, chunk_size=500)
        summaries = []
        buffer = ""  # Buffer to store small chunks

        for chunk in text_chunks:
            chunk = buffer + " " + chunk  # Add leftover text from previous chunk
            buffer = ""  # Reset buffer

            # Skip if too small (less than 10 words)
            if len(chunk.split()) < 10:
                buffer = chunk  # Store for next chunk
                continue

            try:
                # Tokenize the chunk
                tokenized_chunk = tokenizer(chunk, truncation=True, max_length=1024, return_tensors="pt")
                num_words = len(chunk.split())

                # Dynamic min/max length to avoid index errors
                max_len = min(150, num_words // 2) if num_words > 40 else num_words
                min_len = min(30, num_words // 4) if num_words > 20 else 5

                # Summarize
                summary = summarizer(chunk, max_length=max_len, min_length=min_len, do_sample=False)
                summaries.append(summary[0]['summary_text'])

            except IndexError:
                print(f"Warning: IndexError for chunk, trying with smaller length...")
                try:
                    summary = summarizer(chunk, max_length=50, min_length=2, do_sample=False)
                    summaries.append(summary[0]['summary_text'])
                except Exception as e:
                    print(f"Warning: Could not summarize chunk: {str(e)}")
                    buffer = chunk

        # Combine the summaries
        final_summary = " ".join(summaries)
        if not final_summary.strip():
            raise ValueError("Could not generate summary")
            
        return final_summary

    except Exception as e:
        print(f"Error in summarization: {str(e)}")
        raise