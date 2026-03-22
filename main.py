import sys
import json
import uuid
import os
import copy
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QFrame, QSpinBox,
    QLineEdit, QDialog, QFormLayout, QComboBox, QMessageBox,
    QFileDialog, QTabWidget, QListWidget, QDoubleSpinBox,
    QRadioButton, QGroupBox, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIntValidator

# ============================================================
# カラーパレット
# ============================================================
BG         = "#f5f5f5"
PANEL      = "#ffffff"
BORDER     = "#e0e0e0"
BORDER_MID = "#cccccc"
TEXT       = "#1a1a1a"
TEXT_SUB   = "#666666"
TEXT_MUTED = "#aaaaaa"
ACCENT     = "#1a1a1a"
DANGER     = "#e53935"

SS = f"""
* {{
    font-family: "Yu Gothic UI", "Meiryo UI", "MS UI Gothic", sans-serif;
    font-size: 13px;
    color: {TEXT};
}}
QMainWindow, QDialog {{ background: {BG}; }}

QScrollArea {{ border: none; background: transparent; }}
QScrollBar:vertical {{
    background: {BG}; width: 6px; border-radius: 3px; margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {BORDER_MID}; border-radius: 3px; min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{ background: #999; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}

QPushButton {{
    background: {PANEL}; color: {TEXT};
    border: 1px solid {BORDER}; border-radius: 6px; padding: 7px 16px;
}}
QPushButton:hover {{ background: {BG}; border-color: {BORDER_MID}; }}
QPushButton:pressed {{ background: #e8e8e8; }}

QPushButton#btnPrimary {{
    background: {ACCENT}; color: white; border: none; font-weight: bold;
}}
QPushButton#btnPrimary:hover {{ background: #333; }}
QPushButton#btnPrimary:pressed {{ background: #000; }}

QPushButton#btnCopy {{
    background: {ACCENT}; color: white; border: none;
    border-radius: 8px; font-size: 15px; font-weight: bold; padding: 12px;
}}
QPushButton#btnCopy:hover {{ background: #333; }}
QPushButton#btnCopy:disabled {{ background: #555; }}

QPushButton#btnReset {{
    background: {PANEL}; color: {DANGER};
    border: 1.5px solid {DANGER}; border-radius: 8px; padding: 8px;
}}
QPushButton#btnReset:hover {{ background: {DANGER}; color: white; }}

QPushButton#btnCat {{
    background: transparent; color: {TEXT_SUB};
    border: none; border-bottom: 2px solid transparent;
    border-radius: 0; padding: 8px 14px;
}}
QPushButton#btnCat:hover {{ color: {TEXT}; }}
QPushButton#btnCat[active="true"] {{
    color: {TEXT}; border-bottom: 2px solid {ACCENT}; font-weight: bold;
}}

QPushButton#btnToggleOff {{
    background: #ebebeb; color: #999;
    border: 1px solid {BORDER}; border-radius: 6px; padding: 4px 0;
    font-size: 12px; min-width: 56px; max-width: 56px;
    min-height: 30px; max-height: 30px;
}}
QPushButton#btnToggleOff:hover {{ background: #ddd; color: {TEXT_SUB}; }}

QPushButton#btnToggleOn {{
    background: {ACCENT}; color: white;
    border: 1px solid {ACCENT}; border-radius: 6px; padding: 4px 0;
    font-size: 12px; font-weight: bold; min-width: 56px; max-width: 56px;
    min-height: 30px; max-height: 30px;
}}
QPushButton#btnToggleOn:hover {{ background: #333; }}

QPushButton#btnQtyStep {{
    background: {BG}; color: {TEXT};
    border: 1px solid {BORDER}; border-radius: 5px; padding: 0;
    font-size: 16px; font-weight: bold;
    min-width: 30px; max-width: 30px;
    min-height: 30px; max-height: 30px;
}}
QPushButton#btnQtyStep:hover {{
    background: {ACCENT}; color: white; border-color: {ACCENT};
}}

QPushButton#btnRemove {{
    background: transparent; color: {TEXT_MUTED};
    border: 1px solid {BORDER}; border-radius: 5px; padding: 0;
    font-size: 12px;
    min-width: 26px; max-width: 26px;
    min-height: 26px; max-height: 26px;
}}
QPushButton#btnRemove:hover {{
    background: {DANGER}; color: white; border-color: {DANGER};
}}

QPushButton#btnSm {{ padding: 5px 12px; font-size: 12px; }}
QPushButton#btnSmDanger {{
    padding: 5px 12px; font-size: 12px;
    color: {DANGER}; border-color: #ffcdd2;
}}
QPushButton#btnSmDanger:hover {{
    background: {DANGER}; color: white; border-color: {DANGER};
}}

QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
    background: {PANEL}; color: {TEXT};
    border: 1px solid {BORDER}; border-radius: 6px; padding: 6px 10px;
    selection-background-color: #ddd;
}}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
    border-color: {ACCENT};
}}
QSpinBox::up-button, QSpinBox::down-button {{ width:0; height:0; border:none; }}
QComboBox::drop-down {{ border:none; width:20px; }}
QComboBox QAbstractItemView {{
    background: {PANEL}; border: 1px solid {BORDER};
    selection-background-color: {BG}; selection-color: {TEXT}; outline: none;
}}

QTabWidget::pane {{
    border: 1px solid {BORDER}; border-radius: 6px;
    background: {PANEL}; top: -1px;
}}
QTabBar::tab {{
    background: {BG}; color: {TEXT_SUB};
    border: 1px solid {BORDER}; border-bottom: none;
    padding: 7px 20px; border-top-left-radius: 6px;
    border-top-right-radius: 6px; margin-right: 2px;
}}
QTabBar::tab:selected {{ background: {PANEL}; color: {TEXT}; font-weight: bold; }}
QTabBar::tab:hover {{ color: {TEXT}; }}

QListWidget {{
    background: {PANEL}; border: 1px solid {BORDER};
    border-radius: 6px; outline: none;
}}
QListWidget::item {{ padding: 7px 10px; border-bottom: 1px solid {BG}; }}
QListWidget::item:selected {{ background: {BG}; color: {TEXT}; }}
QListWidget::item:hover {{ background: {BG}; }}

QGroupBox {{
    border: 1px solid {BORDER}; border-radius: 6px;
    margin-top: 10px; padding-top: 6px;
    font-size: 11px; color: {TEXT_MUTED};
}}
QGroupBox::title {{ subcontrol-origin: margin; left: 10px; padding: 0 4px; }}

QRadioButton {{ spacing: 6px; color: {TEXT_SUB}; }}
QRadioButton::indicator {{
    width: 14px; height: 14px;
    border: 1.5px solid {BORDER_MID}; border-radius: 7px; background: {PANEL};
}}
QRadioButton::indicator:checked {{ background: {ACCENT}; border-color: {ACCENT}; }}

QFrame#sep {{ background: {BORDER}; max-height: 1px; min-height: 1px; border: none; }}
QFrame#vSep {{ background: {BORDER}; max-width: 1px; min-width: 1px; border: none; }}
"""

