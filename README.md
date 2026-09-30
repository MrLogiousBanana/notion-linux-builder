# Notion Linux Native Builder & Patcher

Набор патчей, скриптов и лаунчера для нативного запуска десктопного приложения **Notion** на Linux (Fedora, Ubuntu, Arch Linux).

---

## ✨ Возможности и исправления

1. **Нативная работа через системный DNS:**
   Лаунчер `launcher/notion-app.sh` использует системный резолвер ОС без жёстко зашитых IP-адресов и прокси-правил.
2. **Исправление вёрстки панели вкладок на Linux (`patches/patch-tabs.py`):**
   Убирает фантомный левый отступ ~80px (остававшийся от macOS traffic-light кнопок в `getContentStartPadding`) и приводит шорткаты вкладок к `Ctrl`.
3. **Исправление стабильности и закрытия окна (`patches/patch-index.py`):**
   * Устраняет падение `TypeError: Object has been destroyed` в `detachFromWindow` при закрытии вкладок и выходе из приложения.
   * Устраняет утечку слушателей `powerMonitor` (`MaxListenersExceededWarning`).
   * Отключает фоновые проверки Windows/AppImage автообновления (`isAutoUpdaterDisabled`).
4. **Патч нативного модуля БД (`patches/better-sqlite3.patch`):**
   Адаптирует сборку `better-sqlite3` при распаковке десктопного релиза на Linux.
5. **Поддержка жестов тачпада и расширенный лимит памяти V8:**
   Включена навигация свайпами двумя пальцами (`TouchpadOverscrollHistoryNavigation`) и увеличен лимит кучи V8 до 4 ГБ (`--max-old-space-size=4096`) для работы с большими базами данных без OOM-падений.

---

## 🚀 Использование

```bash
# 1. Применить патчи к установленному в /opt/notion-app приложению
sudo python3 patches/patch-index.py /opt/notion-app/resources/app/.webpack/main/index.js
sudo python3 patches/patch-tabs.py /opt/notion-app/resources/app/.webpack/renderer/tabs/index.js

# 2. Установить лаунчер и ярлык приложения
sudo cp launcher/notion-app.sh /usr/local/bin/notion-app
sudo chmod +x /usr/local/bin/notion-app
cp desktop/notion.desktop ~/.local/share/applications/
```

---

## ⚖️ Лицензия и отказ от ответственности (Disclaimer)

Код скриптов и патчей в данном репозитории распространяется под лицензией **MIT** (см. [LICENSE](LICENSE)).

> **Disclaimer:** Данный проект является неофициальным набором скриптов сообщества для адаптации под Linux и **не связан** с компанией Notion Labs, Inc. Репозиторий не содержит проприетарного исходного кода или исполняемых файлов Notion. Название и логотип «Notion» являются зарегистрированными товарными знаками Notion Labs, Inc.
