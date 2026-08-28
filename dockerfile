# Use a slim, official Python base image — small footprint, well-maintained
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy just requirements first — this lets Docker cache the pip install layer,
# so rebuilds are fast unless requirements.txt itself changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the app
COPY . .

# The port Gunicorn will listen on inside the container
EXPOSE 8000

# Same command your Procfile already uses on Beanstalk — consistent entry point
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]