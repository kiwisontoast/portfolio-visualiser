import tkinter as tk
from tkinter import ttk
import sv_ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf
import numpy as np

def toggle_theme():
    """Switch between light and dark themes"""
    current_theme = sv_ttk.get_theme()
    if current_theme == "dark":
        # Switch to light theme
        sv_ttk.set_theme("light")
        theme_toggle_button.config(text="Switch to Dark Mode")
        # Update plot colors for light theme
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        ax.tick_params(colors='black')
        ax.set_title(ax.get_title(), color='black')
        ax.set_xlabel(ax.get_xlabel(), color='black')
        ax.set_ylabel(ax.get_ylabel(), color='black')
        ax.legend(facecolor='white', edgecolor='black', labelcolor='black')
        # Update text colors for light theme
        for text in ax.texts:
            text.set_color('black')
    else:
        # Switch to dark theme
        sv_ttk.set_theme("dark")
        theme_toggle_button.config(text="Switch to Light Mode")
        # Update plot colors for dark theme
        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#333333')
        ax.tick_params(colors='white')
        ax.set_title(ax.get_title(), color='white')
        ax.set_xlabel(ax.get_xlabel(), color='white')
        ax.set_ylabel(ax.get_ylabel(), color='white')
        ax.legend(facecolor='gray', edgecolor='white', labelcolor='white')
        # Update text colors for dark theme
        for text in ax.texts:
            text.set_color('white')
    canvas.draw()



# Function to save portfolio data to a file
def save_portfolio_data(portfolio):
    with open('portfolio.txt', 'w') as file:
        for ticker, amount in portfolio.items():
            file.write(f"{ticker}:{amount}\n")

# Function to load portfolio data from a file
def load_portfolio_data():
    portfolio = {}
    try:
        with open('portfolio.txt', 'r') as file:
            for line in file.readlines():
                ticker, amount = line.strip().split(':')
                portfolio[ticker] = float(amount)
    except FileNotFoundError:
        pass
    return portfolio

# Function to save hypothetical portfolio data to a file
def save_hypothetical_portfolio_data(portfolio):
    with open('hypothetical_portfolio.txt', 'w') as file:
        for ticker, percentage in portfolio.items():
            file.write(f"{ticker}:{percentage}\n")

# Function to load hypothetical portfolio data from a file
def load_hypothetical_portfolio_data():
    portfolio = {}
    try:
        with open('hypothetical_portfolio.txt', 'r') as file:
            for line in file.readlines():
                ticker, percentage = line.strip().split(':')
                portfolio[ticker] = float(percentage)
    except FileNotFoundError:
        pass
    return portfolio

# Function to calculate current portfolio value and breakdown
def calculate_portfolio_value(portfolio):
    total_value = 0
    breakdown = {}
    for ticker, amount in portfolio.items():
        data = yf.Ticker(ticker).history(period='1d')['Close'].iloc[-1]
        value = amount * data
        total_value += value
        breakdown[ticker] = value
    return total_value, breakdown

def create_portfolio_pie_chart(portfolio):
    total_value, breakdown = calculate_portfolio_value(portfolio)
    labels = list(breakdown.keys())
    sizes = list(breakdown.values())
    ax.clear()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')
    # Update text colors for pie chart labels
    for text in ax.texts:
        text.set_color('white')
    canvas.draw()
    portfolio_value_label.config(text=f"Portfolio Value: ${total_value:.2f}")

def create_hypothetical_portfolio_pie_chart(portfolio):
    labels = list(portfolio.keys())
    sizes = list(portfolio.values())
    ax.clear()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')
    # Update text colors for pie chart labels
    for text in ax.texts:
        text.set_color('white')
    canvas.draw()


# Function to add stock to portfolio
def add_stock_to_portfolio():
    ticker = ticker_entry.get()
    amount = float(amount_entry.get())
    portfolio[ticker] = amount
    save_portfolio_data(portfolio)
    create_portfolio_pie_chart(portfolio)
    ticker_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

# Function to add stock to hypothetical portfolio
def add_stock_to_hypothetical_portfolio():
    ticker = hypothetical_ticker_entry.get()
    percentage = float(hypothetical_percentage_entry.get())
    hypothetical_portfolio[ticker] = percentage
    save_hypothetical_portfolio_data(hypothetical_portfolio)
    create_hypothetical_portfolio_pie_chart(hypothetical_portfolio)
    hypothetical_ticker_entry.delete(0, tk.END)
    hypothetical_percentage_entry.delete(0, tk.END)

