# 💻 MetaIntelligence CLI Command Guide

MetaIntelligence provides a powerful Command Line Interface (CLI) to interact with its advanced AI systems. This guide details the available commands, their options, and practical usage examples.

## 🚀 Getting Started

The main entry point for the CLI is `fetch_llm_v2.py`. While the project structure is being rebranded to `MetaIntelligence`, the executable script name remains `fetch_llm_v2.py` for now.

### Basic Command Structure

```bash
python fetch_llm_v2.py <provider> "<prompt>" [options]
```

**Parameters:**
- `<provider>`: The LLM provider to use (e.g., openai, claude, gemini, ollama, llamacpp, huggingface)
- `"<prompt>"`: The question or task you want the AI to solve

## ✨ Core Commands

### 1. solve Command (Problem Solving)

This is the primary command for getting MetaIntelligence to solve problems using its various reasoning modes.

#### Usage

```bash
python fetch_llm_v2.py <provider> "<prompt>" --mode <mode> [options]
```

#### Mode Choices

MetaIntelligence offers a comprehensive suite of reasoning modes:

| Mode | Target Complexity | Primary Benefit | Use Case |
|------|------------------|-----------------|----------|
| `efficient` | Low | Overthinking Prevention | Quick questions, basic tasks |
| `balanced` | Medium | Optimal Reasoning Quality | Standard analysis, explanations |
| `decomposed` | High | Collapse Prevention & Speed | Complex problem-solving, system design |
| `adaptive` | Auto-detected | Dynamic Optimization | Questions of unknown or mixed complexity |
| `parallel` | All | Best-of-Breed Quality | Mission-critical tasks, maximum quality |
| `quantum_inspired` | All | Holistic, Synthesized Insight | Brainstorming, philosophical questions, strategy |
| `edge` | Low | Lightweight & Fast | Low-resource devices, quick checks |
| `speculative_thought` | All | Exploratory, Rapid Prototyping | Early-stage ideation, multiple perspectives |
| `paper_optimized` | All | Complete Research Integration | Maximum research benefit, benchmarking |

#### Examples

##### Low Complexity (Efficient Mode)
Get a quick, direct answer.
```bash
python fetch_llm_v2.py ollama "What is 2+2?" --mode efficient --model gemma3:latest
```

##### Medium Complexity (Balanced Mode)
For standard analysis and explanations.
```bash
python fetch_llm_v2.py claude "Explain the main causes of climate change." --mode balanced
```

##### High Complexity (Decomposed Mode)
For complex problem-solving and design tasks.
```bash
python fetch_llm_v2.py openai "Design a sustainable urban transportation system considering technical, economic, social, and environmental factors with implementation timeline." --mode decomposed
```

##### Adaptive Mode (Auto-Detection)
Let MetaIntelligence automatically determine the best approach.
```bash
python fetch_llm_v2.py gemini "How might blockchain technology transform healthcare data management?" --mode adaptive
```

##### Quantum-Inspired Mode
For holistic and synthesized insights, e.g., philosophical questions.
```bash
python fetch_llm_v2.py openai "What is the nature of consciousness?" --mode quantum_inspired
```

##### Speculative Thought Mode
For exploratory rapid prototyping and diverse initial ideas.
```bash
python fetch_llm_v2.py ollama "Generate three innovative business ideas for a remote work future." --mode speculative_thought
```

##### Paper Optimized Mode
Applies all research insights for maximum quality.
```bash
python fetch_llm_v2.py ollama "Analyze the limitations of current reasoning models and propose architectural improvements based on complexity science." --mode paper_optimized --model deepseek-r1
```

### 2. RAG (Retrieval-Augmented Generation) Options

Augment your prompts with external knowledge from Wikipedia or local files.

#### Options

- `--rag`: Enable RAG functionality
- `--knowledge-base <path>`: Specify the path to a local knowledge base (e.g., PDF, text file)
- `--wikipedia`: Use Wikipedia as the knowledge source

#### Examples

##### Wikipedia Integration
```bash
python fetch_llm_v2.py openai "What were the key findings of the LIGO experiment?" --mode balanced --wikipedia
```

##### Local Knowledge Base
```bash
# Assuming 'my_report.pdf' exists in your current directory
python fetch_llm_v2.py claude "Summarize the challenges of renewable energy adoption from this report." --mode balanced --rag --knowledge-base my_report.pdf
```

### 3. System Management & Diagnostic Commands

These commands help you understand the system's status, capabilities, and troubleshoot issues.

#### Available Commands

##### List Providers
Displays all available standard and enhanced V2 LLM providers.
```bash
python fetch_llm_v2.py --list-providers
```

##### System Status
Provides an overview of the MetaIntelligence system's current state, including available providers and V2 modes.
```bash
python fetch_llm_v2.py --system-status
```

##### Health Check
Performs a health check for a specified provider (e.g., API key validity, Ollama server status).
```bash
python fetch_llm_v2.py ollama --health-check
```

