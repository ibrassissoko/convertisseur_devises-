"""
MainWindow — UI principale du convertisseur PySide6 (version Desktop optimisée)
Respect UI/UX Desktop:
- large screen layout (1200x800)
- centered content
- cards (groupbox)
- spacing and readable hierarchy
"""

from PySide6 import QtWidgets, QtCore
from datetime import datetime

from currency_app.core.i18n import Lang, t
from currency_app.domain.models import ConversionRecord
from currency_app.utils.flags import flag_for_currency
from currency_app.ui.styles import apply_black_orange_white
from currency_app.infra.pdf_exporter import export_table_to_pdf


class MainWindow(QtWidgets.QWidget):
    def __init__(self, settings, repo, converter, notifier, chart):
        super().__init__()

        # Services
        self.s = settings
        self.repo = repo
        self.converter = converter
        self.notifier = notifier
        self.chart = chart

        # State interne
        self.lang = Lang.FR
        self._ui_ready = False

        self.setWindowTitle(self.s.app_title)
        self.setMinimumSize(1200, 800)  # Desktop format

        # Build UI
        self._build_ui()

        apply_black_orange_white(self)
        self._populate_defaults()
        self._ui_ready = True
        self._load_history()
        self.notifier.ensure(self)

    # ================================================================================
    # ✅ Build UI
    # ================================================================================
    def _build_ui(self):
        # Scroll container for desktop ergonomics
        outer_layout = QtWidgets.QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        outer_layout.addWidget(scroll)

        container = QtWidgets.QWidget()
        scroll.setWidget(container)

        # Main centered layout
        self.main_layout = QtWidgets.QVBoxLayout(container)
        self.main_layout.setContentsMargins(40, 30, 40, 30)
        self.main_layout.setSpacing(20)

        # ---- Title desktop UI ----
        title = QtWidgets.QLabel("💱 Convertisseur de Devises — Desktop")
        title.setStyleSheet("font-size:22px; font-weight:600; margin-bottom:4px;")

        subtitle = QtWidgets.QLabel("Conversion offline, historique, PDF, graphique en temps réel, notifications")
        subtitle.setStyleSheet("font-size:13px; color:#C7C7C7; margin-bottom:12px;")

        self.main_layout.addWidget(title)
        self.main_layout.addWidget(subtitle)

        # ================================================================================
        # ✅ Language card
        # ================================================================================
        grp_lang = QtWidgets.QGroupBox("🌍 Langue / Language")
        lang_layout = QtWidgets.QHBoxLayout()

        self.cmb_lang = QtWidgets.QComboBox()
        self.cmb_lang.addItems(["Français", "English"])

        lang_layout.addWidget(self.cmb_lang)
        grp_lang.setLayout(lang_layout)
        self.main_layout.addWidget(grp_lang)

        # ================================================================================
        # ✅ Conversion card
        # ================================================================================
        grp_convert = QtWidgets.QGroupBox("💱 Conversion")
        form = QtWidgets.QGridLayout()
        form.setHorizontalSpacing(15)
        form.setVerticalSpacing(12)

        self.cbb_from = QtWidgets.QComboBox()
        self.cbb_to = QtWidgets.QComboBox()

        self.spn_from = QtWidgets.QDoubleSpinBox()
        self.spn_from.setDecimals(4)
        self.spn_from.setMaximum(1_000_000_000)

        self.spn_to = QtWidgets.QDoubleSpinBox()
        self.spn_to.setDecimals(4)
        self.spn_to.setMaximum(1_000_000_000)
        self.spn_to.setReadOnly(True)

        self.btn_swap = QtWidgets.QPushButton("🔁")
        self.btn_convert = QtWidgets.QPushButton(t("convert", self.lang))
        self.lbl_rate = QtWidgets.QLabel(f"{t('rate', self.lang)} : —")

        form.addWidget(QtWidgets.QLabel(t("from", self.lang)), 0, 0)
        form.addWidget(self.cbb_from, 0, 1)
        form.addWidget(self.spn_from, 0, 2)

        form.addWidget(QtWidgets.QLabel(t("to", self.lang)), 1, 0)
        form.addWidget(self.cbb_to, 1, 1)
        form.addWidget(self.spn_to, 1, 2)

        form.addWidget(self.btn_swap, 0, 3, 2, 1)
        form.addWidget(self.btn_convert, 2, 0, 1, 4)

        grp_convert.setLayout(form)
        self.main_layout.addWidget(grp_convert)
        self.main_layout.addWidget(self.lbl_rate)

        # ================================================================================
        # ✅ Notifications card
        # ================================================================================
        grp_notify = QtWidgets.QGroupBox("🔔 Notifications")
        notif = QtWidgets.QHBoxLayout()

        self.chk_notify = QtWidgets.QCheckBox(t("notify_enable", self.lang))
        self.spn_threshold = QtWidgets.QDoubleSpinBox()
        self.spn_threshold.setDecimals(4)
        self.spn_threshold.setRange(0.0, 1_000_000.0)
        self.spn_threshold.setValue(self.s.notify_default_threshold)

        notif.addWidget(self.chk_notify)
        notif.addWidget(QtWidgets.QLabel(t("threshold", self.lang)))
        notif.addWidget(self.spn_threshold)

        grp_notify.setLayout(notif)
        self.main_layout.addWidget(grp_notify)

        # ================================================================================
        # ✅ Table (history)
        # ================================================================================
        self.tbl = QtWidgets.QTableWidget(0, 6)
        self.tbl.setHorizontalHeaderLabels(["Date", "De", "Vers", "Montant", "Résultat", "Taux"])
        self.tbl.horizontalHeader().setStretchLastSection(True)
        self.tbl.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.main_layout.addWidget(self.tbl)

        # ================================================================================
        # ✅ Chart
        # ================================================================================
        self.main_layout.addWidget(self.chart.widget())

        # ================================================================================
        # ✅ Buttons bar
        # ================================================================================
        self.btn_pdf = QtWidgets.QPushButton(t("export_pdf", self.lang))
        self.btn_clear = QtWidgets.QPushButton(t("clear_history", self.lang))

        btn_line = QtWidgets.QHBoxLayout()
        btn_line.addStretch()
        btn_line.addWidget(self.btn_pdf)
        btn_line.addWidget(self.btn_clear)
        self.main_layout.addLayout(btn_line)

        # ---- Events ----
        self.cmb_lang.currentIndexChanged.connect(self._on_change_lang)
        self.btn_swap.clicked.connect(self._swap)
        self.btn_convert.clicked.connect(self.convert)
        self.btn_pdf.clicked.connect(self._export_pdf_clicked)
        self.btn_clear.clicked.connect(self._clear_history_clicked)
        self.spn_from.valueChanged.connect(self.convert)
        self.cbb_from.currentTextChanged.connect(self.convert)
        self.cbb_to.currentTextChanged.connect(self.convert)

    # ================================================================================
    # ✅ Populate currencies
    # ================================================================================
    def _populate_defaults(self):
        currencies = self.converter.list_currencies()

        self.cbb_from.setEditable(True)
        self.cbb_to.setEditable(True)

        for c in currencies:
            self.cbb_from.addItem(f"{flag_for_currency(c)}  {c}", c)
            self.cbb_to.addItem(f"{flag_for_currency(c)}  {c}", c)

        self.cbb_from.setCurrentText(f"{flag_for_currency(self.s.default_from)}  {self.s.default_from}")
        self.cbb_to.setCurrentText(f"{flag_for_currency(self.s.default_to)}  {self.s.default_to}")
        self.spn_from.setValue(self.s.default_amount)
        self.chk_notify.setChecked(self.s.notify_default_enabled)

        comp = QtWidgets.QCompleter(currencies)
        comp.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.cbb_from.setCompleter(comp)
        self.cbb_to.setCompleter(comp)

    def _get_code(self, combo):
        return combo.currentText().split()[-1].upper()

    # ================================================================================
    # ✅ Convert
    # ================================================================================
    def convert(self):
        if not self._ui_ready:
            return

        try:
            frm = self._get_code(self.cbb_from)
            to = self._get_code(self.cbb_to)
            amount = float(self.spn_from.value())

            result, rate = self.converter.convert(amount, frm, to)
            self.spn_to.setValue(result)
            self.lbl_rate.setText(f"{t('rate', self.lang)} : 1 {frm} = {rate:.4f} {to}")

            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            rec = ConversionRecord(ts, frm, to, amount, result, rate)

            self.repo.insert(rec)
            self._add_row(rec)
            self.chart.add_point(ts, rate)

            self.notifier.maybe_notify_threshold(
                frm, to, rate,
                float(self.spn_threshold.value()),
                self.chk_notify.isChecked(),
                t("notif_title", self.lang),
                t("notif_body", self.lang),
            )

        except Exception:
            pass

    def _add_row(self, rec):
        r = self.tbl.rowCount()
        self.tbl.insertRow(r)

        values = [
            rec.ts, rec.from_cur, rec.to_cur,
            f"{rec.amount:.2f}", f"{rec.result:.2f}", f"{rec.rate:.4f}"
        ]

        for c, v in enumerate(values):
            item = QtWidgets.QTableWidgetItem(v)
            if c >= 3:
                item.setTextAlignment(QtCore.Qt.AlignRight)
            self.tbl.setItem(r, c, item)

    def _load_history(self):
        for rec in self.repo.fetch_all():
            self._add_row(rec)
            self.chart.add_point(rec.ts, rec.rate)

    # ================================================================================
    # ✅ Clear history
    # ================================================================================
    def _clear_history_clicked(self):
        self.repo.clear()
        self.tbl.setRowCount(0)
        self.chart.clear()

    # ================================================================================
    # ✅ Swap
    # ================================================================================
    def _swap(self):
        f = self._get_code(self.cbb_from)
        t = self._get_code(self.cbb_to)
        self.cbb_from.setCurrentText(f"{flag_for_currency(t)}  {t}")
        self.cbb_to.setCurrentText(f"{flag_for_currency(f)}  {f}")

    # ================================================================================
    # ✅ Export PDF
    # ================================================================================
    def _export_pdf_clicked(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Exporter en PDF", "", "PDF (*.pdf)")
        if not path:
            return

        headers = [self.tbl.horizontalHeaderItem(i).text() for i in range(self.tbl.columnCount())]
        rows = [[self.tbl.item(r, c).text() for c in range(self.tbl.columnCount())] for r in range(self.tbl.rowCount())]

        export_table_to_pdf(path, "Historique Convertisseur", headers, rows)
        QtWidgets.QMessageBox.information(self, t("dialog_success", self.lang), t("pdf_done", self.lang))

    # ================================================================================
    # ✅ Language switch
    # ================================================================================
    def _on_change_lang(self, idx):
        self.lang = Lang.FR if idx == 0 else Lang.EN
        self.btn_convert.setText(t("convert", self.lang))
        self.btn_pdf.setText(t("export_pdf", self.lang))
        self.btn_clear.setText(t("clear_history", self.lang))
        self.chk_notify.setText(t("notify_enable", self.lang))
        self.lbl_rate.setText(f"{t('rate', self.lang)} : —")
