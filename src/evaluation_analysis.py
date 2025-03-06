import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psutil
import platform
import logging
from rich.console import Console
from rich.table import Table
from rich.style import Style
from rich import box
from tabulate import tabulate

# --------------------------
# LOGGING SYSTEM INFO
# --------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Get system information
os_info = platform.system() + " " + platform.version()
cpu_info = platform.processor()
total_ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)  # Convert bytes to GB
used_ram = round(psutil.virtual_memory().used / (1024 ** 3), 2)  # Used memory in GB
available_ram = round(psutil.virtual_memory().available / (1024 ** 3), 2)  # Available memory in GB

# Log system info
logging.info(f"OS: {os_info}")
logging.info(f"CPU: {cpu_info}")
logging.info(f"Total RAM: {total_ram} GB")
logging.info(f"Used RAM: {used_ram} GB")
logging.info(f"Available RAM: {available_ram} GB")

# --------------------------
# LOAD BENCHMARK RESULTS
# --------------------------
file_path = "./benchmark_results.csv"  # Change if needed
df = pd.read_csv(file_path)

# Debugging: Print the first few rows
#print("📂 Loaded DataFrame:")
#print(df.head())

# Check if df is empty
if df.empty:
    raise ValueError("🚨 The DataFrame is empty! Check if 'benchmark_results.csv' has valid data.")

# Ensure proper data types
df["Time (s)"] = df["Time (s)"].astype(float)
df["Memory Usage (GB)"] = df["Memory Usage (GB)"].astype(float)
df["Accuracy (%)"] = df["Accuracy (%)"].astype(float)

# Extract model names for better readability
df["Model Name"] = df["Model"].apply(lambda x: x.split(":")[0])
df["Optimization"] = df["Optimization"].apply(lambda x: x.replace("{", "").replace("}", ""))  # Clean formatting

# --------------------------
# DISPLAY SYSTEM INFO
# --------------------------
console = Console()

def display_system_info():
    table = Table(title="System Information", box=box.DOUBLE_EDGE)
    table.add_column("Property", style="cyan", justify="left")
    table.add_column("Value", style="bold green", justify="right")

    table.add_row("OS", os_info)
    table.add_row("CPU", cpu_info)
    table.add_row("Total RAM (GB)", str(total_ram))
    table.add_row("Used RAM (GB)", str(used_ram))
    table.add_row("Available RAM (GB)", str(available_ram))

    console.print(table)

display_system_info()

# --------------------------
# DISPLAY BEAUTIFUL TABLE
# --------------------------
def display_dataframe_rich(df, title="📊 Benchmark Results"):
    table = Table(title=title, box=box.ROUNDED)

    # Add columns dynamically
    for col in df.columns:
        table.add_column(str(col), style="bold white", justify="center")

    # Highlight best performing models
    best_time = df["Time (s)"].idxmin()
    best_memory = df["Memory Usage (GB)"].idxmin()
    best_accuracy = df["Accuracy (%)"].idxmax()

    # Add rows
    for idx, row in df.iterrows():
        if idx == best_time:
            style = "bold cyan"
        elif idx == best_memory:
            style = "bold magenta"
        elif idx == best_accuracy:
            style = "bold green"
        else:
            style = "white"

        table.add_row(*[str(x) for x in row], style=style)

    console.print(table)

# Use rich table
display_dataframe_rich(df)

# Alternative: Use tabulate if needed
print("\n📊 Benchmark Results (Tabulate Format):\n")
print(tabulate(df, headers='keys', tablefmt='pretty'))

# --------------------------
# GENERATE INTERACTIVE PLOTS
# --------------------------
df["Model Name"] = df["Model Name"].astype(str)
df["Model Name"] = df["Model Name"].astype("category")
#print(df.dtypes)

# 📌 1️⃣ **Inference Time vs. Models & Quantization**
fig1 = px.scatter(df,
                  x="Model Name",
                  y="Time (s)",
                  color="Quantization",
                  title="⏱ Inference Time by Model & Quantization",
                  size="Accuracy (%)",
                  hover_data=["Optimization"],
                  category_orders={"Model Name": df["Model Name"].unique()})


# 📌 2️⃣ **Memory Usage vs. Models & Quantization**
fig2 = px.bar(df,
              x="Model Name",
              y="Memory Usage (GB)",
              color="Quantization",
              title="🖥 Memory Usage by Model & Quantization",
              barmode="group",
              hover_data=["Optimization"])

# 📌 3️⃣ **Accuracy vs. Models & Quantization**
fig3 = px.line(df,
               x="Model Name",
               y="Accuracy (%)",
               color="Quantization",
               title="🎯 Accuracy by Model & Quantization",
               markers=True,
               line_shape="spline",
               hover_data=["Optimization"])

# 📌 4️⃣ **Quantization Method Distribution**
fig4 = px.pie(df,
              names="Quantization",
              title="🔢 Quantization Distribution",
              hole=0.4)

# Show the plots
fig1.show()
fig2.show()
fig3.show()
fig4.show()

# --------------------------
# KEY OBSERVATIONS
# --------------------------
console.print("\n🔍 [bold cyan]Key Observations:[/bold cyan]\n")

# 🔥 **Best Model for Inference Speed**
best_time = df.loc[df["Time (s)"].idxmin()]
console.print(f"⚡ [bold cyan]Fastest Model:[/bold cyan] {best_time['Model Name']} ({best_time['Quantization']}) | Time: {best_time['Time (s)']}s")

# 🏆 **Best Model for Low Memory Usage**
best_memory = df.loc[df["Memory Usage (GB)"].idxmin()]
console.print(f"🛠️ [bold magenta]Most Efficient Memory Usage:[/bold magenta] {best_memory['Model Name']} ({best_memory['Quantization']}) | Memory: {best_memory['Memory Usage (GB)']}GB")

# 🎯 **Best Model for Accuracy**
best_accuracy = df.loc[df["Accuracy (%)"].idxmax()]
console.print(f"📊 [bold green]Highest Accuracy:[/bold green] {best_accuracy['Model Name']} ({best_accuracy['Quantization']}) | Accuracy: {best_accuracy['Accuracy (%)']}%")

# ⚖ **Best Balance (Speed + Accuracy + Memory)**
balanced_model = df.loc[(df["Time (s)"] < df["Time (s)"].quantile(0.25)) &
                        (df["Memory Usage (GB)"] < df["Memory Usage (GB)"].quantile(0.25)) &
                        (df["Accuracy (%)"] > df["Accuracy (%)"].quantile(0.75))]

if not balanced_model.empty:
    console.print("\n🏅 [bold yellow]Best Overall Model (Balanced Performance)[/bold yellow]")
    print(tabulate(balanced_model[["Model Name", "Quantization", "Time (s)", "Memory Usage (GB)", "Accuracy (%)"]],
                   headers='keys', tablefmt='pretty'))
else:
    console.print("\n⚠️ [bold red]No perfect balanced model, but you can prioritize based on your needs![/bold red]")

console.print("\n✅ [bold green]Use the interactive graphs above to explore different models visually![/bold green]")
