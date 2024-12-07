```mermaid
sequenceDiagram
    actor Client
    participant API
    participant DataViz
    participant DB

    Note over Client,DB: Dashboard Creation Flow
    Client->>API: POST /dashboards
    Note right of Client: {dashboard_title, owner_email, graph_ids, xy_coords, width_height}
    API->>DataViz: create_new_dashboard()
    DataViz->>DB: Insert dashboard & permissions
    DB-->>DataViz: Return dashboard_id
    DataViz-->>API: Return Dashboard object
    API-->>Client: Dashboard response

    Note over Client,DB: View Dashboards Flow
    Client->>API: GET /dashboards/map?user_email=user@example.com
    API->>DataViz: get_dashboard_id_mp()
    DataViz->>DB: Query accessible dashboards
    DB-->>DataViz: Return dashboard metadata
    DataViz-->>API: DashboardMapResponse
    API-->>Client: List of accessible dashboards

    Note over Client,DB: View Single Dashboard
    Client->>API: GET /dashboards?dashboard_id=123&user_email=user@example.com
    API->>DataViz: render_dashboard()
    DataViz->>DB: Check permissions & fetch data
    DB-->>DataViz: Return dashboard data
    DataViz-->>API: Dashboard object
    API-->>Client: Dashboard with graphs

    Note over Client,DB: Manage Permissions
    Client->>API: PUT /dashboards/permissions
    Note right of Client: {dashboard_id, permissions[], requester_email}
    API->>DataViz: update_dashboard_permissions()
    DataViz->>DB: Update permission records
    DB-->>DataViz: Success
    DataViz-->>API: Success response
    API-->>Client: Success message

    Note over Client,DB: Update Access Level
    Client->>API: PUT /dashboards/access-level
    Note right of Client: {dashboard_id, access_level, requester_email}
    API->>DataViz: update_access_level()
    DataViz->>DB: Update access level
    DB-->>DataViz: Success
    DataViz-->>API: Success response
    API-->>Client: Success message

    Note over Client,DB: Delete Dashboard
    Client->>API: DELETE /dashboards
    Note right of Client: {dashboard_id, graph_ids[]}
    API->>DataViz: delete_dashboard()
    DataViz->>DB: Delete dashboard/graphs
    DB-->>DataViz: Success
    DataViz-->>API: Success response
    API-->>Client: Success message

```
### 1. Overall Architecture

The application follows a three-tier architecture:
```
[Frontend (React)] <---> [Backend (FastAPI)] <---> [Database (SQLite)]
```
#### 1.1 System Architecture Diagram

```mermaid
graph TB
    subgraph Frontend
        UI[User Interface]
        RC[React Components]
        AS[Application State]
    end
    subgraph Backend
        API[FastAPI Server]
        BL[Business Logic]
        DM[Data Managers]
    end
    subgraph Database
        SQL[SQLite DB]
        FS[File Storage]
    end
    
 %% Connections
UI --> RC
RC --> AS
RC --> API
API --> BL
BL --> DM
DM --> SQL
DM --> FS
```
#### 1.2 Overall Component Interaction Flow
```mermaid
sequenceDiagram
participant U as User
participant F as Frontend
participant B as Backend
participant DB as Database
participant A as Auth0
U->>F: Access Dashboard
F->>A: Authenticate
A->>F: Return Token
F->>B: Request Dashboard Data
B->>DB: Query Data
DB->>B: Return Data
B->>F: Send Dashboard
F->>U: Display Dashboard
```

**Key Design Patterns:**
- Facade Pattern (Backend)
- Component-Based Architecture (Frontend)
- Repository Pattern (Data Access)
- MVC Pattern (Overall Structure)

