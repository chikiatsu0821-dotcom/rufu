#!/usr/bin/env bash
# rufu Forge サーバー管理ツール。 ./mc help で使い方を表示
set -euo pipefail
cd "$(dirname "$0")"

DATA=data
MODS=mods
EXPORTS=exports

die()  { echo "エラー: $*" >&2; exit 1; }
info() { echo "==> $*"; }

need_env() { [ -f .env ] || die ".env がありません。先に ./mc setup を実行してください"; }
env_get() { grep -E "^$1=" .env 2>/dev/null | tail -n1 | cut -d= -f2- || true; }
env_set() {
  if grep -qE "^$1=" .env; then
    local tmp; tmp="$(mktemp)"
    awk -v k="$1" -v v="$2" 'BEGIN{FS=OFS="="} $1==k{print k"="v; next} {print}' .env >"$tmp"
    cat "$tmp" >.env; rm -f "$tmp"
  else
    echo "$1=$2" >>.env
  fi
}
running() { [ -n "$(docker compose ps -q --status running minecraft 2>/dev/null)" ]; }
current_world() { local l; l="$(env_get LEVEL)"; echo "${l:-world}"; }
valid_name() { [[ "$1" =~ ^[A-Za-z0-9_.-]+$ ]] && [ "$1" != "." ] && [ "$1" != ".." ] || die "名前に使えるのは英数字と _ . - だけです: $1"; }
confirm() { read -r -p "$1 [y/N] " a; [[ "$a" =~ ^[Yy]$ ]]; }
apply() {  # 設定変更を反映（起動中なら再作成）
  if running; then info "サーバーを再起動して反映します…"; docker compose up -d; else info "次回 ./mc start で反映されます"; fi
}

unzip_to() {  # unzip_to <zip> <dir>
  if command -v unzip >/dev/null; then unzip -q "$1" -d "$2"
  elif command -v python3 >/dev/null; then python3 -m zipfile -e "$1" "$2"
  else die "unzip か python3 をインストールしてください"; fi
}
zip_dir() {  # zip_dir <out.zip> <parent> <name>
  local out; out="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
  if command -v zip >/dev/null; then (cd "$2" && zip -qr "$out" "$3")
  elif command -v python3 >/dev/null; then (cd "$2" && python3 -m zipfile -c "$out" "$3")
  else die "zip か python3 をインストールしてください"; fi
}

# ---------------------------------------------------------------- 基本操作
cmd_setup() {
  command -v docker >/dev/null || die "Docker が見つかりません。https://docs.docker.com/engine/install/ からインストールしてください"
  if [ -f .env ]; then info ".env は既に存在します"; else
    cp .env.example .env
    env_set RCON_PASSWORD "$(LC_ALL=C tr -dc 'A-Za-z0-9' </dev/urandom | head -c 24)"
    info ".env を作成しました（RCON パスワードは自動生成）"
  fi
  if [ "$(env_get EULA)" != "TRUE" ]; then
    if confirm "Minecraft EULA (https://aka.ms/MinecraftEULA) に同意しますか?"; then env_set EULA TRUE
    else echo "同意しないと起動できません。後で .env の EULA=TRUE を設定してください"; fi
  fi
  mkdir -p "$DATA" "$MODS" config backups "$EXPORTS"
  echo "次に .env の WHITELIST / OPS を編集し、./mc start で起動してください"
}
cmd_start()   { need_env; docker compose up -d; info "起動中… ./mc logs で様子を確認できます（初回は Forge のインストールで数分かかります）"; }
cmd_stop()    { docker compose down; }
cmd_restart() { need_env; docker compose restart minecraft; }
cmd_logs()    { docker compose logs -f --tail 100 minecraft; }
cmd_console() { running || die "サーバーが起動していません"; docker compose exec minecraft rcon-cli "$@"; }
cmd_status() {
  need_env
  echo "Minecraft : $(env_get MC_VERSION) / Forge: $(env_get FORGE_VERSION | sed 's/^$/推奨版(自動)/')"
  echo "ワールド  : $(current_world)"
  echo "Mod 数    : $(find "$MODS" -maxdepth 1 -name '*.jar' 2>/dev/null | wc -l | tr -d ' ')"
  if running; then echo "状態      : 起動中"; docker compose exec -T minecraft rcon-cli list 2>/dev/null || true
  else echo "状態      : 停止中"; fi
}
cmd_update() { docker compose pull && apply; }

