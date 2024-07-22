ARG PYTHON_IMAGE=python
ARG PIPENV_CUSTOM_VERSION="2021.5.29"
FROM ${PYTHON_IMAGE}:3.9

ENV APP_USER=samuel
ENV APP_DIR=/app
ARG PIPENV_CUSTOM_VERSION

ENV PYTHONPATH="${APP_DIR}:${APP_DIR}/src:${PYTHONPATH}"

COPY ./devops/images/entrypoint.sh /usr/local/bin/

RUN mkdir -p ${APP_DIR} \
    && chmod a+x /usr/local/bin/entrypoint.sh \
    && pip install pipenv==$PIPENV_CUSTOM_VERSION \
    && addgroup --gid 1984 $APP_USER \
    && adduser --uid 1984 --ingroup $APP_USER --disabled-password --gecos "" $APP_USER

WORKDIR ${APP_DIR}
ENTRYPOINT ["entrypoint.sh"]
CMD ["run-server"]

COPY --chown=$APP_USER:$APP_USER Pipfile Pipfile.lock ${APP_DIR}/
USER ${APP_USER}

RUN cd ${APP_DIR} \
    && pipenv install

COPY --chown=${APP_USER}:${APP_USER} app.py ${APP_DIR}/

COPY --chown=${APP_USER}:${APP_USER} src/ ${APP_DIR}/src/