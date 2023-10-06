# Neuro.net MKAD Range Analyzer API

Commissioned by [Neuro.net](https://neuro.net/) for the role of a Python Backend Developer, this project offers a geolocation solution to determine the distance from any address to the [MKAD (Moskovskaya Kol'tsevaya Avtomobil'naya Doroga)](https://maps.app.goo.gl/mc1hgemuSpMnn1E8A). It efficiently leverages the [Yandex Geocoder API](https://yandex.ru/dev/geocode/doc/en/) to achieve precise location results.

## Table of Contents

1. [Disclaimer](#disclaimer)
2. [Project Description](#project-description)
3. [Project Architecture](#project-architecture)
4. [Features](#features)
5. [Installation Guide](#installation-guide)
6. [References](#references)

## Disclaimer

This project repository has been made public with the explicit permission of [Neuro.net](https://neuro.net/). All related rights and code propriety belong to [Neuro.net](https://neuro.net/), and the project is showcased here for demonstrative and portfolio purposes.

## Project Description

Determining the distance between a given location and a city's key landmark, in this case, [Moscow's MKAD](https://maps.app.goo.gl/mc1hgemuSpMnn1E8A), is a frequent use case for services ranging from delivery systems to property listings. This project provides an API solution to this problem, determining if an address lies inside [MKAD](https://maps.app.goo.gl/mc1hgemuSpMnn1E8A) or, if not, how far it is from it. This API leverages the [Yandex Geocoder API](https://yandex.ru/dev/geocode/doc/en/) to determine the precise coordinates of a given address, then calculates the distance from [MKAD](https://maps.app.goo.gl/mc1hgemuSpMnn1E8A).

[Neuro.net](https://neuro.net/) is a leading firm in the Contact Center AI domain, deploying fully autonomous AI-driven contact centers that cover diverse communication channels, including voice, text, and email. Their virtual agents have impressively replaced many human agents, managing over 300 million dialogues. Notably, in these interactions, 99% of the participants believed they were conversing with humans. As [Neuro.net](https://neuro.net/) expands its voice-activated robots that leverage Python for real-time, natural language communications, every supporting service needs to be optimized and efficient.

This geolocation API plays a critical role in that larger vision, offering precise geospatial computations essential for some of their services. [Neuro.net](https://neuro.net/) commissioned this project specifically for the Python back-end developer role, highlighting the company's commitment to robust, accurate, and effective development practices in their drive to innovate.

## Project Architecture

The project's architecture has a structured folder layout for better organization and accessibility. The root directory consists of several sub-folders each dedicated for specific purposes. The project's folder structure would look like this:

```bash
.
├── config
│   └── config.py
├── log
│   └── app.log
├── app.py
└── blueprint.py
```

## Features

- **Rate Limiting**: Ensuring no single user can overwhelm the system.
- **Address Validation**: Verifying and resolving provided addresses.
- **Distance Calculation**: Computation of distance from the provided address to MKAD.
- **Error Handling**: Graceful handling of various error states for robustness.

## Installation Guide

This project is containerized using Docker for consistent deployment and ease of scalability. The guide below provides a step-by-step instruction to get the API running using Docker:

### Build The Docker Image

Ensure you're in the root directory of the project, then build the Docker image with the following command:

```bash
docker build -t mkad-api:latest .
```

### Create and Run The Docker Container

After building the image, create a Docker container with this command:

```bash
docker run -p 5000:5000 mkad-api:latest
```

When the container is running successfully, the API becomes accessible at this [URL](http://localhost:8501/):

```bash
http://localhost:5000/
```

The container will keep running until you stop it. To do so, press <kbd>CTRL</kbd> + <kbd>C</kbd> in your terminal.

### Testing The API

To test the distance calculation functionality, you can use applications like Postman or a simple `curl` command. Send a `POST` request to the endpoint:

```bash
http://localhost:5000/distance
```

With the following JSON payload:

```json
{
  "address": "Your Address Here"
}
```

If the address is inside the MKAD:

```json
{
  "message": "The address is inside the MKAD."
}
```

If the address is outside the MKAD:

```json
{
  "message": "The address is 820.43 km away from the MKAD."
}
```

(Note: The distance in the message will vary based on the address provided.)

This will allow you to understand how far a given address is from the MKAD, either being inside the ring or a specified distance away.

## References

This section lists all the references and resources utilized during the project.

[1] [Flask](https://flask.palletsprojects.com/en/3.0.x/)

[2] [Yandex Geocoder API](https://yandex.ru/dev/geocode/doc/en/)

[3] [Docker](https://www.docker.com/)
