ARG PYTHON_BASE=3.12-slim

FROM python:$PYTHON_BASE AS builder

RUN pip install -U pdm
ENV PDM_CHECK_UPDATE=false

COPY pyproject.toml pdm.lock /project/

WORKDIR /project
RUN pdm install --check --prod --no-editable

FROM python:$PYTHON_BASE

COPY --from=builder /project/.venv/ /project/.venv
COPY main.py /project/

ENV PATH="/project/.venv/bin:$PATH"
CMD ["python", "/project/main.py"]

EXPOSE 9199