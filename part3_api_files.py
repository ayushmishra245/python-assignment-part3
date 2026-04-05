# ============================================================
# BITSOM 3 - Part 3: File I/O, APIs & Exception Handling
# Theme: Product Explorer & Error-Resilient Logger
# ============================================================

import requests
from datetime import datetime

# Task 1 — File Read & Write Basics
# first write the required notes, append 2 extra lines, 
# then read the file back and check line count and keyword matches
print("\n" + "=" * 80)
print("TASK 1 - FILE READ & WRITE BASICS")
print("=" * 80)

# File used for Task 1
file_name = "python_notes.txt"

# Part A: writing the required notes

# 5 lines given in the assignment
notes = [
    "Topic 1: Variables store data. Python is dynamically typed.\n",
    "Topic 2: Lists are ordered and mutable.\n",
    "Topic 3: Dictionaries store key-value pairs.\n",
    "Topic 4: Loops automate repetitive tasks.\n",
    "Topic 5: Exception handling prevents crashes.\n"
]

# writeing initial notes to the file
with open(file_name, "w", encoding="utf-8") as file:
    file.writelines(notes)

print("File written successfully.")

# 2 additional lines added for the assignment
extra_notes = [
    "Topic 6: Functions help organize code into reusable blocks.\n",
    "Topic 7: File handling allows programs to store and retrieve data.\n"
]

# adding the extra lines in the same file
with open(file_name, "a", encoding="utf-8") as file:
    file.writelines(extra_notes)

print("Lines appended successfully.")

# Part B: reading the file and searching for a keyword

# read all lines from the file
with open(file_name, "r", encoding="utf-8") as file:
    all_lines = file.readlines()

# print each line with its line number
for index, line in enumerate(all_lines, start=1):
    print(f"{index}. {line.strip()}")

# counting total lines in the file
total_lines = len(all_lines)
print(f"\nTotal number of lines in the file: {total_lines}")

# Keyword search (case-insensitive)

# taking keyword input from the user
keyword = input("\nEnter a keyword to search in the file: ").strip()

# store matching lines
matching_lines = []

# checking each line for the keyword
# using lower() so capital and small letters both can match
for line in all_lines:
    if keyword.lower() in line.lower():
        matching_lines.append(line.strip())

# Printing matching results
if len(matching_lines) > 0:
    print(f"\nLines containing '{keyword}':")
    for match in matching_lines:
        print(match)
else:
    print(f"\nNo lines found containing the keyword '{keyword}'. Please try another word.")


# Task 2 - API Integration
# use DummyJSON API to fetch, filter, and display product data

print("\n" + "=" * 80)
print("TASK 2 - API INTEGRATION")
print("=" * 80)

# Base URL for DummyJSON products API
base_url = "https://dummyjson.com/products"

# Step 1 — Fetch and Display 20 Products
print("\nStep 1: Fetching 20 products from the API...")
products = []

try:
    response = requests.get(f"{base_url}?limit=20", timeout=5)

    # checking if request was success
    response.raise_for_status()

    # converting response into json format
    data = response.json()

    # extracting products list from the response
    products = data.get("products", [])

    print(f"{'ID':<4} | {'Title':<30} | {'Category':<15} | {'Price':<10} | {'Rating':<6}")
    print("-" * 80)

    for product in products:
        print(
            f"{product['id']:<4} | "
            f"{product['title'][:30]:<30} | "
            f"{product['category'][:15]:<15} | "
            f"{product['price']:<10} | "
            f"{product['rating']:<6}"
        )

except requests.exceptions.RequestException as e:
    print(f"Error while fetching products: {e}")
    products = []


# Step 2 — Filter and Sort products
print("\n" + "-" * 80)
print("Step 2: Filtering products with rating >= 4.5 and sorting by price (high to low)...")

# Only proceed if product data is available
if len(products) > 0:
    # Filtering products with rating 4.5 or above
    filtered_products = []

    for product in products:
        if product.get("rating", 0) >= 4.5:
            filtered_products.append(product)

    # sorting the filtered products by price in decending order
    filtered_products = sorted(filtered_products, key=lambda item: item.get("price", 0), reverse=True)

    if len(filtered_products) > 0:
        print("\nFiltered and Sorted Products:\n")
        print(f"{'ID':<4} | {'Title':<30} | {'Category':<15} | {'Price':<10} | {'Rating':<6}")
        print("-" * 80)

        for product in filtered_products:
            product_id = product.get("id", "N/A")
            title = product.get("title", "N/A")
            category = product.get("category", "N/A")
            price = product.get("price", "N/A")
            rating = product.get("rating", "N/A")

            print(f"{product_id:<4} | {title[:30]:<30} | {category[:15]:<15} | ${price:<9} | {rating:<6}")
    else:
        print("No products found with rating greater than or equal to 4.5.")

