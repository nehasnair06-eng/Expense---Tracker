import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt

from database import (
    create_table,
    add_expense,
    get_expenses,
    delete_expense
)


# -----------------------------
# APP SETTINGS
# -----------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

create_table()


class ExpenseTracker(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Expense Tracker")
        self.geometry("1200x750")
        self.minsize(1000, 650)

        self.configure(fg_color="#0F1117")

        self.selected_expense_id = None

        self.create_ui()
        self.load_expenses()

    # -----------------------------
    # MAIN UI
    # -----------------------------

    def create_ui(self):

        # MAIN CONTAINER
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color="#0F1117"
        )

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # -------------------------
        # HEADER
        # -------------------------

        header = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            pady=(0, 20)
        )

        title = ctk.CTkLabel(
            header,
            text="Expense Tracker",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=30,
                weight="bold"
            ),
            text_color="#FFFFFF"
        )

        title.pack(side="left")

        subtitle = ctk.CTkLabel(
            header,
            text="   Manage your money smarter ✦",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=14
            ),
            text_color="#8B93A7"
        )

        subtitle.pack(side="left", pady=(8, 0))

        add_button = ctk.CTkButton(
            header,
            text="+  Add Expense",
            width=150,
            height=42,
            corner_radius=12,
            fg_color="#6C63FF",
            hover_color="#574FE0",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=self.open_add_window
        )

        add_button.pack(side="right")

        # -------------------------
        # SUMMARY CARDS
        # -------------------------

        cards_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        cards_frame.pack(
            fill="x",
            pady=(0, 20)
        )

        self.total_card = self.create_card(
            cards_frame,
            "TOTAL EXPENSE",
            "₹0.00",
            "#6C63FF"
        )

        self.total_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        self.today_card = self.create_card(
            cards_frame,
            "TODAY",
            "₹0.00",
            "#00C896"
        )

        self.today_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        self.count_card = self.create_card(
            cards_frame,
            "TRANSACTIONS",
            "0",
            "#FFB84D"
        )

        self.count_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        # -------------------------
        # CONTENT
        # -------------------------

        content = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        content.pack(
            fill="both",
            expand=True
        )

        # LEFT SIDE
        left = ctk.CTkFrame(
            content,
            fg_color="#171A23",
            corner_radius=18
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        # Search bar

        search_frame = ctk.CTkFrame(
            left,
            fg_color="transparent"
        )

        search_frame.pack(
            fill="x",
            padx=18,
            pady=18
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍  Search expenses...",
            height=40,
            corner_radius=12,
            fg_color="#20232D",
            border_width=0
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_expenses
        )

        # Recent title

        recent_label = ctk.CTkLabel(
            left,
            text="Recent Transactions",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color="#FFFFFF"
        )

        recent_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        # Scrollable transactions

        self.transaction_frame = ctk.CTkScrollableFrame(
            left,
            fg_color="transparent"
        )

        self.transaction_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        # RIGHT SIDE
        right = ctk.CTkFrame(
            content,
            width=320,
            fg_color="#171A23",
            corner_radius=18
        )

        right.pack(
            side="right",
            fill="y",
            padx=(10, 0)
        )

        right.pack_propagate(False)

        chart_title = ctk.CTkLabel(
            right,
            text="Spending Overview",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color="#FFFFFF"
        )

        chart_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        self.chart_button = ctk.CTkButton(
            right,
            text="📊  View Chart",
            height=42,
            corner_radius=12,
            fg_color="#20232D",
            hover_color="#292D39",
            command=self.show_chart
        )

        self.chart_button.pack(
            fill="x",
            padx=20,
            pady=10
        )

        category_label = ctk.CTkLabel(
            right,
            text="Categories",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        )

        category_label.pack(
            anchor="w",
            padx=20,
            pady=(25, 10)
        )

        self.category_frame = ctk.CTkFrame(
            right,
            fg_color="transparent"
        )

        self.category_frame.pack(
            fill="both",
            expand=True,
            padx=20
        )

    # -----------------------------
    # CARD
    # -----------------------------

    def create_card(
        self,
        parent,
        title,
        value,
        accent
    ):

        card = ctk.CTkFrame(
            parent,
            height=115,
            corner_radius=18,
            fg_color="#171A23"
        )

        card.pack_propagate(False)

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color="#8B93A7"
        )

        title_label.pack(
            anchor="w",
            padx=20,
            pady=(18, 2)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            ),
            text_color=accent
        )

        value_label.pack(
            anchor="w",
            padx=20
        )

        card.value_label = value_label

        return card

    # -----------------------------
    # ADD EXPENSE WINDOW
    # -----------------------------

    def open_add_window(self):

        window = ctk.CTkToplevel(self)

        window.title("Add Expense")
        window.geometry("450x570")
        window.resizable(False, False)

        window.configure(
            fg_color="#11131A"
        )

        title = ctk.CTkLabel(
            window,
            text="Add New Expense",
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        )

        title.pack(
            pady=(30, 5)
        )

        subtitle = ctk.CTkLabel(
            window,
            text="Track where your money goes",
            text_color="#8B93A7"
        )

        subtitle.pack(
            pady=(0, 25)
        )

        # TITLE

        title_entry = ctk.CTkEntry(
            window,
            placeholder_text="Expense title",
            width=350,
            height=45,
            corner_radius=12
        )

        title_entry.pack(pady=8)

        # CATEGORY

        category = ctk.CTkComboBox(
            window,
            values=[
                "Food",
                "Travel",
                "Shopping",
                "Bills",
                "Entertainment",
                "Education",
                "Health",
                "Other"
            ],
            width=350,
            height=45,
            corner_radius=12
        )

        category.set("Food")

        category.pack(pady=8)

        # AMOUNT

        amount_entry = ctk.CTkEntry(
            window,
            placeholder_text="Amount (₹)",
            width=350,
            height=45,
            corner_radius=12
        )

        amount_entry.pack(pady=8)

        # DATE

        date_entry = ctk.CTkEntry(
            window,
            width=350,
            height=45,
            corner_radius=12
        )

        date_entry.insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )

        date_entry.pack(pady=8)

        # DESCRIPTION

        description = ctk.CTkEntry(
            window,
            placeholder_text="Description (optional)",
            width=350,
            height=45,
            corner_radius=12
        )

        description.pack(pady=8)

        def save():

            expense_title = title_entry.get().strip()
            expense_category = category.get()
            amount = amount_entry.get().strip()
            expense_date = date_entry.get().strip()
            expense_description = description.get().strip()

            if not expense_title or not amount:
                messagebox.showwarning(
                    "Missing Information",
                    "Please enter title and amount."
                )
                return

            try:
                amount_value = float(amount)

                if amount_value <= 0:
                    raise ValueError

            except ValueError:

                messagebox.showerror(
                    "Invalid Amount",
                    "Please enter a valid positive amount."
                )

                return

            try:
                datetime.strptime(
                    expense_date,
                    "%Y-%m-%d"
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Date",
                    "Use YYYY-MM-DD format."
                )

                return

            add_expense(
                expense_title,
                expense_category,
                amount_value,
                expense_date,
                expense_description
            )

            window.destroy()

            self.load_expenses()

        save_button = ctk.CTkButton(
            window,
            text="Save Expense",
            width=350,
            height=48,
            corner_radius=12,
            fg_color="#6C63FF",
            hover_color="#574FE0",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=save
        )

        save_button.pack(
            pady=25
        )

    # -----------------------------
    # LOAD EXPENSES
    # -----------------------------

    def load_expenses(self):

        for widget in self.transaction_frame.winfo_children():
            widget.destroy()

        expenses = get_expenses()

        total = 0
        today_total = 0
        today = datetime.now().strftime("%Y-%m-%d")

        categories = {}

        for expense in expenses:

            expense_id = expense[0]
            title = expense[1]
            category = expense[2]
            amount = expense[3]
            date = expense[4]

            total += amount

            if date == today:
                today_total += amount

            categories[category] = (
                categories.get(category, 0) + amount
            )

            self.create_transaction(
                expense_id,
                title,
                category,
                amount,
                date
            )

        self.total_card.value_label.configure(
            text=f"₹{total:,.2f}"
        )

        self.today_card.value_label.configure(
            text=f"₹{today_total:,.2f}"
        )

        self.count_card.value_label.configure(
            text=str(len(expenses))
        )

        self.update_categories(categories)

    # -----------------------------
    # TRANSACTION CARD
    # -----------------------------

    def create_transaction(
        self,
        expense_id,
        title,
        category,
        amount,
        date
    ):

        card = ctk.CTkFrame(
            self.transaction_frame,
            height=70,
            corner_radius=14,
            fg_color="#1D202A"
        )

        card.pack(
            fill="x",
            pady=5,
            padx=3
        )

        card.pack_propagate(False)

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color="#FFFFFF"
        )

        title_label.pack(
            anchor="w",
            padx=15,
            pady=(10, 0)
        )

        info = ctk.CTkLabel(
            card,
            text=f"{category}  •  {date}",
            font=ctk.CTkFont(size=11),
            text_color="#7F879B"
        )

        info.pack(
            anchor="w",
            padx=15
        )

        amount_label = ctk.CTkLabel(
            card,
            text=f"- ₹{amount:,.2f}",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color="#FF6B6B"
        )

        amount_label.place(
            relx=0.72,
            rely=0.28
        )

        delete_button = ctk.CTkButton(
            card,
            text="×",
            width=30,
            height=30,
            corner_radius=10,
            fg_color="#292D39",
            hover_color="#FF4D67",
            command=lambda i=expense_id: self.remove_expense(i)
        )

        delete_button.place(
            relx=0.91,
            rely=0.28
        )

    # -----------------------------
    # DELETE
    # -----------------------------

    def remove_expense(self, expense_id):

        answer = messagebox.askyesno(
            "Delete Expense",
            "Are you sure you want to delete this expense?"
        )

        if answer:

            delete_expense(expense_id)

            self.load_expenses()

    # -----------------------------
    # SEARCH
    # -----------------------------

    def search_expenses(self, event=None):

        query = self.search_entry.get().lower()

        for widget in self.transaction_frame.winfo_children():
            widget.destroy()

        expenses = get_expenses()

        for expense in expenses:

            expense_id = expense[0]
            title = expense[1]
            category = expense[2]
            amount = expense[3]
            date = expense[4]

            if (
                query in title.lower()
                or query in category.lower()
                or query in date.lower()
            ):

                self.create_transaction(
                    expense_id,
                    title,
                    category,
                    amount,
                    date
                )

    # -----------------------------
    # CATEGORY SUMMARY
    # -----------------------------

    def update_categories(self, categories):

        for widget in self.category_frame.winfo_children():
            widget.destroy()

        if not categories:

            label = ctk.CTkLabel(
                self.category_frame,
                text="No expenses yet",
                text_color="#7F879B"
            )

            label.pack(pady=20)

            return

        sorted_categories = sorted(
            categories.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for category, amount in sorted_categories:

            frame = ctk.CTkFrame(
                self.category_frame,
                fg_color="#20232D",
                corner_radius=12
            )

            frame.pack(
                fill="x",
                pady=5
            )

            name = ctk.CTkLabel(
                frame,
                text=category,
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                )
            )

            name.pack(
                side="left",
                padx=12,
                pady=10
            )

            value = ctk.CTkLabel(
                frame,
                text=f"₹{amount:,.0f}",
                text_color="#A8A3FF"
            )

            value.pack(
                side="right",
                padx=12
            )

    # -----------------------------
    # CHART
    # -----------------------------

    def show_chart(self):

        expenses = get_expenses()

        if not expenses:

            messagebox.showinfo(
                "No Data",
                "Add some expenses first."
            )

            return

        categories = {}

        for expense in expenses:

            category = expense[2]
            amount = expense[3]

            categories[category] = (
                categories.get(category, 0) + amount
            )

        plt.figure(
            figsize=(8, 6),
            facecolor="#11131A"
        )

        plt.pie(
            categories.values(),
            labels=categories.keys(),
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title(
            "Expense Distribution",
            color="white",
            fontsize=16
        )

        plt.tight_layout()

        plt.show()


# -----------------------------
# RUN APP
# -----------------------------

if __name__ == "__main__":

    app = ExpenseTracker()

    app.mainloop()