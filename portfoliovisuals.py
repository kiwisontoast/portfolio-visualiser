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
    
    # Clear and redraw the plot
    ax.clear()

    fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    ax.pie(sizes, radius=5, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')
    
    # Update text colors based on current theme
    current_theme = sv_ttk.get_theme()
    text_color = 'white' if current_theme == "dark" else 'black'
    for text in ax.texts:
        text.set_color(text_color)
    
    canvas.draw()
    portfolio_value_label.config(text=f"Portfolio Value: ${total_value:.2f}")

def create_hypothetical_portfolio_pie_chart(portfolio):
    labels = list(portfolio.keys())
    sizes = list(portfolio.values())
    
    ax.clear()
    fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    ax.pie(sizes, radius = 5, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')
    
    current_theme = sv_ttk.get_theme()
    text_color = 'white' if current_theme == "dark" else 'black'
    for text in ax.texts:
        text.set_color(text_color)
    
    canvas.draw()

# Function to add stock to portfolio
def add_stock_to_portfolio():
    ticker = ticker_entry.get()
    amount = float(amount_entry.get())
    if ticker in portfolio:
        # Add to existing amount
        portfolio[ticker] += amount
    else:
        # Add new stock to portfolio
        portfolio[ticker] = amount
    save_portfolio_data(portfolio)
    create_portfolio_pie_chart(portfolio)
    ticker_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

def remove_stock_from_portfolio():
    ticker = ticker_entry.get()
    amount = float(amount_entry.get())
    if ticker in portfolio:
        # Remove specified amount from the stock holding
        portfolio[ticker] -= amount
        if portfolio[ticker] <= 0:
            # If the amount goes to 0 or below, remove the stock from the portfolio
            del portfolio[ticker]
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

def remove_stock_from_hypothetical_portfolio():
    ticker = hypothetical_ticker_entry.get()
    percentage = float(hypothetical_percentage_entry.get())
    if ticker in hypothetical_portfolio:
        # Remove specified percentage from the stock holding
        hypothetical_portfolio[ticker] -= percentage
        if hypothetical_portfolio[ticker] <= 0:
            # If the percentage goes to 0 or below, remove the stock from the portfolio
            del hypothetical_portfolio[ticker]
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

def setup_plot():
    global fig, ax, canvas
    fig = plt.figure(figsize=(12, 8))  # Set a reasonable default figure size
    ax = fig.add_subplot(111)
    
    # Configure plot appearance
    fig.patch.set_facecolor('#333333')
    ax.set_facecolor('#333333')
    ax.tick_params(colors='white')
    
    # Create canvas with proper configuration
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=0, sticky="nsew")
    
    # Configure graph_frame grid
    graph_frame.grid_rowconfigure(0, weight=3)
    graph_frame.grid_columnconfigure(0, weight=2)

# Add this to handle window resizing
def on_resize(event):
    # Update the figure size based on the new window size
    width = event.width / 100  # Convert pixels to inches
    height = event.height / 100
    if hasattr(fig, 'set_size_inches'):  # Check if figure exists
        fig.set_size_inches(width, height, forward=True)
        canvas.draw()

# Create and configure main window
root = tk.Tk()
root.title("Portfolio Visualizer")
root.protocol("WM_DELETE_WINDOW", lambda: root.quit())

# Make the window resizable
root.resizable(True, True)

# Set initial window size to 80% of screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.9)
root.geometry(f"{window_width}x{window_height}")

# Configure main frame with proper weight distribution
frame = ttk.Frame(root)
frame.grid(row=0, column=0, sticky="nsew")

# Configure root grid
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create left and right frames for better organization
left_frame = ttk.Frame(frame)
left_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

graph_frame = ttk.Frame(frame)
graph_frame.grid(row=11, column=0, sticky="nsew", padx=10, pady=10)
frame.grid_rowconfigure(11, weight=1)

# Create UI elements
theme_toggle_button = ttk.Button(left_frame, text="Switch to Light Mode", command=toggle_theme)
theme_toggle_button.grid(row=0, column=0, sticky=tk.W, pady=5)

# Add text under light/dark toggle
portfolio_label = ttk.Label(left_frame, text="Portfolio Add/Remove")
portfolio_label.grid(row=1, column=0, sticky=tk.W, pady=5)

# Portfolio frame
portfolio_frame = ttk.Frame(left_frame)
portfolio_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

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

# Remove stock from portfolio button
remove_stock_button = ttk.Button(portfolio_frame, text="Remove/Reduce Stock", command=remove_stock_from_portfolio)
remove_stock_button.grid(row=3, column=1, sticky=tk.E, pady=5)

# Create portfolio pie chart button
create_portfolio_button = ttk.Button(portfolio_frame, text="Create Portfolio Pie Chart", 
                                   command=lambda: create_portfolio_pie_chart(portfolio))
create_portfolio_button.grid(row=4, column=1, sticky=tk.E, pady=5)

# Portfolio value label
portfolio_value_label = ttk.Label(portfolio_frame, text="Portfolio Value: ")
portfolio_value_label.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=5)

# Add text under portfolio value
hypothetical_portfolio_label = ttk.Label(left_frame, text="Hypothetical Portfolio Add/Remove")
hypothetical_portfolio_label.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)

# Hypothetical portfolio frame
hypothetical_portfolio_frame = ttk.Frame(left_frame)
hypothetical_portfolio_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

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
add_hypothetical_stock_button = ttk.Button(hypothetical_portfolio_frame, text="Add Stock", 
                                         command=add_stock_to_hypothetical_portfolio)
add_hypothetical_stock_button.grid(row=2, column=1, sticky=tk.E, pady=5)

# Remove stock from hypothetical portfolio button
remove_hypothetical_stock_button = ttk.Button(hypothetical_portfolio_frame, text="Remove/Reduce Stock", 
                                            command=remove_stock_from_hypothetical_portfolio)
remove_hypothetical_stock_button.grid(row=3, column=1, sticky=tk.E, pady=5)

# Create hypothetical portfolio pie chart button
create_hypothetical_portfolio_button = ttk.Button(hypothetical_portfolio_frame, text="Create Hypothetical Portfolio Pie Chart", 
                                                command=lambda: create_hypothetical_portfolio_pie_chart(hypothetical_portfolio))
create_hypothetical_portfolio_button.grid(row=4, column=1, sticky=tk.E, pady=5)

# Set theme
sv_ttk.set_theme("dark")

# Set up the plot
setup_plot()

# Bind the resize event
graph_frame.bind('<Configure>', on_resize)

# Load portfolio data
portfolio = load_portfolio_data()
hypothetical_portfolio = load_hypothetical_portfolio_data()

update_graph()

# Start the main event loop
root.mainloop()