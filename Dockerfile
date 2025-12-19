FROM alpine:3.23.2

RUN apk update \
    && apk upgrade --no-cache

# Install Python 3 and pip
RUN apk add --no-cache \
  python3 \
  py3-pip \
  git

# Define build arguments (User ID and Group ID) 
ARG APP_ROOT=/app \
    UID=1000 \
    GID=1000

# Add non-root user
RUN addgroup -g ${UID} -S app \
  && adduser -u ${GID} -S app -G app

# Create application directory
RUN mkdir -p ${APP_ROOT} \
    && chown -R app:app ${APP_ROOT}

WORKDIR ${APP_ROOT}

# Switch to non-root user
USER app

# Create a virtual environment to host python packages
RUN python3 -m venv penv

# Add virtual environment to PATH to avoid ". ./penv/bin/activate ""
ENV VIRTUAL_ENV=${APP_ROOT}/penv
ENV PATH="${APP_ROOT}/penv/bin:$PATH"

COPY src/requirements/requirements.txt .
COPY src/*.py .

# Not working due to private repo
#RUN pip install --upgrade pip \
    #&& pip install --no-cache-dir -r requirements.txt

CMD ["python3", "python_demo.py", "--log-level", "DEBUG"]

# default command keeps the container alive forever
# CMD ["tail", "-f", "/dev/null"]
