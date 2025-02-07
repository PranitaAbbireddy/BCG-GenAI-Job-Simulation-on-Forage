import pandas as pd
import re  # Import regex module

# Load the dataset
df = pd.read_excel("final_financial_data.xlsx")
print(df.index)
df = df.reset_index()
df.columns = df.columns.str.strip()
print("Columns in DataFrame:", df.columns)

# Define a mapping of possible financial queries to dataset column names
query_map = {
    "total revenue": "Total Revenue",
    "net income": "Net Income",
    "total assets": "Total Assets",
    "total liabilities": "Total Liabilities",
    "cash flow": "Cash Flow from Operating Activities",
    "revenue growth": "Revenue Growth (%)",
    "net income growth": "Net Income Growth (%)",
    "asset growth": "Asset Growth (%)",
    "liability growth": "Liability Growth (%)",
    "cash flow growth": "Cash Flow Growth (%)",
}

# Function to extract company, year, and query type from user input
def extract_query_details(user_query):
    user_query = user_query.lower()  # Convert to lowercase for case-insensitive matching

    # Extract year using regex (find a 4-digit number)
    year_match = re.search(r'\b(20\d{2})\b', user_query)  # Matches years like 2022, 2023, etc.
    year = year_match.group(1) if year_match else None

    # Extract company name (match from dataset)
    company = None
    for company_name in df["Company"].unique():
        if company_name.lower() in user_query:
            company = company_name
            break

    # Extract query type (match against query_map keys)
    query_type = None
    for key in query_map.keys():
        if key in user_query:
            query_type = key
            break

    # Debugging prints
    print(f"Extracted Company: {company}")
    print(f"Extracted Year: {year}")
    print(f"Extracted Query Type: {query_type}")

    return company, year, query_type


# Function to get financial data from dataset
def get_financial_data(company, year, query_type):
    if company is None or year is None or query_type is None:
        return "Sorry, I didn't understand your query. Please try again."

    # Filter dataset for requested company and year
    company_data = df[(df["Company"] == company) & (df["Year"] == int(year))]

    if company_data.empty:
        return f"Sorry, no data found for {company} in {year}."

    # Get the corresponding financial metric
    column_name = query_map[query_type]
    value = company_data[column_name].values[0]

    return f"The {query_type} for {company} in {year} is {value}."


# Chatbot loop
print("Welcome to the Financial Chatbot! Ask me about financial data (type 'exit' to quit).")

while True:
    user_query = input("\nEnter your query (e.g., 'What is the total revenue of Microsoft in 2023?'): ")

    if user_query.lower() == 'exit':
        print("Goodbye!")
        break

    company, year, query_type = extract_query_details(user_query)
    response = get_financial_data(company, year, query_type)
    print(response)
