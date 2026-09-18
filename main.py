import sys

from PySide6.QtCore import QUrl, Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTabBar,
    QStackedWidget,
    QToolButton,
    QLineEdit,
    QLabel,
    QDialog,
    QFormLayout,
    QComboBox,
    QDoubleSpinBox,
    QCheckBox,
    QPushButton,
    QGroupBox,
    QMessageBox,
)

from PySide6.QtWebEngineWidgets import QWebEngineView


# ============================================================
# PEGASUS LITEBROWSER
# ============================================================

APP_NAME = "Pegasus LiteBrowser"

HOME_PAGE = "https://search.brave.com"

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 750

DEFAULT_ZOOM = 1.0
MAX_TAB_TITLE_LENGTH = 18


# ============================================================
# WEB VIEW
# ============================================================

class LiteWebView(QWebEngineView):

    def __init__(self, parent=None):
        super().__init__(parent)

        settings = self.settings()

        settings.setAttribute(
            settings.WebAttribute.JavascriptEnabled,
            True
        )

        settings.setAttribute(
            settings.WebAttribute.AutoLoadImages,
            True
        )

        settings.setAttribute(
            settings.WebAttribute.PluginsEnabled,
            False
        )

        settings.setAttribute(
            settings.WebAttribute.FullScreenSupportEnabled,
            False
        )

        settings.setAttribute(
            settings.WebAttribute.PdfViewerEnabled,
            False
        )

        settings.setAttribute(
            settings.WebAttribute.ScreenCaptureEnabled,
            False
        )

        settings.setAttribute(
            settings.WebAttribute.LocalStorageEnabled,
            False
        )

        settings.setAttribute(
            settings.WebAttribute.JavascriptCanOpenWindows,
            False
        )

        settings.setAttribute(
            settings.WebAttribute.JavascriptCanAccessClipboard,
            False
        )

        settings.setAttribute(
            settings.WebAttribute.HyperlinkAuditingEnabled,
            False
        )

        self.setZoomFactor(DEFAULT_ZOOM)


# ============================================================
# SETTINGS DIALOG
# ============================================================

