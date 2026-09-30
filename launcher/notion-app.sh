#!/usr/bin/env bash
# Notion Native Desktop Launcher
cd /opt/notion-app || exit 1
exec /opt/notion-app/notion /opt/notion-app/resources/app \
    --ozone-platform=x11 \
    --enable-features=TouchpadOverscrollHistoryNavigation \
    --js-flags="--max-old-space-size=4096" \
    --host-resolver-rules="MAP *.notion.com 87.228.47.199, MAP notion.com 87.228.47.199, MAP *.notion.so 87.228.47.199, MAP notion.so 87.228.47.199, MAP *.notionusercontent.com 208.103.161.2, MAP notionusercontent.com 208.103.161.2, MAP *.notion-static.com 208.103.161.2, MAP notion-static.com 208.103.161.2" \
    --disable-features=Vulkan,OpaqueResourceBlocking \
    "$@"
