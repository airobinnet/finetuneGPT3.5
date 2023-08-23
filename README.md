# OpenAI GPT-3.5-Turbo Fine-Tuning Example

This is a Python script that demonstrates how to use OpenAI's GPT-3.5-Turbo fine-tuning API to train a model with your own data and then use the trained model for generating completions.

## Requirements

- OpenAI Python package (v0.27.9+)
- An OpenAI API key

## Setup

1. Install the OpenAI Python package:

    ```sh
    pip install openai
    ```

2. Set your OpenAI API key as an environment variable:

    ```sh
    export OPENAI_API_KEY='your-api-key'
    ```
3. Prepare your [JSONL](https://jsonlines.org/validator/) dataset and edit the `FILENAME`, `SYSTEMPROMPT` and `USERPROMPT`

4. Start the code

   ```sh
   python main.py
   ```

## Usage

This script consists of the following steps:

1. `prepare_data()`: This function prepares the data for training. It opens a file containing the training data and creates a file object in OpenAI. It then checks the file status until it is processed.

2. `train_model()`: This function trains the model. It creates a fine-tuning job and checks the job status until it is finished.

3. `use_model()`: This function uses the trained model to generate a chat completion.

4. `main()`: This function runs the above functions in order.

To run the script, simply execute the Python file:

```sh
python main.py
```

## Notes

- Make sure to replace `example_data.jsonl` with the path to your own training data file.
- The `use_model()` function does a test run with a system message "You are an AI." and a user message "test content goes here". You can change these messages to your own test.
- This script uses asyncio for handling the API calls. Make sure your Python environment supports asyncio.

## Limitations

- The OpenAI API has rate limits. If you make too many requests in a short period of time, you may encounter rate limit errors.
- Fine-tuning a model can take a long time and consume a lot of resources. Make sure you have enough quota and resources before running the script.
