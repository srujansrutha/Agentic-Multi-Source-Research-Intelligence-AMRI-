# GPU Acceleration Setup for AMRI

## Prerequisites
- RTX 5050 GPU (8GB VRAM)
- NVIDIA CUDA Toolkit installed
- Ollama installed

## Installation

### 1. Install NVIDIA CUDA Toolkit
```bash
# For Ubuntu/Debian
sudo apt-get install nvidia-cuda-toolkit

# Verify installation
nvidia-smi
```

### 2. Install Ollama
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 3. Start Ollama with GPU

**Option A: Using the provided script**
```bash
chmod +x start-ollama-gpu.sh
./start-ollama-gpu.sh
```

**Option B: Manual start**
```bash
export CUDA_VISIBLE_DEVICES=0
export OLLAMA_NUM_GPU=1
ollama serve
```

### 4. Pull the Model
In another terminal:
```bash
ollama pull mistral:7b
```

### 5. Start AMRI
```bash
docker-compose up -d
```

## Configuration

The system is configured to use:
- **Model**: mistral:7b (7B parameters - fits in 8GB GPU)
- **GPU**: RTX 5050 (CUDA device 0)
- **Ollama URL**: http://localhost:11434

## Performance Tips

1. **Model Selection**: mistral:7b is optimized for 8GB GPUs
2. **Batch Size**: Automatically optimized by Ollama
3. **GPU Memory**: Monitor with `nvidia-smi`
4. **Temperature**: Set to 0 for deterministic outputs

## Verify GPU Usage

```bash
# Monitor GPU in real-time
watch -n 1 nvidia-smi

# Check Ollama logs
ollama logs
```

## Troubleshooting

**GPU not detected:**
```bash
# Check CUDA availability
nvidia-smi

# Verify Ollama GPU support
ollama list
```

**Out of memory:**
- Reduce model size or use quantized versions
- Check: `ollama list` for available models

**Slow inference:**
- Ensure GPU is being used: `nvidia-smi` during inference
- Check CUDA version compatibility
