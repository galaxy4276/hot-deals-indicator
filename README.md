# What is This?
---

![banner.webp](public/service_banner.webp)

실시간 핫딜 정보를 카카오톡으로 전달해주는 서비스 애플리케이션

#### [서비스 아이디어 구상 및 소개 문서](https://woolly-hoodie-ae9.notion.site/11318d349b958068b39ee2468f477e9a?pvs=4)

elk 구성 도커는 `deviantony/docker-elk` [레포지토리](https://github.com/deviantony/docker-elk?tab=readme-ov-file#how-to-configure-logstash) 를 참고하였습니다.


---


# Documentation

## Requirement

| 기술             | 요구 버전       | link                                                                    |
|----------------|-------------|-------------------------------------------------------------------------|
| Node.js        | >=v.20.16.0 | [Official Doc](https://nodejs.org/en/blog/release/v20.16.0)             |
| Docker Compose | >=v2.19.1   | [Release Note](https://docs.docker.com/compose/releases/release-notes/) |
| Python3        | >=v3.12.4 | - |

## Getting Started

1. `elastic-stack` 디렉터리 내에서 `.env.example` 를 참고하여 `.env` 작성
2. `docker-compose up -d` 명령어를 통해 인스턴스를 실행
