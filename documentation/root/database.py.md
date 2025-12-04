# database.py

## 📋 Overview
PostgreSQL database management class that handles user authentication, registration, and language preferences for the KrishiSaathi application.

## 🎯 Purpose
- Secure user authentication and registration
- Password hashing and verification
- User language preference management
- Database connection pooling and error handling
- Support for both local and cloud database deployments

## 🏗️ Class Structure

### UserDatabase Class
```python
class UserDatabase:
    def __init__(self)
    def get_connection(self)
    def init_db(self)
    def hash_password(self, password)
    def create_user(self, username, email, password, language='en')
    def verify_user(self, username, password)
    def update_language(self, username, language)
```

## 🔧 Key Features

### 1. Flexible Database Connection
```python
# Supports both DATABASE_URL (Railway/Heroku) and individual parameters
database_url = os.getenv('DATABASE_URL')
if database_url:
    self.database_url = database_url
    self.use_url = True
else:
    # Fallback to individual environment variables
    self.db_config = {
        'dbname': os.getenv("DB_NAME", "KrishiSaathi"),
        'user': os.getenv("DB_USER", "postgres"),
        'password': os.getenv("DB_PASSWORD", "Prathyush@04"),
        'host': os.getenv("DB_HOST", "localhost"),
        'port': os.getenv("DB_PORT", "5432")
    }
```

### 2. Secure Password Handling
```python
def hash_password(self, password):
    return hashlib.sha256(password.encode()).hexdigest()
```

### 3. Robust Connection Management
```python
def get_connection(self):
    try:
        if self.use_url:
            return psycopg2.connect(
                self.database_url,
                connect_timeout=10,
                application_name='krishisaathi'
            )
        else:
            return psycopg2.connect(
                connect_timeout=10,
                application_name='krishisaathi',
                **self.db_config
            )
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        raise
```

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(64) NOT NULL,
    language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## 🔐 Security Features

### Password Security
- **SHA-256 Hashing**: Passwords are hashed before storage
- **No Plain Text**: Original passwords never stored
- **Salt Consideration**: Consider adding salt for enhanced security

### Database Security
- **Connection Timeout**: 10-second timeout prevents hanging connections
- **Error Handling**: Comprehensive exception handling
- **SQL Injection Protection**: Parameterized queries used throughout

## 🚀 API Methods

### User Registration
```python
def create_user(self, username, email, password, language='en'):
    # Returns True on success, False on duplicate user
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, language) VALUES (%s, %s, %s, %s)",
            (username, email, self.hash_password(password), language)
        )
        return True
    except psycopg2.IntegrityError:
        return False  # Duplicate username/email
```

### User Authentication
```python
def verify_user(self, username, password):
    # Returns user data tuple or None
    cursor.execute(
        "SELECT id, username, email, language FROM users WHERE username = %s AND password_hash = %s",
        (username, self.hash_password(password))
    )
    return cursor.fetchone()
```

### Language Update
```python
def update_language(self, username, language):
    cursor.execute(
        "UPDATE users SET language = %s WHERE username = %s",
        (language, username)
    )
```

## 🔄 Error Handling

### Connection Retry Logic
```python
def init_db(self):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Database initialization
            return
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2)  # Wait before retry
```

### Resource Management
- **Automatic Cleanup**: Connections and cursors properly closed
- **Exception Safety**: Finally blocks ensure resource cleanup
- **Memory Management**: No connection pooling to prevent memory leaks

## 🌍 Environment Variables

### Required Variables
```bash
# Option 1: Database URL (preferred for cloud deployment)
DATABASE_URL=postgresql://user:password@host:port/database

# Option 2: Individual parameters (local development)
DB_NAME=KrishiSaathi
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

## 📈 Performance Considerations

### Connection Management
- **No Pooling**: Prevents segmentation faults in some environments
- **Short-lived Connections**: Each operation opens/closes connection
- **Timeout Protection**: 10-second connection timeout

### Query Optimization
- **Indexed Columns**: Username and email should be indexed
- **Prepared Statements**: Parameterized queries for security and performance

## 🔧 Usage Example

```python
from database import UserDatabase

# Initialize database
db = UserDatabase()

# Register new user
success = db.create_user("farmer1", "farmer@example.com", "password123", "hi")

# Authenticate user
user_data = db.verify_user("farmer1", "password123")
if user_data:
    user_id, username, email, language = user_data
    print(f"Welcome {username}!")

# Update language preference
db.update_language("farmer1", "te")
```

## 🚨 Security Recommendations

### Production Deployment
1. **Use Strong Passwords**: Enforce password complexity
2. **Add Salt**: Implement salted password hashing
3. **Rate Limiting**: Add login attempt rate limiting
4. **SSL/TLS**: Use encrypted database connections
5. **Environment Variables**: Never hardcode credentials

### Database Security
1. **Principle of Least Privilege**: Database user should have minimal required permissions
2. **Network Security**: Restrict database access to application servers only
3. **Regular Backups**: Implement automated backup strategy
4. **Monitoring**: Log and monitor database access patterns

## 🐛 Common Issues

### Connection Problems
- **Firewall**: Ensure database port is accessible
- **Credentials**: Verify environment variables are set correctly
- **Network**: Check network connectivity to database server

### Performance Issues
- **Connection Timeout**: Increase timeout for slow networks
- **Resource Limits**: Monitor database connection limits
- **Query Performance**: Add indexes for frequently queried columns

---

**File Location**: `/database.py`  
**Type**: Python Module  
**Dependencies**: psycopg2, hashlib, os, datetime, logging  
**Used By**: FastAPI main application, authentication endpoints