# rufu Forge Server

Docker で動く **Forge（Mod 対応）** の Minecraft サーバーです。
付属の `./mc` コマンドで **Mod・ワールド・バックアップ** を簡単に管理できます。

## 必要なもの

- Linux / macOS / Windows (WSL2) のマシン、または VPS
- [Docker](https://docs.docker.com/engine/install/)（Docker Compose v2 付き）
- メモリ 8GB 以上のマシン推奨（サーバーには `.env` の `MEMORY`、初期値 6G を割り当て）

## はじめかた

```bash
git clone https://github.com/chikiatsu0821-dotcom/rufu.git
cd rufu
./mc setup      # .env 作成・EULA 同意（パスワードは自動生成）
```

`.env` を開いて `WHITELIST`（参加させるプレイヤー名）と `OPS`（管理者）を書いたら起動します。

```bash
./mc start
./mc logs       # "Done" と出たら起動完了（初回は Forge のインストールで数分かかります）
```

Minecraft から `サーバーのIP:25565` に接続します。
**参加者のパソコンにも同じバージョンの Forge と、同じ Mod が必要です**（`./mc mod pack` 参照）。

## コマンド一覧（`./mc help` でも表示）

### 基本
| コマンド | 内容 |
| --- | --- |
| `./mc start` / `stop` / `restart` | 起動 / 停止 / 再起動 |
| `./mc status` | バージョン・ワールド・Mod 数・接続中プレイヤー |
| `./mc logs` | ログ表示（Ctrl+C で終了） |
| `./mc console` | サーバーコマンドを打てる対話モード（例: `./mc console op Steve`） |
| `./mc update` | サーバーを最新イメージに更新 |

### Mod
| コマンド | 内容 |
| --- | --- |
| `./mc mod list` | 入っている Mod の一覧（番号付き） |
| `./mc mod add <jar or URL>` | Mod を追加（ダウンロードした jar、または直リンク URL） |
| `./mc mod modrinth jei journeymap` | [Modrinth](https://modrinth.com/mods?g=categories:forge) の Mod を名前で登録。依存 Mod も含め自動ダウンロード |
| `./mc mod remove <名前の一部 or 番号>` | Mod を削除 |
| `./mc mod disable` / `enable <名前 or 番号>` | 削除せずに一時的に無効化 / 元に戻す |
| `./mc mod pack` | 参加者に配る mods の zip を `exports/` に作成 |

Mod の jar は `mods/` フォルダに直接置いても OK です。Mod の設定ファイルは `config/` にあります。
変更はサーバー起動中なら自動で再起動して反映されます。

### ワールド
| コマンド | 内容 |
| --- | --- |
| `./mc world list` | ワールド一覧（`*` が使用中） |
| `./mc world new <名前> [シード]` | 新しいワールドを作って切り替え |
| `./mc world switch <名前>` | 別のワールドに切り替え |
| `./mc world import <zip or フォルダ> [名前]` | シングルプレイや配布ワールドを取り込み |
| `./mc world export [名前]` | ワールドを zip で `exports/` に書き出し（シングルで遊べる） |
| `./mc world copy <元> <新しい名前>` | ワールドを複製 |
| `./mc world delete <名前>` | ワールドを削除（使用中のものは不可） |

ワールドは `data/<ワールド名>/` に保存されます。

### バックアップ
| コマンド | 内容 |
| --- | --- |
| `./mc backup` | 今すぐバックアップ |
| `./mc backup list` | バックアップ一覧 |
| `./mc backup restore backups/<ファイル>` | バックアップから復元 |

自動バックアップは `BACKUP_INTERVAL`（初期値 6 時間）ごとに `backups/` へ保存され、`PRUNE_BACKUPS_DAYS` 日（初期値 7 日）より古いものは削除されます。
※ Mod の jar 自体はバックアップに含まれません。`mods/` は別途保管するか Modrinth 登録を使ってください。

## バージョンの変更

`.env` で指定します。

- `MC_VERSION` … Minecraft のバージョン（初期値 `1.20.1`：Forge Mod が最も多い）
- `FORGE_VERSION` … 空なら推奨版を自動選択
- 1.20.5 以降を使う場合は `docker-compose.yml` の `image` を `itzg/minecraft-server:java21` に変更

**バージョンを変えると Mod も対応版に入れ替えが必要です。既存ワールドを下げるのは不可**なので、変更前に `./mc world export` しておくと安全です。

## 参加者（遊ぶ人）側の準備

1. [Forge 公式](https://files.minecraftforge.net/) からサーバーと同じバージョンのインストーラーを入れる
2. 管理者から `./mc mod pack` で作った zip をもらい、中の jar を `.minecraft/mods/` に入れる
3. Forge のプロファイルで起動し、サーバーに接続

## 外部から接続するには

- ルーター / VPS のファイアウォールで TCP `25565` を開放（自宅回線ならポート転送が必要）
- 公開したくない場合は [playit.gg](https://playit.gg/) や Tailscale なども利用可能
- `ONLINE_MODE=TRUE` と `ENABLE_WHITELIST=TRUE` のままにしておくのが安全です

## うまくいかないとき

- 起動しない → `./mc logs` でエラーを確認。Mod のバージョン違い・前提 Mod 不足が多いです（`./mc mod disable` で原因を切り分け）
- `Permission denied` → `data/` はコンテナ内ユーザーの所有になるため、`sudo ./mc ...` で実行
- 重い → `.env` の `MEMORY` を増やす / `VIEW_DISTANCE` を下げる
