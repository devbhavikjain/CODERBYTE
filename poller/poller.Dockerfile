# Use Base Image
FROM base_image

WORKDIR /app

COPY *.py /app/

EXPOSE 5005

CMD ["python3", "-u", "price_fetcher.py"]