#!/usr/bin/env bash
# Cài skill vietnamese-humanizer cho Claude Code (cấp người dùng) bằng symlink.
# Dùng: bash install.sh            -> ~/.claude/skills/vietnamese-humanizer
#       bash install.sh --copy     -> chép file thay vì symlink
set -euo pipefail

case "${1:-}" in
  ''|--copy) ;;
  -h|--help) echo 'Dùng: bash install.sh [--copy]'; exit 0 ;;
  *) echo 'Dùng: bash install.sh [--copy]' >&2; exit 2 ;;
esac
if (( $# > 1 )); then
  echo 'Chỉ nhận một tùy chọn --copy.' >&2
  exit 2
fi

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills/vietnamese-humanizer"
DEST="${HOME}/.claude/skills/vietnamese-humanizer"

mkdir -p "$(dirname "$DEST")"
if [ -e "$DEST" ] || [ -L "$DEST" ]; then
  echo "Đã có $DEST, bỏ qua. Xóa nó trước nếu muốn cài lại." >&2
  exit 1
fi

if [ "${1:-}" = "--copy" ]; then
  cp -r "$SRC" "$DEST"
else
  ln -s "$SRC" "$DEST"
fi
echo "Đã cài: $DEST"
echo "Mở phiên Claude Code mới rồi gõ /vietnamese-humanizer"
