# Use Base Image
FROM base_image

WORKDIR /app

COPY api.py /app/

EXPOSE 5005

CMD ["python3", "-u", "api.py"]