else:
    print("Skipping Step 2 because product data was not fetched successfully.")


# Step 3 - Search by Category
print("\n" + "-" * 80)
print("Step 3: Fetching all products in the laptops category...")

try:
    # getting all products from laptops category
    laptop_response = requests.get(f"{base_url}/category/laptops", timeout=5)
    laptop_response.raise_for_status()
    laptop_data = laptop_response.json()
    laptop_products = laptop_data.get("products", [])

    if len(laptop_products) > 0:
        print("\nLaptops found:\n")

        # show laptop name and price
        for laptop in laptop_products:
            laptop_name = laptop.get("title", "N/A")
            laptop_price = laptop.get("price", "N/A")

            print(f"Product Name: {laptop_name} | Price: ${laptop_price}")
    else:
        print("No laptops found in the category.")

except requests.exceptions.RequestException as e:
    print(f"Error while fetching laptops category: {e}")


# Step 4 - POST Request-Simulation
print("\n" + "-" * 80)
print("Step 4: Sending a simulated POST request to add a product...")

# sample product data for the POST request
new_product = {
    "title": "My Custom Product",
    "price": 999,
    "category": "electronics",
    "description": "A product I created via API"
}

try:
    # sending POST request to the API
    post_response = requests.post(f"{base_url}/add", json=new_product, timeout=5)
    post_response.raise_for_status()
    created_product = post_response.json()

    print("\nPOST request successful.")
    print("Full response returned by the server:\n")

    # printing API response
    print(created_product)

except requests.exceptions.RequestException as e:
    print(f"Error while sending POST request: {e}")


# Task 3 - Exception Handling
# handling common errors for calculations, file access, and API requests

print("\n" + "=" * 80)
print("TASK 3 - EXCEPTION HANDLING")
print("=" * 80)


# Part A — Guarded Calculator
print("\nPart A: Guarded Calculator")


# function to divide 2 values safely with basic error handling
def safe_divide(a, b):
    try:
        result = a / b
        return result

    except ZeroDivisionError:
        return "Error: Cannot divide by zero"

    except TypeError:
        return "Error: Invalid input types"


# Testing the function with given examples 
print("safe_divide(10, 2) =", safe_divide(10, 2))
print("safe_divide(10, 0) =", safe_divide(10, 0))
print('safe_divide("ten", 2) =', safe_divide("ten", 2))


# Part B — Guarded File Reader
print("\n" + "-" * 80)
print("Part B: Guarded File Reader")