def update_graph():
    # Check if there is existing data in the portfolio
    if portfolio:
        # Clear previous plot
        ax.clear()
        # Create pie chart for portfolio breakdown
        create_portfolio_pie_chart(portfolio)
    else:
        # If no data, clear the plot
        ax.clear()
        canvas.draw()

# Create and configure main window
root = tk.Tk()
root.title("Portfolio Visualizer")
root.protocol("WM_DELETE_WINDOW", lambda: root.quit())

# Set window size to 95% of screen height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_height = int(screen_height * 0.95)
window_width = screen_width
root.geometry(f"{window_width}x{window_height}+0+0")

# Create and configure main frame
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame.rowconfigure(11, weight=1)
frame.columnconfigure(0, weight=1)


# Create UI elements
theme_toggle_button = ttk.Button(frame, text="Switch to Light Mode", command=toggle_theme)
theme_toggle_button.grid(row=0, column=0, sticky=tk.W, pady=5)

# Portfolio frame
portfolio_frame = ttk.Frame(frame)
portfolio_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

# Ticker and amount inputs
ticker_label = ttk.Label(portfolio_frame, text="Enter stock ticker:")
ticker_label.grid(row=0, column=0, sticky=tk.W, pady=5)
ticker_entry = ttk.Entry(portfolio_frame, width=10)
ticker_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
amount_label = ttk.Label(portfolio_frame, text="Enter amount invested:")
amount_label.grid(row=1, column=0, sticky=tk.W, pady=5)
amount_entry = ttk.Entry(portfolio_frame, width=10)
amount_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

# Add stock to portfolio button
add_stock_button = ttk.Button(portfolio_frame, text="Add Stock", command=add_stock_to_portfolio)
add_stock_button.grid(row=2, column=1, sticky=tk.E, pady=5)

# Create portfolio pie chart button
create_portfolio_button = ttk.Button(portfolio_frame, text="Create Portfolio Pie Chart", command=lambda: create_portfolio_pie_chart(portfolio))
create_portfolio_button.grid(row=3, column=1, sticky=tk.E, pady=5)

# Portfolio value label
portfolio_value_label = ttk.Label(portfolio_frame, text="Portfolio Value: ")
portfolio_value_label.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)

# Hypothetical portfolio frame
hypothetical_portfolio_frame = ttk.Frame(frame)
hypothetical_portfolio_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

# Hypothetical ticker and percentage inputs
hypothetical_ticker_label = ttk.Label(hypothetical_portfolio_frame, text="Enter stock ticker:")
hypothetical_ticker_label.grid(row=0, column=0, sticky=tk.W, pady=5)
hypothetical_ticker_entry = ttk.Entry(hypothetical_portfolio_frame, width=10)
hypothetical_ticker_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
hypothetical_percentage_label = ttk.Label(hypothetical_portfolio_frame, text="Enter percentage:")
hypothetical_percentage_label.grid(row=1, column=0, sticky=tk.W, pady=5)
hypothetical_percentage_entry = ttk.Entry(hypothetical_portfolio_frame, width=10)
hypothetical_percentage_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

# Add stock to hypothetical portfolio button
add_hypothetical_stock_button = ttk.Button(hypothetical_portfolio_frame, text="Add Stock", command=add_stock_to_hypothetical_portfolio)
add_hypothetical_stock_button.grid(row=2, column=1, sticky=tk.E, pady=5)

# Create hypothetical portfolio pie chart button
create_hypothetical_portfolio_button = ttk.Button(hypothetical_portfolio_frame, text="Create Hypothetical Portfolio Pie Chart", command=lambda: create_hypothetical_portfolio_pie_chart(hypothetical_portfolio))
create_hypothetical_portfolio_button.grid(row=3, column=1, sticky=tk.E, pady=5)

# Set theme
sv_ttk.set_theme("dark")

# Set up the plot
fig, ax = plt.subplots()
fig.patch.set_facecolor('#333333')
ax.set_facecolor('#333333')
ax.tick_params(colors='white')
ax.set_title(ax.get_title(), color='white')
ax.set_xlabel(ax.get_xlabel(), color='white')
ax.set_ylabel(ax.get_ylabel(), color='white')
ax.legend(facecolor='gray', edgecolor='white', labelcolor='white')
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=11, column=0, columnspan=7, sticky=(tk.W, tk.E, tk.N, tk.S))


# Load portfolio data
portfolio = load_portfolio_data()
hypothetical_portfolio = load_hypothetical_portfolio_data()

update_graph()

# Start the main event loop
root.mainloop()
