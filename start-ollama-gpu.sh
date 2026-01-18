#!/bin/bash

# Ollama GPU Setup Script for RTX 5050

echo "🚀 Starting Ollama with GPU acceleration..."

# Set CUDA environment variables
export CUDA_VISIBLE_DEVICES=0
export OLLAMA_NUM_GPU=1

# Start Ollama server
ollama serve &

# Wait for Ollama to start
sleep 5

# Pull and run the model
echo "📥 Pulling mistral:7b model..."
ollama pull mistral:7b

echo "✅ Ollama is ready on http://localhost:11434"
echo "Model: mistral:7b (7B parameters - optimized for 8GB GPU)"

# Keep the process running
wait