# read file safely and always print completion message
def read_file_safe(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
            return content

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

    finally:
        print("File operation attempt complete.")


# Testing with the file created in Task 1
print("\nReading 'python_notes.txt':")
notes_content = read_file_safe("python_notes.txt")

# If content is returned successfully, print it
if notes_content is not None:
    print(notes_content)

# Testing with a file that does not exist
print("\nReading 'ghost_file.txt':")
ghost_content = read_file_safe("ghost_file.txt")

if ghost_content is not None:
    print(ghost_content)


# Part C - Robust API Calls
print("\n" + "-" * 80)
print("Part C: Robust API Calls")

# repeat the API calls with explicit handling for 
# connection, timeout, and unexpected errors

# GET request - Fetch 20 products
print("\nFetching 20 products with better error handling...")

robust_products = []

try:
    response = requests.get(f"{base_url}?limit=20", timeout=5)

    # checking if the API returned was successful
    if response.status_code == 200:
        data = response.json()
        robust_products = data.get("products", [])
        print("Products fetched successfully.")
    else:
        print(f"Request failed with status code: {response.status_code}")

except requests.exceptions.ConnectionError:
    print("Connection failed. Please check your internet.")

except requests.exceptions.Timeout:
    print("Request timed out. Try again later.")

except Exception as e:
    print(f"An unexpected error occurred: {e}")


# GET request - Laptops category
print("\nFetching laptops category with better error handling...")

try:
    laptop_response = requests.get(f"{base_url}/category/laptops", timeout=5)

    # checking if the API call was successful
    if laptop_response.status_code == 200:
        laptop_data = laptop_response.json()
        laptop_products = laptop_data.get("products", [])

        print("Laptops fetched successfully.")

        for laptop in laptop_products:
            laptop_name = laptop.get("title", "N/A")
            laptop_price = laptop.get("price", "N/A")
            print(f"Product Name: {laptop_name} | Price: ${laptop_price}")
    else:
        print(f"Request failed with status code: {laptop_response.status_code}")

except requests.exceptions.ConnectionError:
    print("Connection failed. Please check your internet.")

except requests.exceptions.Timeout:
    print("Request timed out. Try again later.")

except Exception as e:
    print(f"An unexpected error occurred: {e}")


# POST request - Simulated add product
print("\nSending POST request with better error handling...")

new_product = {
    "title": "My Custom Product",
    "price": 999,
    "category": "electronics",
    "description": "A product I created via API"
}

try:
    post_response = requests.post(f"{base_url}/add", json=new_product, timeout=5)

    # checking if the POST request was successful
    if post_response.status_code in [200, 201]:
        created_product = post_response.json()
        print("POST request successful.")
        print("Server response:")
        print(created_product)
    else:
        print(f"POST request failed with status code: {post_response.status_code}")

except requests.exceptions.ConnectionError:
    print("Connection failed. Please check your internet.")

except requests.exceptions.Timeout:
    print("Request timed out. Try again later.")

except Exception as e:
    print(f"An unexpected error occurred: {e}")


# Part D - Input Validation Loop
print("\n" + "-" * 80)
print("Part D: Input Validation Loop")

# keep asking until the user enters a valid product ID or quits

while True:
    user_input = input("\nEnter a product ID to look up (1–100), or 'quit' to exit: ").strip()

    # if user wants to stop the loop
    if user_input.lower() == "quit":
        print("Exiting product lookup.")
        break

    # checking if the input is a numeric
    if not user_input.isdigit():
        print("Invalid input. Please enter a whole number between 1 and 100.")
        continue

    # converting to integer after validation
    product_id = int(user_input)

    # checking if the number is in valid range
    if product_id < 1 or product_id > 100:
        print("Invalid product ID. Please enter a number between 1 and 100.")
        continue

    # if input is valid, then call API
    try:
        product_response = requests.get(f"{base_url}/{product_id}", timeout=5)

        # checking if product exists or not
        if product_response.status_code == 404:
            print("Product not found.")

        elif product_response.status_code == 200:
            product_data = product_response.json()
            product_title = product_data.get("title", "N/A")
            product_price = product_data.get("price", "N/A")

            print(f"Product Title: {product_title}")
            print(f"Product Price: ${product_price}")

        else:
            print(f"Request failed with status code: {product_response.status_code}")

    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")

    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Task 4 - Logging to File
# save error details in a log file for later review

print("\n" + "=" * 80)
print("TASK 4 - LOGGING TO FILE")
print("=" * 80)

# Log file name
log_file = "error_log.txt"


# helper function to save errors in the log file
def log_error(function_name, error_type, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"[{timestamp}] ERROR in {function_name}: {error_type} — {message}\n"

    with open(log_file, "a", encoding="utf-8") as file:
        file.write(log_entry)


# Trigger 1 - ConnectionError
print("\nTriggering a ConnectionError intentionally...")

# using a wrong URL to trigger error
bad_url = "https://this-host-does-not-exist-xyz.com/api"

try:
    bad_response = requests.get(bad_url, timeout=5)

except requests.exceptions.ConnectionError as e:
    print("ConnectionError caught and logged.")
    log_error("fetch_products", "ConnectionError", "No connection could be made")

except requests.exceptions.Timeout as e:
    # handling timeout
    print("Timeout caught and logged.")
    log_error("fetch_products", "Timeout", str(e))

except Exception as e:
    print("Unexpected error caught and logged.")
    log_error("fetch_products", type(e).__name__, str(e))


# Trigger 2 - Invalid Product ID
print("\nChecking an invalid product ID to trigger error...")

# use an invalid product ID to log an HTTP error
invalid_product_id = 999

try:
    invalid_response = requests.get(f"{base_url}/{invalid_product_id}", timeout=5)

    if invalid_response.status_code != 200:
        print("HTTP error response detected and logged.")
        log_error(
            "lookup_product",
            "HTTPError",
            f"{invalid_response.status_code} Not Found for product ID {invalid_product_id}"
        )
    else:
        # just in case the product is found
        print("Unexpectedly found product 999.")

except requests.exceptions.ConnectionError:
    print("Connection failed while checking invalid product.")
    log_error("lookup_product", "ConnectionError", "No connection could be made")

except requests.exceptions.Timeout:
    print("Request timed out while checking invalid product.")
    log_error("lookup_product", "Timeout", "Request timed out")

except Exception as e:
    print("Unexpected error caught and logged.")
    log_error("lookup_product", type(e).__name__, str(e))

# Read and display the full log file
print("\nReading full contents of error_log.txt...\n")

try:
    with open(log_file, "r", encoding="utf-8") as file:
        log_contents = file.read()
        print(log_contents)

except FileNotFoundError:
    print("Log file not found.")