#!/usr/bin/env python3
"""Тест Ollama API"""
import asyncio
import aiohttp

async def test_ollama():
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "qwen2.5:7b",
        "prompt": "Привет, как дела?",
        "stream": False
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            result = await response.json()
            print(f"Status: {response.status}")
            print(f"Result keys: {result.keys()}")
            print(f"Response field: {result.get('response', 'EMPTY')[:200]}")
            print(f"Full result: {result}")

if __name__ == "__main__":
    asyncio.run(test_ollama())
