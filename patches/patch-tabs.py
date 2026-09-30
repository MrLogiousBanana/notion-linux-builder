import sys

def patch_tabs(path):
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    # 1. Start padding fix (stop adding macOS traffic light 80px width on Linux)
    target1 = 'return"win32"===t?(0,r.areLocaleDirectionsAligned)(a)?i:(0,n.getWindowControlsPaddingWin)(s):(0,r.areLocaleDirectionsAligned)(a)?l({paddingType:"start",isFullscreen:o,zoomFactor:s,systemVersion:c}):i'
    repl1 = 'return("win32"===t||"linux"===t)?(0,r.areLocaleDirectionsAligned)(a)?i:(0,n.getWindowControlsPaddingWin)(s):(0,r.areLocaleDirectionsAligned)(a)?l({paddingType:"start",isFullscreen:o,zoomFactor:s,systemVersion:c}):i'
    
    if target1 in code:
        code = code.replace(target1, repl1, 1)
        print("✓ Patched getContentStartPadding for Linux")
    else:
        print("Notice: target1 already patched or not found")

    # 2. boxSizing fix
    target2 = 'boxSizing:"win32"===n?"border-box":void 0'
    repl2 = 'boxSizing:("win32"===n||"linux"===n)?"border-box":void 0'
    if target2 in code:
        code = code.replace(target2, repl2, 1)
        print("✓ Patched boxSizing for Linux")

    # 3. Ctrl shortcut tooltip
    target3 = '"win32"===t.systemPlatform?"Ctrl+\\":'
    repl3 = '("win32"===t.systemPlatform||"linux"===t.systemPlatform)?"Ctrl+\\":'
    if target3 in code:
        code = code.replace(target3, repl3, 1)
        print("✓ Patched sidebar shortcut for Linux")

    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    print("Done patching tabs/index.js")

if __name__ == "__main__":
    patch_tabs(sys.argv[1])