### 2. Frontend Architecture
```mermaid

graph TB
subgraph Components
UC3[UC3 Main Component]
L[Landing]
SD[SingleDashboard]
RD[ReadOnlyDash]
PD[PublicDashboard]
ATP[AddTilePage]
G[Graph]
T[Tile]
end
subgraph State Management
Props[Props]
State[Local State]
API[API Calls]
end
UC3 --> L & SD & RD & PD
SD --> ATP & T
RD --> T
T --> G
PD --> RD
L & SD & RD & PD --> State
State --> API
```

**Detailed Dashboard Card Types:**

1. **OwnerDashboardCard**
```javascript
// Full control over dashboard
- Share functionality
- Manage permissions
- Delete dashboard
- Edit layout
- Add/remove graphs
```

2. **EditDashboardCard**
```javascript
// Can modify but not share/delete
- Edit layout
- Add/remove graphs
- Cannot share with others
- Cannot delete dashboard
```

3. **ViewOnlyDashboardCard**
```javascript
// Can only view
- View graphs
- No edit capabilities
- No sharing permissions
- No delete access
```

4. **CreateDashboardCard**
```javascript
// Special card for creating new dashboards
- "+" icon design
- Creates new dashboard on click
- Always appears first in grid
```


**Component Interaction Model:**

```mermaid
sequenceDiagram
    participant U as User
    participant DL as DashboardList
    participant SD as SingleDashboard
    participant GT as GraphTile
    participant API as Backend API

    U->>DL: View Dashboards
    DL->>API: Fetch Dashboards
    API-->>DL: Return Dashboard List
    
    U->>SD: Select Dashboard
    SD->>API: Fetch Dashboard Details
    API-->>SD: Return Dashboard Data
    
    U->>GT: Interact with Graph
    GT->>GT: Apply Filters/Sort
    
    U->>GT: Save Changes
    GT->>SD: Update Layout
    SD->>API: Save Dashboard State
    API-->>SD: Confirm Update
```





This breakdown shows how the different types of dashboard cards have different capabilities and UI elements based on the user's permission level, making the hierarchy and permission system clearer.

### 3. Backend Architecture

**Technology Stack:**
- FastAPI
- SQLite
- Pydantic for data validation

**Architectural Layers:**

1. **API Layer**
```python
# REST Endpoints
/dashboards           # Dashboard CRUD
/graphs              # Graph management
/tables              # Data source management
/permissions         # Access control
```

2. **Facade Layer (DataVisualizationFacade)**
```python
class DataVisualizationFacade:
    def __init__(self):
        self.dashb_manager = DashboardManager()
        self.graph_manager = GraphManager()
        self.table_manager = TableManager()
```

3. **Manager Layer**
```python
# Handles specific domain operations
- DashboardManager
- GraphManager
- TableManager
```

4. **Data Access Layer**
```python
# Database connection and operations
- SQLite connection management
- SQL query execution
- Data transformation
```
5. **Backend Architecture**

```mermaid
graph TB
subgraph API Layer
FE[FastAPI Endpoints]
MW[Middleware]
Val[Validators]
end
subgraph Business Layer
DVF[DataVisualizationFacade]
DM[DashboardManager]
GM[GraphManager]
TM[TableManager]
end
subgraph Data Layer
DB[(SQLite DB)]
FS[File System]
end
FE --> MW --> Val
Val --> DVF
DVF --> DM & GM & TM
DM & GM & TM --> DB
TM --> FS
```
   

### 4. Database Design

**Core Tables:**
```sql
1. dashboard_permissions
   - dashboard_id (PK, FK)
   - user_email
   - permission_type

2. dashboard_title_mp
   - dashboard_id (PK)
   - dashboard_title

3. master_dashboard
   - dashboard_id (FK)
   - graph_id (FK)
   - width, height
   - x_coord, y_coord

4. graphs
   - graph_id (PK)
   - graph_title
   - graph_type
   - table_id (FK)
   - ax0, ax1

5. tables
   - table_id (PK)
   - table_name

6. table_data
   - table_id (FK)
   - column_name
   - value
```

