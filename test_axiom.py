import os, sys, traceback, asyncio

os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONUTF8'] = '1'
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

os.environ['AXIOM_LLM_BACKEND'] = 'local_llama'
os.environ['AXIOM_LLAMA_MODEL_PATH'] = r'D:\models\Qwen2.5-7B-Instruct-Q4_K_M.gguf'
os.environ['AXIOM_LLM_CTX_WINDOW'] = '4096'
os.environ['AXIOM_LLM_MAX_TOKENS'] = '512'

async def main():
    from axiom_v1 import AxiomBrain
    print('Creating AxiomBrain...')
    brain = AxiomBrain()
    backend = brain.llm.backend if brain.llm else 'none'
    print('LLM Backend:', backend)
    print('LLM Available:', brain.llm.is_available() if brain.llm else False)

    print('Sending test experience...')
    result = await brain.experience('Hello, how are you?')
    print('Output type:', type(result).__name__)
    if isinstance(result, dict):
        keys = list(result.keys())[:10]
        for k in keys:
            v = result[k]
            if isinstance(v, str):
                print(f'  {k}: {v[:150]}')
            elif isinstance(v, (int, float)):
                print(f'  {k}: {v}')
            else:
                print(f'  {k}: {type(v).__name__}')
    print('AXIOM TEST SUCCESS!')
    brain.close()

try:
    asyncio.run(main())
except Exception as e:
    traceback.print_exc()
    sys.exit(1)
