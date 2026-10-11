# Using Informaniak's provider, the pricing for the google/gemma-4-31B-it model is as follows:
# INPUT : CHF 0.002 / 10K tokens 
# OUTPUT : CHF 0.004 / 10K tokens

def calculate_ik_gemma_price(input_tokens, output_tokens):
    INPUT_PRICE_PER_MILLION = 0.20
    OUTPUT_PRICE_PER_MILLION = 0.40

    input_cost = (input_tokens / 1_000_000) * INPUT_PRICE_PER_MILLION
    output_cost = (output_tokens / 1_000_000) * OUTPUT_PRICE_PER_MILLION
    total_cost = input_cost + output_cost

    return {
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
    }


def print_cost_breakdown(cost_breakdown):
    print(f"Input Cost: CHF {cost_breakdown['input_cost']:.6f}")
    print(f"Output Cost: CHF {cost_breakdown['output_cost']:.6f}")
    print(f"Total Cost: CHF {cost_breakdown['total_cost']:.6f}")