### 5. Key Features & Workflows

1. **Dashboard Management**
```mermaid
sequenceDiagram
    User->>Frontend: Create Dashboard
    Frontend->>Backend: POST /dashboards
    Backend->>Database: Insert Dashboard
    Database-->>Frontend: Dashboard Created
```

2. **Permission Control**
```mermaid
sequenceDiagram
    Owner->>Frontend: Share Dashboard
    Frontend->>Backend: PUT /permissions
    Backend->>Database: Update Permissions
    Database-->>Frontend: Access Granted
```

3. **Graph Creation**
```mermaid
sequenceDiagram
    User->>Frontend: Configure Graph
    Frontend->>Backend: POST /graphs
    Backend->>Database: Store Graph
    Backend->>Frontend: Return Graph Data
    Frontend->>User: Display Graph
```


### 6. Technology Architecture

#### 6.1 Web Application Architecture
Detailed component breakdown:

```mermaid
graph TB
subgraph Client Side
React[React SPA]
MUI[Material UI]
Plotly[Plotly.js]
Grid[React Grid Layout]
end
subgraph Server Side
FastAPI[FastAPI]
Pandas[Pandas]
NumPy[NumPy]
SQLite[SQLite]
end
subgraph External Services
Auth0[Auth0]
Storage[File Storage]
end
React --> MUI & Plotly & Grid
FastAPI --> Pandas & NumPy & SQLite
React --> FastAPI
FastAPI --> Auth0
FastAPI --> Storage
```

#### 6.2 Data Flow Architecture

```mermaid
sequenceDiagram
participant User
participant Frontend
participant API
participant Manager
participant Database
User->>Frontend: Upload CSV
Frontend->>API: POST /tables
API->>Manager: Process Data
Manager->>Database: Store Data
Database->>Manager: Confirm Storage
Manager->>API: Return Table ID
API->>Frontend: Success Response
Frontend->>User: Show Success
```



### 7. Database Schema

```mermaid
erDiagram
master_tables ||--o{ graphs : contains
graphs ||--o{ dashboard_graphs : includes
dashboard_title_mp ||--o{ dashboard_graphs : has
dashboard_title_mp ||--o{ dashboard_permissions : manages
master_tables {
int table_id PK
string table_name
string db_name
}
graphs {
int graph_id PK
int table_id FK
string graph_title
string graph_type
string ax0
string ax1
}
dashboard_title_mp {
int dashboard_id PK
string dashboard_title
string created_by
string access_level
}
dashboard_permissions {
int dashboard_id FK
string user_email
string permission_type
}
```

### 8. Key Features Implementation

#### Dashboard Creation Flow

```mermaid
graph TD
A[User Input] -->|Create Dashboard| B(Validate Input)
B --> C{Check Permissions}
C -->|Valid| D[Create Dashboard Entry]
D --> E[Initialize Layout]
E --> F[Save to Database]
C -->|Invalid| G[Show Error]
F --> H[Return Dashboard ID]
H --> I[Redirect to Editor]
```

#### Permission Management System
```mermaid
graph TD
A[User Action] -->|Share Dashboard| B(Check Owner)
B --> C{Is Owner?}
C -->|Yes| D[Show Share Modal]
D --> E[Set Permissions]
E --> F[Save Permissions]
C -->|No| G[Show Error]
F --> H[Notify Users]
```

### 9. Security & Performance

**Security Measures:**
1. Permission-based access control
2. Input validation using Pydantic
3. SQL injection prevention
4. CORS configuration

**Performance Optimizations:**
1. Efficient SQL queries with JOINs
2. Frontend component memoization
3. Optimized re-rendering
4. Lazy loading of dashboard data

### 10. Error Handling

1. **Frontend:**
```javascript
try {
    // API calls with axios
} catch (error) {
    // Error handling and user feedback
}
```

2. **Backend:**
```python
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
```

