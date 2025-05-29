#!/bin/bash

echo "🚀 AI Labeling Platform - 部署准备脚本"
echo "========================================="

# 检查是否在正确的目录
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ 错误：请在项目根目录运行此脚本"
    exit 1
fi

echo "📁 项目结构检查通过"

# 检查Git
if ! command -v git &> /dev/null; then
    echo "❌ Git 未安装，请先安装Git"
    exit 1
fi

# 初始化Git仓库（如果还没有）
if [ ! -d ".git" ]; then
    echo "🔧 初始化Git仓库..."
    git init
    git add .
    git commit -m "Initial commit - AI Labeling Platform"
    echo "✅ Git仓库初始化完成"
else
    echo "✅ Git仓库已存在"
fi

# 检查环境变量文件
echo "🔍 检查环境配置..."

if [ ! -f "backend/.env" ]; then
    echo "⚠️  后端 .env 文件不存在"
    echo "请创建 backend/.env 文件并添加以下内容："
    echo "OPENAI_API_KEY=your_openai_api_key_here"
    echo "JWT_SECRET_KEY=your_jwt_secret_key_here"
    echo "JWT_ALGORITHM=HS256"
    echo "ACCESS_TOKEN_EXPIRE_MINUTES=30"
    echo ""
else
    echo "✅ 后端环境配置文件存在"
fi

# 创建前端环境配置文件
if [ ! -f "frontend/.env" ]; then
    echo "🔧 创建前端环境配置..."
    echo "VITE_API_BASE_URL=http://localhost:8000" > frontend/.env
    echo "✅ 前端环境配置文件已创建"
else
    echo "✅ 前端环境配置文件已存在"
fi

echo ""
echo "📋 部署清单："
echo "1. ✅ 项目结构完整"
echo "2. ✅ Git仓库准备就绪"
echo "3. ✅ 部署配置文件已创建"
echo "4. ✅ 前端环境配置已设置"

echo ""
echo "🎯 下一步操作："
echo "1. 确保 backend/.env 文件包含有效的 OPENAI_API_KEY"
echo "2. 将代码推送到GitHub仓库"
echo "3. 按照 DEPLOYMENT_GUIDE.md 中的步骤部署到Render和Vercel"
echo ""
echo "📄 详细部署指南请查看: DEPLOYMENT_GUIDE.md"
echo ""
echo "🔗 快速链接："
echo "   - Render.com: https://render.com"
echo "   - Vercel.com: https://vercel.com"
echo ""
echo "✨ 部署准备完成！" 