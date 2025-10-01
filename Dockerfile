FROM jupyter/datascience-notebook

USER root

# 1) 한글 폰트 설치 (Nanum + 대안 Noto CJK 함께)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        fontconfig \
        fonts-nanum \
        fonts-noto-cjk && \
    rm -rf /var/lib/apt/lists/*

# 2) 시스템 폰트 캐시 갱신
RUN fc-cache -fv

# 3) jovyan 사용자의 matplotlib 캐시 폴더 정리(있다면)
RUN rm -rf /home/jovyan/.cache/matplotlib

USER jovyan
