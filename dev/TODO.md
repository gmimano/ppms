# SiasaCloud Development Plan

This plan outlines the steps to build the SiasaCloud platform as specified in the Technical Design Document (`TDD.md`).

## Phase 1: Project Setup & Tenant Architecture
- [ ] Initialize the Django project named `ppms`.
- [ ] Integrate and configure the `django-tenants` library for schema-based multi-tenancy.
- [ ] Create a `tenants` app to manage shared models (Client/Tenant, Domain).
- [ ] Create the `Client` (Tenant) model in the `tenants` app with fields for party name, schema name, colors, and logo.
- [ ] Create a `core` app for the tenant-specific application logic.
- [ ] Set up the Django project to use PostgreSQL with the PostGIS extension enabled.
- [ ] Configure `settings.py` for `django-tenants` (DATABASE_ROUTERS, SHARED_APPS, TENANT_APPS).
- [ ] Create initial migrations for the tenant and shared apps and provision the public tenant.

## Phase 2: User and Authentication Module
- [ ] In the `core` app, create a custom `User` model inheriting from `AbstractUser`.
- [ ] Set the `USERNAME_FIELD` to `phone_number` and add `national_id` as a unique, indexed field.
- [ ] Add other fields to the User model as specified in the TDD (e.g., `wallet_balance`, `roles`).
- [ ] Implement a Django REST Framework (DRF) `ViewSet` for user registration.
- [ ] Create a mock OTP generation and verification service for the registration endpoint.
- [ ] Set up DRF `Serializers` for the User model.
- [ ] Configure JWT or Token-based authentication for the API.

## Phase 3: Geographic and Party Structure
- [ ] Create a `Location` model in the `core` app for Nation, County, Constituency, Ward, using a self-referential parent key for the hierarchy.
- [ ] Create a `RegionLevel` enum or model to define the different location types.
- [ ] Create a `PartyOrgan` model to define party structures (e.g., NEC, Youth League) with a `level` FK to `RegionLevel`.
- [ ] Create the `Position` model to manage roles within a `PartyOrgan`.
- [ ] Write a data migration or management command to seed the database with the 47 Kenyan Counties and their constituencies/wards from the provided JSON file.
- [ ] Create read-only API endpoints to list geographic units.

## Phase 4: Frontend Scaffolding & Theming
- [ ] Initialize a new React project using Vite in a `frontend` directory.
- [ ] Install and configure Tailwind CSS.
- [ ] Install and set up `shadcn/ui` as the component library.
- [ ] Create an API endpoint in Django that serves the current tenant's theme (primary_color, secondary_color).
- [ ] Implement a `ThemeProvider` in React to fetch the theme and apply it globally using CSS variables.
- [ ] Create a basic application layout (e.g., Sidebar, Navbar, Main Content area).

## Phase 5: Core Membership & Finance
- [ ] Create the `MemberProfile` model with a `OneToOneField` to the `User` model.
- [ ] Create the `Wallet` model with a `OneToOneField` to the `User` model.
- [ ] Create the `Transaction` model with fields for type, amount, reference, and timestamp.
- [ ] Implement DRF `ViewSets` for Wallet and Transaction operations.
- [ ] Develop a service module for M-Pesa integration.
- [ ] Create a mock endpoint that simulates receiving an M-Pesa STK Push callback and updates the wallet atomically.

## Phase 6: Advanced Modules & Compliance
- [ ] Develop the `Campaign` finance model and logic to check against financing act limits.
- [ ] Implement the `DisputeCase` model and associated logic for the IDRM module.
- [ ] Build the Compliance Engine:
    - [ ] Write a scheduled task (Celery) to validate the 2/3rds gender rule for `PartyOrgan` positions.
    - [ ] Create a dashboard component to flag compliance alerts.
- [ ] Create the Communication Hub backend, including an approval workflow for sending bulk messages.
- [ ] Implement a basic Role-Based Access Control (RBAC) system using Django's built-in permissions or a dedicated library.
