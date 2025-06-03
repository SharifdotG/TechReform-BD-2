# Activity Diagram - TechReform E-commerce System

```mermaid
flowchart TD
    A[User visits TechReform] --> B{User logged in?}

    B -->|No| C[Browse as Guest]
    B -->|Yes| D[Browse as Authenticated User]

    C --> E[View Products]
    D --> E

    E --> F{Select Action}

    F -->|Product Details| G[View Product Details]
    F -->|Add to Cart| H[Add to Cart]
    F -->|Add to Wishlist| I[Add to Wishlist]
    F -->|Compare Products| J[Add to Compare]
    F -->|PC Builder| K[Open PC Builder]
    F -->|Blog| L[Read Blog Posts]
    F -->|Search| M[Search Products]

    G --> N{Want to purchase?}
    N -->|Yes| H
    N -->|No| E

    H --> O{User logged in?}
    O -->|No| P[Guest Checkout]
    O -->|Yes| Q[User Checkout]

    P --> R[Enter Shipping Details]
    Q --> S{Has saved address?}
    S -->|Yes| T[Select Address]
    S -->|No| R

    R --> U[Select Payment Method]
    T --> U

    U --> V[Review Order]
    V --> W[Confirm Order]
    W --> X[Order Created]
    X --> Y[Order Processing]

    Y --> Z{Payment Method}
    Z -->|Cash on Delivery| AA[Ship Order]
    Z -->|Online Payment| BB[Process Payment]

    BB --> CC{Payment Success?}
    CC -->|Yes| AA
    CC -->|No| DD[Payment Failed]
    DD --> E

    AA --> EE[Order Shipped]
    EE --> FF[Order Delivered]
    FF --> GG[Order Complete]

    I --> HH{User logged in?}
    HH -->|No| II[Store in Session]
    HH -->|Yes| JJ[Store in Database]

    II --> E
    JJ --> E

    J --> KK[Compare Products Side by Side]
    KK --> LL{Want to purchase?}
    LL -->|Yes| H
    LL -->|No| E

    K --> MM[Select Components]
    MM --> NN{All required components?}
    NN -->|No| OO[Add Missing Components]
    NN -->|Yes| PP[View Build Summary]

    OO --> MM
    PP --> QQ{Save Build?}
    QQ -->|Yes| RR[Save PC Build]
    QQ -->|No| SS{Purchase all?}

    RR --> SS
    SS -->|Yes| TT[Add All to Cart]
    SS -->|No| E

    TT --> H

    L --> UU[View Blog Post]
    UU --> VV{Want to comment?}
    VV -->|Yes| WW{User logged in?}
    VV -->|No| E

    WW -->|Yes| XX[Write Comment]
    WW -->|No| YY[Login Required]

    XX --> ZZ[Submit Comment]
    ZZ --> AAA[Comment Pending Approval]
    YY --> BBB[Redirect to Login]

    M --> CCC[Display Search Results]
    CCC --> DDD{Filter/Sort?}
    DDD -->|Yes| EEE[Apply Filters]
    DDD -->|No| E

    EEE --> CCC

    %% Admin Activities
    FFF[Admin Login] --> GGG[Admin Dashboard]
    GGG --> HHH{Admin Action}

    HHH -->|Manage Products| III[CRUD Products]
    HHH -->|Process Orders| JJJ[Update Order Status]
    HHH -->|Manage Users| KKK[User Management]
    HHH -->|Blog Management| LLL[Approve Posts/Comments]
    HHH -->|Support Tickets| MMM[Handle Customer Support]

    III --> GGG
    JJJ --> GGG
    KKK --> GGG
    LLL --> GGG
    MMM --> GGG

    %% Support System
    NNN[Customer Issues] --> OOO[Create Support Ticket]
    OOO --> PPP[Ticket Submitted]
    PPP --> QQQ[Staff Assignment]
    QQQ --> RRR[Staff Response]
    RRR --> SSS{Issue Resolved?}
    SSS -->|Yes| TTT[Close Ticket]
    SSS -->|No| UUU[Continue Discussion]
    UUU --> RRR

    style A fill:#e1f5fe
    style GG fill:#c8e6c9
    style DD fill:#ffcdd2
    style AAA fill:#fff3e0
    style TTT fill:#c8e6c9
```

## Activity Flow Description

### Customer Journey

1. **Product Discovery**: Users browse products, search, and filter
2. **Product Evaluation**: View details, compare products, read reviews
3. **Cart Management**: Add items, modify quantities, apply coupons
4. **Checkout Process**: Enter shipping details, select payment method
5. **Order Tracking**: Monitor order status from processing to delivery

### PC Builder Workflow

1. **Component Selection**: Choose CPU, GPU, RAM, etc.
2. **Compatibility Check**: Ensure components work together
3. **Build Validation**: Check power requirements and completeness
4. **Save/Purchase**: Save build or add all components to cart

### Blog Interaction

1. **Content Consumption**: Read blog posts and articles
2. **User Engagement**: Comment on posts (requires login)
3. **Content Moderation**: Admin approval for comments

### Admin Operations

1. **Product Management**: Add, edit, delete products
2. **Order Processing**: Update order status and tracking
3. **User Management**: Handle user accounts and permissions
4. **Content Moderation**: Approve blog posts and comments
5. **Customer Support**: Respond to support tickets

### Support System

1. **Ticket Creation**: Customer submits support request
2. **Ticket Assignment**: Staff member assigned to ticket
3. **Resolution Process**: Back-and-forth communication until resolved
4. **Ticket Closure**: Mark ticket as resolved when issue is fixed
