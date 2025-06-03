# Sequence Diagram - TechReform E-commerce System

## 1. User Registration and Login Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant V as AuthView
    participant M as UserModel
    participant P as UserProfile
    participant D as Database

    Note over U,D: User Registration Process
    U->>F: Access registration page
    F->>V: GET /register/
    V->>F: Render registration form
    F->>U: Show registration form

    U->>F: Submit registration data
    F->>V: POST /register/ (username, email, password)
    V->>V: Validate form data
    V->>M: Create new user
    M->>D: Save user to database
    D-->>M: User created
    M-->>V: User instance
    V->>P: Create user profile (signal)
    P->>D: Save profile to database
    D-->>P: Profile created
    V->>F: Redirect to login
    F->>U: Show success message
```

## 2. Shopping Cart and Checkout Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant CV as CartView
    participant C as Cart
    participant CI as CartItem
    participant O as Order
    participant OI as OrderItem
    participant SA as ShippingAddress
    participant D as Database

    Note over U,D: Add to Cart Process
    U->>F: Click "Add to Cart"
    F->>CV: POST /cart/add/
    CV->>CV: Get or create cart
    CV->>C: Find user cart
    C->>D: Query cart
    D-->>C: Return cart
    CV->>CI: Create cart item
    CI->>D: Save cart item
    D-->>CI: Item saved
    CV->>F: JSON response (cart updated)
    F->>U: Update cart UI

    Note over U,D: Checkout Process
    U->>F: Click "Checkout"
    F->>CV: GET /checkout/
    CV->>C: Get cart items
    C->>D: Query cart items
    D-->>C: Return items
    CV->>F: Render checkout form
    F->>U: Show checkout form

    U->>F: Submit order
    F->>CV: POST /checkout/
    CV->>O: Create order
    O->>D: Save order
    D-->>O: Order created
    CV->>OI: Create order items
    OI->>D: Save order items
    D-->>OI: Items saved
    CV->>SA: Create shipping address
    SA->>D: Save address
    D-->>SA: Address saved
    CV->>C: Clear cart
    C->>D: Delete cart items
    CV->>F: Redirect to success
    F->>U: Show order confirmation
```

## 3. Product Search and Filter Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant PV as ProductView
    participant PM as ProductModel
    participant D as Database

    Note over U,D: Product Search Process
    U->>F: Enter search query
    F->>PV: GET /products/?search=query
    PV->>PV: Parse search parameters
    PV->>PM: Filter products
    PM->>D: Execute query with filters
    D-->>PM: Return filtered products
    PM-->>PV: Product queryset
    PV->>F: Render product list
    F->>U: Display search results

    Note over U,D: Apply Filters
    U->>F: Select filter options
    F->>PV: GET /products/?category=CPU&brand=Intel
    PV->>PM: Apply additional filters
    PM->>D: Execute filtered query
    D-->>PM: Return filtered results
    PM-->>PV: Filtered queryset
    PV->>F: Render filtered results
    F->>U: Update product display
```

## 4. Blog Post Creation and Comment Sequence

```mermaid
sequenceDiagram
    participant A as Author
    participant F as Frontend
    participant BV as BlogView
    participant BP as BlogPost
    participant C as Comment
    participant U as User
    participant D as Database

    Note over A,D: Blog Post Creation
    A->>F: Access blog creation
    F->>BV: GET /blog/create/
    BV->>F: Render blog form
    F->>A: Show blog creation form

    A->>F: Submit blog post
    F->>BV: POST /blog/create/
    BV->>BV: Validate form
    BV->>BP: Create blog post
    BP->>D: Save blog post
    D-->>BP: Post saved
    BP-->>BV: Blog post instance
    BV->>F: Redirect to post
    F->>A: Show created post

    Note over A,D: Comment Process
    U->>F: View blog post
    F->>BV: GET /blog/post/slug/
    BV->>BP: Get blog post
    BP->>D: Query post and comments
    D-->>BP: Return post data
    BP-->>BV: Post with comments
    BV->>F: Render post page
    F->>U: Display blog post

    U->>F: Submit comment
    F->>BV: POST /blog/comment/
    BV->>C: Create comment
    C->>D: Save comment (is_approved=False)
    D-->>C: Comment saved
    BV->>F: Success response
    F->>U: Show pending approval message
