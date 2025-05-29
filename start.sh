#!/bin/bash

echo "🚀 AI Labeling Platform 启动脚本"
echo "=================================="

# 检查是否在项目根目录
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

echo "📋 启动说明："
echo "1. 这个脚本会给出启动命令，请在不同终端窗口执行"
echo "2. 后端需要在虚拟环境中运行"
echo "3. 前端需要Node.js环境"
echo ""

echo "🔧 第一步：启动后端API"
echo "请在 终端1 中执行："
echo "cd backend"
echo "source /Users/keyi/Library/Caches/pypoetry/virtualenvs/ai-labeling-ueEwKQCn-py3.12/bin/activate"
echo "python -m uvicorn app.main:app --reload --port 8000"
echo ""

echo "🌐 第二步：启动前端应用"
echo "请在 终端2 中执行："
echo "cd frontend"
echo "npm run dev"
echo ""

echo "🌍 第三步：访问应用"
echo "前端地址: http://localhost:3000"
echo "后端API: http://127.0.0.1:8000"
echo "API文档: http://127.0.0.1:8000/docs"
echo ""

echo "🔑 测试账户:"
echo "admin / admin123"
echo "user1 / user123"
echo "demo / demo123"
echo ""

echo "💡 提示："
echo "- 确保OpenAI API密钥已配置在 backend/.env 文件中"
echo "- 如果遇到问题，请查看 STARTUP_GUIDE.md 获取详细指南" 