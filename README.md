# URL Shortener

A comprehensive URL shortening service built with FastAPI, featuring microservices architecture, JWT authentication, rate limiting, and analytics capabilities.

## 📋 Features

- **URL Shortening**: Convert long URLs into short, shareable links
- **Authentication**: JWT-based secure authentication
- **Rate Limiting**: Protect API endpoints from abuse
- **Analytics**: Track URL clicks and usage statistics
- **Microservices Architecture**: Modular design with separate services
- **Redis Caching**: Fast data retrieval and session management
- **PostgreSQL Database**: Persistent data storage
- **Async Processing**: Celery worker for background tasks
- **Docker Support**: Easy deployment with Docker Compose

## 🏗️ Architecture

This project uses a microservices architecture with the following services:

### Services

1. **Auth Service** (Port 8001)
   - User authentication and registration
   - JWT token generation and validation
   - User management

2. **URL Service** (Port 8002)
   - URL shortening and creation
   - URL redirection
   - Custom alias support

3. **Analytics Service** (Port 8003)
   - Click tracking and statistics
   - Usage analytics
   - Background task processing with Celery

### Infrastructure

- **PostgreSQL**: Primary database for data persistence
- **Redis**: Caching layer and message broker for Celery
- **Celery Worker**: Asynchronous task processing

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI
- **Language**: Python 3.8+
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Task Queue**: Celery
- **Authentication**: JWT (JSON Web Tokens)
- **Containerization**: Docker & Docker Compose
- **Deployment**: Render.yaml configuration included

## 📊 Project Statistics

- **Language Composition**: Python (97.1%), Dockerfile (2.9%)
- **Topics**: backend, docker, fastapi, jwt, microservices, postgresql, python3, rate-limiting, redis, url-shortener

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.8+ (for local development)
- Git

### Setup with Docker Compose

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ujjwalverma2803/url-shortener.git
   cd url-shortener
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Verify services are running**
   ```bash
   docker-compose ps
   ```

### Service Endpoints

- Auth Service: `http://localhost:8001`
- URL Service: `http://localhost:8002`
- Analytics Service: `http://localhost:8003`
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

## 📝 Environment Configuration

Create a `.env` file based on `.env.example`:

```env
# PostgreSQL
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=url_shortener_db

# Redis
REDIS_URL=redis://redis:6379/0

# JWT
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256

# Service Ports
AUTH_PORT=8001
URL_PORT=8002
ANALYTICS_PORT=8003
```

## 🔌 API Usage

### Authentication

```bash
# Register a new user
curl -X POST http://localhost:8001/register \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'

# Login
curl -X POST http://localhost:8001/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'
```

### URL Shortening

```bash
# Create a short URL
curl -X POST http://localhost:8002/shorten \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://example.com/very/long/url"}'

# Redirect to original URL
curl -L http://localhost:8002/r/{short_code}
```

### Analytics

```bash
# Get URL statistics
curl -X GET http://localhost:8003/stats/{short_code} \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 📁 Project Structure

```
url-shortener/
├── services/
│   ├── auth/
│   │   ├── main.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── url/
│   │   ├── main.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── analytics/
│       ├── main.py
│       ├── tasks.py
│       ├── Dockerfile
│       └── requirements.txt
├── tests/
├── docker-compose.yml
├── render.yaml
├── .env.example
├── .gitignore
└── README.md
```

## 🧪 Testing

Run tests locally:

```bash
cd services/auth
pytest

cd ../url
pytest

cd ../analytics
pytest
```

## 🐳 Docker Commands

```bash
# Start services
docker-compose up

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild images
docker-compose build --no-cache

# Run specific service
docker-compose up -d auth
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Rate Limiting**: Prevent API abuse
- **HTTPS Ready**: Configure SSL/TLS in production
- **Environment Variables**: Sensitive data management
- **Password Hashing**: Secure password storage

## 🚀 Deployment

### Render Deployment

The project includes a `render.yaml` configuration for easy deployment to Render:

```bash
# Deploy to Render
git push origin main
# Render will automatically detect render.yaml and deploy
```

## 📊 Performance Considerations

- **Redis Caching**: Reduces database queries
- **Async Processing**: Celery workers handle long-running tasks
- **Connection Pooling**: Efficient database connection management
- **Load Balancing**: Multiple service instances support

## 🐛 Troubleshooting

### Services won't start
- Check Docker daemon is running
- Verify `.env` file is properly configured
- Check port availability (8001, 8002, 8003)

### Database connection errors
- Ensure PostgreSQL healthcheck passes
- Verify connection string in `.env`
- Check database user permissions

### Redis connection issues
- Verify Redis service is running
- Check `REDIS_URL` in `.env`
- Verify network connectivity

## 📚 API Documentation

Each service provides Swagger documentation:

- Auth Service Docs: `http://localhost:8001/docs`
- URL Service Docs: `http://localhost:8002/docs`
- Analytics Service Docs: `http://localhost:8003/docs`

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Ujjwal Verma**
- GitHub: [@Ujjwalverma2803](https://github.com/Ujjwalverma2803)

## 📞 Support

For issues and questions:
- Open an issue on [GitHub Issues](https://github.com/Ujjwalverma2803/url-shortener/issues)
- Check existing documentation in the wiki

## 🔗 Related Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/docs/)
- [Celery Documentation](https://docs.celeryproject.io/)

---

**Last Updated**: 2026-07-09
