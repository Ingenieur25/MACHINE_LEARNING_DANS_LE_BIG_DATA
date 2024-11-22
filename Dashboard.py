import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Directory containing the output files and images
output_dir = "C:/laragon/www/html/output"  # Change path as needed
images_dir = "C:/laragon/www/html/Images_des_articles"  # Directory with product images

# Function to load data from the output directory
def load_data(start_date, end_date):
    # Convert dates to the YMD format
    start_date = start_date.replace("/", "")
    end_date = end_date.replace("/", "")
    
    data = []

    # Loop through files in the output directory
    for file_name in os.listdir(output_dir):
        if file_name.endswith(".txt"):
            file_date = file_name.split(".")[0]  # Extract YMDh from the file name
            if start_date <= file_date[:8] <= end_date:  # Filter files by date range
                file_path = os.path.join(output_dir, file_name)
                # Load file into DataFrame
                with open(file_path, "r") as file:
                    for line in file:
                        hour, product, total_price = line.strip().split("|")
                        data.append({"hour": hour, "product": product, "total_price": int(total_price)})
    
    return pd.DataFrame(data)

# Function to load an image for a product
def load_image(product_name):
    image_path = os.path.join(images_dir, f"{product_name}.jpg")  # Change extension if needed
    if os.path.exists(image_path):
        return plt.imread(image_path)
    return None

# Function to plot the dashboard
def plot_dashboard(data):
    if data.empty:
        print("No data available for the selected date range.")
        return

    product_sales = data.groupby("product")["total_price"].sum().reset_index()
    sales_trend = data.groupby("hour")["total_price"].sum().reset_index()

    plt.figure(figsize=(12, 12))

    plt.subplot(2, 1, 1)
    plt.bar(product_sales["product"], product_sales["total_price"], color="skyblue")
    plt.title("Total Sales Per Product")
    plt.xlabel("Product")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=45)

    ax = plt.gca()
    for idx, product in enumerate(product_sales["product"]):
        image = load_image(product)
        if image is not None:
            offset_image = OffsetImage(image, zoom=0.2)
            ab = AnnotationBbox(offset_image, (idx, product_sales["total_price"].iloc[idx] + 2000), frameon=False)
            ax.add_artist(ab)

    plt.subplot(2, 1, 2)
    plt.plot(sales_trend["hour"], sales_trend["total_price"], marker="o", color="orange")
    plt.title("Sales Trend Over Time")
    plt.xlabel("Hour")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    start_date = input("Enter the start date (YYYY/MM/DD): ")
    end_date = input("Enter the end date (YYYY/MM/DD): ")
    print("Loading data...")
    aggregated_data = load_data(start_date, end_date)
    print("Displaying dashboard...")
    plot_dashboard(aggregated_data)
