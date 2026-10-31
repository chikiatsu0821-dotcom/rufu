#!/usr/bin/env bash
# 初回セットアップ: .env を作成し、RCON パスワードを自動生成する
set -euo pipefail
cd "$(dirname "$0")/.."

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker が見つかりません。https://docs.docker.com/engine/install/ からインストールしてください。" >&2
  exit 1
fi

if [ -f .env ]; then
  echo ".env は既に存在します。内容を確認してから 'docker compose up -d' を実行してください。"
  exit 0
fi

cp .env.example .env
pw="$(LC_ALL=C tr -dc 'A-Za-z0-9' </dev/urandom | head -c 24)"
sed -i.bak "s/^RCON_PASSWORD=.*/RCON_PASSWORD=${pw}/" .env && rm -f .env.bak

read -r -p "Minecraft EULA (https://aka.ms/MinecraftEULA) に同意しますか? [y/N] " ans
if [[ "${ans}" =~ ^[Yy]$ ]]; then
  sed -i.bak "s/^EULA=.*/EULA=TRUE/" .env && rm -f .env.bak
else
  echo "EULA に同意しないとサーバーは起動できません。後で .env の EULA=TRUE を設定してください。"
fi

echo ".env を作成しました（RCON パスワードは自動生成済み）。"
echo "WHITELIST / OPS などを編集したら 'docker compose up -d' で起動します。"
