# Contentizer

A content management and search application built for the Sketch & Search Hackathon.

## Overview

Contentizer is a tool designed to help you manage and search through your content efficiently.

## Installation

clone the project repository:
```bash
git clone 
```

in the project directory, run the mongodb server:
```bash
docker compose up -d
```

### Backend Installation

move to the backend directory:
```bash
cd back
```

create a virtual environment and activate it:
```bash
python -m venv .venv 
```

or 

```bash
python3 -m venv .venv
```

install the required packages:
```bash
uv sync --active
```

Now you can run the backend server:
‍
```bash
uv run uvicorn src.api.main:app --reload --port 8000
```

### Frontend Installation

move to the frontend directory and install dependencies:
```bash
cd front/contentizer

npm install

npm run dev
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License
MIT