class SettingsDialog(QDialog):

    def __init__(self, browser):
        super().__init__(browser)

        self.browser = browser

        self.setWindowTitle("Pegasus Settings")
        self.setMinimumWidth(430)

        layout = QVBoxLayout(self)

        # ----------------------------------------------------
        # GENERAL
        # ----------------------------------------------------

        general_group = QGroupBox("General")

        general_layout = QFormLayout(general_group)

        self.homepage = QLineEdit(
            browser.home_page
        )

        self.homepage.setPlaceholderText(
            "https://example.com"
        )

        general_layout.addRow(
            "Homepage:",
            self.homepage
        )

        self.search_engine = QComboBox()

        self.search_engine.addItems([
                "Google",
                "Bing",
                "DuckDuckGo",
                "Brave Search"
            ])

        self.search_engine.setCurrentText(
            browser.search_engine
        )

        general_layout.addRow(
            "Search engine:",
            self.search_engine
        )

        layout.addWidget(general_group)

        # ----------------------------------------------------
        # APPEARANCE
        # ----------------------------------------------------

        appearance_group = QGroupBox("Appearance")

        appearance_layout = QFormLayout(
            appearance_group
        )

        self.theme = QComboBox()

        self.theme.addItems([
            "Dark",
            "Light"
        ])

        self.theme.setCurrentText(
            browser.theme
        )

        appearance_layout.addRow(
            "Theme:",
            self.theme
        )

        self.zoom = QDoubleSpinBox()

        self.zoom.setRange(
            0.5,
            3.0
        )

        self.zoom.setSingleStep(
            0.1
        )

        self.zoom.setValue(
            browser.zoom
        )

        self.zoom.setSuffix("x")

        appearance_layout.addRow(
            "Default zoom:",
            self.zoom
        )

        layout.addWidget(
            appearance_group
        )

        # ----------------------------------------------------
        # PRIVACY
        # ----------------------------------------------------

        privacy_group = QGroupBox("Privacy")

        privacy_layout = QVBoxLayout(
            privacy_group
        )

        self.clear_on_exit = QCheckBox(
            "Clear cookies and cache when Pegasus closes"
        )

        self.clear_on_exit.setChecked(
            browser.clear_on_exit
        )

        privacy_layout.addWidget(
            self.clear_on_exit
        )

        self.disable_javascript = QCheckBox(
            "Disable JavaScript"
        )

        self.disable_javascript.setChecked(
            browser.disable_javascript
        )

        privacy_layout.addWidget(
            self.disable_javascript
        )

        layout.addWidget(
            privacy_group
        )

        # ----------------------------------------------------
        # PERFORMANCE
        # ----------------------------------------------------

        performance_group = QGroupBox(
            "Performance"
        )

        performance_layout = QVBoxLayout(
            performance_group
        )

        self.load_images = QCheckBox(
            "Load images"
        )

        self.load_images.setChecked(
            browser.load_images
        )

        performance_layout.addWidget(
            self.load_images
        )

        self.disable_plugins = QCheckBox(
            "Disable browser plugins"
        )

        self.disable_plugins.setChecked(
            browser.disable_plugins
        )

        performance_layout.addWidget(
            self.disable_plugins
        )

        layout.addWidget(
            performance_group
        )

        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        button_layout = QHBoxLayout()

        reset_button = QPushButton(
            "Reset"
        )

        reset_button.clicked.connect(
            self.reset_settings
        )

        cancel_button = QPushButton(
            "Cancel"
        )

        cancel_button.clicked.connect(
            self.reject
        )

        save_button = QPushButton(
            "Save"
        )

        save_button.clicked.connect(
            self.save_settings
        )

        button_layout.addWidget(
            reset_button
        )

        button_layout.addStretch()

        button_layout.addWidget(
            cancel_button
        )

        button_layout.addWidget(
            save_button
        )

        layout.addLayout(
            button_layout
        )

    # ========================================================
    # RESET
    # ========================================================

    def reset_settings(self):

        self.homepage.setText(
            HOME_PAGE
        )

        self.search_engine.setCurrentText(
            "Brave Search"
        )

        self.theme.setCurrentText(
            "Dark"
        )

        self.zoom.setValue(
            1.0
        )

        self.clear_on_exit.setChecked(
            False
        )

        self.disable_javascript.setChecked(
            False
        )

        self.load_images.setChecked(
            True
        )

        self.disable_plugins.setChecked(
            True
        )

    # ========================================================
    # SAVE
    # ========================================================

    def save_settings(self):

        self.browser.home_page = (
            self.homepage.text().strip()
        )

        self.browser.search_engine = (
            self.search_engine.currentText()
        )

        self.browser.theme = (
            self.theme.currentText()
        )

        self.browser.zoom = (
            self.zoom.value()
        )

        self.browser.clear_on_exit = (
            self.clear_on_exit.isChecked()
        )

        self.browser.disable_javascript = (
            self.disable_javascript.isChecked()
        )

        self.browser.load_images = (
            self.load_images.isChecked()
        )

        self.browser.disable_plugins = (
            self.disable_plugins.isChecked()
        )

        # Apply settings to every tab

        for i in range(
            self.browser.tabs.count()
        ):

            view = self.browser.tabs.tabData(i)

            if isinstance(
                view,
                LiteWebView
            ):

                settings = view.settings()

                settings.setAttribute(
                    settings.WebAttribute.JavascriptEnabled,
                    not self.browser.disable_javascript
                )

                settings.setAttribute(
                    settings.WebAttribute.AutoLoadImages,
                    self.browser.load_images
                )

                settings.setAttribute(
                    settings.WebAttribute.PluginsEnabled,
                    not self.browser.disable_plugins
                )

                view.setZoomFactor(
                    self.browser.zoom
                )

        self.browser.apply_theme()

        self.accept()


# ============================================================
# MAIN BROWSER
# ============================================================

