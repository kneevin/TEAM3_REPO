### 1. Overall Architecture

The application follows a three-tier architecture:
```
[Frontend (React)] <---> [Backend (FastAPI)] <---> [Database (SQLite)]
```

**Key Design Patterns:**
- Facade Pattern (Backend)
- Component-Based Architecture (Frontend)
- Repository Pattern (Data Access)
- MVC Pattern (Overall Structure)

### 1. Frontend Architecture
```
App
├── Navigation
│   └── NavigationBar
├── DashboardList (MyDashboards)
│   ├── DashboardCards
│   │   ├── OwnerDashboardCard
│   │   │   ├── ShareModal
│   │   │   │   ├── EmailInput
│   │   │   │   └── PermissionSelect
│   │   │   ├── ManagePermissionsModal
│   │   │   │   ├── PermissionsList
│   │   │   │   └── DeletePermissionButton
│   │   │   └── DeleteDashboardButton
│   │   ├── EditDashboardCard
│   │   │   └── EditControls
│   │   └── ViewOnlyDashboardCard
│   └── CreateDashboardCard
├── SingleDashboard
│   ├── DashboardHeader
│   │   ├── EditView
│   │   │   ├── AddTileButton
│   │   │   ├── EditTitleButton
│   │   │   └── SaveLayoutButton
│   │   └── ReadOnlyView
│   │       └── DashboardTitle
│   ├── GridLayout
│   │   ├── EditableGraphTile
│   │   ├── GraphVisualization
│   │   ├── TileControls
│   │   │   ├── ResizeHandle
│   │   │   ├── DragHandle
│   │   │   └── DeleteButton
│   │   ├── FilterControls
│   │   │   │   ├── FilterButton
│   │   │   │   │   └── FilterMenu
│   │   │   │   │       ├── DateRangeFilter
│   │   │   │   │       ├── CategoryFilter
│   │   │   │   │       └── ApplyFilterButton
│   │   │   │   ├── SortButton
│   │   │   │   │   └── SortMenu
│   │   │   │   │       ├── SortByOptions
│   │   │   │   │       └── SortDirectionToggle
│   │   │   │   └── ResetFiltersButton
│   │   │   └── EditGraphSettings
│   │   │       ├── TitleEdit
│   │   │       └── GraphTypeEdit
│   │   └── ReadOnlyGraphTile
│   │       ├── GraphVisualization
│   │       ├── TileInfo
│   │       └── FilterControls // Same as EditableGraphTile
│   └── LayoutControls
│        ├── EditView
│        │   ├── SaveLayout
│        │   └── ResetLayout
│        └── ReadOnlyView
│            └── ViewModeIndicator
├── AddTilePage
│   ├── TableSelector
│   │   └── TableList
│   ├── ChartTypeSelector
│   │   └── ChartTypeOptions
│   ├── AxisSelector
│   │   ├── XAxisSelect
│   │   └── YAxisSelect
│   └── PreviewSection
│       └── GraphPreview
└── ErrorBoundary
    └── ErrorDisplay
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

**Visual Representation:**
```mermaid
graph TD
    DL[DashboardList] --> CDC[CreateDashboardCard]
    DL --> ODC[OwnerDashboardCard]
    DL --> EDC[EditDashboardCard]
    DL --> VDC[ViewOnlyDashboardCard]
    
    ODC --> SM[ShareModal]
    ODC --> MPM[ManagePermissionsModal]
    ODC --> DDB[DeleteDashboardButton]
    
    EDC --> EC[EditControls]
    
    subgraph "Owner Permissions"
        SM
        MPM
        DDB
    end
    
    subgraph "Edit Permissions"
        EC
    end
