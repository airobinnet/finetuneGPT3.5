import os
import openai

# Get OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define filename, system prompt, and user prompt
# system and user prompts are used to test the model
FILENAME = "example_data.jsonl"
SYSTEMPROMPT = "You are an AI."
USERPROMPT = "test content goes here"

async def prepare_data(filename):
    '''Prepare data for training'''
    print(filename)
    last_step = ''
    # Open file and create a file object in OpenAI
    with open(filename, "rb") as f:
        data = await openai.File.acreate(file=f.read(), purpose="fine-tune")
    print(data)
    # Check file status until it is processed
    while True:
        file_status = openai.File.retrieve(data.id).status
        if file_status == 'uploaded':
            if last_step != file_status:
                print("File uploaded successfully with id: {}".format(data.id))
                last_step = file_status
        elif file_status == 'error':
            print("File upload failed.")
            break
        elif file_status == 'processed':
            print("File processed successfully.")
            break
        else:
            print("File upload still in progress. Waiting for 5 seconds...")
            time.sleep(5)

    return data

import time

async def train_model(dataid):
    '''Train the model'''
    last_step = ''
    print(dataid)
    # Create a fine tuning job
    job = await openai.FineTuningJob.acreate(
        training_file=dataid,
        model="gpt-3.5-turbo"
    )
    print("Job created. Waiting for the job to finish...")
    # Check job status until it is finished
    while True:
        job_status = openai.FineTuningJob.retrieve(job.id)
        print(job_status.status)
        if job_status.status == 'succeeded':
            if last_step != job_status.status:
                print("Job finished successfully.")
                last_step = job_status.status
            if job_status.fine_tuned_model is not None:
                print("Model created with id: {}".format(job_status.fine_tuned_model))
                return job_status.fine_tuned_model
        elif job_status.status == 'failed':
            print("Job failed.")
            return None
        else:
            print("Job still in progress. Waiting for 60 seconds...")
            time.sleep(60)

async def use_model(fine_tuned_model):
    '''Use the trained model'''
    print('loading ' + fine_tuned_model)
    # Generate chat completion with the trained model
    completion = await openai.ChatCompletion.acreate(
    model=fine_tuned_model,
    # do a test run
    messages=[
        {"role": "system", "content": SYSTEMPROMPT},
        {"role": "user", "content": USERPROMPT}
    ]
    )

    print(completion.choices[0].message)

# Main function
async def main():
    # Prepare data
    data = await prepare_data(FILENAME)
    # Train model
    model = await train_model(data.id)
    # Use model
    await use_model(model)

# Run main function
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
