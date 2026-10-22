import time
from tqdm.auto import tqdm

def calculate_token_costs(usage, model):

    match model:
        case "google/gemma-4-31B-it":
            INPUT_PRICE_PER_MILLION = 0.20
            OUTPUT_PRICE_PER_MILLION = 0.40
        case "Qwen/Qwen3.8-27B-FP8":
            INPUT_PRICE_PER_MILLION = 0.40
            OUTPUT_PRICE_PER_MILLION = 3.00
        case "Qwen/Qwen3.5-122B-A10B-FP8":
            INPUT_PRICE_PER_MILLION = 0.80
            OUTPUT_PRICE_PER_MILLION = 3.60
        case _:
            raise ValueError("Man! I don't know the costs for this mode. Give me costs data.")

    input_cost = (usage.prompt_tokens / 1_000_000) * INPUT_PRICE_PER_MILLION
    output_cost = (usage.completion_tokens / 1_000_000) * OUTPUT_PRICE_PER_MILLION
    total_cost = input_cost + output_cost

    return {
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
    }



# call llm using expecting a structured response
def llm_structured(client, instructions, user_prompt, output_type, model, max_retries=1):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.parse(
                model=model,
                messages=[
                    {"role": "developer", "content": instructions},
                    {"role": "user", "content": user_prompt}
                ],
                response_format=output_type
            )
            return response.choices[0].message.parsed, response.usage
        except Exception as e:
            if attempt == max_retries - 1:
                print("Max retries reched")
                print(e)
                raise
            time.sleep(2 ** attempt)


def map_progress(pool, seq, f):
    results = []

    with tqdm(total=len(seq)) as progress:
        futures = []

        for el in seq:
            future = pool.submit(f, el)
            future.add_done_callback(lambda p: progress.update())
            futures.append(future)

        for future in futures:
            result = future.result()
            results.append(result)

    return results