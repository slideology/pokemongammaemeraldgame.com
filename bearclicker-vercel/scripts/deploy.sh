#!/bin/bash

# 部署脚本
# 用于将项目部署到Vercel平台

# 设置错误时退出
set -e

# 项目路径
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.."
cd "$PROJECT_DIR"

echo "=== 开始部署Bear Clicker Vercel项目 ==="

# 更新游戏配置
echo "正在更新游戏配置..."
node scripts/update-config.js

# 运行测试
echo "正在运行测试..."
npm test

# 部署到Vercel
echo "正在部署到Vercel..."
npx vercel --prod

echo "=== 部署完成 ==="
