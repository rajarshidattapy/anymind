# Anymind Backend API Documentation

Complete documentation for the Anymind backend API, including authentication, endpoints, data models, and UI integration.

## Table of Contents

- [Overview](#overview)
- [Base URL](#base-url)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Data Models](#data-models)
- [Error Handling](#error-handling)
- [UI Integration](#ui-integration)
- [Configuration](#configuration)

## Overview

The Anymind backend is a FastAPI-based REST API that provides:

- User authentication and API key management
- Agent lifecycle management (create, list, update, delete)
- Agent versioning and artifact uploads
- Build validation and processing
- Runtime execution of agents
- Logging and observability

**API Version:** v1  
**Base Path:** `/api/v1`

## Base URL

Default base URL: `http://localhost:8000`

Configure via environment variable:
```bash
ANYMIND_API_URL=http://localhost:8000
```

## Authentication

The API supports two authentication methods:

### 1. JWT Token Authentication (Web UI)

For web UI interactions, use JWT tokens obtained via login:

```http
Authorization: Bearer <jwt-token>
```

**Endpoints:**
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user info

### 2. API Key Authentication (CLI/SDK)

For CLI and SDK usage, use API keys:

```http
X-API-Key: <api-key>
```

API keys are created via the web UI and are hashed in the database. The full key is only shown once upon creation.

**Endpoints:**
- `POST /api/v1/api-keys` - Create API key (requires JWT)
- `GET /api/v1/api-keys` - List API keys (requires JWT)
- `DELETE /api/v1/api-keys/{api_key_id}` - Revoke API key (requires JWT)

### Authentication Priority

The `get_authenticated_user` dependency checks:
1. `X-API-Key` header (for CLI)
2. `Authorization: Bearer` header (for web UI)

## API Endpoints

### Authentication Endpoints

#### Register User

```http
POST /api/v1/auth/register
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password",
  "full_name": "Full Name" // optional
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "is_active": true
}
```

#### Login

```http
POST /api/v1/auth/login
Content-Type: application/json
```

**Request Body:**
```json
{
  "username": "username",
  "password": "password"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### Get Current User

```http
GET /api/v1/auth/me
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "is_active": true
}
```

### API Key Management

#### Create API Key

```http
POST /api/v1/api-keys
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "My CLI Key"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "key": "anymind_abc123...", // Only shown once!
  "key_prefix": "anymind_abc1",
  "name": "My CLI Key",
  "created_at": "2024-01-01T00:00:00"
}
```

#### List API Keys

```http
GET /api/v1/api-keys
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "key_prefix": "anymind_abc1",
    "name": "My CLI Key",
    "is_active": true,
    "last_used_at": "2024-01-01T12:00:00",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

#### Revoke API Key

```http
DELETE /api/v1/api-keys/{api_key_id}
Authorization: Bearer <token>
```

**Response:** `204 No Content`

### Agent Management

#### Create Agent

```http
POST /api/v1/agents
X-API-Key: <api-key>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "my-agent",
  "description": "My AI agent" // optional
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "my-agent",
  "description": "My AI agent",
  "user_id": 1,
  "status": "draft",
  "current_version_id": null,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

#### List Agents

```http
GET /api/v1/agents?skip=0&limit=100
X-API-Key: <api-key>
```

**Query Parameters:**
- `skip` (int, default: 0) - Number of records to skip
- `limit` (int, default: 100) - Maximum records to return

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "my-agent",
    "description": "My AI agent",
    "user_id": 1,
    "status": "ready",
    "current_version_id": 5,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

#### Get Agent

```http
GET /api/v1/agents/{agent_id}
X-API-Key: <api-key>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "my-agent",
  "description": "My AI agent",
  "user_id": 1,
  "status": "ready",
  "current_version_id": 5,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

#### Update Agent

```http
PATCH /api/v1/agents/{agent_id}
X-API-Key: <api-key>
Content-Type: application/json
```

**Request Body:** (all fields optional)
```json
{
  "name": "updated-name",
  "description": "Updated description",
  "status": "archived"
}
```

**Response:** `200 OK` (same as Get Agent)

#### Delete Agent

```http
DELETE /api/v1/agents/{agent_id}
X-API-Key: <api-key>
```

**Response:** `204 No Content`

### Artifact Upload

#### Upload Agent Artifact

```http
POST /api/v1/uploads/agent/{agent_id}
X-API-Key: <api-key>
Content-Type: multipart/form-data
```

**Request:**
- `file`: `.tar.gz` file (multipart/form-data)

**Response:** `201 Created`
```json
{
  "id": 1,
  "agent_id": 1,
  "version": "v1",
  "status": "queued",
  "build_log": null,
  "tarball_path": "agents/1/artifacts/agent_1_artifact.tar.gz",
  "entrypoint": null,
  "config": null,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**Notes:**
- File must be `.tar.gz` format
- Maximum file size: 100MB (configurable)
- Automatically creates a new `AgentVersion` with status `queued`
- Triggers background build job

#### Download File

```http
GET /api/v1/uploads/{filepath}
X-API-Key: <api-key>
```

**Response:** `200 OK` (binary file content)

### Runtime Execution

#### Execute Agent

```http
POST /api/v1/runtime/{agent_id}/execute
X-API-Key: <api-key>
Content-Type: application/json
```

**Request Body:**
```json
{
  "payload": {
    "input": "Hello, world!"
  }
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "agent_version_id": 5,
  "user_id": 1,
  "status": "completed",
  "input_data": {"input": "Hello, world!"},
  "output_data": {"result": "Response from agent"},
  "error_message": null,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**Notes:**
- Uses the latest `ready` version of the agent
- Executes with 30-second timeout
- Returns execution result or error

#### List Executions

```http
GET /api/v1/runtime/executions?agent_version_id=5&skip=0&limit=100
X-API-Key: <api-key>
```

**Query Parameters:**
- `agent_version_id` (int, optional) - Filter by version
- `skip` (int, default: 0)
- `limit` (int, default: 100)

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "agent_version_id": 5,
    "user_id": 1,
    "status": "completed",
    "input_data": {...},
    "output_data": {...},
    "error_message": null,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

#### Get Execution

```http
GET /api/v1/runtime/executions/{execution_id}
X-API-Key: <api-key>
```

**Response:** `200 OK` (same structure as execution in list)

#### Cancel Execution

```http
POST /api/v1/runtime/executions/{execution_id}/cancel
X-API-Key: <api-key>
```

**Response:** `200 OK` (execution object with status `cancelled`)

### Logs

#### Get Agent Logs

```http
GET /api/v1/logs/{agent_id}
X-API-Key: <api-key>
```

**Response:** `200 OK`
```json
[
  {
    "timestamp": "2024-01-01T00:00:00",
    "level": "INFO",
    "message": "Build completed successfully",
    "source": "build",
    "metadata": {
      "version_id": 1,
      "status": "ready"
    }
  },
  {
    "timestamp": "2024-01-01T12:00:00",
    "level": "INFO",
    "message": "Execution 1 completed successfully",
    "source": "runtime",
    "metadata": {
      "execution_id": 1,
      "status": "completed"
    }
  }
]
```

#### Get Execution Logs

```http
GET /api/v1/logs/executions/{execution_id}/logs
X-API-Key: <api-key>
```

**Response:** `200 OK` (array of log entries)

## Data Models

### Agent

```typescript
{
  id: number
  name: string
  description?: string
  user_id: number
  status: "draft" | "building" | "ready" | "failed" | "archived"
  current_version_id?: number
  created_at: string (ISO 8601)
  updated_at: string (ISO 8601)
}
```

### AgentVersion

```typescript
{
  id: number
  agent_id: number
  version: string // e.g., "v1", "v2"
  status: "queued" | "building" | "ready" | "failed"
  build_log?: string
  tarball_path?: string
  entrypoint?: string // e.g., "agent.main:handle"
  config?: string // YAML config as string
  created_at: string (ISO 8601)
  updated_at: string (ISO 8601)
}
```

### Execution

```typescript
{
  id: number
  agent_version_id: number
  user_id: number
  status: "pending" | "running" | "completed" | "failed" | "cancelled"
  input_data?: object
  output_data?: object
  error_message?: string
  logs?: string
  created_at: string (ISO 8601)
  updated_at: string (ISO 8601)
}
```

### User

```typescript
{
  id: number
  email: string
  username: string
  full_name?: string
  is_active: boolean
}
```

### APIKey

```typescript
{
  id: number
  key_prefix: string // First 12 chars for display
  name: string
  is_active: boolean
  last_used_at?: string (ISO 8601)
  created_at: string (ISO 8601)
}
```

### LogEntry

```typescript
{
  timestamp: string (ISO 8601)
  level: "INFO" | "ERROR" | "WARNING" | "DEBUG"
  message: string
  source?: "build" | "runtime"
  metadata?: object
}
```

## Error Handling

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

- `200 OK` - Success
- `201 Created` - Resource created
- `204 No Content` - Success, no content
- `400 Bad Request` - Invalid request
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `413 Request Entity Too Large` - File too large
- `500 Internal Server Error` - Server error

### Common Errors

**401 Unauthorized:**
```json
{
  "detail": "Invalid API key"
}
```

**404 Not Found:**
```json
{
  "detail": "Agent not found"
}
```

**400 Bad Request:**
```json
{
  "detail": "File must be a .tar.gz archive"
}
```

## UI Integration

### Frontend Setup

1. **Base Configuration:**
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const API_V1 = `${API_BASE_URL}/api/v1`;
```

2. **Authentication Flow:**

```javascript
// Login
const login = async (username, password) => {
  const response = await fetch(`${API_V1}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  const data = await response.json();
  // Store token: localStorage.setItem('token', data.access_token);
  return data;
};

// Authenticated requests
const authenticatedFetch = async (url, options = {}) => {
  const token = localStorage.getItem('token');
  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
};
```

3. **Agent Management:**

```javascript
// List agents
const listAgents = async () => {
  const response = await authenticatedFetch(`${API_V1}/agents`);
  return response.json();
};

// Create agent
const createAgent = async (name, description) => {
  const response = await authenticatedFetch(`${API_V1}/agents`, {
    method: 'POST',
    body: JSON.stringify({ name, description })
  });
  return response.json();
};

// Upload artifact
const uploadArtifact = async (agentId, file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const token = localStorage.getItem('token');
  const response = await fetch(`${API_V1}/uploads/agent/${agentId}`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData
  });
  return response.json();
};
```

4. **Real-time Updates:**

For build status updates, poll the agent endpoint:

```javascript
const pollAgentStatus = async (agentId, onUpdate) => {
  const interval = setInterval(async () => {
    const agent = await getAgent(agentId);
    onUpdate(agent);
    
    // Stop polling when build is complete
    if (['ready', 'failed'].includes(agent.status)) {
      clearInterval(interval);
    }
  }, 2000); // Poll every 2 seconds
};
```

5. **Error Handling:**

```javascript
const handleApiError = async (response) => {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }
  return response.json();
};
```

### CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:3000` (default React dev server)
- `http://localhost:8000` (backend itself)

Configure via `CORS_ORIGINS` environment variable (comma-separated).

### Example React Hook

```javascript
import { useState, useEffect } from 'react';

const useAgents = () => {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const response = await authenticatedFetch(`${API_V1}/agents`);
        const data = await response.json();
        setAgents(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchAgents();
  }, []);

  return { agents, loading, error };
};
```

## Configuration

### Environment Variables

Create a `.env` file in the `server/` directory:

```bash
# Application
APP_NAME=Agent Management API
APP_VERSION=1.0.0
DEBUG=False

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/anymind

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Storage
STORAGE_PATH=./storage
UPLOAD_MAX_SIZE=104857600

# Workers
WORKER_CONCURRENCY=4
```

### Database Setup

1. Create PostgreSQL database
2. Run migrations (Alembic):
```bash
cd server
alembic upgrade head
```

### Running the Server

```bash
cd server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

## Build Process

1. **Upload:** Agent artifact uploaded via `POST /api/v1/uploads/agent/{agent_id}`
2. **Queue:** Version created with status `queued`
3. **Build:** Background worker processes the build:
   - Extracts tarball
   - Validates `anymind.yaml`
   - Validates entrypoint exists and is callable
   - Updates status to `ready` or `failed`
4. **Ready:** Agent can be executed once status is `ready`

## Runtime Execution

1. **Request:** `POST /api/v1/runtime/{agent_id}/execute`
2. **Load:** Latest `ready` version is selected
3. **Extract:** Agent tarball is extracted to temp directory
4. **Import:** Entrypoint module is dynamically imported
5. **Execute:** `handle(payload)` function is called
6. **Timeout:** 30-second timeout enforced
7. **Response:** Execution result or error returned

## Security Considerations

- API keys are hashed using SHA256
- JWT tokens expire after 30 minutes (configurable)
- Passwords are hashed using bcrypt
- CORS is configured for specific origins
- File uploads are limited to 100MB
- All endpoints require authentication (except `/auth/register` and `/auth/login`)