```

## 5. PC Builder Configuration Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant PCV as PCBuilderView
    participant PCB as PCBuilder
    participant PCI as PCBuilderItem
    participant PM as ProductModel
    participant D as Database

    Note over U,D: Create PC Build
    U->>F: Access PC Builder
    F->>PCV: GET /pcbuilder/
    PCV->>PCB: Get or create build
    PCB->>D: Query user builds
    D-->>PCB: Return builds
    PCV->>F: Render PC builder interface
    F->>U: Show component selection

    Note over U,D: Add Component
    U->>F: Select CPU component
    F->>PCV: POST /pcbuilder/add-component/
    PCV->>PM: Get product details
    PM->>D: Query product
    D-->>PM: Return product
    PCV->>PCI: Create/Update builder item
    PCI->>D: Save component
    D-->>PCI: Item saved
    PCV->>PCB: Calculate totals
    PCB->>F: JSON response (updated build)
    F->>U: Update build summary

    Note over U,D: Build Validation
    U->>F: Check compatibility
    F->>PCV: GET /pcbuilder/validate/
    PCV->>PCB: Check required components
    PCB->>PCI: Get all items
    PCI->>D: Query build items
    D-->>PCI: Return items
    PCV->>PCV: Validate compatibility
    PCV->>F: Validation results
    F->>U: Show compatibility status
```

## 6. Order Processing and Status Update Sequence

```mermaid
sequenceDiagram
    participant C as Customer
    participant F as Frontend
    participant OV as OrderView
    participant O as Order
    participant A as Admin
    participant AF as AdminFrontend
    participant AV as AdminView
    participant D as Database

    Note over C,D: Order Status Check
    C->>F: Check order status
    F->>OV: GET /orders/track/order-number/
    OV->>O: Get order details
    O->>D: Query order
    D-->>O: Return order data
    O-->>OV: Order instance
    OV->>F: Render order status
    F->>C: Display order info

    Note over C,D: Admin Order Management
    A->>AF: Login to admin
    AF->>AV: GET /admin/orders/
    AV->>O: Get pending orders
    O->>D: Query orders
    D-->>O: Return order list
    AV->>AF: Render order list
    AF->>A: Show orders

    A->>AF: Update order status
    AF->>AV: POST /admin/orders/update/
    AV->>O: Update order status
    O->>D: Save status change
    D-->>O: Status updated
    AV->>AF: Success response
    AF->>A: Show updated status

    Note over C,D: Customer Notification
    O->>O: Status change signal
    O->>C: Email notification (if implemented)
```

## 7. Support Ticket Management Sequence

```mermaid
sequenceDiagram
    participant C as Customer
    participant F as Frontend
    participant SV as SupportView
    participant ST as SupportTicket
    participant SR as SupportResponse
    participant S as Staff
    participant SF as StaffFrontend
    participant D as Database

    Note over C,D: Create Support Ticket
    C->>F: Access support form
    F->>SV: GET /support/create/
    SV->>F: Render support form
    F->>C: Show ticket form

    C->>F: Submit support request
    F->>SV: POST /support/create/
    SV->>ST: Create ticket
    ST->>D: Save ticket
    D-->>ST: Ticket created
    SV->>F: Success response
    F->>C: Show ticket confirmation

    Note over C,D: Staff Response
    S->>SF: Login to staff panel
    SF->>SV: GET /support/tickets/
    SV->>ST: Get pending tickets
    ST->>D: Query tickets
    D-->>ST: Return tickets
    SV->>SF: Render ticket list
    SF->>S: Show tickets

    S->>SF: Respond to ticket
    SF->>SV: POST /support/respond/
    SV->>SR: Create response
    SR->>D: Save response
    D-->>SR: Response saved
    SV->>ST: Update ticket status
    ST->>D: Save status
    SV->>SF: Success response
    SF->>S: Show updated ticket
```

## Key Sequence Patterns

### Authentication Flow

- User registration automatically creates profile via Django signals
- Login validation and session management
- Role-based access control for different user types

### E-commerce Flow

- Session-based cart for anonymous users
- Database-persistent cart for authenticated users
- Order creation with item copying and address management

### Content Management

- Blog post creation with approval workflow
- Comment moderation system
- Rich text content handling

### Product Management

- Dynamic product filtering and search
- Category-based product organization
- Inventory tracking and availability

### Admin Operations

- Centralized admin interface for all models
- Bulk operations and status updates
- Audit trail for administrative actions
