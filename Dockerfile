FROM python:latest
COPY . .
# COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN pip install -r requirements.txt
# RUN chmod +x /docker-entrypoint.sh
# RUN python seed_database.py
EXPOSE 8000
CMD python server.py
# ENTRYPOINT ["/docker-entrypoint.sh"]