```



**Detailed Visual Representation of Frontend Architecture:**

```mermaid
graph TD
    subgraph "App Container"
        App[App Component]
        Nav[Navigation]
        Router[Router]
    end

    subgraph "Dashboard Views"
        DL[DashboardList]
        SD[SingleDashboard]
        ATP[AddTilePage]
    end

    subgraph "Dashboard Cards"
        CDC[CreateDashboardCard]
        ODC[OwnerDashboardCard]
        EDC[EditDashboardCard]
        VDC[ViewOnlyDashboardCard]
    end

    subgraph "Single Dashboard Components"
        DH[DashboardHeader]
        GL[GridLayout]
        LC[LayoutControls]
    end

    subgraph "Graph Tiles"
        EGT[EditableGraphTile]
        RGT[ReadOnlyGraphTile]
        FC[FilterControls]
        GV[GraphVisualization]
    end

    subgraph "Filter Components"
        FB[FilterButton]
        FM[FilterMenu]
        RF[ResetFilters]
    end

    subgraph "Modal Components"
        ShareM[ShareModal]
        PermM[PermissionsModal]
    end

    %% Main Flow
    App --> Nav
    App --> Router
    Router --> DL
    Router --> SD
    Router --> ATP

    %% Dashboard List Flow
    DL --> CDC
    DL --> ODC
    DL --> EDC
    DL --> VDC

    %% Single Dashboard Flow
    SD --> DH
    SD --> GL
    SD --> LC

    %% Graph Tile Flow
    GL --> EGT
    GL --> RGT
    EGT --> FC
    EGT --> GV
    RGT --> FC
    RGT --> GV

    %% Filter Flow
    FC --> FB
    FC --> RF
    FB --> FM

    %% Modal Flow
    ODC --> ShareM
    ODC --> PermM

    classDef container fill:#e6f3ff,stroke:#4a90e2,stroke-width:2px
    classDef component fill:#f9f9f9,stroke:#666,stroke-width:1px
    classDef interactive fill:#f0fff0,stroke:#2ecc71,stroke-width:1px
    classDef modal fill:#fff0f0,stroke:#e74c3c,stroke-width:1px

    class App,Nav,Router container
    class DL,SD,ATP component
    class CDC,ODC,EDC,VDC interactive
    class ShareM,PermM modal
```

**Component State Flow:**

```mermaid
flowchart TD
    subgraph "State Management"
        direction TB
        US[User State]
        DS[Dashboard State]
        FS[Filter State]
        LS[Layout State]
    end

    subgraph "Components"
        direction TB
        App --> US
        DashboardList --> DS
        SingleDashboard --> DS
        SingleDashboard --> LS
        GraphTile --> FS
    end

    subgraph "Data Flow"
        direction LR
        API[API Calls]
        Props[Props]
        Events[Events]
    end

    US --> Props
    DS --> Props
    FS --> Props
    LS --> Props
    
    Props --> Events
    Events --> API
    API --> US
    API --> DS

    classDef stateNode fill:#f9f2ff,stroke:#9b51e0,stroke-width:2px
    classDef componentNode fill:#e6f3ff,stroke:#4a90e2,stroke-width:2px
    classDef dataNode fill:#fff0f0,stroke:#e74c3c,stroke-width:2px

    class US,DS,FS,LS stateNode
    class App,DashboardList,SingleDashboard,GraphTile componentNode
    class API,Props,Events dataNode
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

**Permission-Based Rendering:**
```javascript
function DashboardCard({ dashboard, permissionType }) {
    switch(permissionType) {
        case 'owner':
            return <OwnerDashboardCard dashboard={dashboard} />;
        case 'edit':
            return <EditDashboardCard dashboard={dashboard} />;
        case 'view':
            return <ViewOnlyDashboardCard dashboard={dashboard} />;
        default:
            return null;
    }
}
```

**Card-Specific Features:**

1. **OwnerDashboardCard Features:**
```javascript
const OwnerDashboardCard = ({ dashboard }) => {
    return (
        <Card>
            <CardHeader 
                action={
                    <>
                        <ShareButton />
                        <ManagePermissionsButton />
                        <DeleteButton />
                    </>
                }
            />
            <CardContent>
                // Dashboard content
            </CardContent>
        </Card>
    );
};
```

2. **EditDashboardCard Features:**
```javascript
const EditDashboardCard = ({ dashboard }) => {
    return (
        <Card>
            <CardHeader 
                action={
                    <EditControls />
                }
            />
            <CardContent>
                // Dashboard content
            </CardContent>
        </Card>
    );
};
```

3. **ViewOnlyDashboardCard Features:**
```javascript
const ViewOnlyDashboardCard = ({ dashboard }) => {
    return (
        <Card>
            <CardHeader />
            <CardContent>
                // Dashboard content
            </CardContent>
        </Card>
    );
};
```

4. **CreateDashboardCard Features:**
```javascript
const CreateDashboardCard = () => {
    return (
        <Card>
            <CardActionArea onClick={handleCreate}>
                <AddIcon />
                <Typography>
                    Create New Dashboard
                </Typography>
            </CardActionArea>
        </Card>
    );
};
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

### 6. Security & Performance

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

### 7. Error Handling

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

