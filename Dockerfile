FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN apk add curl
COPY . .
RUN chown -R nobody:nobody /app/
USER nobody

EXPOSE 8000

HEALTHCHECK --interval=1m --timeout=2s --retries=4 --start-period=2m CMD curl -s -o /dev/null -w "http/%{http_code}" -f http://localhost:8000/healthcheck || exit 1

CMD ["python", "app.py"]