# ---------------------------------------------------------------- Mod
cmd_mod() {
  local sub="${1:-list}"; shift || true
  mkdir -p "$MODS"
  case "$sub" in
    list|ls)
      local n=0
      while IFS= read -r f; do
        n=$((n+1)); printf '%3d  %-60s %s\n' "$n" "$(basename "$f")" "$(du -h "$f" | cut -f1)"
      done < <(find "$MODS" -maxdepth 1 \( -name '*.jar' -o -name '*.jar.disabled' \) | sort)
      [ "$n" -gt 0 ] || echo "Mod は入っていません（./mc mod add <ファイル or URL>）"
      local mr; mr="$(env_get MODRINTH_PROJECTS)"; [ -z "$mr" ] || echo "Modrinth 自動取得: $mr" ;;
    add)
      [ $# -gt 0 ] || die "使い方: ./mc mod add <jarファイル or URL> ..."
      for src in "$@"; do
        if [[ "$src" =~ ^https?:// ]]; then
          local name; name="$(basename "${src%%\?*}")"; [[ "$name" == *.jar ]] || name="${name}.jar"
          curl -fL --progress-bar -o "$MODS/$name" "$src" || die "ダウンロード失敗: $src"
          info "追加: $name"
        else
          [ -f "$src" ] || die "ファイルがありません: $src"
          [[ "$src" == *.jar ]] || die "Mod は .jar ファイルです: $src"
          cp "$src" "$MODS/"; info "追加: $(basename "$src")"
        fi
      done
      apply ;;
    modrinth)
      [ $# -gt 0 ] || die "使い方: ./mc mod modrinth <プロジェクト名> ...  (例: jei journeymap)"
      local cur; cur="$(env_get MODRINTH_PROJECTS)"
      for p in "$@"; do
        if [[ ",$cur," == *",$p,"* ]]; then echo "既に登録済み: $p"; else cur="${cur:+$cur,}$p"; info "登録: $p"; fi
      done
      env_set MODRINTH_PROJECTS "$cur"; apply ;;
    remove|rm)
      [ $# -gt 0 ] || die "使い方: ./mc mod remove <名前の一部 or 番号>"
      local f; f="$(find_mod "$1")"
      confirm "$(basename "$f") を削除しますか?" || exit 0
      rm -f "$f"; info "削除しました"
      echo "※ Modrinth 登録分は .env の MODRINTH_PROJECTS からも消してください"
      apply ;;
    disable)
      local f; f="$(find_mod "${1:?使い方: ./mc mod disable <名前の一部 or 番号>}")"
      [[ "$f" == *.disabled ]] && die "既に無効です"
      mv "$f" "$f.disabled"; info "無効化: $(basename "$f")"; apply ;;
    enable)
      local f; f="$(find_mod "${1:?使い方: ./mc mod enable <名前の一部 or 番号>}")"
      [[ "$f" == *.disabled ]] || die "無効化されていません"
      mv "$f" "${f%.disabled}"; info "有効化: $(basename "${f%.disabled}")"; apply ;;
    pack)
      mkdir -p "$EXPORTS"
      local out; out="$EXPORTS/client-mods-$(date +%Y%m%d).zip"; rm -f "$out"
      local tmp; tmp="$(mktemp -d)"; mkdir "$tmp/mods"
      find "$MODS" -maxdepth 1 -name '*.jar' -exec cp {} "$tmp/mods/" \;
      zip_dir "$out" "$tmp" mods; rm -rf "$tmp"
      info "作成: $out"
      echo "参加者は Forge $(env_get MC_VERSION) をインストールし、この zip の中身を .minecraft/mods に入れてください" ;;
    *) die "不明なサブコマンド: mod $sub（./mc help 参照）" ;;
  esac
}
find_mod() {
  local key="$1" list; list="$(find "$MODS" -maxdepth 1 \( -name '*.jar' -o -name '*.jar.disabled' \) | sort)"
  if [[ "$key" =~ ^[0-9]+$ ]]; then
    local f; f="$(sed -n "${key}p" <<<"$list")"; [ -n "$f" ] || die "番号 $key の Mod はありません"; echo "$f"; return
  fi
  local m; m="$(grep -iF -- "$key" <<<"$list" || true)"
  [ -n "$m" ] || die "一致する Mod がありません: $key"
  [ "$(wc -l <<<"$m")" -eq 1 ] || { echo "$m" >&2; die "複数一致しました。番号で指定してください"; }
  echo "$m"
}

