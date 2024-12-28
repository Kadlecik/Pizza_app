import matplotlib.pyplot as plt


def plot_sales_data(sales_data):
    try:
        # Převod dat na číselné hodnoty
        numeric_sales_data = [float(value) for value in sales_data if
                              isinstance(value, (int, float)) or value.replace('.', '', 1).isdigit()]

        # Vykreslení grafu
        plt.plot(numeric_sales_data)
        plt.title("Sales Data")
        plt.xlabel("Order Index")
        plt.ylabel("Revenue ($)")
        plt.show()
    except ValueError as e:
        logging.error(f"Error in converting sales data: {e}")
