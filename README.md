# rufu Minecraft Server

Docker Compose で動く Minecraft（Java 版）サーバーです。
[itzg/minecraft-server](https://github.com/itzg/docker-minecraft-server) イメージを使い、デフォルトは軽量で高性能な **Paper** サーバー。自動バックアップ付き。

## 必要なもの

- Linux / macOS / Windows (WSL2) のマシン、または VPS
- [Docker](https://docs.docker.com/engine/install/) と Docker Compose v2
- メモリ 4GB 以上推奨（`.env` の `MEMORY` で調整）

## 起動手順

```bash
git clone https://github.com/chikiatsu0821-dotcom/rufu.git
cd rufu
./scripts/setup.sh        # .env を作成（EULA 同意・RCON パスワード自動生成）
```

`.env` を開いて `WHITELIST`（参加させるプレイヤー名）と `OPS`（管理者）を設定し、起動します。

```bash
docker compose up -d
docker compose logs -f minecraft   # "Done" と出たら起動完了 (Ctrl+C でログ表示終了)
```

Minecraft から `サーバーのIPアドレス:25565` に接続してください。

## よく使う操作

| やりたいこと | コマンド |
| --- | --- |
| 停止 | `docker compose down` |
| 再起動 | `docker compose restart minecraft` |
| 管理コンソール | `./scripts/console.sh` |
| ホワイトリスト追加 | `./scripts/console.sh whitelist add プレイヤー名` |
| OP 付与 | `./scripts/console.sh op プレイヤー名` |
| 最新版へ更新 | `docker compose pull && docker compose up -d` |

## 設定

`.env` の値を変えて `docker compose up -d` で反映されます。

- `SERVER_TYPE` … `PAPER`（推奨）/ `VANILLA` / `FABRIC` / `FORGE`
- `MC_VERSION` … `LATEST` または `1.21.4` などの固定バージョン
- `DIFFICULTY`, `MODE`, `MAX_PLAYERS`, `MOTD`, `PVP` など … server.properties に自動反映
- 統合版（スマホ・Switch 等）から参加させたい場合は `PLUGINS` 行（Geyser/Floodgate）のコメントを外し、UDP `19132` も開放して `docker-compose.yml` の `ports` に `- "19132:19132/udp"` を追加

その他の環境変数は [itzg/minecraft-server のドキュメント](https://docker-minecraft-server.readthedocs.io/) を参照。

## データとバックアップ

- ワールド・設定: `./data/`
- バックアップ: `./backups/`（`BACKUP_INTERVAL` ごとに自動取得、`PRUNE_BACKUPS_DAYS` 日より古いものは削除）

復元するには、サーバーを停止して `data/world*` を消し、バックアップの tar を `data/` に展開してから起動します。

```bash
docker compose down
tar -xzf backups/<ファイル名>.tgz -C data
docker compose up -d
```

## 外部から接続するには

- ルーター / VPS のファイアウォールで TCP `25565` を開放（自宅回線ならポート転送が必要）
- 自宅で公開したくない場合は [playit.gg](https://playit.gg/) や Tailscale などのトンネルも利用可能
- `ONLINE_MODE=TRUE` と `ENABLE_WHITELIST=TRUE` のままにしておくのが安全です