# ---------------------------------------------------------------- ワールド
worlds() { find "$DATA" -mindepth 2 -maxdepth 2 -name level.dat 2>/dev/null | xargs -r -n1 dirname | xargs -r -n1 basename | sort; }

cmd_world() {
  local sub="${1:-list}"; shift || true
  need_env; mkdir -p "$DATA"
  case "$sub" in
    list|ls)
      local cur; cur="$(current_world)" found=0
      while IFS= read -r w; do
        [ -n "$w" ] || continue; found=1
        printf '%s %-30s %s\n' "$([ "$w" = "$cur" ] && echo '*' || echo ' ')" "$w" "$(du -sh "$DATA/$w" | cut -f1)"
      done <<<"$(worlds)"
      [ "$found" = 1 ] || echo "ワールドはまだありません（初回起動時に '$cur' が作られます）"
      echo "(* = 現在のワールド)" ;;
    new)
      local name="${1:?使い方: ./mc world new <名前> [シード]}" seed="${2:-}"; valid_name "$name"
      [ ! -e "$DATA/$name" ] || die "既に存在します: $name"
      env_set LEVEL "$name"; env_set SEED "$seed"
      info "新しいワールド '$name' に切り替えました${seed:+（シード: $seed）}"; apply ;;
    switch|use)
      local name="${1:?使い方: ./mc world switch <名前>}"; valid_name "$name"
      [ -f "$DATA/$name/level.dat" ] || die "ワールドがありません: $name（./mc world list で確認）"
      env_set LEVEL "$name"; info "ワールドを '$name' に切り替えました"; apply ;;
    import)
      local src="${1:?使い方: ./mc world import <zip or フォルダ> [名前]}" name="${2:-}"
      local tmp; tmp="$(mktemp -d)"
      if [ -d "$src" ]; then cp -r "$src" "$tmp/"
      elif [ -f "$src" ]; then unzip_to "$src" "$tmp"
      else rm -rf "$tmp"; die "見つかりません: $src"; fi
      local lvl; lvl="$(find "$tmp" -name level.dat -not -path '*/DIM*' | awk '{print length, $0}' | sort -n | head -n1 | cut -d' ' -f2-)"
      [ -n "$lvl" ] || { rm -rf "$tmp"; die "level.dat が見つかりません。Minecraft のワールドではないようです"; }
      local dir; dir="$(dirname "$lvl")"
      [ -n "$name" ] || name="$(basename "$dir")"; [ "$name" != "$(basename "$tmp")" ] || name="$(basename "${src%.zip}")"
      name="$(tr -c 'A-Za-z0-9_.\n-' '_' <<<"$name")"; valid_name "$name"
      [ ! -e "$DATA/$name" ] || { rm -rf "$tmp"; die "既に存在します: $name（別名を2つ目の引数で指定）"; }
      mv "$dir" "$DATA/$name"; rm -rf "$tmp"
      info "インポート: $name（使うには ./mc world switch $name）" ;;
    export)
      local name="${1:-$(current_world)}"; valid_name "$name"
      [ -d "$DATA/$name" ] || die "ワールドがありません: $name"
      [ "$name" != "$(current_world)" ] || ! running || cmd_console save-all flush >/dev/null
      mkdir -p "$EXPORTS"; local out; out="$EXPORTS/$name-$(date +%Y%m%d-%H%M).zip"
      zip_dir "$out" "$DATA" "$name"; info "エクスポート: $out（シングルプレイの saves フォルダに展開して遊べます）" ;;
    copy|cp)
      local from="${1:?使い方: ./mc world copy <元> <新しい名前>}" to="${2:?使い方: ./mc world copy <元> <新しい名前>}"
      valid_name "$from"; valid_name "$to"
      [ -d "$DATA/$from" ] || die "ワールドがありません: $from"; [ ! -e "$DATA/$to" ] || die "既に存在します: $to"
      [ "$from" != "$(current_world)" ] || ! running || cmd_console save-all flush >/dev/null
      cp -a "$DATA/$from" "$DATA/$to"; info "コピー: $from -> $to" ;;
    delete|rm)
      local name="${1:?使い方: ./mc world delete <名前>}"; valid_name "$name"
      [ -d "$DATA/$name" ] || die "ワールドがありません: $name"
      [ "$name" != "$(current_world)" ] || die "使用中のワールドは削除できません。先に別のワールドへ切り替えてください"
      confirm "ワールド '$name' を完全に削除しますか?（元に戻せません）" || exit 0
      rm -rf "${DATA:?}/$name"; info "削除しました" ;;
    *) die "不明なサブコマンド: world $sub（./mc help 参照）" ;;
  esac
}

