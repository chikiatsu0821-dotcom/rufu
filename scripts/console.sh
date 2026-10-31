#!/usr/bin/env bash
# サーバーに管理コマンドを送る。引数なしなら対話モード。
#   ./scripts/console.sh                -> 対話コンソール
#   ./scripts/console.sh whitelist add Steve
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose exec minecraft rcon-cli "$@"
