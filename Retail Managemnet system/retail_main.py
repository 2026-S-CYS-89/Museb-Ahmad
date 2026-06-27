"""
main.py  —  Retail Management System
======================================
PyQt5 desktop application with:
  • Products   : Add / Edit / Delete product catalog
  • Sales      : Billing — add items to cart, generate bill
  • Inventory  : Stock levels + low stock alerts
  • Customers  : Customer records management

Database : SQLite  (retail_store.db  — single file)
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QGroupBox, QFormLayout, QLabel, QLineEdit, QComboBox,
    QSpinBox, QDoubleSpinBox, QPushButton, QTableWidget, QTableWidgetItem,
    QTextEdit, QMessageBox, QHeaderView, QAbstractItemView, QSplitter,
    QDialog, QDialogButtonBox, QScrollArea
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor
import retail_db as db

# ==============================================================
#  STYLESHEET  (same dark Catppuccin theme as CGPA project)
# ==============================================================
APP_STYLE = """
QWidget {
    background-color: #1E1E2E;
    color: #CDD6F4;
    font-family: "Segoe UI", sans-serif;
    font-size: 13px;
}
QTabWidget::pane {
    border: 1px solid #45475A;
    border-radius: 8px;
    padding: 8px;
}
QTabBar::tab {
    background-color: #313244;
    color: #CDD6F4;
    padding: 10px 24px;
    border-radius: 6px 6px 0 0;
    margin-right: 2px;
    font-weight: 600;
}
QTabBar::tab:selected {
    background-color: #CBA6F7;
    color: #1E1E2E;
}
QTabBar::tab:hover:!selected { background-color: #45475A; }
QGroupBox {
    border: 1px solid #45475A;
    border-radius: 8px;
    margin-top: 14px;
    font-weight: 600;
    color: #89B4FA;
    padding: 8px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    color: #89B4FA;
}
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
    background-color: #313244;
    border: 1px solid #45475A;
    border-radius: 6px;
    padding: 6px 10px;
    color: #CDD6F4;
    min-height: 20px;
}
QLineEdit:focus, QComboBox:focus,
QSpinBox:focus, QDoubleSpinBox:focus { border-color: #CBA6F7; }
QComboBox::drop-down { border: none; }
QComboBox QAbstractItemView {
    background-color: #313244;
    selection-background-color: #585B70;
}
QPushButton {
    background-color: #45475A;
    border: none;
    border-radius: 8px;
    padding: 9px 16px;
    color: #CDD6F4;
    font-weight: 600;
}
QPushButton:hover   { background-color: #585B70; }
QPushButton:pressed { background-color: #6C7086; }
QPushButton#btn_green  { background-color: #40A02B; color: #E6E9EF; }
QPushButton#btn_green:hover  { background-color: #4ABE33; }
QPushButton#btn_blue   { background-color: #1E66F5; color: #E6E9EF; }
QPushButton#btn_blue:hover   { background-color: #3B7AF5; }
QPushButton#btn_purple { background-color: #7287FD; color: #E6E9EF; }
QPushButton#btn_purple:hover { background-color: #8899FF; }
QPushButton#btn_red    { background-color: #E64553; color: #E6E9EF; }
QPushButton#btn_red:hover    { background-color: #EE5A66; }
QPushButton#btn_yellow { background-color: #DF8E1D; color: #E6E9EF; }
QPushButton#btn_yellow:hover { background-color: #E8A020; }
QTableWidget {
    background-color: #181825;
    gridline-color: #45475A;
    border: none;
    border-radius: 6px;
    alternate-background-color: #1E1E2E;
}
QTableWidget::item { padding: 4px; }
QTableWidget::item:selected {
    background-color: #313244;
    color: #CDD6F4;
}
QHeaderView::section {
    background-color: #313244;
    color: #89B4FA;
    font-weight: 700;
    padding: 7px;
    border: none;
    border-bottom: 1px solid #45475A;
}
QTextEdit {
    background-color: #181825;
    border: 1px solid #45475A;
    border-radius: 6px;
    padding: 8px;
    color: #CDD6F4;
    font-family: "Consolas", monospace;
    font-size: 12px;
}
QLabel#title_label {
    font-size: 22px;
    font-weight: 700;
    color: #CBA6F7;
    padding: 8px 0;
}
QLabel#stat_label {
    font-size: 18px;
    font-weight: 700;
    color: #A6E3A1;
    padding: 6px;
    background-color: #181825;
    border-radius: 8px;
    border: 1px solid #45475A;
}
QLabel#warn_label {
    font-size: 13px;
    color: #FAB387;
    font-weight: 600;
}
QLabel#status_bar {
    color: #6C7086;
    font-size: 11px;
    padding: 3px 6px;
    border-top: 1px solid #313244;
}
"""

CATEGORIES = ["Electronics", "Clothing", "Food & Grocery",
               "Furniture", "Stationery", "Medicine", "Other"]


# ==============================================================
#  MAIN WINDOW
# ==============================================================
class RetailManagementSystem(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Retail Management System")
        self.resize(1100, 750)
        self._cart = []          # list of cart items for current sale
        self._edit_product_id = None

        db.initialize_db()
        self._build_ui()
        self._refresh_all()

    # ----------------------------------------------------------
    #  BUILD UI
    # ----------------------------------------------------------
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 16, 16, 8)
        root.setSpacing(10)

        # Title
        title = QLabel("🏪  Retail Management System")
        title.setObjectName("title_label")
        title.setAlignment(Qt.AlignCenter)
        root.addWidget(title)

        # Tab Widget
        self.tabs = QTabWidget()
        root.addWidget(self.tabs)

        self._build_dashboard_tab()
        self._build_products_tab()
        self._build_sales_tab()
        self._build_inventory_tab()
        self._build_customers_tab()

        # Status bar
        self.lbl_status = QLabel("Ready.")
        self.lbl_status.setObjectName("status_bar")
        root.addWidget(self.lbl_status)

    # ── DASHBOARD ─────────────────────────────────────────────
    def _build_dashboard_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)

        # Stat cards row
        stats_row = QHBoxLayout()
        self.lbl_total_products  = self._stat_card("📦 Total Products",  "0")
        self.lbl_total_customers = self._stat_card("👥 Customers",        "0")
        self.lbl_total_sales     = self._stat_card("🧾 Total Sales",      "0")
        self.lbl_total_revenue   = self._stat_card("💰 Revenue (Rs.)",    "0.00")
        for card in [self.lbl_total_products, self.lbl_total_customers,
                     self.lbl_total_sales, self.lbl_total_revenue]:
            stats_row.addWidget(card)
        layout.addLayout(stats_row)

        # Recent sales table
        grp = QGroupBox("📋  Recent Sales")
        g_layout = QVBoxLayout(grp)
        self.tbl_recent_sales = self._make_table(
            ["Sale ID", "Customer", "Total (Rs.)", "Date"])
        g_layout.addWidget(self.tbl_recent_sales)
        layout.addWidget(grp)

        # Low stock warning
        grp2 = QGroupBox("⚠️  Low Stock Alerts  (≤ 5 units)")
        g2_layout = QVBoxLayout(grp2)
        self.tbl_low_stock = self._make_table(
            ["Product", "Category", "Stock Remaining"])
        g2_layout.addWidget(self.tbl_low_stock)
        layout.addWidget(grp2)

        btn_refresh = QPushButton("🔄  Refresh Dashboard")
        btn_refresh.setObjectName("btn_blue")
        btn_refresh.clicked.connect(self._refresh_all)
        layout.addWidget(btn_refresh)

        self.tabs.addTab(tab, "📊 Dashboard")

    def _stat_card(self, label_text, value):
        w = QWidget()
        v = QVBoxLayout(w)
        lbl = QLabel(label_text)
        lbl.setAlignment(Qt.AlignCenter)
        val = QLabel(value)
        val.setObjectName("stat_label")
        val.setAlignment(Qt.AlignCenter)
        v.addWidget(lbl)
        v.addWidget(val)
        w._value_label = val
        return w

    # ── PRODUCTS ──────────────────────────────────────────────
    def _build_products_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)

        # Left: form
        form_widget = QWidget()
        form_widget.setMaximumWidth(320)
        form_layout = QVBoxLayout(form_widget)

        grp = QGroupBox("➕  Add / Edit Product")
        form = QFormLayout(grp)

        self.txt_prod_name = QLineEdit()
        self.txt_prod_name.setPlaceholderText("e.g., Samsung TV 42\"")
        form.addRow("Product Name:", self.txt_prod_name)

        self.cmb_prod_cat = QComboBox()
        for c in CATEGORIES:
            self.cmb_prod_cat.addItem(c)
        form.addRow("Category:", self.cmb_prod_cat)

        self.spn_prod_price = QDoubleSpinBox()
        self.spn_prod_price.setMaximum(9999999)
        self.spn_prod_price.setPrefix("Rs. ")
        self.spn_prod_price.setDecimals(2)
        form.addRow("Price:", self.spn_prod_price)

        self.spn_prod_stock = QSpinBox()
        self.spn_prod_stock.setMaximum(99999)
        form.addRow("Stock (units):", self.spn_prod_stock)

        form_layout.addWidget(grp)

        btn_row = QHBoxLayout()
        self.btn_save_product = QPushButton("💾  Save Product")
        self.btn_save_product.setObjectName("btn_green")
        self.btn_save_product.clicked.connect(self._on_save_product)

        self.btn_clear_prod = QPushButton("🔄  Clear")
        self.btn_clear_prod.clicked.connect(self._clear_product_form)

        btn_row.addWidget(self.btn_save_product)
        btn_row.addWidget(self.btn_clear_prod)
        form_layout.addLayout(btn_row)

        self.btn_delete_product = QPushButton("🗑️  Delete Selected")
        self.btn_delete_product.setObjectName("btn_red")
        self.btn_delete_product.clicked.connect(self._on_delete_product)
        form_layout.addWidget(self.btn_delete_product)
        form_layout.addStretch()

        layout.addWidget(form_widget)

        # Right: table
        right = QWidget()
        r_layout = QVBoxLayout(right)
        grp2 = QGroupBox("📦  Product Catalog")
        g2 = QVBoxLayout(grp2)
        self.tbl_products = self._make_table(
            ["ID", "Name", "Category", "Price (Rs.)", "Stock"])
        self.tbl_products.cellClicked.connect(self._on_product_row_click)
        g2.addWidget(self.tbl_products)
        r_layout.addWidget(grp2)
        layout.addWidget(right)

        self.tabs.addTab(tab, "📦 Products")

    # ── SALES / BILLING ───────────────────────────────────────
    def _build_sales_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Top: customer + product selector
        top = QHBoxLayout()

        grp_cust = QGroupBox("👤  Customer")
        cust_form = QFormLayout(grp_cust)
        self.txt_sale_customer = QLineEdit()
        self.txt_sale_customer.setPlaceholderText("Customer name (optional)")
        cust_form.addRow("Name:", self.txt_sale_customer)
        top.addWidget(grp_cust)

        grp_item = QGroupBox("🛒  Add Item to Cart")
        item_form = QFormLayout(grp_item)
        self.cmb_sale_product = QComboBox()
        item_form.addRow("Product:", self.cmb_sale_product)
        self.spn_sale_qty = QSpinBox()
        self.spn_sale_qty.setMinimum(1)
        self.spn_sale_qty.setMaximum(9999)
        item_form.addRow("Quantity:", self.spn_sale_qty)
        self.lbl_unit_price = QLabel("Unit Price: Rs. 0.00")
        item_form.addRow(self.lbl_unit_price)
        self.cmb_sale_product.currentIndexChanged.connect(self._on_product_selected)
        top.addWidget(grp_item)

        btn_add_cart = QPushButton("➕  Add to Cart")
        btn_add_cart.setObjectName("btn_green")
        btn_add_cart.clicked.connect(self._on_add_to_cart)
        top.addWidget(btn_add_cart)

        layout.addLayout(top)

        # Cart table
        grp_cart = QGroupBox("🛒  Cart")
        cart_layout = QVBoxLayout(grp_cart)
        self.tbl_cart = self._make_table(
            ["Product", "Qty", "Unit Price", "Subtotal"])
        cart_layout.addWidget(self.tbl_cart)
        layout.addWidget(grp_cart)

        # Bottom: total + buttons
        bot = QHBoxLayout()
        self.lbl_cart_total = QLabel("Total:  Rs. 0.00")
        f = QFont(); f.setPointSize(16); f.setBold(True)
        self.lbl_cart_total.setFont(f)
        self.lbl_cart_total.setStyleSheet("color: #A6E3A1;")
        bot.addWidget(self.lbl_cart_total)
        bot.addStretch()

        btn_remove = QPushButton("❌  Remove Item")
        btn_remove.setObjectName("btn_yellow")
        btn_remove.clicked.connect(self._on_remove_cart_item)

        btn_clear_cart = QPushButton("🗑️  Clear Cart")
        btn_clear_cart.setObjectName("btn_red")
        btn_clear_cart.clicked.connect(self._on_clear_cart)

        btn_checkout = QPushButton("✅  Checkout & Generate Bill")
        btn_checkout.setObjectName("btn_blue")
        btn_checkout.clicked.connect(self._on_checkout)

        for b in [btn_remove, btn_clear_cart, btn_checkout]:
            bot.addWidget(b)
        layout.addLayout(bot)

        self.tabs.addTab(tab, "🧾 Sales & Billing")

    # ── INVENTORY ─────────────────────────────────────────────
    def _build_inventory_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Summary stats
        stats = QHBoxLayout()
        self.lbl_inv_total    = self._stat_card("📦 Total Products", "0")
        self.lbl_inv_stock    = self._stat_card("🔢 Total Units",    "0")
        self.lbl_inv_lowstock = self._stat_card("⚠️ Low Stock",      "0")
        self.lbl_inv_value    = self._stat_card("💰 Stock Value",    "Rs. 0")
        for card in [self.lbl_inv_total, self.lbl_inv_stock,
                     self.lbl_inv_lowstock, self.lbl_inv_value]:
            stats.addWidget(card)
        layout.addLayout(stats)

        grp = QGroupBox("📋  Full Inventory")
        g = QVBoxLayout(grp)
        self.tbl_inventory = self._make_table(
            ["ID", "Product", "Category", "Price", "Stock", "Stock Value", "Status"])
        g.addWidget(self.tbl_inventory)
        layout.addWidget(grp)

        btn_refresh = QPushButton("🔄  Refresh Inventory")
        btn_refresh.setObjectName("btn_purple")
        btn_refresh.clicked.connect(self._refresh_inventory)
        layout.addWidget(btn_refresh)

        self.tabs.addTab(tab, "📋 Inventory")

    # ── CUSTOMERS ─────────────────────────────────────────────
    def _build_customers_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)

        # Left: form
        form_widget = QWidget()
        form_widget.setMaximumWidth(300)
        form_layout = QVBoxLayout(form_widget)

        grp = QGroupBox("➕  Add Customer")
        form = QFormLayout(grp)

        self.txt_cust_name = QLineEdit()
        self.txt_cust_name.setPlaceholderText("Full name")
        form.addRow("Name:", self.txt_cust_name)

        self.txt_cust_phone = QLineEdit()
        self.txt_cust_phone.setPlaceholderText("03xx-xxxxxxx")
        form.addRow("Phone:", self.txt_cust_phone)

        self.txt_cust_email = QLineEdit()
        self.txt_cust_email.setPlaceholderText("email@example.com")
        form.addRow("Email:", self.txt_cust_email)

        form_layout.addWidget(grp)

        btn_add_cust = QPushButton("💾  Add Customer")
        btn_add_cust.setObjectName("btn_green")
        btn_add_cust.clicked.connect(self._on_add_customer)
        form_layout.addWidget(btn_add_cust)

        btn_del_cust = QPushButton("🗑️  Delete Selected")
        btn_del_cust.setObjectName("btn_red")
        btn_del_cust.clicked.connect(self._on_delete_customer)
        form_layout.addWidget(btn_del_cust)
        form_layout.addStretch()

        layout.addWidget(form_widget)

        # Right: table
        right = QWidget()
        r_layout = QVBoxLayout(right)
        grp2 = QGroupBox("👥  Customer Records")
        g2 = QVBoxLayout(grp2)
        self.tbl_customers = self._make_table(
            ["ID", "Name", "Phone", "Email", "Joined"])
        g2.addWidget(self.tbl_customers)
        r_layout.addWidget(grp2)
        layout.addWidget(right)

        self.tabs.addTab(tab, "👥 Customers")

    # ----------------------------------------------------------
    #  HELPER: make a standard table
    # ----------------------------------------------------------
    def _make_table(self, headers):
        tbl = QTableWidget(0, len(headers))
        tbl.setHorizontalHeaderLabels(headers)
        tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
        tbl.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tbl.setAlternatingRowColors(True)
        tbl.verticalHeader().setVisible(False)
        h = tbl.horizontalHeader()
        for i in range(len(headers)):
            h.setSectionResizeMode(i, QHeaderView.Stretch)
        return tbl

    def _fill_table(self, tbl, rows):
        tbl.setRowCount(0)
        for row_data in rows:
            row = tbl.rowCount()
            tbl.insertRow(row)
            for col, val in enumerate(row_data):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                tbl.setItem(row, col, item)

    def _set_status(self, msg):
        self.lbl_status.setText(msg)

    # ----------------------------------------------------------
    #  REFRESH ALL
    # ----------------------------------------------------------
    def _refresh_all(self):
        self._refresh_products()
        self._refresh_customers()
        self._refresh_inventory()
        self._refresh_dashboard()
        self._refresh_sale_product_combo()

    def _refresh_dashboard(self):
        products  = db.get_all_products()
        customers = db.get_all_customers()
        sales     = db.get_all_sales()
        revenue   = db.get_total_revenue()
        low_stock = db.get_low_stock_products()

        self.lbl_total_products ._value_label.setText(str(len(products)))
        self.lbl_total_customers._value_label.setText(str(len(customers)))
        self.lbl_total_sales    ._value_label.setText(str(len(sales)))
        self.lbl_total_revenue  ._value_label.setText(f"{revenue:,.2f}")

        # Recent 10 sales
        recent = sales[:10]
        self._fill_table(self.tbl_recent_sales, [
            (s["id"], s["customer_name"] or "Walk-in",
             f"Rs. {s['total_amount']:,.2f}", s["sale_date"])
            for s in recent
        ])

        # Low stock
        self._fill_table(self.tbl_low_stock, [
            (p["name"], p["category"], p["stock"])
            for p in low_stock
        ])

    def _refresh_products(self):
        products = db.get_all_products()
        self._fill_table(self.tbl_products, [
            (p["id"], p["name"], p["category"],
             f"Rs. {p['price']:,.2f}", p["stock"])
            for p in products
        ])
        # Colour low-stock rows red
        for row in range(self.tbl_products.rowCount()):
            stock_item = self.tbl_products.item(row, 4)
            if stock_item and int(stock_item.text()) <= 5:
                for col in range(self.tbl_products.columnCount()):
                    it = self.tbl_products.item(row, col)
                    if it:
                        it.setForeground(QColor("#F38BA8"))

    def _refresh_customers(self):
        customers = db.get_all_customers()
        self._fill_table(self.tbl_customers, [
            (c["id"], c["name"], c["phone"] or "—",
             c["email"] or "—", c["created_at"][:10])
            for c in customers
        ])

    def _refresh_inventory(self):
        products = db.get_all_products()
        total_units = sum(p["stock"] for p in products)
        low_count   = sum(1 for p in products if p["stock"] <= 5)
        total_value = sum(p["stock"] * p["price"] for p in products)

        self.lbl_inv_total   ._value_label.setText(str(len(products)))
        self.lbl_inv_stock   ._value_label.setText(str(total_units))
        self.lbl_inv_lowstock._value_label.setText(str(low_count))
        self.lbl_inv_value   ._value_label.setText(f"Rs. {total_value:,.0f}")

        rows = []
        for p in products:
            val    = p["stock"] * p["price"]
            status = "✅ OK" if p["stock"] > 5 else ("⚠️ Low" if p["stock"] > 0 else "❌ Out")
            rows.append((p["id"], p["name"], p["category"],
                         f"Rs. {p['price']:,.2f}", p["stock"],
                         f"Rs. {val:,.2f}", status))
        self._fill_table(self.tbl_inventory, rows)

        # Colour status column
        for row in range(self.tbl_inventory.rowCount()):
            it = self.tbl_inventory.item(row, 6)
            if it:
                if "Out" in it.text():
                    it.setForeground(QColor("#F38BA8"))
                elif "Low" in it.text():
                    it.setForeground(QColor("#FAB387"))
                else:
                    it.setForeground(QColor("#A6E3A1"))

    def _refresh_sale_product_combo(self):
        self.cmb_sale_product.blockSignals(True)
        self.cmb_sale_product.clear()
        for p in db.get_all_products():
            if p["stock"] > 0:
                self.cmb_sale_product.addItem(
                    f"{p['name']}  (Stock: {p['stock']})", userData=p)
        self.cmb_sale_product.blockSignals(False)
        self._on_product_selected()

    # ----------------------------------------------------------
    #  PRODUCT SLOTS
    # ----------------------------------------------------------
    def _on_save_product(self):
        name  = self.txt_prod_name.text().strip()
        cat   = self.cmb_prod_cat.currentText()
        price = self.spn_prod_price.value()
        stock = self.spn_prod_stock.value()

        if not name:
            QMessageBox.warning(self, "Input Error", "Product name cannot be empty.")
            return
        if price <= 0:
            QMessageBox.warning(self, "Input Error", "Price must be greater than 0.")
            return

        if self._edit_product_id:
            db.update_product(self._edit_product_id, name, cat, price, stock)
            self._set_status(f"✅  Product updated: {name}")
            self._edit_product_id = None
            self.btn_save_product.setText("💾  Save Product")
        else:
            db.add_product(name, cat, price, stock)
            self._set_status(f"✅  Product added: {name}")

        self._clear_product_form()
        self._refresh_products()
        self._refresh_sale_product_combo()
        self._refresh_dashboard()
        self._refresh_inventory()

    def _on_product_row_click(self, row, col):
        """Load selected product into form for editing."""
        id_item = self.tbl_products.item(row, 0)
        if not id_item:
            return
        self._edit_product_id = int(id_item.text())
        self.txt_prod_name.setText(self.tbl_products.item(row, 1).text())
        cat = self.tbl_products.item(row, 2).text()
        idx = self.cmb_prod_cat.findText(cat)
        if idx >= 0:
            self.cmb_prod_cat.setCurrentIndex(idx)
        price_text = self.tbl_products.item(row, 3).text().replace("Rs. ", "").replace(",", "")
        self.spn_prod_price.setValue(float(price_text))
        self.spn_prod_stock.setValue(int(self.tbl_products.item(row, 4).text()))
        self.btn_save_product.setText("✏️  Update Product")
        self._set_status(f"Editing product ID {self._edit_product_id} — make changes and click Update.")

    def _on_delete_product(self):
        row = self.tbl_products.currentRow()
        if row < 0:
            QMessageBox.information(self, "Select Product", "Please select a product to delete.")
            return
        name = self.tbl_products.item(row, 1).text()
        pid  = int(self.tbl_products.item(row, 0).text())
        r = QMessageBox.question(self, "Delete Product",
            f"Delete '{name}'? This cannot be undone.",
            QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.Yes:
            db.delete_product(pid)
            self._refresh_products()
            self._refresh_sale_product_combo()
            self._refresh_dashboard()
            self._refresh_inventory()
            self._set_status(f"🗑️  Deleted product: {name}")

    def _clear_product_form(self):
        self.txt_prod_name.clear()
        self.cmb_prod_cat.setCurrentIndex(0)
        self.spn_prod_price.setValue(0)
        self.spn_prod_stock.setValue(0)
        self._edit_product_id = None
        self.btn_save_product.setText("💾  Save Product")

    # ----------------------------------------------------------
    #  SALES SLOTS
    # ----------------------------------------------------------
    def _on_product_selected(self):
        data = self.cmb_sale_product.currentData()
        if data:
            self.lbl_unit_price.setText(f"Unit Price: Rs. {data['price']:,.2f}")

    def _on_add_to_cart(self):
        data = self.cmb_sale_product.currentData()
        if not data:
            QMessageBox.information(self, "No Products",
                "No products available. Add products first.")
            return
        qty = self.spn_sale_qty.value()
        if qty > data["stock"]:
            QMessageBox.warning(self, "Insufficient Stock",
                f"Only {data['stock']} units available.")
            return

        # Check if already in cart
        for item in self._cart:
            if item["product_id"] == data["id"]:
                item["quantity"]  += qty
                item["subtotal"]   = item["quantity"] * item["unit_price"]
                self._refresh_cart_table()
                return

        self._cart.append({
            "product_id":   data["id"],
            "product_name": data["name"],
            "quantity":     qty,
            "unit_price":   data["price"],
            "subtotal":     qty * data["price"],
        })
        self._refresh_cart_table()
        self._set_status(f"🛒  Added to cart: {data['name']} × {qty}")

    def _refresh_cart_table(self):
        self._fill_table(self.tbl_cart, [
            (i["product_name"], i["quantity"],
             f"Rs. {i['unit_price']:,.2f}",
             f"Rs. {i['subtotal']:,.2f}")
            for i in self._cart
        ])
        total = sum(i["subtotal"] for i in self._cart)
        self.lbl_cart_total.setText(f"Total:  Rs. {total:,.2f}")

    def _on_remove_cart_item(self):
        row = self.tbl_cart.currentRow()
        if row < 0:
            return
        self._cart.pop(row)
        self._refresh_cart_table()

    def _on_clear_cart(self):
        self._cart.clear()
        self._refresh_cart_table()
        self._set_status("🗑️  Cart cleared.")

    def _on_checkout(self):
        if not self._cart:
            QMessageBox.information(self, "Empty Cart",
                "Add items to cart before checkout.")
            return
        customer = self.txt_sale_customer.text().strip() or "Walk-in Customer"
        total    = sum(i["subtotal"] for i in self._cart)

        r = QMessageBox.question(self, "Confirm Sale",
            f"Customer: {customer}\n"
            f"Items: {len(self._cart)}\n"
            f"Total: Rs. {total:,.2f}\n\nProceed?",
            QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.No:
            return

        sale_id = db.create_sale(customer, self._cart)
        self._show_bill(sale_id, customer, total)
        self._cart.clear()
        self.txt_sale_customer.clear()
        self._refresh_cart_table()
        self._refresh_all()
        self._set_status(f"✅  Sale #{sale_id} completed — Rs. {total:,.2f}")

    def _show_bill(self, sale_id, customer, total):
        items = db.get_sale_items(sale_id)
        lines = [
            "=" * 42,
            "       RETAIL MANAGEMENT SYSTEM",
            "            — RECEIPT —",
            "=" * 42,
            f"  Sale ID  : #{sale_id}",
            f"  Customer : {customer}",
            "-" * 42,
            f"  {'Item':<22} {'Qty':>4}  {'Amount':>10}",
            "-" * 42,
        ]
        for it in items:
            lines.append(
                f"  {it['product_name']:<22} {it['quantity']:>4}  "
                f"Rs. {it['subtotal']:>8,.2f}"
            )
        lines += [
            "-" * 42,
            f"  {'TOTAL':>28}  Rs. {total:>8,.2f}",
            "=" * 42,
            "       Thank you for shopping!",
            "=" * 42,
        ]
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Bill — Sale #{sale_id}")
        dlg.resize(420, 400)
        v = QVBoxLayout(dlg)
        txt = QTextEdit()
        txt.setReadOnly(True)
        txt.setPlainText("\n".join(lines))
        v.addWidget(txt)
        btn = QPushButton("Close")
        btn.setObjectName("btn_blue")
        btn.clicked.connect(dlg.accept)
        v.addWidget(btn)
        dlg.exec_()

    # ----------------------------------------------------------
    #  CUSTOMER SLOTS
    # ----------------------------------------------------------
    def _on_add_customer(self):
        name  = self.txt_cust_name.text().strip()
        phone = self.txt_cust_phone.text().strip()
        email = self.txt_cust_email.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Customer name is required.")
            return
        db.add_customer(name, phone, email)
        self.txt_cust_name.clear()
        self.txt_cust_phone.clear()
        self.txt_cust_email.clear()
        self._refresh_customers()
        self._refresh_dashboard()
        self._set_status(f"✅  Customer added: {name}")

    def _on_delete_customer(self):
        row = self.tbl_customers.currentRow()
        if row < 0:
            QMessageBox.information(self, "Select", "Select a customer to delete.")
            return
        name = self.tbl_customers.item(row, 1).text()
        cid  = int(self.tbl_customers.item(row, 0).text())
        r = QMessageBox.question(self, "Delete Customer",
            f"Delete customer '{name}'?",
            QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.Yes:
            db.delete_customer(cid)
            self._refresh_customers()
            self._refresh_dashboard()
            self._set_status(f"🗑️  Deleted customer: {name}")


# ==============================================================
#  ENTRY POINT
# ==============================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)
    window = RetailManagementSystem()
    window.show()
    sys.exit(app.exec_())
