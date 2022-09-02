FROM docker.io/fnndsc/conda:python3.10.6

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="Average Edge Length" \
      org.opencontainers.image.description="Average edge length about each vertex of a surface mesh."

WORKDIR /usr/local/src/pl-obj-avg-edge-length

RUN conda install -c conda-forge numpy=1.22.4
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ARG extras_require=none
RUN pip install ".[${extras_require}]"

CMD ["edgy", "--help"]
