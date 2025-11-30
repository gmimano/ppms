Technical Design Document: SiasaCloud (Political Party ERP)
===========================================================
1\. Executive Summary
---------------------

**Project:** Multitenant SaaS for Political Party Management in Kenya. **Context:** A digital platform enabling political parties to manage membership, finances, governance structures, and communications in compliance with the Political Parties Act (2011) and the Constitution of Kenya (2010). **Core Stack:** Python (Django), PostgreSQL, React.js.

2\. Technology Stack & Architecture
-----------------------------------

### 2.1 Backend: Django (The Logic Layer)

-   **Framework:** Django 5.x (Latest Stable).

-   **API:** Django REST Framework (DRF) for serving the frontend.

-   **Multitenancy:** `django-tenants` (Schema-based isolation). This is crucial. Every political party gets its own PostgreSQL schema. This ensures data strict isolation (a legal requirement for party membership lists).

-   **Task Queue:** Celery + Redis (for bulk SMS, email broadcasting, and report generation).

-   **Audit Logging:** `django-simple-history` (To track changes to member lists and financial records for ORPP compliance).

### 2.2 Database: PostgreSQL (The Data Layer)

-   **Version:** PostgreSQL 16+.

-   **Geo-Spatial:** PostGIS (Required for mapping Wards, Constituencies, and geo-tagging incident reports as requested in `prd.md`).

### 2.3 Frontend: React + UI Libraries (The Beauty Layer)

To ensure the "beauty and usability" requested:

-   **Framework:** React (Vite) as a Single Page Application (SPA).

-   **Styling System:** **Tailwind CSS** (Utility-first).

-   **Component Library:** **Shadcn/UI** (Based on Radix UI).

    -   *Reasoning:* It is highly customizable, accessible (WCAG compliant), and professional-looking out of the box. It looks much better than standard Bootstrap or Material UI.

-   **State Management:** TanStack Query (React Query) for handling API data efficiently.

-   **Icons:** Lucide React.

-   **Charts/Analytics:** Recharts (for fundraising and gender demographics dashboards).

3\. Database Schema Design
--------------------------

*This is the most critical section for your AI assistant to get right.*

### 3.1 Tenant Management (Shared Schema)

-   `Client`: Represents the Political Party (Name, Subdomain, Logo, Primary Color, Secondary Color).

-   `Domain`: The URL for the tenant (e.g., `odm.siasacloud.com`, `uda.siasacloud.com`).

### 3.2 Core Logic (Tenant Schemas)

#### A. Users & Authentication

-   **CustomUser:**

    -   `username`: Phone Number (Unique identifier per `prd.md`).

    -   `national_id`: CharField (Unique, Verified).

    -   `is_verified`: Boolean (OTP check).

    -   `wallet_balance`: Decimal.

    -   `roles`: ManyToMany (Mapped to RBAC).

#### B. Geographic Structure (The Kenyan Context)

*Based on `parties.md` requirements for National/County/Ward structure.*

-   `RegionLevel`: Enum (National, County, Constituency, Ward, Polling Unit).

-   `Location`:

    -   `name`: (e.g., "Nairobi City", "Westlands").

    -   `level`: FK to `RegionLevel`.

    -   `parent`: Self-referential FK (Ward belongs to Constituency).

    -   `code`: IEBC Code.

#### C. Party Governance Structure

*Flexible enough to handle the "Democratic Party Structure" example in `parties.md`.*

-   `PartyOrgan`: (e.g., "National Executive Committee", "Youth League", "Women League").

    -   `name`: String.

    -   `level`: FK to `RegionLevel`.

    -   `gender_quota_rule`: Integer (Default 33% for compliance).

-   `Position`: (e.g., "Chairperson", "Treasurer", "Secretary General").

    -   `organ`: FK to `PartyOrgan`.

    -   `holder`: FK to `User`.

    -   `term_start`: Date.

    -   `term_end`: Date.

#### D. Membership & Recruitment

-   `MemberProfile`:

    -   `user`: OneToOne to `User`.

    -   `membership_number`: String (Auto-generated).

    -   `recruited_by`: FK to `User` (For the gamification/referral system in `prd.md`).

    -   `voter_registration_status`: Boolean.

    -   `gender`: Enum (Male, Female, Intersex) - *Critical for 2/3rds gender rule logic.*

    -   `disability_status`: Boolean - *Critical for Disability League inclusion.*

#### E. Finance & Wallets

-   `Wallet`:

    -   `user`: OneToOne.

    -   `balance`: Decimal.

    -   `pin_hash`: String (For transaction security).

