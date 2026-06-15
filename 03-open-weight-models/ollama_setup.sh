#!/bin/bash
set -e
echo "═══════════════════════════════════════════"
echo "  Pulling open-weight models..."
echo "═══════════════════════════════════════════"

echo ""
echo "📦 Pulling Llama 3.2 3B..."
ollama pull llama3.2:3b

echo ""
echo "📦 Pulling Qwen 2.5 7B..."
ollama pull phi4-mini

echo ""
echo "═══════════════════════════════════════════"
echo "  ✅ Models ready!"
echo "═══════════════════════════════════════════"
echo ""
ollama list