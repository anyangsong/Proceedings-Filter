from pathlib import Path
from vllm import LLM, SamplingParams

s_template = '''# Please determine whether the paper belongs to the field of Machine-Generated Text Detection based solely on its title

Requirements:
- The input consists only of the paper title; base your judgment solely on the title.
- Output only "Yes" or "No".
- Err on the side of caution: if a paper is even suspected of belonging to the field of Machine-Generated Text Detection, output "Yes".

## Samples

### Sample Input 1

MAGA-Bench: Machine-Augment-Generated Text via Alignment Detection Benchmark

### Sample Output 1

Yes

### Sample Input 2

A Survey on In-Context Learning

### Sample Output 2

No

### Sample Input 3

ALISON: Fast and Effective Stylometric Authorship Obfuscation

### Sample Output 3

Yes

## Formal Input

### Input

{title}

### Output

'''

if __name__ == '__main__':
    input_dir = Path("./data")
    output_dir = Path("./results/mgt-detection")

    output_dir.mkdir(parents=True, exist_ok=True)

    llm = LLM(
        model="/root/models/Qwen/Qwen3.5-35B-A3B-FP8",
        enforce_eager=True,
        max_model_len=1024,
        tensor_parallel_size=2,
        gpu_memory_utilization=0.92,
    )

    sampling_params = SamplingParams(
        seed=42,
        temperature=0,
        top_p=0.95,
        top_k=20,
        max_tokens=128
    )

    for txt_file in sorted(input_dir.glob("*.txt")):
        print(f"Processing {txt_file.name}...")

        with open(txt_file, "r", encoding="utf-8") as f:
            titles = [line.strip() for line in f if line.strip()]
        print(f">> Total titles: {len(titles)}")

        messages = [
            [
                {
                    "role": "user",
                    "content": s_template.format(title=title)
                }
            ]
            for title in titles
        ]

        responses = llm.chat(
            messages,
            sampling_params=sampling_params,
            chat_template_kwargs={"enable_thinking": False}
        )

        kept_titles = []
        for title, response in zip(titles, responses):
            output = response.outputs[0].text.strip()
            if "no" not in output.lower():
                kept_titles.append(title)

        print(f">> Kept titles: {len(kept_titles)}")

        output_file = output_dir / txt_file.name

        with open(output_file, "w", encoding="utf-8") as f:
            for title in kept_titles:
                f.write(title + "\n")

        print(f"Saved to {output_file}")

    print("All done.")
