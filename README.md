# Notion Linux Native Repack & Builder

Набор конфигураций, патчей и лаунчера для нативного запуска официального десктопного Notion под Linux (Fedora / Ubuntu / Arch).

## Особенности
1. **Обход блокировок и ускорение без внешнего VPN:**
   Лаунчер использует `--host-resolver-rules` для прямого маппинга IP-адресов Notion (`app.notion.com`, `notion.so`, `file.notion.com` и др.), что исключает сбои DNS и замедления провайдерами.
2. **Патч для Linux-компиляции (`patches/better-sqlite3.patch`):**
   Решает проблему нативного модуля базы данных `better-sqlite3` при распаковке Windows-релиза на Linux.
3. **Нативные жесты и скролл:**
   Включена поддержка `--enable-features=TouchpadOverscrollHistoryNavigation` (навигация вперед/назад свайпом двумя пальцами).
4. **Кастомные ассеты пространств (`assets/custom_assets`):**
   Иконки и баннеры для Personal, Financial, Quiet Space и Workspace.

## Использование
- Поместите `launcher/notion-app.sh` в `/usr/local/bin/notion-app`
- Поместите `desktop/notion.desktop` в `~/.local/share/applications/`
