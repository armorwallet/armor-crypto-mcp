from prowl import ProwlStack, prowl
import os

async def build(prompt:str=None, model='anthropic/claude-3.7-sonnet', use_cot=False):
    # pass the prompt from source.md
    # Load in the coding reference material
    with open('armor_client.py') as f:
        python_code = f.read()
    inputs = {}
    inputs['code'] = prowl.Variable('code', value=python_code)
    async def token_event(text, finish_reason, variable_name):
        print(text, end="")
    r:prowl.Return = await prowl.fill(
        prowl.load('source_think.md' if use_cot else 'source.md'), 
        stops=['```'] if use_cot else ['\n\n\n\n\n#'], 
        variables=inputs,
        model=model, 
        continue_ratio=0.2,
        token_event=token_event,
    )
    print(r.completion)
    print(r.usage.dict())
    
    # Output to proper build path
    build_root = f"build/{model}/"
    build_path = f"{build_root}/server.py"
    os.makedirs(build_root, exist_ok=True)
    with open(build_path, 'w+') as f:
        f.write(r.val('mcp_code'))
    
if __name__ == "__main__":
    import asyncio
    # "google/gemini-2.0-flash-thinking-exp:free"
    # "google/gemini-2.0-flash-001"
    # "anthropic/claude-3.7-sonnet"
    asyncio.run(build(model="deepseek/deepseek-r1-zero:free"))