# ---------------------------------------------------------------- バックアップ
cmd_backup() {
  local sub="${1:-now}"; shift || true
  case "$sub" in
    now)  running || die "サーバーが起動していません"; docker compose exec backup backup now; info "backups/ に保存しました" ;;
    list|ls) ls -lh backups/ 2>/dev/null || echo "バックアップはまだありません" ;;
    restore)
      local f="${1:?使い方: ./mc backup restore backups/<ファイル>}"; [ -f "$f" ] || die "ファイルがありません: $f"
      confirm "サーバーを停止し、$f で現在のデータを上書きしますか?" || exit 0
      docker compose down
      case "$f" in *.tgz|*.tar.gz) tar -xzf "$f" -C "$DATA" ;; *.zip) unzip_to "$f" "$DATA" ;; *) die "対応していない形式です: $f" ;; esac
      info "復元しました。./mc start で起動してください" ;;
    *) die "不明なサブコマンド: backup $sub" ;;
  esac
}

cmd_help() {
  cat <<'EOF'
rufu Forge サーバー管理ツール

基本:
  ./mc setup                  初回セットアップ（.env 作成・EULA 同意）
  ./mc start | stop | restart 起動 / 停止 / 再起動
  ./mc status                 状態・ワールド・Mod 数・接続中プレイヤー
  ./mc logs                   ログを表示（Ctrl+C で終了）
  ./mc console [コマンド]     サーバーコマンド実行（引数なしで対話モード）
  ./mc update                 サーバーイメージを最新化

Mod:
  ./mc mod list               Mod 一覧（番号付き）
  ./mc mod add <jar|URL>...   Mod を追加（ファイル or ダウンロード URL）
  ./mc mod modrinth <名前>... Modrinth から自動取得する Mod を登録（依存 Mod も自動）
  ./mc mod remove <名前|番号> Mod を削除
  ./mc mod disable <名前|番号> 一時的に無効化 / enable で戻す
  ./mc mod pack               参加者配布用の mods zip を exports/ に作成

ワールド:
  ./mc world list             ワールド一覧（* が使用中）
  ./mc world new <名前> [シード]  新しいワールドを作って切り替え
  ./mc world switch <名前>    ワールドを切り替え
  ./mc world import <zip|フォルダ> [名前]  シングルプレイ等のワールドを取り込み
  ./mc world export [名前]    ワールドを zip で exports/ に書き出し
  ./mc world copy <元> <新>   ワールドを複製
  ./mc world delete <名前>    ワールドを削除

バックアップ:
  ./mc backup [now]           今すぐバックアップ
  ./mc backup list            バックアップ一覧
  ./mc backup restore <file>  バックアップから復元
EOF
}

cmd="${1:-help}"; shift || true
case "$cmd" in
  setup|start|stop|restart|logs|console|status|update|mod|world|backup|help) "cmd_$cmd" "$@" ;;
  -h|--help) cmd_help ;;
  *) die "不明なコマンド: $cmd（./mc help 参照）" ;;
esac
