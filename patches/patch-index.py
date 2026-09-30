#!/usr/bin/env python3
"""
Patcher for Notion desktop on Linux:
1. Patches .webpack/main/index.js:
   - Fixes crash on exit/tab destroy (detachFromWindow)
   - Prevents EventEmitter memory leak warning on powerMonitor
   - Disables Linux auto-updater error spam
   - Removes duplicate hardcoded navIcons injection (if present)
2. Patches config.json in-place:
   - Sets "isAutoUpdaterDisabled": true
"""
import json
import os
import sys


def patch_config(app_dir):
    config_path = os.path.join(app_dir, "config.json")
    if not os.path.exists(config_path):
        return
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        if cfg.get("isAutoUpdaterDisabled") is not True:
            cfg["isAutoUpdaterDisabled"] = True
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=2)
                f.write("\n")
            print("✓ Enabled isAutoUpdaterDisabled in", config_path)
    except Exception as e:
        print("Warning: could not patch config.json:", e)


def patch_index(filepath):
    with open(filepath, "rb") as f:
        data = f.read()

    # 1. Early powerMonitor setMaxListeners
    target_early = b"/*! For license information please see index.js.LICENSE.txt */\n"
    insert_early = b'try{require("electron").powerMonitor.setMaxListeners(100);}catch(e){}\n'
    if insert_early not in data and data.startswith(target_early):
        data = target_early + insert_early + data[len(target_early):]
        print("✓ Injected early powerMonitor.setMaxListeners(100)")

    # 2. navIcons removal
    target1_start = b"\n\n        // Patch navigation icons\n"
    target1_end = b"el.prepend(icon);\n                }\n            }\n        }\n"
    pos1 = data.find(target1_start)
    if pos1 != -1:
        pos1_end = data.find(target1_end, pos1)
        if pos1_end != -1:
            pos1_end += len(target1_end)
            data = data[:pos1] + b"\n" + data[pos1_end:]
            print("✓ Removed duplicate navIcons injection")

    # 3. Safe detachFromWindow
    target2 = b"this.parentWindow.contentView.removeChildView(this.notion)"
    repl2 = b"(()=>{try{if(this.parentWindow&&!this.parentWindow.isDestroyed()&&this.parentWindow.contentView&&this.notion&&!this.notion.isDestroyed?.())this.parentWindow.contentView.removeChildView(this.notion)}catch(e){}})()"
    if target2 in data:
        data = data.replace(target2, repl2)
        print("✓ Patched detachFromWindow crash check")

    # 4. Disable autoUpdater
    target4 = b"function F(){const e=E.Store.getState().app.preferences?.isAutoUpdaterDisabled"
    repl4 = b"function F(){return!0;const e=E.Store.getState().app.preferences?.isAutoUpdaterDisabled"
    if target4 in data:
        data = data.replace(target4, repl4)
        print("✓ Disabled auto-updater checks")

    with open(filepath, "wb") as f:
        f.write(data)
    print("Done patching", filepath)

    # Also patch config.json if located alongside .webpack
    app_dir = os.path.abspath(os.path.join(os.path.dirname(filepath), "..", ".."))
    patch_config(app_dir)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "/opt/notion-app/resources/app/.webpack/main/index.js"
    patch_index(path)