class LiteBrowser(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            APP_NAME
        )

        self.resize(
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )

        # ----------------------------------------------------
        # SETTINGS
        # ----------------------------------------------------

        self.home_page = HOME_PAGE

        self.search_engine = "Brave Search"

        self.theme = "Dark"

        self.zoom = DEFAULT_ZOOM

        self.clear_on_exit = False

        self.disable_javascript = False

        self.load_images = True

        self.disable_plugins = True

        # ----------------------------------------------------
        # UI
        # ----------------------------------------------------

        self.setup_ui()

        self.add_tab(
            self.home_page
        )

    # ========================================================
    # UI
    # ========================================================

    def setup_ui(self):

        central = QWidget()

        self.setCentralWidget(
            central
        )

        main_layout = QVBoxLayout(
            central
        )

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        main_layout.setSpacing(
            0
        )

        # ====================================================
        # TABS
        # ====================================================

        self.tabs = QTabBar()

        self.tabs.setExpanding(
            False
        )

        self.tabs.setMovable(
            True
        )

        self.tabs.setTabsClosable(
            True
        )

        self.tabs.setDocumentMode(
            True
        )

        self.tabs.tabCloseRequested.connect(
            self.close_tab
        )

        self.tabs.currentChanged.connect(
            self.change_tab
        )

        main_layout.addWidget(
            self.tabs,
            0
        )

        # ====================================================
        # NAVIGATION BAR
        # ====================================================

        navigation = QWidget()

        navigation.setFixedHeight(
            48
        )

        nav_layout = QHBoxLayout(
            navigation
        )

        nav_layout.setContentsMargins(
            6,
            5,
            6,
            5
        )

        nav_layout.setSpacing(
            4
        )

        # Back

        self.back_button = self.make_button(
            "←"
        )

        self.back_button.clicked.connect(
            self.go_back
        )

        # Forward

        self.forward_button = self.make_button(
            "→"
        )

        self.forward_button.clicked.connect(
            self.go_forward
        )

        # Reload

        self.reload_button = self.make_button(
            "⟳"
        )

        self.reload_button.clicked.connect(
            self.reload
        )

        # Home

        self.home_button = self.make_button(
            "⌂"
        )

        self.home_button.clicked.connect(
            self.go_home
        )

        # URL

        self.url_bar = QLineEdit()

        self.url_bar.setPlaceholderText(
            "Search or enter address..."
        )

        self.url_bar.returnPressed.connect(
            self.navigate
        )

        # Privacy

        self.privacy_button = self.make_button(
            "🛡"
        )

        self.privacy_button.clicked.connect(
            self.clear_privacy
        )

        # Settings

        self.settings_button = self.make_button(
            "⚙"
        )

        self.settings_button.clicked.connect(
            self.open_settings
        )

        # New tab

        self.new_tab_button = self.make_button(
            "+"
        )

        self.new_tab_button.clicked.connect(
            lambda: self.add_tab(
                self.home_page
            )
        )

        # ----------------------------------------------------
        # ADD BUTTONS
        # ----------------------------------------------------

        nav_layout.addWidget(
            self.back_button
        )

        nav_layout.addWidget(
            self.forward_button
        )

        nav_layout.addWidget(
            self.reload_button
        )

        nav_layout.addWidget(
            self.home_button
        )

        nav_layout.addWidget(
            self.url_bar,
            1
        )

        nav_layout.addWidget(
            self.privacy_button
        )

        nav_layout.addWidget(
            self.settings_button
        )

        nav_layout.addWidget(
            self.new_tab_button
        )

        main_layout.addWidget(
            navigation,
            0
        )

        # ====================================================
        # WEB PAGES
        # ====================================================

        self.pages = QStackedWidget()

        main_layout.addWidget(
            self.pages,
            1
        )

        # ====================================================
        # STATUS
        # ====================================================

        self.status = QLabel(
            "Ready"
        )

        self.status.setFixedHeight(
            18
        )

        main_layout.addWidget(
            self.status,
            0
        )

        self.apply_theme()

    # ========================================================
    # BUTTON CREATOR
    # ========================================================

    def make_button(
        self,
        text
    ):

        button = QToolButton()

        button.setText(
            text
        )

        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        return button

    # ========================================================
    # ADD TAB
    # ========================================================

    def add_tab(
        self,
        url=None
    ):

        view = LiteWebView()

        # Apply current settings

        settings = view.settings()

        settings.setAttribute(
            settings.WebAttribute.JavascriptEnabled,
            not self.disable_javascript
        )

        settings.setAttribute(
            settings.WebAttribute.AutoLoadImages,
            self.load_images
        )

        settings.setAttribute(
            settings.WebAttribute.PluginsEnabled,
            not self.disable_plugins
        )

        view.setZoomFactor(
            self.zoom
        )

        self.pages.addWidget(
            view
        )

        index = self.tabs.addTab(
            "New Tab"
        )

        self.tabs.setTabData(
            index,
            view
        )

        self.tabs.setCurrentIndex(
            index
        )

        # Signals

        view.urlChanged.connect(
            lambda url, v=view:
            self.update_url(url, v)
        )

        view.titleChanged.connect(
            lambda title, v=view:
            self.update_title(title, v)
        )

        view.loadStarted.connect(
            self.load_started
        )

        view.loadFinished.connect(
            self.load_finished
        )

        if url:

            view.setUrl(
                QUrl(url)
            )

    # ========================================================
    # CURRENT VIEW
    # ========================================================

    def current_view(self):

        index = self.tabs.currentIndex()

        if index < 0:
            return None

        view = self.tabs.tabData(
            index
        )

        if isinstance(
            view,
            LiteWebView
        ):

            return view

        return None

    # ========================================================
    # TAB CHANGE
    # ========================================================

    def change_tab(
        self,
        index
    ):

        if index < 0:
            return

        view = self.tabs.tabData(
            index
        )

        if view:

            self.pages.setCurrentWidget(
                view
            )

            self.url_bar.setText(
                view.url().toString()
            )

    # ========================================================
    # NAVIGATION
    # ========================================================

    def go_back(self):

        view = self.current_view()

        if view:
            view.back()

    def go_forward(self):

        view = self.current_view()

        if view:
            view.forward()

    def reload(self):

        view = self.current_view()

        if view:
            view.reload()

    def go_home(self):

        view = self.current_view()

        if view:

            view.setUrl(
                QUrl(
                    self.home_page
                )
            )

    # ========================================================
    # SEARCH ENGINE
    # ========================================================

    def search_url(self, query):

        from urllib.parse import quote_plus

        query = quote_plus(query)

        if self.search_engine == "Google":
            return "https://www.google.com/search?q=" + query

        if self.search_engine == "Bing":
            return "https://www.bing.com/search?q=" + query

        if self.search_engine == "DuckDuckGo":
            return "https://duckduckgo.com/?q=" + query

        if self.search_engine == "Brave Search":
            return "https://search.brave.com/search?q=" + query

        # Fallback
        return "https://search.brave.com/search?q=" + query
    
    # ========================================================
    # NAVIGATE
    # ========================================================

    def navigate(self):

        view = self.current_view()

        if not view:
            return

        text = self.url_bar.text().strip()

        if not text:
            return

        if (
            text.startswith("http://")
            or text.startswith("https://")
        ):

            url = text

        elif text.startswith(
            "file://"
        ):

            url = text

        elif (
            " " in text
            or "." not in text
        ):

            url = self.search_url(
                text
            )

        else:

            url = "https://" + text

        view.setUrl(
            QUrl(url)
        )

    # ========================================================
    # URL UPDATE
    # ========================================================

    def update_url(
        self,
        url,
        view
    ):

        if view != self.current_view():

            return

        self.url_bar.setText(
            url.toString()
        )

    # ========================================================
    # TITLE UPDATE
    # ========================================================

    def update_title(
        self,
        title,
        view
    ):

        index = -1

        for i in range(
            self.tabs.count()
        ):

            if self.tabs.tabData(i) == view:

                index = i

                break

        if index == -1:
            return

        if not title:

            title = "New Tab"

        if len(title) > MAX_TAB_TITLE_LENGTH:

            title = (
                title[:MAX_TAB_TITLE_LENGTH]
                + "..."
            )

        self.tabs.setTabText(
            index,
            title
        )

    # ========================================================
    # CLOSE TAB
    # ========================================================

    def close_tab(
        self,
        index
    ):

        if self.tabs.count() <= 1:

            view = self.current_view()

            if view:

                view.setUrl(
                    QUrl(
                        self.home_page
                    )
                )

            return

        view = self.tabs.tabData(
            index
        )

        self.tabs.removeTab(
            index
        )

        if view:

            self.pages.removeWidget(
                view
            )

            view.stop()

            view.deleteLater()

    # ========================================================
    # PRIVACY
    # ========================================================

    def clear_privacy(self):

        view = self.current_view()

        if not view:

            return

        profile = view.page().profile()

        profile.clearHttpCache()

        profile.cookieStore().deleteAllCookies()

        self.status.setText(
            "Privacy data cleared"
        )

    # ========================================================
    # SETTINGS
    # ========================================================

    def open_settings(self):

        dialog = SettingsDialog(
            self
        )

        dialog.exec()

    # ========================================================
    # THEME
    # ========================================================

    def apply_theme(self):

        if self.theme == "Light":

            self.setStyleSheet(
                """
                QMainWindow {
                    background: #f5f5f5;
                }

                QWidget {
                    background: #f5f5f5;
                    color: #222222;
                }

                QTabBar {
                    background: #f5f5f5;
                }

                QTabBar::tab {
                    background: #e5e5e5;
                    color: #444444;
                    padding: 8px 16px;
                    margin-right: 1px;
                    border: 0px;
                }

                QTabBar::tab:selected {
                    background: #ffffff;
                    color: #111111;
                }

                QTabBar::tab:hover {
                    background: #eeeeee;
                }

                QLineEdit {
                    background: #ffffff;
                    border: 1px solid #cccccc;
                    border-radius: 7px;
                    padding: 7px;
                    color: #222222;
                }

                QLineEdit:focus {
                    border: 1px solid #999999;
                }

                QToolButton {
                    background: #ffffff;
                    border: 0px;
                    border-radius: 6px;
                    padding: 7px 10px;
                    color: #333333;
                }

                QToolButton:hover {
                    background: #e8e8e8;
                }

                QLabel {
                    color: #777777;
                    padding-left: 6px;
                }

                QDialog {
                    background: #f5f5f5;
                }

                QGroupBox {
                    font-weight: bold;
                    border: 1px solid #cccccc;
                    border-radius: 6px;
                    margin-top: 10px;
                    padding: 10px;
                }

                QPushButton {
                    padding: 7px 14px;
                }
                """
            )

        else:

            self.setStyleSheet(
                """
                QMainWindow {
                    background: #111111;
                }

                QWidget {
                    background: #111111;
                    color: #eeeeee;
                }

                QTabBar {
                    background: #111111;
                }

                QTabBar::tab {
                    background: #191919;
                    color: #cccccc;
                    padding: 8px 16px;
                    margin-right: 1px;
                    border: 0px;
                }

                QTabBar::tab:selected {
                    background: #242424;
                    color: white;
                }

                QTabBar::tab:hover {
                    background: #202020;
                }

                QLineEdit {
                    background: #1b1b1b;
                    border: 1px solid #333333;
                    border-radius: 7px;
                    padding: 7px;
                    color: white;
                }

                QLineEdit:focus {
                    border: 1px solid #555555;
                }

                QToolButton {
                    background: #1b1b1b;
                    border: 0px;
                    border-radius: 6px;
                    padding: 7px 10px;
                    color: #eeeeee;
                }

                QToolButton:hover {
                    background: #292929;
                }

                QLabel {
                    color: #777777;
                    padding-left: 6px;
                }

                QDialog {
                    background: #111111;
                    color: #eeeeee;
                }

                QGroupBox {
                    font-weight: bold;
                    border: 1px solid #333333;
                    border-radius: 6px;
                    margin-top: 10px;
                    padding: 10px;
                }

                QPushButton {
                    padding: 7px 14px;
                    background: #1b1b1b;
                    color: #eeeeee;
                    border: 1px solid #333333;
                    border-radius: 5px;
                }

                QPushButton:hover {
                    background: #292929;
                }

                QComboBox {
                    background: #1b1b1b;
                    color: #eeeeee;
                    border: 1px solid #333333;
                    padding: 5px;
                    border-radius: 5px;
                }

                QDoubleSpinBox {
                    background: #1b1b1b;
                    color: #eeeeee;
                    border: 1px solid #333333;
                    padding: 5px;
                    border-radius: 5px;
                }

                QCheckBox {
                    color: #eeeeee;
                }
                """
            )

    # ========================================================
    # LOAD STATUS
    # ========================================================

    def load_started(self):

        self.status.setText(
            "Loading..."
        )

    def load_finished(
        self,
        success
    ):

        if success:

            self.status.setText(
                "Ready"
            )

        else:

            self.status.setText(
                "Failed to load"
            )

    # ========================================================
    # KEYBOARD SHORTCUTS
    # ========================================================

    def keyPressEvent(
        self,
        event
    ):

        modifiers = event.modifiers()

        if (
            event.key() == Qt.Key.Key_L
            and modifiers
            & Qt.KeyboardModifier.ControlModifier
        ):

            self.url_bar.setFocus()

            self.url_bar.selectAll()

            return

        if (
            event.key() == Qt.Key.Key_T
            and modifiers
            & Qt.KeyboardModifier.ControlModifier
        ):

            self.add_tab(
                self.home_page
            )

            return

        if (
            event.key() == Qt.Key.Key_W
            and modifiers
            & Qt.KeyboardModifier.ControlModifier
        ):

            self.close_tab(
                self.tabs.currentIndex()
            )

            return

        if event.key() == Qt.Key.Key_F5:

            self.reload()

            return

        if (
            event.key() == Qt.Key.Key_F
            and modifiers
            & Qt.KeyboardModifier.ControlModifier
        ):

            self.open_settings()

            return

        super().keyPressEvent(
            event
        )

    # ========================================================
    # CLOSE EVENT
    # ========================================================

    def closeEvent(
        self,
        event
    ):

        if self.clear_on_exit:

            for i in range(
                self.tabs.count()
            ):

                view = self.tabs.tabData(i)

                if isinstance(
                    view,
                    LiteWebView
                ):

                    profile = (
                        view.page().profile()
                    )

                    profile.clearHttpCache()

                    profile.cookieStore().deleteAllCookies()

        event.accept()


# ============================================================
# MAIN
# ============================================================

def main():

    QApplication.setAttribute(
        Qt.ApplicationAttribute.AA_ShareOpenGLContexts
    )

    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        APP_NAME
    )

    browser = LiteBrowser()

    browser.show()

    sys.exit(
        app.exec()
    )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()