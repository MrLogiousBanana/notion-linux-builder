package com.notion.android;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.CookieManager;
import android.webkit.WebSettings;
import android.webkit.WebView;
import androidx.activity.OnBackPressedCallback;
import com.getcapacitor.BridgeActivity;
import com.getcapacitor.BridgeWebViewClient;

public class MainActivity extends BridgeActivity {

    private static final String PREFS_NAME = "notion_prefs";
    private static final String KEY_LAST_URL = "last_url";
    private static final String DEFAULT_START_URL = "https://app.notion.com";

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        WebView webView = this.getBridge().getWebView();
        if (webView != null) {
            WebSettings settings = webView.getSettings();

            // 1. Clean User-Agent: strip Android WebView markers ('; wv' and 'Version/4.0 ')
            // and present as Desktop Chrome while keeping the device's genuine Chrome/<version>
            // so Notion serves the full Desktop Client UI and Google OAuth permits in-app login.
            String defaultUa = settings.getUserAgentString();
            if (defaultUa != null) {
                String cleanUa = defaultUa
                    .replace("; wv", "")
                    .replace("Version/4.0 ", "")
                    .replaceAll("\\(Linux; Android [^)]+\\)", "(X11; Linux x86_64)")
                    .replace(" Mobile Safari/", " Safari/");
                settings.setUserAgentString(cleanUa);
            }

            // 2. Storage, Viewport & Cookie Persistence
            settings.setDomStorageEnabled(true);
            settings.setDatabaseEnabled(true);
            settings.setJavaScriptEnabled(true);
            settings.setJavaScriptCanOpenWindowsAutomatically(true);
            settings.setCacheMode(WebSettings.LOAD_DEFAULT);
            settings.setUseWideViewPort(true);
            settings.setSupportZoom(true);
            settings.setBuiltInZoomControls(true);
            settings.setDisplayZoomControls(false);

            CookieManager cookieManager = CookieManager.getInstance();
            cookieManager.setAcceptCookie(true);
            cookieManager.setAcceptThirdPartyCookies(webView, true);

            SharedPreferences prefs = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);

            // 3. Monitor page loads to flush cookies to SQLite and remember the active workspace URL
            this.getBridge().setWebViewClient(new BridgeWebViewClient(this.getBridge()) {
                @Override
                public void onPageFinished(WebView view, String url) {
                    super.onPageFinished(view, url);
                    CookieManager.getInstance().flush();

                    // Save last URL if within user's Notion workspace (excluding login/auth redirects)
                    if (url != null && (url.contains("notion.com") || url.contains("notion.so"))) {
                        if (!url.contains("/login")
                                && !url.contains("/google-auth")
                                && !url.contains("identity.notion.com")
                                && !url.contains("accounts.google")
                                && !url.contains("/logout")) {
                            prefs.edit().putString(KEY_LAST_URL, url).apply();
                        }
                    }
                }
            });

            // 4. Hardware Back Navigation inside Notion history
            getOnBackPressedDispatcher().addCallback(this, new OnBackPressedCallback(true) {
                @Override
                public void handleOnBackPressed() {
                    if (webView.canGoBack()) {
                        webView.goBack();
                    } else {
                        setEnabled(false);
                        getOnBackPressedDispatcher().onBackPressed();
                    }
                }
            });

            // 5. Load deep link intent or restore last visited workspace page
            String targetUrl = DEFAULT_START_URL;
            Intent intent = getIntent();
            if (intent != null && intent.getData() != null) {
                Uri uri = intent.getData();
                String scheme = uri.getScheme();
                if ("notion".equalsIgnoreCase(scheme)) {
                    targetUrl = uri.toString()
                        .replaceFirst("notion://", "https://app.notion.com/")
                        .replaceFirst("notion:", "https://app.notion.com/");
                } else {
                    targetUrl = uri.toString();
                }
            } else {
                String savedUrl = prefs.getString(KEY_LAST_URL, null);
                if (savedUrl != null && !savedUrl.isEmpty()) {
                    targetUrl = savedUrl;
                }
            }

            webView.loadUrl(targetUrl);
        }
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        WebView webView = this.getBridge().getWebView();
        if (webView != null && intent != null && intent.getData() != null) {
            Uri uri = intent.getData();
            String scheme = uri.getScheme();
            String target = uri.toString();
            if ("notion".equalsIgnoreCase(scheme)) {
                target = target
                    .replaceFirst("notion://", "https://app.notion.com/")
                    .replaceFirst("notion:", "https://app.notion.com/");
            }
            webView.loadUrl(target);
        }
    }

    @Override
    public void onResume() {
        super.onResume();
        CookieManager.getInstance().flush();
    }

    @Override
    public void onPause() {
        super.onPause();
        CookieManager.getInstance().flush();
    }

    @Override
    public void onStop() {
        super.onStop();
        CookieManager.getInstance().flush();
    }
}
