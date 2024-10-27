# Use the official Python image.
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the app
COPY . .

# Expose the port that Streamlit runs on
EXPOSE 8080

# Run the app
CMD streamlit run app.py --server.port 8080 --server.enableCORS false
