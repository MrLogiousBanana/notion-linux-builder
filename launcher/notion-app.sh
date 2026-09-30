#!/usr/bin/env bash
# Notion Native Desktop Launcher
cd /opt/notion-app || exit 1
exec /opt/notion-app/notion /opt/notion-app/resources/app \
    --ozone-platform=x11 \
    --enable-features=TouchpadOverscrollHistoryNavigation \
    --js-flags="--max-old-space-size=4096" \
    --disable-features=Vulkan,OpaqueResourceBlocking \
    "$@"
