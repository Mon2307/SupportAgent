FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install pysqlite3-binary
RUN pip install -r requirements.txt --upgrade

EXPOSE 8000

ENV IS_USING_IMAGE_RUNTIME=True

COPY api_handler.py ${LAMBDA_TASK_ROOT}
COPY rag_app ${LAMBDA_TASK_ROOT}/rag_app
COPY chroma ${LAMBDA_TASK_ROOT}/chroma