# ============================================================
# 設定 I/O
# ============================================================
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

def load_config(path=None):
    t = path or CONFIG_PATH
    if os.path.exists(t):
        with open(t, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"shop_name": "新規ショップ", "categories": [], "products": []}

def save_config(data, path=None):
    with open(path or CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ============================================================
# トグルボタン（ON/OFF）
# ============================================================
class ToggleButton(QPushButton):
    toggled_state = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__("OFF", parent)
        self._on = False
        self.setObjectName("btnToggleOff")
        self.clicked.connect(self._flip)

    def _flip(self):
        self.set_on(not self._on)
        self.toggled_state.emit(self._on)

    def set_on(self, val: bool):
        self._on = val
        self.setText("ON" if val else "OFF")
        self.setObjectName("btnToggleOn" if val else "btnToggleOff")
        self.style().unpolish(self)
        self.style().polish(self)

    def is_on(self): return self._on
    def reset(self): self.set_on(False)

# ============================================================
# 数量ウィジェット（＋／－付き）
# ============================================================
class QtyWidget(QWidget):
    value_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        hl = QHBoxLayout(self)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(4)

        self.btn_m = QPushButton("−")
        self.btn_m.setObjectName("btnQtyStep")
        hl.addWidget(self.btn_m)

        self.spin = QSpinBox()
        self.spin.setRange(0, 9999)
        self.spin.setFixedWidth(50)
        self.spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spin.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        hl.addWidget(self.spin)

        self.btn_p = QPushButton("+")
        self.btn_p.setObjectName("btnQtyStep")
        hl.addWidget(self.btn_p)

        self.btn_m.clicked.connect(lambda: self.spin.setValue(max(0, self.spin.value()-1)))
        self.btn_p.clicked.connect(lambda: self.spin.setValue(self.spin.value()+1))
        self.spin.valueChanged.connect(self.value_changed.emit)

    def value(self): return self.spin.value()
    def setValue(self, v):
        self.spin.blockSignals(True); self.spin.setValue(v); self.spin.blockSignals(False)
    def reset(self): self.setValue(0)

# ============================================================
# 商品カード
# ============================================================
class ProductCard(QFrame):
    changed = pyqtSignal()

    def __init__(self, product, parent=None):
        super().__init__(parent)
        self.product = product
        self.setFixedHeight(64)
        self.setStyleSheet(
            f"QFrame {{ background:{PANEL}; border:1px solid {BORDER}; border-radius:8px; }}"
        )
        self._build()

    def _build(self):
        hl = QHBoxLayout(self)
        hl.setContentsMargins(14, 0, 14, 0)
        hl.setSpacing(12)

        name = QLabel(self.product["name"])
        name.setFont(QFont("Yu Gothic UI", 12))
        name.setStyleSheet(f"color:{TEXT}; background:transparent; border:none;")
        hl.addWidget(name, stretch=1)

        price = QLabel(f"¥{self.product['price']:,}")
        price.setStyleSheet(f"color:{TEXT_SUB}; font-size:12px; background:transparent; border:none;")
        price.setFixedWidth(90)
        price.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        hl.addWidget(price)

        if self.product["input_type"] == "checkbox":
            self.input_w = ToggleButton()
            self.input_w.toggled_state.connect(lambda _: self.changed.emit())
        else:
            self.input_w = QtyWidget()
            self.input_w.value_changed.connect(lambda _: self.changed.emit())
        hl.addWidget(self.input_w)

    def get_quantity(self):
        if self.product["input_type"] == "checkbox":
            return 1 if self.input_w.is_on() else 0
        return self.input_w.value()

    def reset(self): self.input_w.reset()

    def set_quantity(self, qty):
        if self.product["input_type"] == "checkbox":
            self.input_w.set_on(qty > 0)
        else:
            self.input_w.setValue(qty)

# ============================================================
# カート行
# ============================================================
class CartRow(QFrame):
    remove_requested = pyqtSignal(str)
    qty_changed      = pyqtSignal(str, int)

    def __init__(self, product, quantity, parent=None):
        super().__init__(parent)
        self.product = product
        self.setFixedHeight(46)
        self.setStyleSheet(
            f"QFrame {{ background:transparent; border:none;"
            f" border-bottom:1px solid {BORDER}; border-radius:0; }}"
        )
        hl = QHBoxLayout(self)
        hl.setContentsMargins(4, 0, 4, 0)
        hl.setSpacing(8)

        name = QLabel(self.product["name"])
        name.setStyleSheet(f"color:{TEXT}; border:none; background:transparent;")
        hl.addWidget(name, stretch=1)

        if self.product["input_type"] == "checkbox":
            lbl = QLabel("✓")
            lbl.setFixedWidth(72)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(f"color:{TEXT_MUTED}; font-size:14px; border:none; background:transparent;")
            hl.addWidget(lbl)
        else:
            self.qty_w = QtyWidget()
            self.qty_w.setValue(quantity)
            self.qty_w.setFixedWidth(114)
            self.qty_w.value_changed.connect(lambda v: self.qty_changed.emit(self.product["id"], v))
            hl.addWidget(self.qty_w)

        self.sub_lbl = QLabel(f"¥{self.product['price']*quantity:,}")
        self.sub_lbl.setFixedWidth(80)
        self.sub_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.sub_lbl.setStyleSheet(f"color:{TEXT}; font-weight:bold; border:none; background:transparent;")
        hl.addWidget(self.sub_lbl)

        btn_del = QPushButton("✕")
        btn_del.setObjectName("btnRemove")
        btn_del.clicked.connect(lambda: self.remove_requested.emit(self.product["id"]))
        hl.addWidget(btn_del)

# ============================================================
# メインウィンドウ
# ============================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config  = load_config()
        self.cart: dict[str, int] = {}
        self.current_cat = None
        self.product_cards: dict[str, ProductCard] = {}
        self.discount_type  = "fixed"
        self.discount_value = 0.0
        self._total_value   = 0

        self.setWindowTitle("FiveM ショップ電卓")
        self.setMinimumSize(1000, 640)
        self.resize(1160, 720)
        self.setStyleSheet(SS)
        self._build_ui()
        self._refresh_products()
        self._update_total()

    # ---- UI構築 ----
    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        vl = QVBoxLayout(root)
        vl.setContentsMargins(0,0,0,0); vl.setSpacing(0)
        vl.addWidget(self._mk_header())
        sep = QFrame(); sep.setObjectName("sep"); vl.addWidget(sep)

        body = QWidget(); body.setStyleSheet(f"background:{BG};")
        hl = QHBoxLayout(body)
        hl.setContentsMargins(0,0,0,0); hl.setSpacing(0)
        hl.addWidget(self._mk_product_panel(), stretch=1)
        sep2 = QFrame(); sep2.setObjectName("vSep"); hl.addWidget(sep2)
        hl.addWidget(self._mk_cart_panel(), stretch=0)
        vl.addWidget(body, stretch=1)

    def _mk_header(self):
        hdr = QFrame()
        hdr.setFixedHeight(52)
        hdr.setStyleSheet(f"background:{PANEL}; border:none;")
        hl = QHBoxLayout(hdr)
        hl.setContentsMargins(20,0,16,0); hl.setSpacing(8)

        self.lbl_shop = QLabel(self.config.get("shop_name","ショップ"))
        self.lbl_shop.setFont(QFont("Yu Gothic UI", 16, QFont.Weight.Bold))
        self.lbl_shop.setStyleSheet(f"color:{TEXT}; border:none; background:transparent;")
        hl.addWidget(self.lbl_shop)
        hl.addStretch()

        for text, slot in [("設定を読込", self._load_cfg), ("設定を保存", self._save_cfg)]:
            b = QPushButton(text); b.setFixedHeight(32); b.clicked.connect(slot)
            hl.addWidget(b)

        btn = QPushButton("商品設定")
        btn.setObjectName("btnPrimary"); btn.setFixedHeight(32)
        btn.clicked.connect(self._open_settings)
        hl.addWidget(btn)
        return hdr

    def _mk_product_panel(self):
        w = QWidget(); w.setStyleSheet(f"background:{BG};")
        vl = QVBoxLayout(w)
        vl.setContentsMargins(20,14,14,14); vl.setSpacing(10)

        self.cat_bar = QFrame()
        self.cat_bar.setStyleSheet(
            f"background:transparent; border:none; border-bottom:1px solid {BORDER};"
        )
        self.cat_bar_hl = QHBoxLayout(self.cat_bar)
        self.cat_bar_hl.setContentsMargins(0,0,0,0); self.cat_bar_hl.setSpacing(0)
        vl.addWidget(self.cat_bar)

        self.prod_scroll = QScrollArea()
        self.prod_scroll.setWidgetResizable(True)
        self.prod_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.prod_scroll.setStyleSheet("background:transparent; border:none;")
        self.prod_cont = QWidget(); self.prod_cont.setStyleSheet("background:transparent;")
        self.prod_vl = QVBoxLayout(self.prod_cont)
        self.prod_vl.setContentsMargins(0,6,6,6); self.prod_vl.setSpacing(6)
        self.prod_vl.addStretch()
        self.prod_scroll.setWidget(self.prod_cont)
        vl.addWidget(self.prod_scroll, stretch=1)
        return w

    def _mk_cart_panel(self):
        w = QWidget(); w.setFixedWidth(360)
        w.setStyleSheet(f"background:{PANEL}; border:none;")
        vl = QVBoxLayout(w)
        vl.setContentsMargins(16,14,16,16); vl.setSpacing(0)

        lbl = QLabel("カート")
        lbl.setFont(QFont("Yu Gothic UI", 11, QFont.Weight.Bold))
        lbl.setStyleSheet(f"color:{TEXT}; border:none;")
        vl.addWidget(lbl)
        vl.addSpacing(8)

        self.cart_scroll = QScrollArea()
        self.cart_scroll.setWidgetResizable(True)
        self.cart_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.cart_scroll.setStyleSheet("background:transparent; border:none;")
        self.cart_cont = QWidget(); self.cart_cont.setStyleSheet("background:transparent;")
        self.cart_vl = QVBoxLayout(self.cart_cont)
        self.cart_vl.setContentsMargins(0,0,0,0); self.cart_vl.setSpacing(0)
        self.cart_vl.addStretch()
        self.cart_scroll.setWidget(self.cart_cont)
        vl.addWidget(self.cart_scroll, stretch=1)
        vl.addSpacing(8)

        row_sub = QHBoxLayout(); row_sub.addStretch()
        self.lbl_subtotal = QLabel("小計  ¥0")
        self.lbl_subtotal.setStyleSheet(f"color:{TEXT_MUTED}; font-size:12px; border:none;")
        row_sub.addWidget(self.lbl_subtotal)
        vl.addLayout(row_sub)
        vl.addSpacing(10)

        vl.addWidget(self._mk_discount())
        vl.addSpacing(12)

        # 合計枠
        tf = QFrame()
        tf.setStyleSheet(f"QFrame{{background:{BG};border:1px solid {BORDER};border-radius:8px;}}")
        tf_vl = QVBoxLayout(tf); tf_vl.setContentsMargins(14,10,14,10); tf_vl.setSpacing(2)
        lbl_t = QLabel("合計金額")
        lbl_t.setStyleSheet(f"color:{TEXT_MUTED};font-size:11px;border:none;background:transparent;")
        self.lbl_total = QLabel("¥0")
        self.lbl_total.setFont(QFont("Yu Gothic UI", 26, QFont.Weight.Bold))
        self.lbl_total.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lbl_total.setStyleSheet(f"color:{TEXT};border:none;background:transparent;")
        tf_vl.addWidget(lbl_t); tf_vl.addWidget(self.lbl_total)
        vl.addWidget(tf)
        vl.addSpacing(10)

        self.btn_copy = QPushButton("金額をコピー")
        self.btn_copy.setObjectName("btnCopy"); self.btn_copy.setFixedHeight(46)
        self.btn_copy.clicked.connect(self._copy_total)
        vl.addWidget(self.btn_copy)
        vl.addSpacing(6)

        btn_reset = QPushButton("リセット")
        btn_reset.setObjectName("btnReset"); btn_reset.setFixedHeight(36)
        btn_reset.clicked.connect(self._reset_all)
        vl.addWidget(btn_reset)
        return w

    def _mk_discount(self):
        grp = QGroupBox("値引き")
        grp.setStyleSheet(
            f"QGroupBox{{background:{BG};border:1px solid {BORDER};border-radius:8px;"
            f"margin-top:10px;padding:8px 10px 8px 10px;}}"
            f"QGroupBox::title{{subcontrol-origin:margin;left:10px;"
            f"padding:0 4px;color:{TEXT_MUTED};font-size:11px;}}"
        )
        gl = QVBoxLayout(grp); gl.setSpacing(6)

        type_hl = QHBoxLayout()
        self.rb_fixed   = QRadioButton("固定額")
        self.rb_percent = QRadioButton("割合 (%)")
        self.rb_fixed.setChecked(True)
        self.rb_fixed.toggled.connect(self._on_dis_type)
        type_hl.addWidget(self.rb_fixed); type_hl.addWidget(self.rb_percent); type_hl.addStretch()
        gl.addLayout(type_hl)

        inp_hl = QHBoxLayout(); inp_hl.setSpacing(6)
        self.dis_input = QDoubleSpinBox()
        self.dis_input.setRange(0, 9999999); self.dis_input.setDecimals(0)
        self.dis_input.setPrefix("¥"); self.dis_input.setFixedHeight(32)
        self.dis_input.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        self.dis_input.valueChanged.connect(self._on_dis_val)
        inp_hl.addWidget(self.dis_input)
        btn_clr = QPushButton("クリア"); btn_clr.setFixedHeight(32)
        btn_clr.clicked.connect(lambda: self.dis_input.setValue(0))
        inp_hl.addWidget(btn_clr)
        gl.addLayout(inp_hl)

        self.lbl_dis = QLabel("値引き  −¥0")
        self.lbl_dis.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lbl_dis.setStyleSheet(f"color:{TEXT_MUTED};font-size:12px;border:none;background:transparent;")
        gl.addWidget(self.lbl_dis)
        return grp

    # ---- カテゴリバー ----
    def _rebuild_cat_bar(self):
        while self.cat_bar_hl.count():
            item = self.cat_bar_hl.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        def mk(label, cat_id):
            b = QPushButton(label); b.setObjectName("btnCat")
            b.setProperty("active", self.current_cat == cat_id)
            b.style().unpolish(b); b.style().polish(b)
            b.clicked.connect(lambda: self._set_cat(cat_id))
            return b

        self.cat_bar_hl.addWidget(mk("すべて", None))
        for c in sorted(self.config.get("categories",[]), key=lambda x: x.get("order",0)):
            self.cat_bar_hl.addWidget(mk(c["name"], c["id"]))
        self.cat_bar_hl.addStretch()

    def _set_cat(self, cat_id):
        self.current_cat = cat_id
        self._refresh_products()

    # ---- 商品一覧 ----
    def _refresh_products(self):
        self._rebuild_cat_bar()
        while self.prod_vl.count() > 1:
            item = self.prod_vl.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self.product_cards.clear()

        prods = self.config.get("products", [])
        if self.current_cat is not None:
            prods = [p for p in prods if p.get("category_id") == self.current_cat]
        prods = sorted(prods, key=lambda p: p.get("order",0))

        if not prods:
            lbl = QLabel("商品がありません\n[商品設定] から追加してください")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(f"color:{TEXT_MUTED};padding:40px;border:none;")
            self.prod_vl.insertWidget(0, lbl)
            return

        for p in prods:
            card = ProductCard(p)
            card.changed.connect(self._on_card_changed)
            if p["id"] in self.cart:
                card.blockSignals(True)
                card.set_quantity(self.cart[p["id"]])
                card.blockSignals(False)
            self.product_cards[p["id"]] = card
            self.prod_vl.insertWidget(self.prod_vl.count()-1, card)

    def _on_card_changed(self):
        for pid, card in self.product_cards.items():
            qty = card.get_quantity()
            if qty > 0:
                self.cart[pid] = qty
            else:
                self.cart.pop(pid, None)
        self._rebuild_cart()
        self._update_total()

    # ---- カート ----
    def _rebuild_cart(self):
        while self.cart_vl.count() > 1:
            item = self.cart_vl.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        prod_map = {p["id"]: p for p in self.config.get("products",[])}
        if not self.cart:
            lbl = QLabel("商品を選択してください")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(f"color:{TEXT_MUTED};padding:20px;border:none;")
            self.cart_vl.insertWidget(0, lbl)
            return

        for pid, qty in self.cart.items():
            prod = prod_map.get(pid)
            if not prod: continue
            row = CartRow(prod, qty)
            row.remove_requested.connect(self._cart_remove)
            row.qty_changed.connect(self._cart_qty_changed)
            self.cart_vl.insertWidget(self.cart_vl.count()-1, row)

    def _cart_remove(self, pid):
        self.cart.pop(pid, None)
        card = self.product_cards.get(pid)
        if card:
            card.blockSignals(True); card.reset(); card.blockSignals(False)
        self._rebuild_cart(); self._update_total()

    def _cart_qty_changed(self, pid, qty):
        if qty <= 0:
            self._cart_remove(pid); return
        self.cart[pid] = qty
        card = self.product_cards.get(pid)
        if card and card.product["input_type"] == "quantity":
            card.blockSignals(True); card.set_quantity(qty); card.blockSignals(False)
        self._rebuild_cart(); self._update_total()

    # ---- 合計計算 ----
    def _update_total(self):
        prod_map = {p["id"]: p for p in self.config.get("products",[])}
        subtotal = sum(prod_map[pid]["price"]*qty for pid, qty in self.cart.items() if pid in prod_map)
        dv = self.discount_value
        dis = int(subtotal * dv / 100) if self.discount_type == "percent" else int(dv)
        total = max(0, subtotal - dis)
        self._total_value = total
        self.lbl_subtotal.setText(f"小計  ¥{subtotal:,}")
        self.lbl_dis.setText(f"値引き  −¥{dis:,}")
        self.lbl_total.setText(f"¥{total:,}")

    def _on_dis_type(self):
        if self.rb_percent.isChecked():
            self.discount_type = "percent"
            self.dis_input.setPrefix(""); self.dis_input.setSuffix(" %")
            self.dis_input.setRange(0, 100)
        else:
            self.discount_type = "fixed"
            self.dis_input.setPrefix("¥"); self.dis_input.setSuffix("")
            self.dis_input.setRange(0, 9999999)
        self.dis_input.setValue(0); self._update_total()

    def _on_dis_val(self, v):
        self.discount_value = v; self._update_total()

    # ---- コピー・リセット ----
    def _copy_total(self):
        QApplication.clipboard().setText(str(self._total_value))
        self.btn_copy.setText("コピーしました  ✓")
        self.btn_copy.setEnabled(False)
        QTimer.singleShot(1200, lambda: (
            self.btn_copy.setText("金額をコピー"),
            self.btn_copy.setEnabled(True)
        ))

    def _reset_all(self):
        if QMessageBox.question(
            self, "確認", "カートをリセットしますか？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes: return
        self.cart.clear()
        for card in self.product_cards.values():
            card.blockSignals(True); card.reset(); card.blockSignals(False)
        self.dis_input.setValue(0)
        self._rebuild_cart(); self._update_total()

    # ---- 設定 ----
    def _load_cfg(self):
        path, _ = QFileDialog.getOpenFileName(self, "設定ファイルを選択", "", "JSON (*.json)")
        if not path: return
        try:
            self.config = load_config(path)
            self.cart.clear(); self.current_cat = None
            self.lbl_shop.setText(self.config.get("shop_name","ショップ"))
            self._refresh_products(); self._rebuild_cart(); self._update_total()
            QMessageBox.information(self, "読込完了", f"読み込みました：\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "エラー", str(e))

    def _save_cfg(self):
        path, _ = QFileDialog.getSaveFileName(self, "保存先を選択", "config.json", "JSON (*.json)")
        if not path: return
        try:
            save_config(self.config, path)
            QMessageBox.information(self, "保存完了", f"保存しました：\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "エラー", str(e))

    def _open_settings(self):
        dlg = SettingsDialog(self.config, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.config = dlg.config
            self.cart.clear(); self.current_cat = None
            self.lbl_shop.setText(self.config.get("shop_name","ショップ"))
            save_config(self.config)
            self._refresh_products(); self._rebuild_cart(); self._update_total()


# ============================================================
# 設定ダイアログ
# ============================================================
class SettingsDialog(QDialog):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = copy.deepcopy(config)
        self.setWindowTitle("商品設定")
        self.setMinimumSize(780, 540)
        self.setStyleSheet(SS)
        self._build()
        self._reload_cats()
        self._reload_prods()

    def _build(self):
        vl = QVBoxLayout(self)
        vl.setContentsMargins(16,16,16,16); vl.setSpacing(10)

        row = QHBoxLayout(); row.addWidget(QLabel("ショップ名："))
        self.shop_inp = QLineEdit(self.config.get("shop_name",""))
        self.shop_inp.textChanged.connect(lambda t: self.config.update({"shop_name": t}))
        row.addWidget(self.shop_inp); vl.addLayout(row)

        tabs = QTabWidget()
        tabs.addTab(self._build_cat_tab(), "カテゴリ管理")
        tabs.addTab(self._build_prod_tab(), "商品管理")
        vl.addWidget(tabs, stretch=1)

        btn_row = QHBoxLayout(); btn_row.addStretch()
        bc = QPushButton("キャンセル"); bc.clicked.connect(self.reject)
        bo = QPushButton("保存して閉じる"); bo.setObjectName("btnPrimary"); bo.clicked.connect(self.accept)
        btn_row.addWidget(bc); btn_row.addWidget(bo); vl.addLayout(btn_row)

    # ---- カテゴリタブ ----
    def _build_cat_tab(self):
        w = QWidget(); hl = QHBoxLayout(w); hl.setSpacing(12)
        self.cat_list = QListWidget()
        self.cat_list.currentRowChanged.connect(self._on_cat_sel)
        hl.addWidget(self.cat_list, stretch=1)

        right = QVBoxLayout()
        grp = QGroupBox("カテゴリ情報"); fl = QFormLayout(grp)
        self.cat_name_inp = QLineEdit()
        fl.addRow("カテゴリ名：", self.cat_name_inp)
        right.addWidget(grp); right.addStretch()

        for lbl, oid, slot in [
            ("＋ 追加",  "btnPrimary",  self._cat_add),
            ("✏ 更新",   "btnSm",       self._cat_update),
            ("🗑 削除",  "btnSmDanger", self._cat_del),
            ("▲ 上へ",  "btnSm",       lambda: self._cat_move(-1)),
            ("▼ 下へ",  "btnSm",       lambda: self._cat_move(1)),
        ]:
            b = QPushButton(lbl); b.setObjectName(oid); b.setFixedHeight(34)
            b.clicked.connect(slot); right.addWidget(b)
        hl.addLayout(right); return w

    def _reload_cats(self):
        self.cat_list.clear()
        for c in sorted(self.config.get("categories",[]), key=lambda x: x.get("order",0)):
            self.cat_list.addItem(c["name"])
        self._reload_cat_combo()

    def _on_cat_sel(self, row):
        cats = sorted(self.config.get("categories",[]), key=lambda x: x.get("order",0))
        if 0 <= row < len(cats): self.cat_name_inp.setText(cats[row]["name"])

    def _cat_add(self):
        name = self.cat_name_inp.text().strip()
        if not name: QMessageBox.warning(self, "エラー", "カテゴリ名を入力してください"); return
        cats = self.config.setdefault("categories",[])
        cats.append({"id": uuid.uuid4().hex[:8], "name": name,
                     "order": max((c.get("order",0) for c in cats), default=-1)+1})
        self.cat_name_inp.clear(); self._reload_cats()

    def _cat_update(self):
        row = self.cat_list.currentRow()
        cats = sorted(self.config.get("categories",[]), key=lambda x: x.get("order",0))
        if row < 0 or row >= len(cats): return
        name = self.cat_name_inp.text().strip()
        if not name: return
        tid = cats[row]["id"]
        for c in self.config["categories"]:
            if c["id"] == tid: c["name"] = name; break
        self._reload_cats(); self.cat_list.setCurrentRow(row)

    def _cat_del(self):
        row = self.cat_list.currentRow()
        cats = sorted(self.config.get("categories",[]), key=lambda x: x.get("order",0))
        if row < 0 or row >= len(cats): return
        tid = cats[row]["id"]
        for p in self.config.get("products",[]): 
            if p.get("category_id") == tid: p["category_id"] = ""
        self.config["categories"] = [c for c in self.config["categories"] if c["id"] != tid]
        self._reload_cats()

    def _cat_move(self, d):
        row = self.cat_list.currentRow()
        cats = sorted(self.config["categories"], key=lambda x: x.get("order",0))
        new = row + d
        if new < 0 or new >= len(cats): return
        cats[row]["order"], cats[new]["order"] = cats[new]["order"], cats[row]["order"]
        self._reload_cats(); self.cat_list.setCurrentRow(new)

    # ---- 商品タブ ----
    def _build_prod_tab(self):
        w = QWidget(); hl = QHBoxLayout(w); hl.setSpacing(12)
        self.prod_list = QListWidget()
        self.prod_list.currentRowChanged.connect(self._on_prod_sel)
        hl.addWidget(self.prod_list, stretch=1)

        right = QVBoxLayout()
        grp = QGroupBox("商品情報"); fl = QFormLayout(grp)
        self.prod_name_inp  = QLineEdit()
        self.prod_price_inp = QLineEdit()
        self.prod_price_inp.setValidator(QIntValidator(0, 99999999))
        self.prod_type_cb = QComboBox()
        self.prod_type_cb.addItem("数量入力 （＋／－）", "quantity")
        self.prod_type_cb.addItem("ON/OFFトグル",       "checkbox")
        self.prod_cat_cb = QComboBox()
        fl.addRow("商品名：",    self.prod_name_inp)
        fl.addRow("価格（円）：", self.prod_price_inp)
        fl.addRow("入力方式：",   self.prod_type_cb)
        fl.addRow("カテゴリ：",   self.prod_cat_cb)
        right.addWidget(grp); right.addStretch()

        for lbl, oid, slot in [
            ("＋ 追加",  "btnPrimary",  self._prod_add),
            ("✏ 更新",   "btnSm",       self._prod_update),
            ("🗑 削除",  "btnSmDanger", self._prod_del),
            ("▲ 上へ",  "btnSm",       lambda: self._prod_move(-1)),
            ("▼ 下へ",  "btnSm",       lambda: self._prod_move(1)),
        ]:
            b = QPushButton(lbl); b.setObjectName(oid); b.setFixedHeight(34)
            b.clicked.connect(slot); right.addWidget(b)
        hl.addLayout(right); return w

    def _reload_cat_combo(self):
        self.prod_cat_cb.clear()
        self.prod_cat_cb.addItem("（未分類）", "")
        for c in sorted(self.config.get("categories",[]), key=lambda x: x.get("order",0)):
            self.prod_cat_cb.addItem(c["name"], c["id"])

    def _reload_prods(self):
        self.prod_list.clear()
        cat_map = {c["id"]: c["name"] for c in self.config.get("categories",[])}
        for p in sorted(self.config.get("products",[]), key=lambda x: x.get("order",0)):
            cat = cat_map.get(p.get("category_id",""), "未分類")
            self.prod_list.addItem(f'{p["name"]}  ¥{p["price"]:,}  [{cat}]')

    def _on_prod_sel(self, row):
        prods = sorted(self.config.get("products",[]), key=lambda x: x.get("order",0))
        if row < 0 or row >= len(prods): return
        p = prods[row]
        self.prod_name_inp.setText(p["name"])
        self.prod_price_inp.setText(str(p["price"]))
        idx = self.prod_type_cb.findData(p.get("input_type","quantity"))
        if idx >= 0: self.prod_type_cb.setCurrentIndex(idx)
        idx2 = self.prod_cat_cb.findData(p.get("category_id",""))
        if idx2 >= 0: self.prod_cat_cb.setCurrentIndex(idx2)

    def _prod_add(self):
        name = self.prod_name_inp.text().strip()
        price_s = self.prod_price_inp.text().strip()
        if not name or not price_s:
            QMessageBox.warning(self, "エラー", "商品名と価格を入力してください"); return
        prods = self.config.setdefault("products",[])
        prods.append({
            "id": uuid.uuid4().hex[:8], "name": name, "price": int(price_s),
            "input_type": self.prod_type_cb.currentData(),
            "category_id": self.prod_cat_cb.currentData(),
            "order": max((p.get("order",0) for p in prods), default=-1)+1
        })
        self._reload_prods()

    def _prod_update(self):
        row = self.prod_list.currentRow()
        prods = sorted(self.config.get("products",[]), key=lambda x: x.get("order",0))
        if row < 0 or row >= len(prods): return
        name = self.prod_name_inp.text().strip()
        price_s = self.prod_price_inp.text().strip()
        if not name or not price_s: return
        tid = prods[row]["id"]
        for p in self.config["products"]:
            if p["id"] == tid:
                p["name"] = name; p["price"] = int(price_s)
                p["input_type"] = self.prod_type_cb.currentData()
                p["category_id"] = self.prod_cat_cb.currentData()
                break
        self._reload_prods(); self.prod_list.setCurrentRow(row)

    def _prod_del(self):
        row = self.prod_list.currentRow()
        prods = sorted(self.config.get("products",[]), key=lambda x: x.get("order",0))
        if row < 0 or row >= len(prods): return
        tid = prods[row]["id"]
        self.config["products"] = [p for p in self.config["products"] if p["id"] != tid]
        self._reload_prods()

    def _prod_move(self, d):
        row = self.prod_list.currentRow()
        prods = sorted(self.config["products"], key=lambda x: x.get("order",0))
        new = row + d
        if new < 0 or new >= len(prods): return
        prods[row]["order"], prods[new]["order"] = prods[new]["order"], prods[row]["order"]
        self._reload_prods(); self.prod_list.setCurrentRow(new)


# ============================================================
# エントリポイント
# ============================================================
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Yu Gothic UI", 10))
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
