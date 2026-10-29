FROM alpine:3.24.3

# Install Python 3 and pip
RUN  apk upgrade --no-cache
     apk add --no-cache \
       python3 \
       py3-pip \
       git

# Define build arguments (User ID and Group ID) 
ARG APP_ROOT=/app \
    UID=1000 \
    GID=1000

# Add non-root user
RUN addgroup -g ${GID} -S app \
  && adduser -u ${UID} -S app -G app

# Create application directory
RUN mkdir -p ${APP_ROOT} \
    && chown -R app:app ${APP_ROOT}

WORKDIR ${APP_ROOT}

# Switch to non-root user
USER ${UID}:${GID}

# Create a virtual environment to host python packages
RUN python3 -m venv penv

# Add virtual environment to PATH to avoid ". ./penv/bin/activate ""
ENV VIRTUAL_ENV=${APP_ROOT}/penv
ENV PATH="${APP_ROOT}/penv/bin:$PATH"

COPY --chown=${UID}:${GID} src/requirements/requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY --chown=${UID}:${GID} src/*.py .

CMD ["python3", "python_demo.py", "--log-level", "DEBUG"]

# default command keeps the container alive forever
# CMD ["tail", "-f", "/dev/null"]
