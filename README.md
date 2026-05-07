# devcheck — containerized DevOps environment checker

A multi-container application that checks your DevOps tool installations 
and stores results in MongoDB.

## Architecture

Three containers connected via Docker Compose:
- nginx — reverse proxy (frontend network)
- devcheck — Python CLI tool that checks installed DevOps tools (both networks)
- mongodb — stores check results as JSON documents (backend network)

Network isolation: nginx cannot directly reach mongodb. 
devcheck sits on both networks as the bridge between tiers.

## Prerequisites

- Docker
- Docker Compose

## Usage

Start all containers:
```bash
docker compose up -d
```

Run environment check and save results to MongoDB:
```bash
docker compose run --rm devcheck --save
```

Run check without saving:
```bash
docker compose run --rm devcheck
```

Generate JSON report:
```bash
docker compose run --rm devcheck --report
```

Deploy latest version:
```bash
./deploy.sh
```

## Tools checked

Docker, Git, kubectl, Terraform, Ansible

## Data persistence

MongoDB data is stored in a named volume and survives container restarts. 
To wipe all data:
```bash
docker compose down -v
```