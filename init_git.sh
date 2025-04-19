#!/bin/bash
git init
git add .
git commit -m "Initial commit for gs_app"
git branch -M main
echo "请输入你的 GitHub 仓库地址（例如 https://github.com/yourname/gs_app.git）："
read repo
git remote add origin $repo
git push -u origin main
