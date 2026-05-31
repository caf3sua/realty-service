# Anh Duong Property API Service

This is the backend API service for **Anh Duong Property** built using **FastAPI** and **MongoDB (Motor - asynchronous driver)**. It serves listings (products), projects, and developer brands dynamically.

## Directory Structure

```text
realty-service/
├── app/
│   ├── core/
│   │   ├── config.py       # Configuration loader (Pydantic Settings)
│   │   └── database.py     # MongoDB connection setup (Motor client)
│   ├── models/
│   │   ├── developer.py    # Developer brand schemas
│   │   ├── product.py      # Real estate product listing schemas
│   │   └── project.py      # Project schemas
│   ├── routers/
│   │   ├── developers.py   # Developer API endpoints
│   │   ├── products.py     # Product CRUD and filter API endpoints
│   │   └── projects.py     # Project detail and list endpoints
│   └── main.py             # FastAPI entry point & CORS configuration
├── .env                    # Local environment variables
├── .env.example            # Example environment template
├── .gitignore              # Ignored files (virtualenv, cache, .env)
├── requirements.txt        # Package dependencies list
├── seed.py                 # Initial data seeding script
└── README.md               # Setup and development guide
```

---

## Installation & Setup

### 1. Prerequisites
- Python 3.10+ installed
- MongoDB instance (Atlas cluster or local)

### 2. Create Virtual Environment
Inside the `realty-service` directory, run:
```bash
python -m venv .venv
```

### 3. Activate Virtual Environment
- **Windows (PowerShell)**:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **macOS/Linux**:
  ```bash
  source .venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Environment Configuration
Create a `.env` file in the root directory and configure it (you can copy `.env.example`):
```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/?appName=anh-duong-land
DB_NAME=anh_duong_land
PORT=8000
HOST=0.0.0.0
```

---

## Seeding Database

To populate the database collections with mock data initially, run:
```bash
python seed.py
```
This drops the `developers`, `projects`, and `products` collections and fills them with the official list of items matching the frontend layout.

---

## Running the Application

Start the local Uvicorn development server:
```bash
uvicorn app.main:app --reload --port 8000
```

Once running:
- **API Base URL**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **Alternative ReDoc**: `http://localhost:8000/redoc`

---

## API Endpoints

### Products (Listings)
- `GET /api/products` - List all products (supports optional query filters: `product_type`, `developer`, `is_premium`, `project_slug`).
- `GET /api/products/{id}` - Fetch single product details.
- `POST /api/products` - Create new listing.
- `PUT /api/products/{id}` - Update a listing.
- `DELETE /api/products/{id}` - Delete a listing.

### Projects
- `GET /api/projects` - List all projects.
- `GET /api/projects/{slug}` - Fetch a single project.
- `POST /api/projects` - Create a project.

### Developers
- `GET /api/developers` - List all developers.
- `POST /api/developers` - Add a developer.
