#!/usr/bin/env bash
# Cài skill viet-nhu-nguoi cho Claude Code (cấp người dùng) bằng symlink.
# Dùng: bash install.sh            -> ~/.claude/skills/viet-nhu-nguoi
#       bash install.sh --copy     -> chép file thay vì symlink
#       bash install.sh --update   -> thay bản đã cài bằng bản này (dùng kèm --copy được)
set -euo pipefail

USAGE='Dùng: bash install.sh [--copy] [--update]'
COPY=0
UPDATE=0
for arg in "$@"; do
  case "$arg" in
    --copy) COPY=1 ;;
    --update) UPDATE=1 ;;
    -h|--help) echo "$USAGE"; exit 0 ;;
    *) echo "$USAGE" >&2; exit 2 ;;
  esac
done

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills/viet-nhu-nguoi"
DEST="${HOME}/.claude/skills/viet-nhu-nguoi"

mkdir -p "$(dirname "$DEST")"
if [ -e "$DEST" ] || [ -L "$DEST" ]; then
  if (( ! UPDATE )); then
    echo "Đã có $DEST, bỏ qua. Chạy lại với --update để thay bằng bản này." >&2
    exit 1
  fi
  if [ -L "$DEST" ]; then
    rm "$DEST"
  elif [ -f "$DEST/SKILL.md" ] && grep -q '^name: viet-nhu-nguoi' "$DEST/SKILL.md"; then
    rm -rf "$DEST"
  else
    echo "$DEST không giống thư mục skill viet-nhu-nguoi, không dám xóa. Hãy tự kiểm tra." >&2
    exit 1
  fi
fi

if (( COPY )); then
  cp -r "$SRC" "$DEST"
else
  ln -s "$SRC" "$DEST"
fi
echo "Đã cài: $DEST"
echo "Mở phiên Claude Code mới rồi gõ /viet-nhu-nguoi"
