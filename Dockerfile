FROM jupyter/datascience-notebook

  USER root

  RUN apt-get update && \
      apt-get install -y --no-install-recommends \
          fontconfig \
          fonts-nanum \
          fonts-noto-cjk && \
      rm -rf /var/lib/apt/lists/*

  RUN fc-cache -fv
  RUN rm -rf /home/jovyan/.cache/matplotlib

  USER jovyan