##### Troubleshooting Guide
Displays a quick troubleshooting guide for common issues.
```bash
python fetch_llm_v2.py --troubleshooting
```

### 4. General Options

These options can be combined with problem-solving commands.

#### Available Options

- `--model <name>`: Override the default model for the selected provider
- `-f <file_path>` or `--file <file_path>`: Read the prompt from a specified file instead of directly from the command line
- `--system-prompt "<prompt>"`: Provide a system-level instruction or role for the AI
- `--temperature <value>`: Control the randomness of the output (0.0 for deterministic, 1.0 for highly creative)
- `--max-tokens <value>`: Set the maximum number of tokens in the AI's response
- `--json`: Output the response in JSON format, including detailed metadata

#### Examples

##### Specify Model and Temperature
```bash
python fetch_llm_v2.py openai "Write a short poem about AI." --model gpt-4o-mini --temperature 0.8
```

##### Read Prompt from File
```bash
# Assuming 'my_long_prompt.txt' contains your detailed prompt
python fetch_llm_v2.py claude -f my_long_prompt.txt --mode decomposed
```

##### System Prompt for Role-Based Response
```bash
python fetch_llm_v2.py ollama "Explain the concept of quantum superposition." --system-prompt "You are a physics professor explaining to a high school student."
```

##### JSON Output for Scripting
```bash
python fetch_llm_v2.py openai "Summarize machine learning." --json | jq .text
# `jq` is a command-line JSON processor
```

## ⚙️ V2-Specific Options

These options provide fine-grained control over MetaIntelligence's V2 features.

### Available Options

- `--force-v2`: Force the use of V2 enhanced functionalities, even if the mode isn't explicitly a V2-specific one
- `--no-fallback`: Disable the fallback mechanism. If the primary V2 enhanced provider fails, the system will not try the standard provider
- `--no-real-time-adjustment`: Disable dynamic re-evaluation and adjustment of complexity during runtime

### Examples

#### Force V2 Processing
```bash
python fetch_llm_v2.py openai "Simple question" --force-v2 --mode efficient
# Efficient mode normally wouldn't trigger full V2
```

#### Debug Fallback Behavior
```bash
LOG_LEVEL=DEBUG python fetch_llm_v2.py openai "Test failure" --no-fallback --mode adaptive
```

## 🔧 Advanced Configuration

### Environment Variables

Set these in your `.env` file or export them in your shell:

```bash
# API Keys
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_claude_key_here
GOOGLE_API_KEY=your_gemini_key_here

# Logging
LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR

# Default Settings
DEFAULT_PROVIDER=ollama
DEFAULT_MODE=balanced
DEFAULT_MODEL=gemma3:latest

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TIMEOUT=300

# Performance Settings
MAX_CONCURRENT_REQUESTS=5
REQUEST_TIMEOUT=120
```

### Configuration Files

You can also use configuration files for complex setups:

```bash
# Using a custom config file
python fetch_llm_v2.py openai "Your question" --config custom_config.yaml
```

Example `custom_config.yaml`:
```yaml
# Path: /config/custom_config.yaml
providers:
  openai:
    model: "gpt-4o"
    temperature: 0.7
    max_tokens: 2000
  
  ollama:
    model: "llama3.1:70b"
    temperature: 0.5
    
default_settings:
  mode: "balanced"
  enable_rag: false
  enable_v2: true

v2_settings:
  auto_complexity_detection: true
  real_time_adjustment: true
  fallback_enabled: true
```

## 📊 Output Formats

### Standard Output
By default, MetaIntelligence provides clean, formatted text output:

```bash
python fetch_llm_v2.py ollama "Explain quantum computing"
```

### JSON Output
For programmatic use, request JSON format:

```bash
python fetch_llm_v2.py ollama "Explain quantum computing" --json
```

Example JSON structure:
```json
{
  "text": "Quantum computing is a revolutionary computing paradigm...",
  "provider": "ollama",
  "model": "gemma3:latest",
  "mode": "balanced",
  "v2_enhanced": true,
  "metadata": {
    "processing_time": 3.45,
    "token_count": 256,
    "complexity_detected": "medium",
    "confidence_score": 0.92
  },
  "reasoning_trace": [
    "Analyzed prompt complexity",
    "Selected balanced reasoning mode",
    "Applied quantum computing knowledge base"
  ]
}
```

### Verbose Output
For debugging and understanding the reasoning process:

```bash
python fetch_llm_v2.py ollama "Complex question" --verbose --mode decomposed
```

## 🔍 Debugging and Logging

### Enable Debug Logging

```bash
# Set environment variable
export LOG_LEVEL=DEBUG
python fetch_llm_v2.py ollama "Your question"

# Or inline
LOG_LEVEL=DEBUG python fetch_llm_v2.py ollama "Your question"
```

### Log Output Locations

- **Console**: Real-time logging to stdout/stderr
- **File**: Logs saved to `logs/metaintelligence.log`
- **JSON Logs**: Machine-readable logs in `logs/metaintelligence.jsonl`