-   `Transaction`:

    -   `type`: Enum (Deposit, Donation, Withdrawal, ServicePayment).

    -   `reference`: String (M-Pesa Receipt Number).

    -   `amount`: Decimal.

    -   `timestamp`: DateTime.

-   `Campaign`:

    -   `title`: String.

    -   `target_amount`: Decimal.

    -   `beneficiary`: FK to `User` (Candidate) or `Party`.

    -   `is_compliant`: Boolean (Checks against Election Campaign Financing Act limits).

#### F. Dispute Resolution (IDRM)

*As per `parties.md` requirement for internal mechanisms.*

-   `DisputeCase`:

    -   `complainant`: FK to `User`.

    -   `respondent`: FK to `User` or `PartyOrgan`.

    -   `category`: Enum (Nomination, Disciplinary, Financial).

    -   `status`: Enum (Filed, Hearing, Verdict, Appealed to PPDT).

    -   `verdict_doc`: FileField (Written decision required by law).

4\. Key Functional Modules (Logic & Algorithms)
-----------------------------------------------

### 4.1. Compliance Engine (The "Guardrail")

-   **Gender Rule Validator:** A scheduled task that runs against `PartyOrgan` and `Position`. If any organ has >66% of one gender, it flags a "Compliance Alert" on the Admin Dashboard.

-   **Regional Diversity Check:** Ensures the party has at least 1,000 members in at least 24 counties (from `parties.md`). Visualized on a map.

### 4.2. Communication Hub

-   **Approval Workflow:**

    1.  Draft Message (SMS/Email).

    2.  Calculate Cost (Audience Size \* Unit Cost).

    3.  Check Wallet Balance.

    4.  Status -> "Pending Approval".

    5.  Approver (Secretary General/Admin) clicks "Approve".

    6.  Celery Worker dispatches via Twilio/Africa's Talking.

### 4.3. Payments & Wallets

-   **M-Pesa STK Push:**

    -   Endpoint to trigger STK push to user's phone.

    -   Callback URL to handle M-Pesa IPN and update `Wallet` balance atomically.
  
5\. UI/UX Strategy (Themes & Branding)
--------------------------------------

Since beauty is key to adoption, we will use a **White-Labeling System**.

1.  **Global Theming:** The React app will read the `Client` configuration API on load.

2.  **CSS Variables:** We will use Tailwind's configuration to map colors dynamically.

```
:root {
  --party-primary: #FF5733; /* Fetched from DB for ODM */
  --party-secondary: #000000;
  --radius: 0.5rem;
}
```


3.  **Layouts:**

    -   **Public Portal:** High-impact imagery, "Join Now" buttons, Donation widgets.

    -   **Member Dashboard:** Gamified view (Badges, Referral Links, Wallet Balance).

    -   **Admin Dashboard:** Dense data tables (Shadcn Data Table), Compliance Heatmaps.

6\. Security & Compliance (Non-Functional)
------------------------------------------

1.  **Data Sovereignty:** Host in a Kenya-compliant cloud zone or local data center if required by ODPC.

2.  **RBAC (Role-Based Access Control):**

    -   Strict permissions. A "Branch Chairman" can only see members in their specific County.

3.  **Input Sanitation:** Strict validation on all inputs to prevent injection, specifically on the "Voting Offenses" reporting module (uploads).

7\. Implementation Plan (Prompts for your AI Coding Assistant)
--------------------------------------------------------------

You can copy-paste these blocks to your AI assistant to start coding.

### Phase 1: Project Setup & Tenants

> "Create a Django project named `siasacloud`. Configure `django-tenants`. Create a `Shared` app for tenant management and a `Core` app for the actual party logic. Set up PostgreSQL with PostGIS. Create the Tenant model with fields for `party_name`, `primary_color`, `logo_url`."

### Phase 2: User & Auth

> "In the `Core` app, create a Custom User model. The username field should be `phone_number`. Add fields for `national_id` and `county_of_residence`. Implement a DRF ViewSet for Registration that triggers a mock OTP generation."

### Phase 3: Structure & Organs

> "Create models for `AdministrativeUnit` (Nation, County, Constituency, Ward) using a tree structure (Django-Mptt or simple Parent FK). Create a `PartyOrgan` model. Seed the database with the 47 Counties of Kenya."

### Phase 4: Frontend Scaffolding

> "Initialize a React project using Vite. Install Tailwind CSS and Shadcn/UI. Configure a `ThemeProvider` context that fetches the current Tenant's color scheme from a Django API endpoint and applies it to CSS variables."

### Phase 5: Finance & Wallets

> "Create a `Wallet` model and a `Transaction` model. Implement an atomic transaction method in Django to handle deposits. Write a mock service for M-Pesa STK Push."