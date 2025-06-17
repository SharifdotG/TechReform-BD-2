# 🖥️ TechReform BD 2

## 🚀 Revolutionary E-Commerce Platform for PC Components

<div align="center">

[![Django](https://img.shields.io/badge/Django-5.1.4-092e20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-D7FF64?style=for-the-badge)](https://github.com/astral-sh/ruff)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

</div>

> **TechReform BD 2** is a next-generation e-commerce platform built with Django, Tailwind CSS, and modern web technologies.
> Bringing *fair pricing*, *transparent supply chains*, and *reliable after-sales service* to PC enthusiasts in Bangladesh.

---

## 🎯 Mission Statement

> **Empowering Bangladesh’s PC community by transforming how components are bought and sold.**
>
> We are committed to:
>
> - 💰 **Fair Pricing:** Ensuring access to genuine products at or near MSRP.
> - 🔍 **Transparent Supply Chains:** Building trust through clear, direct sourcing from manufacturers to users.
> - 🛠️ **Reliable After-Sales Service:** Providing manufacturer-backed warranty and support for every purchase.
>
> **TechReform BD 2** stands for a future where technology is accessible, affordable, and dependable for all.

---

## 📋 Table of Contents

<details>
<summary><strong>Expand to view all sections</strong></summary>

- [🖥️ TechReform BD 2](#️-techreform-bd-2)
  - [🚀 Revolutionary E-Commerce Platform for PC Components](#-revolutionary-e-commerce-platform-for-pc-components)
  - [🎯 Mission Statement](#-mission-statement)
  - [📋 Table of Contents](#-table-of-contents)
  - [🖼️ Preview](#️-preview)
    - [✨ Application Demo](#-application-demo)
  - [🎯 Project Motivation](#-project-motivation)
    - [🚨 The Problems We’re Solving](#-the-problems-were-solving)
    - [🎯 Our Mission](#-our-mission)
  - [✨ Features](#-features)
    - [🛍️ E-Commerce Core](#️-e-commerce-core)
    - [👥 User Management](#-user-management)
    - [🖥️ PC Builder Tool](#️-pc-builder-tool)
    - [📊 Product Features](#-product-features)
    - [📝 Content Management](#-content-management)
    - [🎨 Modern UI/UX](#-modern-uiux)
  - [👥 Development Team](#-development-team)
    - [Meet the Team Behind TechReform BD 2](#meet-the-team-behind-techreform-bd-2)
  - [🏛️ Technical Architecture](#️-technical-architecture)
    - [🏗️ Design Patterns](#️-design-patterns)
    - [🛠️ Development Methodology](#️-development-methodology)
    - [🗄️ Database Design](#️-database-design)
  - [🏗️ Architecture](#️-architecture)
    - [Project Structure](#project-structure)
      - [📂 Overview](#-overview)
      - [🔄 Request Lifecycle](#-request-lifecycle)
      - [📁 Directory Layout](#-directory-layout)
      - [🔐 Security Highlights](#-security-highlights)
      - [🔌 Middleware \& Extensions](#-middleware--extensions)
      - [📦 Database Model Overview](#-database-model-overview)
      - [🌐 URL Structure](#-url-structure)
    - [Application Components](#application-components)
      - [**ProductsApp – Product Catalog**](#productsapp--product-catalog)
      - [**AuthApp – Authentication \& Support**](#authapp--authentication--support)
      - [**CartApp – Shopping \& Orders**](#cartapp--shopping--orders)
      - [**PCBuilderApp – PC Configuration**](#pcbuilderapp--pc-configuration)
      - [**CompareApp – Product Comparison**ges)](#compareapp--product-comparisonges)
      - [**WishlistApp – User Favorites**](#wishlistapp--user-favorites)
      - [**BlogApp – Content Management**tes](#blogapp--content-managementtes)
      - [TechReform Core - Project Foundation](#techreform-core---project-foundation)
  - [🚀 Quick Start](#-quick-start)
    - [📋 Prerequisites](#-prerequisites)
    - [⚡ Installation Steps](#-installation-steps)
      - [1. 📥 Clone the Repository](#1--clone-the-repository)
      - [2. 🐍 Set Up Python Virtual Environment](#2--set-up-python-virtual-environment)
      - [3. 📦 Install Python Dependencies](#3--install-python-dependencies)
      - [4. 🎨 Install Node.js Dependencies \& Build Tailwind CSS](#4--install-nodejs-dependencies--build-tailwind-css)
      - [5. ⚙️ Environment Configuration (Optional)](#5-️-environment-configuration-optional)
      - [6. 🗄️ Database Setup](#6-️-database-setup)
      - [7. 👤 Create Superuser](#7--create-superuser)
      - [8. 📂 Collect Static Files](#8--collect-static-files)
      - [9. 🏃 Start Development Servers](#9--start-development-servers)
      - [10. 🌐 Access the Application](#10--access-the-application)
  - [🔧 Troubleshooting](#-troubleshooting)
    - [Common Issues and Solutions](#common-issues-and-solutions)
      - [🚨 Site Shows Raw HTML Without Styling](#-site-shows-raw-html-without-styling)
      - [🐍 "ModuleNotFoundError: No module named 'django'"](#-modulenotfounderror-no-module-named-django)
      - [📦 "npm audit" Issues](#-npm-audit-issues)
      - [🚪 "That port is already in use"](#-that-port-is-already-in-use)
  - [🛠️ Development](#️-development)
    - [🧹 Code Quality \& Standards](#-code-quality--standards)
    - [🗄️ Database Management](#️-database-management)
    - [🎨 Code Formatting \& Linting](#-code-formatting--linting)
    - [💠 Tailwind CSS Workflow](#-tailwind-css-workflow)
  - [📦 Dependencies](#-dependencies)
    - [🔧 Core Dependencies](#-core-dependencies)
    - [🛠️ Development Dependencies](#️-development-dependencies)
    - [🚀 Production Dependencies](#-production-dependencies)
    - [🔐 Authentication](#-authentication)
  - [🧪 Testing](#-testing)
    - [📊 Test Coverage Overview](#-test-coverage-overview)
    - [📁 Test Suite Structure](#-test-suite-structure)
    - [🏃 How to Run Tests](#-how-to-run-tests)
      - [🔹 Run All Tests](#-run-all-tests)
      - [🔹 Run a Specific Test File](#-run-a-specific-test-file)
      - [🔹 Generate Coverage Report](#-generate-coverage-report)
  - [🤝 Contributing](#-contributing)
    - [🚀 Development Workflow](#-development-workflow)
    - [📏 Code Standards](#-code-standards)
    - [🔄 Pull Request Checklist](#-pull-request-checklist)
    - [🎯 Where to Contribute?](#-where-to-contribute)
  - [📄 License](#-license)
  - [🙏 Acknowledgments](#-acknowledgments)
  - [📞 Support](#-support)
  - [🗺️ Roadmap](#️-roadmap)
    - [🚀 Version 2.0 (Upcoming)](#-version-20-upcoming)
    - [🌟 Version 2.1 (Planned/Future)](#-version-21-plannedfuture)
    - [🚀 Join the TechReform Movement](#-join-the-techreform-movement)
      - [🤝 Get Involved \& Shape the Future](#-get-involved--shape-the-future)

</details>

---

**Tip:** Click the arrow to expand/collapse the full Table of Contents for easier navigation.
      - [📊 Admin Analytics](#-admin-analytics)
      - [🏪 Multi-vendor Marketplace](#-multi-vendor-marketplace)
    - [Join the TechReform Movement](#join-the-techreform-movement)

---

## 🖼️ Preview

<div align="center">

### ✨ Application Demo

</div>

<div align="center">

<img src="placeholder/Preview.gif" alt="TechReform BD Application Preview" width="800" style="border-radius: 12px; box-shadow: 0 4px 24px rgba(0,0,0,0.12);" />

</div>

<p align="center">
<em>
A glimpse of <strong>TechReform BD 2</strong> in action — experience seamless navigation, modern UI, and powerful features designed for PC enthusiasts in Bangladesh.
</em>
</p>

## 🎯 Project Motivation

**TechReform BD 2** is built to solve the most pressing issues facing Bangladesh’s PC component market by reimagining the entire supply chain for fairness, trust, and user empowerment.

### 🚨 The Problems We’re Solving

| **Challenge**                | **Traditional Market**                                         | **TechReform BD 2 Approach**                                 |
|------------------------------|---------------------------------------------------------------|--------------------------------------------------------------|
| 💰 **Inflated Prices**       | 30–50% markup from multiple intermediaries                    | Direct manufacturer partnerships—no unnecessary markups       |
| 🔍 **Opaque Pricing**        | Hidden costs, unclear profit margins                          | Transparent, MSRP-aligned pricing for every product           |
| 🛠️ **After-Sales Hassles**   | Complicated, multi-step warranty claims                       | Seamless, manufacturer-backed warranty and RMA support        |
| ✅ **Product Authenticity**   | Risk of counterfeits and unauthorized imports                 | 100% genuine products with verified warranties                |
| 📊 **Information Gap**       | Limited product knowledge and misleading marketing            | Honest education, clear specs, and fair pricing awareness     |

### 🎯 Our Mission

By championing a **“manufacturer → authorized local supplier → user”** model, TechReform BD 2 is committed to:

- 💰 **Fair Pricing:** Access to genuine products at or near MSRP
- 🔍 **Transparent Supply Chains:** Direct, traceable sourcing—no hidden markups
- 🛠️ **Reliable Support:** Manufacturer-backed warranty and responsive after-sales service
- 📚 **Community Education:** Empowering users with knowledge about fair pricing, product authenticity, and warranty rights

## ✨ Features

### 🛍️ E-Commerce Core

💰 **Fair Pricing Model**: Direct supply chain from manufacturers to eliminate intermediary markups
🏷️ **MSRP Transparency**: Clear pricing aligned with Manufacturer's Suggested Retail Price
📦 **Product Catalog**: Comprehensive catalog for computer hardware and accessories
🛒 **Shopping Cart**: Session-based cart for anonymous users and persistent cart for registered users
🔒 **Secure Checkout**: Complete order processing with multiple payment options
📋 **Order Management**: Full order lifecycle tracking from cart to delivery
📊 **Inventory Management**: Real-time stock tracking and availability status
✅ **Authentic Products**: Genuine products with full manufacturer warranty coverage

### 👥 User Management

🔐 **Role-Based Authentication**: Multiple user roles (Admin, Staff, Content Manager, Blogger, Customer, Guest)
👤 **User Profiles**: Extended user profiles with customizable information
🎧 **Customer Support**: Comprehensive ticket system with categories and responses
✉️ **Account Verification**: Email-based user verification system
🛡️ **Warranty & RMA Support**: Direct access to manufacturer-backed warranty and RMA services

### 🖥️ PC Builder Tool

⚙️ **Custom PC Configuration**: Interactive PC building tool with component compatibility
✅ **Real-time Compatibility Checking**: Automatic validation of component combinations (CPU socket vs motherboard, RAM type, PSU wattage)
⚡ **Power Calculation**: Total system power consumption estimation
🔗 **Build Sharing**: Public/private build configurations with sharing capabilities
💰 **Fair Pricing Integration**: All components displayed with MSRP transparency
💾 **Saved Builds**: Save and manage multiple PC configurations in user profiles

### 📊 Product Features

⚖️ **Product Comparison**: Side-by-side comparison of up to multiple products
❤️ **Wishlist Management**: Save favorite products for later purchase
🔍 **Advanced Search**: Filter products by specifications, price, brand, and availability
⭐ **Product Reviews**: User ratings and reviews system

### 📝 Content Management

📰 **Blog System**: Rich content management with CKEditor integration
🔍 **SEO Optimization**: URL slugs, meta descriptions, and search-friendly URLs
📁 **Category Management**: Hierarchical product and content categorization
🎨 **Media Management**: Comprehensive image and file upload system

### 🎨 Modern UI/UX

📱 **Responsive Design**: Mobile-first approach with Tailwind CSS
🌓 **Dark/Light Mode**: Theme switching capabilities
✨ **Modern Interface**: Clean, professional design with intuitive navigation
⚡ **Performance Optimized**: Fast loading times and optimized queries

## 👥 Development Team

<div align="center">

### Meet the Team Behind TechReform BD 2

<!-- Team Member Cards in Grid -->
<div style="display: flex; justify-content: center; gap: 40px; flex-wrap: wrap;">

  <div style="flex: 0 1 220px; text-align: center;">
    <img src="static/index/images/team/Sharif.jpg" width="100" style="border-radius: 50%; box-shadow: 0 2px 12px rgba(0,0,0,0.10);" alt="Sharif Md. Yousuf"/><br>
    <b>Sharif Md. Yousuf</b><br>
    <sub>Project Manager & Lead Developer</sub><br>
    <a href="https://github.com/SharifdotG" target="_blank">
      <img src="https://img.shields.io/badge/GitHub-SharifdotG-181717?style=flat-square&logo=github" alt="GitHub"/>
    </a>
    <br>
    <span style="font-size: 0.9em;">
      <b>Skills:</b> Django, React, Python
    </span>
  </div>

  <div style="flex: 0 1 220px; text-align: center;">
    <img src="static/index/images/team/Priom.jpg" width="100" style="border-radius: 50%; box-shadow: 0 2px 12px rgba(0,0,0,0.10);" alt="Noor Mohammed Priom"/><br>
    <b>Noor Mohammed Priom</b><br>
    <sub>Backend Developer & Database Architect</sub><br>
    <a href="https://github.com/SOrtINgmASteR" target="_blank">
      <img src="https://img.shields.io/badge/GitHub-SOrtINgmASteR-181717?style=flat-square&logo=github" alt="GitHub"/>
    </a>
    <br>
    <span style="font-size: 0.9em;">
      <b>Skills:</b> Django, SQL, Python
    </span>
  </div>

  <div style="flex: 0 1 220px; text-align: center;">
    <img src="static/index/images/team/Shorna.jpg" width="100" style="border-radius: 50%; box-shadow: 0 2px 12px rgba(0,0,0,0.10);" alt="Shornali Akter"/><br>
    <b>Shornali Akter</b><br>
    <sub>Frontend Developer & UI/UX Designer</sub><br>
    <a href="https://github.com/nudhar60" target="_blank">
      <img src="https://img.shields.io/badge/GitHub-nudhar60-181717?style=flat-square&logo=github" alt="GitHub"/>
    </a>
    <br>
    <span style="font-size: 0.9em;">
      <b>Skills:</b> HTML/CSS, Tailwind, Figma
    </span>
  </div>

</div>
</div>

Together, we combine expertise in backend, frontend, and UI/UX to deliver a seamless, modern, and reliable e-commerce experience for PC enthusiasts in Bangladesh.

---

## 🏛️ Technical Architecture

### 🏗️ Design Patterns

- **Model-View-Template (MVT):**
  Leverages Django’s robust separation of concerns for scalable, maintainable code.
- **Repository Pattern:**
  Clean abstraction of data access using Django ORM, simplifying database operations.
- **Factory Pattern:**
  Modular logic for dynamic component creation and PC build assembly.

### 🛠️ Development Methodology

- **Agile/Scrum:**
  Rapid, iterative progress with focused 2-week sprints and regular feedback loops.
- **Version Control:**
  Git-based workflow with feature branches for safe, collaborative development.
- **Test-Driven Development (TDD):**
  Unit and integration tests ensure reliability and catch regressions early.
- **Continuous Integration (CI):**
  Automated pipelines for testing, linting, and code quality enforcement.

### 🗄️ Database Design

The platform is powered by a relational database, structured for clarity and extensibility:

- **User Management:**
  Comprehensive user profiles, role-based permissions, and secure authentication.
- **Product Catalog:**
  Detailed component models, hierarchical categories, rich specifications, and transparent pricing.
- **E-commerce:**
  Shopping cart, order processing, order items, and real-time inventory management.
- **PC Builder:**
  Saved build configurations, compatibility validation, and component relationship rules.
- **Content:**
  Blog posts, threaded comments, and user-generated content for community engagement.

---

## 🏗️ Architecture

### Project Structure

#### 📂 Overview

TechReform BD 2 is organized as a modular Django project, with each core feature encapsulated in its own app for clarity, scalability, and maintainability. The backend is powered by **Django 5.1.4** with **SQLite** for development and optional **PostgreSQL** for production. The frontend leverages **Tailwind CSS** for responsive, modern design, and **CKEditor** for rich content editing.

#### 🔄 Request Lifecycle

1. **Routing:** URLs in `TechReform/urls.py` direct requests to the appropriate app.
2. **View Logic:** Views handle business logic, interact with models, and render templates.
3. **Context Processors:** Inject cart, wishlist, and comparison data globally.
4. **Templating:** Tailwind CSS ensures responsive, accessible UI.
5. **Security:** CSRF middleware protects form submissions.
6. **Authentication:** Middleware manages sessions and permissions.

#### 📁 Directory Layout

```text
TechReform BD 2/
├── AuthApp/         # User authentication & support
├── BlogApp/         # Blog & content management
├── CartApp/         # Shopping cart & orders
├── CompareApp/      # Product comparison
├── PCBuilderApp/    # PC configuration builder
├── ProductsApp/     # Product catalog & inventory
├── WishlistApp/     # User wishlists & favorites
├── TechReform/      # Project settings & URLs
├── templates/       # HTML templates (modular by app)
├── static/          # Static assets (CSS, JS, images)
├── media/           # User uploads (profile, blog, products)
├── theme/           # Tailwind CSS theme & config
├── tests/           # Automated test suites
├── manage.py        # Django management script
└── requirements.txt # Python dependencies
```

> **Tip:** Each app contains its own `models.py`, `views.py`, `urls.py`, `admin.py`, `forms.py`, `tests.py`, and migrations for clear separation of concerns.

#### 🔐 Security Highlights

- **CSRF Protection:** Prevents cross-site request forgery.
- **Password Validation:** Enforces strong password policies.
- **Role-Based Access:** Custom decorators for permission control.
- **Session Security:** Secure cookies and session timeouts.
- **XSS Prevention:** Template escaping and sanitization.

#### 🔌 Middleware & Extensions

- **Security Middleware:** Enforces HTTPS and security headers.
- **Authentication Middleware:** Associates users with requests.
- **Session Middleware:** Manages user state.
- **CKEditor:** Rich text editing for content.
- **Browser Reload:** Auto-refresh during development.
- **Tailwind CSS:** Utility-first styling.

#### 📦 Database Model Overview

- **User Models:** Extended profiles, roles, and permissions.
- **Product Models:** Detailed models for each hardware type.
- **E-commerce Models:** Cart, order, and payment tracking.
- **Content Models:** Blog posts, categories, comments.
- **Builder Models:** PC configurations and compatibility.
- **Support Models:** Customer tickets and support logs.

#### 🌐 URL Structure

| Path           | Purpose                          |
|----------------|----------------------------------|
| `/`            | Homepage & product catalog       |
| `/auth/`       | User authentication & profiles   |
| `/cart/`       | Shopping cart & checkout        |
| `/pc-builder/` | PC configuration tool           |
| `/compare/`    | Product comparison              |
| `/wishlist/`   | User wishlists                  |
| `/blog/`       | Blog & articles                 |
| `/admin/`      | Admin dashboard                 |

---

### Application Components

#### **ProductsApp – Product Catalog**

- **Models:** CPU, GPU, Motherboard, RAM, SSD, HDD, Cooler, PSU, Casing, Monitor, Keyboard, Mouse, Headphone
- **Features:** Advanced filtering, inventory, pricing, categorization
- **Media:** Multiple images per product, optimized storage
- **API:** Endpoints for PC Builder and comparison tools

#### **AuthApp – Authentication & Support**

- **User Management:** Extended profiles, role-based permissions
- **Support:** Ticketing system with categories and tracking
- **Security:** Password validation, email verification, password reset
- **Roles:** Admin, Staff, Content Manager, Blogger, Customer, Guest

#### **CartApp – Shopping & Orders**

- **Cart:** Session-based and persistent carts
- **Orders:** Full lifecycle management, status tracking
- **Shipping:** Address management, shipping calculations
- **Payments:** Ready for multiple gateways
- **Order History:** User-accessible purchase records

#### **PCBuilderApp – PC Configuration**

- **Component Selection:** Guided, filterable interface
- **Compatibility:** Real-time validation of component choices
- **Build Management:** Save, share, and manage builds
- **Power Calculation:** Estimate system power needs
│   ├── auth/               # Authentication templates
│   ├── blog/               # Blog and content templates
│   ├── cart/               # Cart and checkout templates
│   ├── compare/            # Product comparison templates
│   ├── pcbuilder/          # PC Builder templates
│   ├── product/            # Product catalog templates
│   ├── static/             # Static template parts
│   ├── user/               # User profile templates
- **Cart Integration:** Add all build components to cart

#### **CompareApp – Product Comparison**ges)

- **Multi-Product:** Compare up to 4 products side-by-side
- **Category Views:** Tailored for each product type
- **History:** Track previous comparisons
- **Highlighting:** Visual differences for key specs
- **Export:** Save as PDF or shareable links
   └── *_images/           # Product category images

#### **WishlistApp – User Favorites**

e

- **Management:** Save and organize products   ├── **init**.py         # Package initialization
- **Multiple Lists:** Themed wishlistsration
- **Static Assets:** CSS, JS, media management
- **Deployment:** WSGI/ASGI setup for production*Notifications:** Stock and price alertses
- **Tracking:** Price change monitoringates

---

#### **BlogApp – Content Management**tes
>
> This modular, security-focused architecture ensures TechReform BD 2 is robust, scalable, and easy to maintain—ready to deliver a seamless experience for users and developers alike.

- **Comment System**: User engagement through comments
- **Author Management**: Content attribution and writer profiles
- **Content Types**: Blog posts, tutorials, product reviews, news updates

#### TechReform Core - Project Foundation

- **Settings Configuration**: Environment-specific application settings
- **URL Routing**: Central request dispatcher to application views
- **Middleware Stack**: Request/response processing pipeline
- **Template Structure**: Base templates and inheritance patterns
- **Static Asset Management**: CSS, JavaScript, and media handling
- **Deployment Configuration**: WSGI/ASGI setup for production

---

## 🚀 Quick Start

### 📋 Prerequisites

Make sure you have these tools installed before starting:

| Requirement      | Version   | Purpose                |
|------------------|-----------|------------------------|
| 🐍 **Python**    | 3.8 or higher | Backend runtime      |
| 📦 **Node.js**   | 16 or higher | Frontend tooling     |
| 📥 **npm**       | 8 or higher  | JS package manager   |
| 🔄 **Git**       | Latest    | Version control        |

---

### ⚡ Installation Steps

#### 1. 📥 Clone the Repository

```bash
git clone https://github.com/SharifdotG/TechReform-BD-2.git
cd TechReform-BD-2
```

#### 2. 🐍 Set Up Python Virtual Environment

<details>
<summary><strong>Windows (PowerShell)</strong></summary>

```powershell
pip install virtualenv
python -m venv venv
venv\Scripts\Activate.ps1
```

</details>

<details>
<summary><strong>macOS / Linux</strong></summary>

```bash
pip install virtualenv
python -m venv venv
source venv/bin/activate
```

</details>

#### 3. 📦 Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 4. 🎨 Install Node.js Dependencies & Build Tailwind CSS

```bash
cd theme/static_src
npm install
npm run build
cd ../..
```

> 💡 **Important:** This step builds the Tailwind CSS files. Without this, the site will display raw HTML without styling.

#### 5. ⚙️ Environment Configuration (Optional)

```bash
cp .env.example .env
# Edit .env to match your local setup
```

#### 6. 🗄️ Database Setup

**⚠️ Make sure your virtual environment is activated before running Django commands:**

```bash
# Ensure virtual environment is active
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate     # Windows

# Run database migrations
python manage.py makemigrations
python manage.py migrate
```

#### 7. 👤 Create Superuser

```bash
python manage.py createsuperuser
```

#### 8. 📂 Collect Static Files

```bash
python manage.py collectstatic --noinput
```

#### 9. 🏃 Start Development Servers

**You need to run TWO servers simultaneously in separate terminals:**

- **Terminal 1** — Django backend:

  ```bash
  # Make sure virtual environment is activated
  source venv/bin/activate  # Linux/macOS
  # OR
  venv\Scripts\activate     # Windows

  # Start Django server
  python manage.py runserver
  # using SQLite for development, PostgreSQL is used in production
  ```

- **Terminal 2** — Tailwind CSS watcher (for live CSS updates):

  ```bash
  cd theme/static_src
  npm run dev
  ```

> 🚨 **Troubleshooting:** If you see raw HTML without styling, ensure both servers are running and the Tailwind CSS was built (step 4).

#### 10. 🌐 Access the Application

| Service            | URL                                 | Description                |
|--------------------|-------------------------------------|----------------------------|
| 🏠 **Main Site**   | [http://localhost:8000](http://localhost:8000)       | User-facing web app        |
| ⚙️ **Admin Panel** | [http://localhost:8000/admin](http://localhost:8000/admin) | Django admin dashboard     |

---

> 💡 **Tip:** For a smooth experience, keep both Django and Tailwind servers running in separate terminals.

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 🚨 Site Shows Raw HTML Without Styling

**Problem:** The website displays unstyled HTML content.

**Solution:**
1. Ensure Tailwind CSS is built:
   ```bash
   cd theme/static_src
   npm run build
   ```
2. Make sure both servers are running:
   - Django server: `python manage.py runserver`
   - Tailwind watcher: `npm run dev` (in `theme/static_src` directory)

#### 🐍 "ModuleNotFoundError: No module named 'django'"

**Problem:** Python can't find Django or other dependencies.

**Solution:** Activate your virtual environment:
```bash
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate     # Windows
```

#### 📦 "npm audit" Issues

**Problem:** Security vulnerabilities in npm packages.

**Solution:** Run audit fix from the correct directory:
```bash
cd theme/static_src
npm audit fix
```

#### 🚪 "That port is already in use"

**Problem:** Port 8000 is occupied by another process.

**Solutions:**
- Use a different port: `python manage.py runserver 8001`
- Kill existing processes: `pkill -f "python manage.py runserver"`

---

## 🛠️ Development

### 🧹 Code Quality & Standards

- **PEP 8 Compliance:** All Python code adheres to [PEP 8](https://peps.python.org/pep-0008/) style guidelines for readability and consistency.
- **Ruff:** Blazing-fast linter and code formatter for Python. Ensures code is clean and error-free.
- **Type Hints:** Extensive use of type annotations for improved maintainability and editor support.
- **Pre-commit Hooks:** Automated checks for formatting, linting, and static analysis before every commit.

---

### 🗄️ Database Management

```bash
# Create new migrations based on model changes
python manage.py makemigrations

# Apply migrations to update the database schema
python manage.py migrate

# Reset the database (development only – erases all data)
python manage.py flush

# Load sample data for testing and development
python manage.py loaddata fixtures/sample_data.json
```

---

### 🎨 Code Formatting & Linting

```bash
# Format all code using Ruff
ruff format .

# Check and automatically fix linting issues
ruff check --fix .

# Check code for linting issues (no changes made)
ruff check .

# Run static type checking (if using mypy)
mypy .
```

---

### 💠 Tailwind CSS Workflow

```bash
# Navigate to the Tailwind directory
cd theme/static_src

# Start Tailwind CSS in watch mode for live development
npm run dev

# Build Tailwind CSS for production deployment
npm run build

# Install or update Tailwind CSS dependencies
npm install

# Build and clean (for production)
npm run build:clean && npm run build:tailwind
```

> **Important:** Use `npm run dev` instead of Django's tailwind commands for better compatibility and performance.
> Keep the Tailwind watcher (`npm run dev`) running in a separate terminal during development.

> **Tip:** Keep Django and Tailwind servers running in separate terminals for the best development experience.

---

## 📦 Dependencies

### 🔧 Core Dependencies

| Package                | Version  | Purpose                                         | Documentation                                      |
|------------------------|----------|-------------------------------------------------|----------------------------------------------------|
| **Django**             | 5.1.4    | High-level Python web framework (MVT)            | [Docs](https://www.djangoproject.com/)             |
| **Pillow**             | 11.0.0   | Image processing for products & avatars          | [Docs](https://pillow.readthedocs.io/)             |
| **django-ckeditor**    | 6.7.1    | Rich text editor for blog/content                | [Docs](https://django-ckeditor.readthedocs.io/)    |
| **django-tailwind**    | 3.8.0    | Tailwind CSS integration for Django              | [Docs](https://django-tailwind.readthedocs.io/)    |
| **python-slugify**     | 8.0.4    | SEO-friendly URL slug generation                 | [Docs](https://github.com/un33k/python-slugify)    |
| **requests**           | 2.32.3   | HTTP client for API integrations                 | [Docs](https://requests.readthedocs.io/)           |
| **markdown-it-py**     | 3.0.0    | Markdown rendering for blog posts                | [Docs](https://markdown-it-py.readthedocs.io/)     |

---

### 🛠️ Development Dependencies

| Package                   | Version  | Purpose                                 |
|---------------------------|----------|-----------------------------------------|
| **django-browser-reload** | 1.18.0   | Live browser reload during development  |
| **django-extensions**     | 3.2.3    | Extra management commands for Django    |
| **django-environ**        | 0.11.2   | Environment variable management         |

---

### 🚀 Production Dependencies

| Package             | Version  | Purpose                        |
|---------------------|----------|--------------------------------|
| **gunicorn**        | 21.2.0   | WSGI HTTP server for deployment|
| **whitenoise**      | 6.6.0    | Static file serving            |
| **psycopg2-binary** | 2.9.10   | PostgreSQL database adapter    |
| **redis**           | 5.0.1    | Caching & session storage      |
| **celery**          | 5.3.4    | Asynchronous task processing   |

---

### 🔐 Authentication

TechReform BD 2 supports multiple authentication strategies:

- 🍪 **Session-based authentication** — Secure login for web users (Django default)
- 🎫 **Token-based authentication** — For mobile and external API clients
- 🔑 **JWT authentication** — For modern SPAs and stateless API access

> **Tip:** Choose the authentication method that best fits your client application (web, mobile, or SPA).

---

## 🧪 Testing

### 📊 Test Coverage Overview

| Test Type                | Scope/Target                | Description                                              |
|--------------------------|-----------------------------|----------------------------------------------------------|
| **✅ Unit Tests**        | Models, Views, Forms        | Isolated testing of individual components                |
| **🔄 Integration Tests** | End-to-end Workflows        | Cart-to-checkout, PC builder, and multi-app interactions |
| **🔐 Auth Tests**        | User Management             | Registration, login, permissions, and access control     |
| **🎯 Functional Tests**  | User Journeys               | Real-world feature flows across the platform             |
| **⚡ Performance Tests** | Load & Stress Scenarios     | High-traffic and resource-intensive operations           |

---

### 📁 Test Suite Structure

All tests are organized by feature for clarity and maintainability:

```text
tests/
├── cart_checkout.py        # 🛒 E-commerce workflow tests
├── create_blog.py          # 📝 Blog and content management tests
├── pc_builder.py           # 🖥️ PC builder logic and compatibility tests
├── signup_login.py         # 🔐 Authentication and user flow tests
├── user_management.py      # 👥 User profile and management tests
└── *_report.html           # 📋 HTML coverage reports
```

---

### 🏃 How to Run Tests

#### 🔹 Run All Tests

```bash
python manage.py test
```

#### 🔹 Run a Specific Test File

```bash
python manage.py test tests.cart_checkout
```

#### 🔹 Generate Coverage Report

```bash
coverage run --source='.' manage.py test
coverage report
coverage html
```

> **Tip:** Coverage reports are generated as HTML files for easy visualization of test coverage.

---

## 🤝 Contributing

We’re excited to have you contribute to **TechReform BD 2**! Whether you’re fixing bugs, adding features, improving docs, or enhancing the UI, your input is valued.

---

### 🚀 Development Workflow

1. **Fork** this repository to your GitHub account.
2. **Create a feature branch**

  ```bash
  git checkout -b feature/your-feature-name
  ```

3. **Make your changes**

- Write clear, maintainable code.
- Add or update tests as needed.

4. **Run tests**

  ```bash
  python manage.py test
  ```

5. **Format & lint your code**

  ```bash
  ruff format .
  ruff check --fix .
  ```

6. **Commit your changes**

  ```bash
  git commit -m "feat: add your feature description"
  ```

7. **Push to your fork**

  ```bash
  git push origin feature/your-feature-name
  ```

8. **Open a Pull Request**

- Describe your changes clearly.
- Reference related issues if applicable.

---

### 📏 Code Standards

| Standard                | Tool/Guideline           | Purpose                        |
|-------------------------|--------------------------|--------------------------------|
| 🐍 Python Style         | PEP 8 + Ruff             | Consistent, readable code      |
| 📝 Commit Messages      | Conventional Commits     | Clear, semantic history        |
| 🧪 Testing              | Django TestCase          | Reliable, robust features      |
| 📖 Documentation        | Markdown & Docstrings    | Easy onboarding & maintenance  |
| 🔄 Compatibility        | Semantic Versioning      | Predictable releases           |

---

### 🔄 Pull Request Checklist

- [ ] Update `README.md` if your changes affect documentation.
- [ ] Update `requirements.txt` if you add new dependencies.
- [ ] Bump version numbers (see [Semantic Versioning](https://semver.org/)).
- [ ] Ensure all tests and CI checks pass.
- [ ] Request a review from project maintainers.

---

### 🎯 Where to Contribute?

We especially welcome help with:

- 🐛 **Bug Fixes** — Squash those pesky issues!
- ✨ **New Features** — Bring your ideas to life.
- 📖 **Documentation** — Make the project easier to use.
- 🧪 **Testing** — Improve coverage and reliability.
- 🎨 **UI/UX** — Polish the look and feel.
- ⚡ **Performance** — Make things faster and smoother.

---

**Thank you for making TechReform BD 2 better!**
Your contributions help empower the PC community in Bangladesh.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
You are free to use, modify, and distribute this software with proper attribution.

---

## 🙏 Acknowledgments

Special thanks to the open-source community and the following projects for making TechReform BD 2 possible:

- **[Django](https://www.djangoproject.com/)** — The robust web framework powering our backend.
- **[Tailwind CSS](https://tailwindcss.com/)** — For rapid, utility-first frontend styling.
- **[CKEditor](https://ckeditor.com/)** — For enabling rich text editing in our content management.
- **All Contributors** — Every developer, designer, and tester who helped shape this project.

---

## 📞 Support

Need help or want to get involved?

- **🐞 Issues:** [Report bugs or request features](../../issues)
- **💬 Discussions:** [Join the community conversation](../../discussions)
- **📧 Contact:** For other inquiries, reach out via the project's GitHub page.

Your feedback and participation help us grow and improve!

---

## 🗺️ Roadmap

### 🚀 Version 2.0 (Upcoming)

- [ ] **🤖 AI-Powered PC Builder:**
  Personalized PC building assistant offering recommendations tailored to your usage, budget, and performance needs.
- [ ] **📊 Real-time Price Comparison:**
  Instantly compare prices across multiple local vendors for maximum transparency and the best deals.
- [ ] **⭐ Enhanced User Reviews:**
  Rich review system featuring verified purchase badges, photo uploads, and in-depth product experiences.
- [ ] **💬 Community Forum:**
  Interactive platform for tech discussions, build showcases, and peer-to-peer support.
- [ ] **📱 Mobile Applications:**
  Native iOS and Android apps with push notifications for a seamless mobile experience.
- [ ] **🚚 Delivery Services Integration:**
  Real-time order tracking and faster delivery through integration with local courier APIs.

---

### 🌟 Version 2.1 (Planned/Future)

- [ ] **🧠 AI Product Recommendations:**
  Intelligent suggestions based on your browsing and purchase history.
- [ ] **🇧🇩 Bengali Localization:**
  Full Bengali language support to make the platform accessible to all local users.
- [ ] **🔍 AR Component Visualization:**
  Augmented reality tools to preview PC components in your own space.
- [ ] **🎮 Gamification:**
  Earn points, badges, and rewards for active participation and contributions.
- [ ] **📊 Admin Analytics:**
  Advanced dashboards for sales insights, user behavior analytics, and inventory management.
- [ ] **🏪 Multi-vendor Marketplace:**
  Expansion to include trusted vendors, ensuring fair pricing and greater selection.

---

> **Stay tuned!**
> We’re committed to continuous improvement—your feedback shapes our roadmap.
> [Suggest a feature or join the discussion &rarr;](../../discussions)

---

### 🚀 Join the TechReform Movement

**TechReform BD 2** isn’t just an e-commerce platform—it’s a community-driven initiative to revolutionize how PC components are bought and sold in Bangladesh. We believe in *fair pricing*, *transparency*, and *reliable service* for all.

<div align="center">

#### 🤝 Get Involved & Shape the Future

<a href="https://github.com/SharifdotG/TechReform-BD-2/issues" target="_blank">
  <img src="https://img.shields.io/badge/Report%20Issues-181717?style=for-the-badge&logo=github" alt="Report Issues"/>
</a>
<a href="https://github.com/SharifdotG/TechReform-BD-2/discussions" target="_blank">
  <img src="https://img.shields.io/badge/Join%20Discussions-181717?style=for-the-badge&logo=github" alt="Join Discussions"/>
</a>
<a href="https://github.com/SharifdotG/TechReform-BD-2" target="_blank">
  <img src="https://img.shields.io/github/watchers/SharifdotG/TechReform-BD-2?style=for-the-badge&label=Subscribe%20to%20Updates" alt="Subscribe to Updates"/>
</a>

</div>

- 💡 **Report bugs or suggest features** to help us improve.
- 💬 **Join discussions** and connect with fellow PC enthusiasts.
- 📢 **Subscribe** to stay updated on new features and releases.

---

<p align="center">
  Made with <span style="color: #e25555;">❤️</span> by the <strong>TechReform BD 2 Team</strong>
</p>