### Common Debug Scenarios

#### Provider Connection Issues
```bash
LOG_LEVEL=DEBUG python fetch_llm_v2.py ollama --health-check
```

#### V2 Enhancement Debugging
```bash
LOG_LEVEL=DEBUG python fetch_llm_v2.py openai "Test question" --force-v2 --verbose
```

#### RAG System Debugging
```bash
LOG_LEVEL=DEBUG python fetch_llm_v2.py claude "Question about document" --rag --knowledge-base document.pdf --verbose
```

## ⚠️ Troubleshooting Tips

### 1. Ollama Model Not Found/Server Down

**Symptoms**: Connection errors, model not found errors

**Solutions**:
```bash
# Ensure Ollama server is running
ollama serve

# Pull required models
ollama pull gemma3:latest

# Verify available models
ollama list

# Test Ollama connection
python fetch_llm_v2.py ollama --health-check
```

### 2. API Key Errors

**Symptoms**: Authentication failures, 401/403 errors

**Solutions**:
```bash
# Check your .env file for correct API key configurations
cat .env | grep API_KEY

# Verify environment variables are loaded
python -c "import os; print(os.getenv('OPENAI_API_KEY'))"

# Test API key validity
python fetch_llm_v2.py openai --health-check
```

### 3. Connection/Timeout Errors

**Symptoms**: Network timeouts, connection refused

**Solutions**:
```bash
# Check network connectivity
curl -I https://api.openai.com/v1/models

# Increase timeout settings
python fetch_llm_v2.py openai "Question" --timeout 300

# Check proxy settings if applicable
export HTTP_PROXY=your_proxy_url
export HTTPS_PROXY=your_proxy_url
```

### 4. V2 Features Not Working

**Symptoms**: Standard responses instead of enhanced reasoning

**Solutions**:
```bash
# Check V2 system status
python fetch_llm_v2.py --system-status

# Force V2 enhancement
python fetch_llm_v2.py openai "Question" --force-v2

# Enable debug logging to trace V2 activation
LOG_LEVEL=DEBUG python fetch_llm_v2.py openai "Question" --mode decomposed
```

### 5. Memory Issues

**Symptoms**: Out of memory errors, slow performance

**Solutions**:
```bash
# Use lightweight edge mode
python fetch_llm_v2.py ollama "Question" --mode edge

# Reduce token limits
python fetch_llm_v2.py ollama "Question" --max-tokens 500

# Use smaller models
python fetch_llm_v2.py ollama "Question" --model gemma3:2b
```

### 6. File Processing Issues

**Symptoms**: RAG not working, file reading errors

**Solutions**:
```bash
# Verify file exists and is readable
ls -la your_document.pdf

# Test file processing
python fetch_llm_v2.py claude "Test" --rag --knowledge-base your_document.pdf --verbose

# Check supported file formats
python fetch_llm_v2.py --help | grep -A 10 "knowledge-base"
```

## 📋 Quick Reference Commands

### Essential Commands
```bash
# Basic question
python fetch_llm_v2.py ollama "Your question"

# Complex analysis
python fetch_llm_v2.py openai "Complex problem" --mode decomposed

# With external knowledge
python fetch_llm_v2.py claude "Question about topic" --wikipedia

# System diagnostics
python fetch_llm_v2.py --system-status
python fetch_llm_v2.py ollama --health-check
```

### One-Liner Examples
```bash
# Quick fact check
python fetch_llm_v2.py ollama "What's the capital of Japan?" --mode efficient

# Creative writing
python fetch_llm_v2.py openai "Write a haiku about AI" --temperature 0.9

# Technical analysis
python fetch_llm_v2.py claude "Analyze this code: print('hello')" --mode balanced

# Research synthesis
python fetch_llm_v2.py openai "Summarize recent AI developments" --wikipedia --mode paper_optimized
```

## 🎯 Best Practices

### 1. Choose the Right Mode
- Use `efficient` for simple, factual questions
- Use `balanced` for general analysis and explanations
- Use `decomposed` for complex, multi-step problems
- Use `adaptive` when unsure about complexity
- Use `quantum_inspired` for creative or philosophical tasks

### 2. Optimize Performance
- Start with local models (Ollama) for development
- Use cloud APIs (OpenAI, Claude) for production
- Enable V2 features for complex reasoning tasks
- Use appropriate temperature settings (0.0-0.3 for factual, 0.7-1.0 for creative)

### 3. Effective Prompting
- Be specific and clear in your questions
- Provide context when relevant
- Use system prompts to define roles and constraints
- Break complex problems into smaller parts

### 4. Error Prevention
- Always test API keys with health checks
- Verify file paths before using RAG
- Use verbose mode for debugging
- Set appropriate timeouts for long-running tasks

For comprehensive troubleshooting, run:
```bash
python fetch_llm_v2.py --troubleshooting
```