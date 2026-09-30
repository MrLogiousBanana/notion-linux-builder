# Notion Desktop Builder & Patcher (Linux & Android)

Единый проект для запуска полноценного десктопного клиента **Notion** на **Linux** (Fedora, Ubuntu, Arch Linux) и **Android** (смартфоны, планшеты, складные устройства).

---

## 🖥️ 1. Linux Desktop (`launcher/`, `patches/`, `desktop/`)

Набор патчей и лаунчер для нативного запуска десктопного приложения Notion на Linux:

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

### Установка на Linux

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

## 📱 2. Android Desktop Client (`android-app/`)

Обёртка на базе **Capacitor 6**, предоставляющая полноценный **десктопный интерфейс Notion** на Android без урезаний мобильной веб-версии:

1. **Полноценный десктопный режим (`MainActivity.java`):**
   * Срезает маркеры Android WebView (`; wv`, `Version/4.0 `) и представляет клиент как десктопный Chrome (`X11; Linux x86_64`), сохраняя реальную версию движка Chromium устройства.
   * Открывает полный десктопный интерфейс Notion (`https://app.notion.com`) без баннеров «Скачайте мобильное приложение» и ограничений мобильной вёрстки.
   * Разрешает вход через **Google OAuth**, **Apple ID** и **Magic Links** прямо внутри приложения без ошибки `403 disallowed_useragent` и без выброса во внешний браузер.
2. **Сохранение сессии и рабочей области:**
   * Принудительная синхронизация cookies в SQLite (`CookieManager.flush()`) при каждом переходе и сворачивании приложения.
   * Автоматическое запоминание последней открытой страницы воркспейса (`last_url`) с фильтрацией промежуточных страниц авторизации (`identity.notion.com`, `/login`, `/google-auth`).
3. **Нативный системный DNS и системные эмодзи:**
   * Работает напрямую через системный DNS Android (включая Private DNS / DoT / VPN).
   * Использует нативные системные эмодзи без сторонних подмен шрифтов.
4. **Официальная адаптивная иконка и тёмный сплэш-экран (`#191919`).**

### Сборка APK из исходников

Готовый `.apk` доступен в разделе **[Releases](../../releases)**. Для самостоятельной сборки:

```bash
cd android-app
npm install
npx cap copy android
cd android
./gradlew assembleDebug
# Готовый пакет: android/app/build/outputs/apk/debug/app-debug.apk
```

---

## ⚖️ Лицензия и отказ от ответственности (Disclaimer)

Код скриптов, патчей и обёртки в данном репозитории распространяется под лицензией **MIT** (см. [LICENSE](LICENSE)).

> **Disclaimer:** Данный проект является неофициальным проектом сообщества для адаптации под Linux и Android и **не связан** с компанией Notion Labs, Inc. Репозиторий не содержит проприетарного исходного кода или серверов Notion. Название и логотип «Notion» являются зарегистрированными товарными знаками Notion Labs, Inc.
