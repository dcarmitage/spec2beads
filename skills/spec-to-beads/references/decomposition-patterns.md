# Decomposition Patterns

Templates for decomposing common spec types into beads.

## Authentication System

```
Epic: Authentication System
├── Spike: Auth architecture decision (P1)
│   └── Decide: JWT vs sessions, token refresh, OAuth providers
├── Feature: Email/Password Auth (P1)
│   ├── Task: Create users table migration
│   ├── Task: Implement password hashing (bcrypt)
│   ├── Task: POST /auth/register endpoint
│   ├── Task: POST /auth/login endpoint
│   ├── Task: POST /auth/logout endpoint
│   ├── Task: Email verification flow
│   └── Task: Password reset flow
├── Feature: OAuth Integration (P2)
│   ├── Task: Configure OAuth providers
│   ├── Task: OAuth callback handling
│   └── Task: Account linking logic
├── Feature: Session Management (P1)
│   ├── Task: JWT generation/validation
│   ├── Task: Refresh token rotation
│   └── Task: Session invalidation
└── Feature: Auth UI (P1)
    ├── Task: Login form component
    ├── Task: Registration form component
    ├── Task: Password reset forms
    └── Task: OAuth buttons
```

## CRUD Resource

```
Epic: [Resource] Management
├── Spike: Data model design (P1)
├── Feature: [Resource] API (P1)
│   ├── Task: Database migration
│   ├── Task: Model/entity definition
│   ├── Task: GET /resources (list with pagination)
│   ├── Task: GET /resources/:id
│   ├── Task: POST /resources (create)
│   ├── Task: PUT /resources/:id (update)
│   ├── Task: DELETE /resources/:id
│   └── Task: Input validation
├── Feature: [Resource] UI (P1)
│   ├── Task: List view component
│   ├── Task: Detail view component
│   ├── Task: Create/Edit form
│   ├── Task: Delete confirmation
│   └── Task: Loading/error states
└── Chore: [Resource] Tests (P2)
    ├── Task: API integration tests
    └── Task: UI component tests
```

## Payment Integration

```
Epic: Payment Processing
├── Spike: Payment provider selection (P1)
│   └── Compare: Stripe vs Braintree vs Adyen
├── Feature: Payment API Integration (P1)
│   ├── Task: Provider SDK setup
│   ├── Task: Webhook endpoint
│   ├── Task: Payment intent creation
│   ├── Task: Payment confirmation handling
│   └── Task: Refund processing
├── Feature: Subscription Management (P2)
│   ├── Task: Plan/pricing model
│   ├── Task: Subscription CRUD
│   ├── Task: Upgrade/downgrade logic
│   └── Task: Cancellation flow
├── Feature: Payment UI (P1)
│   ├── Task: Checkout form (PCI compliant)
│   ├── Task: Payment method management
│   ├── Task: Invoice/receipt display
│   └── Task: Billing history
└── Chore: PCI Compliance (P1)
    ├── Task: Audit logging
    ├── Task: Data retention policy
    └── Task: Security documentation
```

## Search Feature

```
Epic: Search Implementation
├── Spike: Search architecture (P1)
│   └── Decide: Full-text DB vs Elasticsearch vs Algolia
├── Feature: Search Backend (P1)
│   ├── Task: Index schema design
│   ├── Task: Indexing pipeline
│   ├── Task: Search query endpoint
│   ├── Task: Filters implementation
│   ├── Task: Sorting options
│   └── Task: Pagination
├── Feature: Search UI (P1)
│   ├── Task: Search input component
│   ├── Task: Results list
│   ├── Task: Filter sidebar
│   ├── Task: Empty/no results state
│   └── Task: Search suggestions
└── Feature: Search Analytics (P3)
    ├── Task: Query logging
    ├── Task: Click tracking
    └── Task: Popular searches
```

## File Upload

```
Epic: File Upload System
├── Spike: Storage solution (P1)
│   └── Decide: S3 vs GCS vs local
├── Feature: Upload API (P1)
│   ├── Task: Multipart upload endpoint
│   ├── Task: File validation (type, size)
│   ├── Task: Virus scanning integration
│   ├── Task: Storage service abstraction
│   └── Task: Presigned URL generation
├── Feature: Upload UI (P1)
│   ├── Task: Drag-and-drop zone
│   ├── Task: Progress indicator
│   ├── Task: File preview
│   ├── Task: Error handling
│   └── Task: Multi-file support
└── Chore: Cleanup (P2)
    ├── Task: Orphan file detection
    └── Task: Storage quota enforcement
```

## Notification System

```
Epic: Notification System
├── Spike: Notification architecture (P1)
│   └── Decide: Push vs polling, real-time requirements
├── Feature: Notification Backend (P1)
│   ├── Task: Notification model/storage
│   ├── Task: Event-to-notification mapping
│   ├── Task: Delivery queue (email, push, in-app)
│   ├── Task: Read/unread tracking
│   └── Task: Notification preferences
├── Feature: Email Notifications (P1)
│   ├── Task: Email service integration
│   ├── Task: Template system
│   ├── Task: Unsubscribe handling
│   └── Task: Delivery tracking
├── Feature: In-App Notifications (P1)
│   ├── Task: Notification bell component
│   ├── Task: Notification list/dropdown
│   ├── Task: Real-time updates (WebSocket)
│   └── Task: Mark as read
└── Feature: Push Notifications (P3)
    ├── Task: Service worker setup
    ├── Task: Push subscription management
    └── Task: Push delivery
```

## Reporting/Analytics Dashboard

```
Epic: Analytics Dashboard
├── Spike: Data pipeline design (P1)
│   └── Decide: Real-time vs batch, aggregation strategy
├── Feature: Data Collection (P1)
│   ├── Task: Event tracking schema
│   ├── Task: Collection endpoint
│   ├── Task: ETL pipeline
│   └── Task: Data warehouse setup
├── Feature: Dashboard API (P1)
│   ├── Task: Metrics calculation
│   ├── Task: Time-series aggregation
│   ├── Task: Comparison periods
│   └── Task: Export (CSV/PDF)
├── Feature: Dashboard UI (P1)
│   ├── Task: Chart components (line, bar, pie)
│   ├── Task: KPI cards
│   ├── Task: Date range picker
│   ├── Task: Filter controls
│   └── Task: Responsive layout
└── Chore: Performance (P2)
    ├── Task: Query optimization
    └── Task: Caching layer
```

## Dependency Modeling Rules

1. **Spikes first**: Architecture decisions unblock implementation
2. **Backend before frontend**: API must exist for UI to consume
3. **Data layer first**: Migrations → Models → Services → Handlers
4. **Parallel tracks**: UI and API can often proceed in parallel after spike
5. **Tests follow implementation**: Test tasks depend on implementation tasks
