<div align="center">

# 🖥️ TechReform BD 2

<h2 style="color: #2563eb; font-weight: bold;">Revolutionary E-Commerce Platform for PC Components</h2>

</div>

<div align="center">

[![Django](https://img.shields.io/badge/Django-5.1.4-092e20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-D7FF64?style=for-the-badge)](https://github.com/astral-sh/ruff)

[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

</div>

---

<div align="center">
<table>
<tr>
<td align="center" width="100%" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px;">
<h3 style="color: white; margin: 0;">🎯 Mission Statement</h3>
<p style="color: white; font-size: 18px; margin: 10px 0; font-weight: bold;">
Revolutionizing PC component purchasing in Bangladesh through <em>fair pricing</em>, <em>transparent supply chains</em>, and <em>reliable after-sales service</em>
</p>
</td>
</tr>
</table>
</div>

---

## 📋 Table of Contents

- [🖥️ TechReform BD 2](#️-techreform-bd-2)
  - [📋 Table of Contents](#-table-of-contents)
  - [📖 Overview](#-overview)
  - [🖼️ Preview](#️-preview)
  - [🎯 Project Motivation](#-project-motivation)
    - [🚨 Problems We Solve](#-problems-we-solve)
    - [🎯 Our Mission](#-our-mission)
  - [✨ Features](#-features)
  - [👥 Development Team](#-development-team)
  - [🏛️ Technical Architecture](#️-technical-architecture)
    - [Design Patterns](#design-patterns)
    - [Development Methodology](#development-methodology)
    - [Database Design](#database-design)
  - [🏗️ Architecture](#️-architecture)
  - [🚀 Quick Start](#-quick-start)
- [Edit .env with your configuration](#edit-env-with-your-configuration)
  - [🛠️ Development](#️-development)
    - [Code Quality](#code-quality)
    - [Database Management](#database-management)
    - [Code Formatting and Linting](#code-formatting-and-linting)
    - [Tailwind CSS Development](#tailwind-css-development)
  - [📦 Dependencies](#-dependencies)
    - [🔧 Core Dependencies](#-core-dependencies)
    - [🛠️ Development Dependencies](#️-development-dependencies)
    - [🚀 Production Dependencies](#-production-dependencies)
    - [🔐 Authentication](#-authentication)
  - [🧪 Testing](#-testing)
  - [🤝 Contributing](#-contributing)
    - [🚀 Development Workflow](#-development-workflow)
    - [📏 Code Standards](#-code-standards)
    - [🔄 Pull Request Process](#-pull-request-process)
    - [🎯 Contribution Areas](#-contribution-areas)
  - [📄 License](#-license)
  - [🙏 Acknowledgments](#-acknowledgments)
  - [📞 Support](#-support)
    - [Getting Help](#getting-help)
  - [🗺️ Roadmap](#️-roadmap)

---

## 📖 Overview

**TechReform BD 2** is a comprehensive e-commerce platform specializing in PC components and accessories. Built with Django and modern web technologies, it revolutionizes how PC components are purchased in Bangladesh by ensuring users get fair prices at or near Manufacturer's Suggested Retail Price (MSRP) and reliable after-sales service through a streamlined **"manufacturer → authorized local supplier → user"** model.

## 🖼️ Preview

<div style="border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 8px; padding: 20px; margin-bottom: 20px; background-color: var(--vscode-editor-background, #f5f5f5);">
  <h3 style="margin-top: 0; color: var(--vscode-editor-foreground, #333);">✨ Application Demo</h3>

  <div style="text-align: center; margin: 20px 0;">
    <img src="placeholder/Preview.gif" alt="TechReform BD Application Preview" style="max-width: 100%; border-radius: 8px; border: 1px solid var(--vscode-panel-border, #ddd); box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
  </div>

  <p style="text-align: center; color: var(--vscode-editor-foreground, #333); margin-top: 10px; font-style: italic;">
    Preview of TechReform BD 2 showing the complete user experience and key features
  </p>
</div>

## 🎯 Project Motivation

**TechReform BD 2** addresses critical challenges in Bangladesh's PC component market by revolutionizing the traditional supply chain.

### 🚨 Problems We Solve

| Challenge | Traditional Market | TechReform BD 2 Solution |
|-----------|-------------------|--------------------------|
| 💰 **Inflated Prices** | Multiple intermediary layers add 30-50% markup | Direct manufacturer partnerships eliminate unnecessary markups |
| 🔍 **Price Transparency** | Hidden pricing, unclear margins | Clear MSRP-aligned pricing with transparency |
| 🛠️ **After-Sales Service** | Complex multi-step warranty claims | Streamlined manufacturer-backed warranty and RMA |
| ✅ **Product Authenticity** | Risk of counterfeit products | Guaranteed genuine products with valid warranties |
| 📊 **Information Gap** | Limited product knowledge | Comprehensive education and fair pricing awareness |

### 🎯 Our Mission

By implementing a **"manufacturer → authorized local supplier → user"** model, TechReform BD 2 empowers the Bangladeshi tech community with:

- ✅ **Fair Pricing** at or near MSRP
- ✅ **Transparent Supply Chain** operations
- ✅ **Reliable Support Services** with direct manufacturer relationships
- ✅ **Community Education** about fair pricing and warranty procedures

## ✨ Features

<details open>
<summary>
<h3 style="display: inline-block; margin: 0;">🛍️ E-Commerce Core</h3>
</summary>
<div style="padding: 10px 20px; background-color: var(--vscode-editor-background, #f8fafc); border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 8px; margin-top: 10px;">
<table>
<tr>
<td width="50" align="center">💰</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Fair Pricing Model</strong>: Direct supply chain from manufacturers to eliminate intermediary markups</td>
</tr>
<tr>
<td width="50" align="center">🏷️</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>MSRP Transparency</strong>: Clear pricing aligned with Manufacturer's Suggested Retail Price</td>
</tr>
<tr>
<td width="50" align="center">📦</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Product Catalog</strong>: Comprehensive catalog for computer hardware and accessories</td>
</tr>
<tr>
<td width="50" align="center">🛒</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Shopping Cart</strong>: Session-based cart for anonymous users and persistent cart for registered users</td>
</tr>
<tr>
<td width="50" align="center">🔒</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Secure Checkout</strong>: Complete order processing with multiple payment options</td>
</tr>
<tr>
<td width="50" align="center">📋</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Order Management</strong>: Full order lifecycle tracking from cart to delivery</td>
</tr>
<tr>
<td width="50" align="center">📊</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Inventory Management</strong>: Real-time stock tracking and availability status</td>
</tr>
<tr>
<td width="50" align="center">✅</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Authentic Products</strong>: Genuine products with full manufacturer warranty coverage</td>
</tr>
</table>
</div>
</details>

<details open>
<summary>
<h3 style="display: inline-block; margin: 0;">👥 User Management</h3>
</summary>
<div style="padding: 10px 20px; background-color: var(--vscode-editor-background, #f8fafc); border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 8px; margin-top: 10px;">
<table>
<tr>
<td width="50" align="center">🔐</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Role-Based Authentication</strong>: Multiple user roles (Admin, Staff, Content Manager, Blogger, Customer, Guest)</td>
</tr>
<tr>
<td width="50" align="center">👤</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>User Profiles</strong>: Extended user profiles with customizable information</td>
</tr>
<tr>
<td width="50" align="center">🎧</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Customer Support</strong>: Comprehensive ticket system with categories and responses</td>
</tr>
<tr>
<td width="50" align="center">✉️</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Account Verification</strong>: Email-based user verification system</td>
</tr>
<tr>
<td width="50" align="center">🛡️</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Warranty & RMA Support</strong>: Direct access to manufacturer-backed warranty and RMA services</td>
</tr>
</table>
</div>
</details>

<details open>
<summary>
<h3 style="display: inline-block; margin: 0;">🖥️ PC Builder Tool</h3>
</summary>
<div style="padding: 10px 20px; background-color: var(--vscode-editor-background, #f8fafc); border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 8px; margin-top: 10px;">
<table>
<tr>
<td width="50" align="center">⚙️</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Custom PC Configuration</strong>: Interactive PC building tool with component compatibility</td>
</tr>
<tr>
<td width="50" align="center">✅</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Real-time Compatibility Checking</strong>: Automatic validation of component combinations (CPU socket vs motherboard, RAM type, PSU wattage)</td>
</tr>
<tr>
<td width="50" align="center">⚡</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Power Calculation</strong>: Total system power consumption estimation</td>
</tr>
<tr>
<td width="50" align="center">🔗</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Build Sharing</strong>: Public/private build configurations with sharing capabilities</td>
</tr>
<tr>
<td width="50" align="center">💰</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Fair Pricing Integration</strong>: All components displayed with MSRP transparency</td>
</tr>
<tr>
<td width="50" align="center">💾</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Saved Builds</strong>: Save and manage multiple PC configurations in user profiles</td>
</tr>
</table>
</div>
</details>

<details open>
<summary>
<h3 style="display: inline-block; margin: 0;">📊 Product Features</h3>
</summary>
<div style="padding: 10px 20px; background-color: var(--vscode-editor-background, #f8fafc); border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 8px; margin-top: 10px;">
<table>
<tr>
<td width="50" align="center">⚖️</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Product Comparison</strong>: Side-by-side comparison of up to multiple products</td>
</tr>
<tr>
<td width="50" align="center">❤️</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Wishlist Management</strong>: Save favorite products for later purchase</td>
</tr>
<tr>
<td width="50" align="center">🔍</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Advanced Search</strong>: Filter products by specifications, price, brand, and availability</td>
</tr>
<tr>
<td width="50" align="center">⭐</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Product Reviews</strong>: User ratings and reviews system</td>
</tr>
</table>
</div>
</details>

<details open>
<summary>
<h3 style="display: inline-block; margin: 0;">📝 Content Management</h3>
</summary>
<div style="padding: 10px 20px; background-color: var(--vscode-editor-background, #f8fafc); border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 8px; margin-top: 10px;">
<table>
<tr>
<td width="50" align="center">📰</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Blog System</strong>: Rich content management with CKEditor integration</td>
</tr>
<tr>
<td width="50" align="center">🔍</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>SEO Optimization</strong>: URL slugs, meta descriptions, and search-friendly URLs</td>
</tr>
<tr>
<td width="50" align="center">📁</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Category Management</strong>: Hierarchical product and content categorization</td>
</tr>
<tr>
<td width="50" align="center">🎨</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Media Management</strong>: Comprehensive image and file upload system</td>
</tr>
</table>
</div>
</details>

<details open>
<summary>
<h3 style="display: inline-block; margin: 0;">🎨 Modern UI/UX</h3>
</summary>
<div style="padding: 10px 20px; background-color: var(--vscode-editor-background, #f8fafc); border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 8px; margin-top: 10px;">
<table>
<tr>
<td width="50" align="center">📱</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Responsive Design</strong>: Mobile-first approach with Tailwind CSS</td>
</tr>
<tr>
<td width="50" align="center">🌓</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Dark/Light Mode</strong>: Theme switching capabilities</td>
</tr>
<tr>
<td width="50" align="center">✨</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Modern Interface</strong>: Clean, professional design with intuitive navigation</td>
</tr>
<tr>
<td width="50" align="center">⚡</td>
<td style="color: var(--vscode-editor-foreground, #333);"><strong>Performance Optimized</strong>: Fast loading times and optimized queries</td>
</tr>
</table>
</div>
</details>

## 👥 Development Team

<div style="border-radius: 8px; padding: 20px; margin-bottom: 20px; border: 1px solid var(--vscode-panel-border, #ddd);">
<h3 style="text-align: center; margin-top: 0; margin-bottom: 15px; font-size: 20px; color: var(--vscode-editor-foreground, #333);">Meet the Team Behind TechReform BD 2</h3>
<p style="text-align: center; max-width: 800px; margin: 0 auto 20px auto; font-size: 16px; color: var(--vscode-editor-foreground, #333);">
Our platform is developed by a passionate team of software engineering students dedicated to revolutionizing the PC component market in Bangladesh.
</p>

<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; margin-bottom: 20px;">
  <!-- Team Member Card 1 -->
  <div style="border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 8px; width: 300px; padding: 0; overflow: hidden;">
    <div style="border-bottom: 1px solid var(--vscode-panel-border, #ddd); padding: 12px; text-align: center; background-color: var(--vscode-editor-selectionBackground, rgba(0, 120, 215, 0.1));">
      <img src="https://img.shields.io/badge/👨‍💻-Lead%20Developer-blue?style=for-the-badge" alt="Lead Developer"/>
    </div>
    <div style="padding: 15px; text-align: center;">
      <h3 style="margin: 0 0 10px 0; font-size: 18px; color: var(--vscode-editor-foreground, #333);">Sharif Md. Yousuf</h3>
      <div style="border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 15px; padding: 4px 10px; display: inline-block; margin-bottom: 12px;">
        <span style="font-weight: bold; color: var(--vscode-editor-foreground, #333);">Project Manager & Lead Developer</span>
      </div>
      <p style="margin: 0; color: var(--vscode-editor-foreground, #333); line-height: 1.5;">Project architecture, team coordination, full-stack development</p>      <div style="margin-top: 12px; display: flex; justify-content: center; gap: 8px; flex-wrap: wrap;">
        <span style="border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 15px; padding: 2px 8px; font-size: 12px; color: var(--vscode-editor-foreground, #333);">Django</span>
        <span style="border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 15px; padding: 2px 8px; font-size: 12px; color: var(--vscode-editor-foreground, #333);">React</span>
        <span style="border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 15px; padding: 2px 8px; font-size: 12px; color: var(--vscode-editor-foreground, #333);">Python</span>
      </div>
      <div style="margin-top: 12px; display: flex; justify-content: center;">
        <a href="https://github.com/SharifdotG" target="_blank" style="text-decoration: none;">
          <img src="https://img.shields.io/badge/GitHub-SharifdotG-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Profile"/>
        </a>
      </div>
    </div>
  </div>

  <!-- Team Member Card 2 -->
  <div style="border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 8px; width: 300px; padding: 0; overflow: hidden;">
    <div style="border-bottom: 1px solid var(--vscode-panel-border, #ddd); padding: 12px; text-align: center; background-color: var(--vscode-editor-selectionBackground, rgba(0, 120, 215, 0.1));">
      <img src="https://img.shields.io/badge/🔧-Backend%20Developer-green?style=for-the-badge" alt="Backend Developer"/>
    </div>
    <div style="padding: 15px; text-align: center;">
      <h3 style="margin: 0 0 10px 0; font-size: 18px; color: var(--vscode-editor-foreground, #333);">Noor Mohammed Priom</h3>
      <div style="border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 15px; padding: 4px 10px; display: inline-block; margin-bottom: 12px;">
        <span style="font-weight: bold; color: var(--vscode-editor-foreground, #333);">Backend Developer & Database Architect</span>
      </div>
      <p style="margin: 0; color: var(--vscode-editor-foreground, #333); line-height: 1.5;">Django backend, database design, API development</p>      <div style="margin-top: 12px; display: flex; justify-content: center; gap: 8px; flex-wrap: wrap;">
        <span style="border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 15px; padding: 2px 8px; font-size: 12px; color: var(--vscode-editor-foreground, #333);">Django</span>
        <span style="border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 15px; padding: 2px 8px; font-size: 12px; color: var(--vscode-editor-foreground, #333);">SQL</span>
        <span style="border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 15px; padding: 2px 8px; font-size: 12px; color: var(--vscode-editor-foreground, #333);">Python</span>
      </div>
      <div style="margin-top: 12px; display: flex; justify-content: center;">
        <a href="https://github.com/SOrtINgmASteR" target="_blank" style="text-decoration: none;">
          <img src="https://img.shields.io/badge/GitHub-SOrtINgmASteR-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Profile"/>
        </a>
      </div>
    </div>
  </div>

  <!-- Team Member Card 3 -->
  <div style="border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 8px; width: 300px; padding: 0; overflow: hidden;">
    <div style="border-bottom: 1px solid var(--vscode-panel-border, #ddd); padding: 12px; text-align: center; background-color: var(--vscode-editor-selectionBackground, rgba(0, 120, 215, 0.1));">
      <img src="https://img.shields.io/badge/🎨-Frontend%20Developer-purple?style=for-the-badge" alt="Frontend Developer"/>
    </div>
    <div style="padding: 15px; text-align: center;">
      <h3 style="margin: 0 0 10px 0; font-size: 18px; color: var(--vscode-editor-foreground, #333);">Shornali Akter</h3>
      <div style="border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 15px; padding: 4px 10px; display: inline-block; margin-bottom: 12px;">
        <span style="font-weight: bold; color: var(--vscode-editor-foreground, #333);">Frontend Developer & UI/UX Designer</span>
      </div>
      <p style="margin: 0; color: var(--vscode-editor-foreground, #333); line-height: 1.5;">User interface design, frontend implementation, user experience</p>      <div style="margin-top: 12px; display: flex; justify-content: center; gap: 8px; flex-wrap: wrap;">
        <span style="border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 15px; padding: 2px 8px; font-size: 12px; color: var(--vscode-editor-foreground, #333);">HTML/CSS</span>
        <span style="border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 15px; padding: 2px 8px; font-size: 12px; color: var(--vscode-editor-foreground, #333);">Tailwind</span>
        <span style="border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 15px; padding: 2px 8px; font-size: 12px; color: var(--vscode-editor-foreground, #333);">Figma</span>
      </div>
      <div style="margin-top: 12px; display: flex; justify-content: center;">
        <a href="https://github.com/nudhar60" target="_blank" style="text-decoration: none;">
          <img src="https://img.shields.io/badge/GitHub-nudhar60-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Profile"/>
        </a>
      </div>
    </div>
  </div>
</div>
</div>

## 🏛️ Technical Architecture

### Design Patterns

- **Model-View-Template (MVT)**: Django's architectural pattern for separation of concerns
- **Repository Pattern**: Abstracted data access through Django ORM
- **Factory Pattern**: Component creation and PC build assembly logic

### Development Methodology

- **Agile/Scrum**: Iterative development with 2-week sprints
- **Version Control**: Git with feature branch workflow
- **Test-Driven Development**: Comprehensive testing at unit and integration levels
- **Continuous Integration**: Automated testing and quality checks

### Database Design

The application uses a relational database with key entities:

- **User Management**: User profiles, roles, authentication
- **Product Catalog**: Components, categories, specifications, pricing
- **E-commerce**: Cart, orders, order items, inventory tracking
- **PC Builder**: Build configurations, component compatibility rules
- **Content**: Blog posts, comments, user-generated content

## 🏗️ Architecture

<div style="border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 8px; padding: 20px; margin-bottom: 20px;">
<h3 style="color: var(--vscode-editor-foreground, #333); margin-top: 0; margin-bottom: 15px;">Project Structure</h3>

<div style="display: flex; margin-bottom: 20px;">
  <div style="flex: 1; background-color: var(--vscode-editor-background, #f5f5f5); border-radius: 6px; padding: 15px; margin-right: 10px; color: var(--vscode-editor-foreground, #333);">
    <h4 style="margin-top: 0; margin-bottom: 10px; color: var(--vscode-editor-foreground, #333); border-bottom: 1px solid var(--vscode-panel-border, #ddd); padding-bottom: 5px;">
      📂 Project Overview
    </h4>
    <p style="margin-top: 0; margin-bottom: 10px; font-size: 14px;">
      TechReform BD 2 follows a modular architecture with specialized Django apps for each core functionality. The project is built on <strong>Django 5.1.4</strong> and uses <strong>SQLite</strong> for development and can be configured for <strong>PostgreSQL</strong> in production.
    </p>
    <p style="margin-top: 0; font-size: 14px;">
      The front-end uses <strong>Tailwind CSS</strong> for responsive styling with both light and dark mode support, while rich content management is handled through <strong>CKEditor</strong> integration.
    </p>
  </div>

  <div style="flex: 1; background-color: var(--vscode-editor-background, #f5f5f5); border-radius: 6px; padding: 15px; color: var(--vscode-editor-foreground, #333);">
    <h4 style="margin-top: 0; margin-bottom: 10px; color: var(--vscode-editor-foreground, #333); border-bottom: 1px solid var(--vscode-panel-border, #ddd); padding-bottom: 5px;">
      🔄 Request Flow
    </h4>
    <p style="margin-top: 0; margin-bottom: 10px; font-size: 14px;">
      <strong>1.</strong> URL patterns in <code>TechReform/urls.py</code> route requests to appropriate app views<br>
      <strong>2.</strong> Views process requests, interact with models, and render templates<br>
      <strong>3.</strong> Global context processors inject cart, wishlist, and comparison data<br>
      <strong>4.</strong> Templates use Tailwind CSS for responsive rendering<br>
      <strong>5.</strong> Form submissions are protected with CSRF middleware<br>
      <strong>6.</strong> Authentication middleware manages user sessions and permissions
    </p>
  </div>
</div>

<div style="background-color: var(--vscode-editor-background, #f5f5f5); border-radius: 6px; padding: 15px; font-family: monospace; white-space: pre; overflow-x: auto; color: var(--vscode-editor-foreground, #333); margin-bottom: 20px;">
<span style="color: var(--vscode-textPreformat-foreground, #0550ae); font-weight: bold;">TechReform BD 2/</span>
├── 📁 <span style="color: var(--vscode-textLink-foreground, #2563eb);">AuthApp/</span>              # User authentication & customer support
│   ├── __init__.py         # Package initialization
│   ├── admin.py            # Admin panel configuration
│   ├── apps.py             # App configuration
│   ├── decorators.py       # Custom auth decorators for role-based access
│   ├── forms.py            # User registration and profile forms
│   ├── models.py           # User profile and support ticket models
│   ├── tests.py            # Unit tests for authentication features
│   ├── urls.py             # Authentication URL routing
│   ├── views.py            # Authentication and user management views
│   └── migrations/         # Database migrations for user models
│
├── 📁 <span style="color: var(--vscode-textLink-foreground, #2563eb);">BlogApp/</span>              # Content management system
│   ├── __init__.py         # Package initialization
│   ├── admin.py            # Blog content admin interface
│   ├── apps.py             # App configuration
│   ├── forms.py            # Blog post creation and editing forms
│   ├── models.py           # Blog post, category, and comment models
│   ├── tests.py            # Content management test cases
│   ├── urls.py             # Blog content URL patterns
│   ├── views.py            # Blog content views and processing
│   └── migrations/         # Database migrations for blog models
│
├── 📁 <span style="color: var(--vscode-textLink-foreground, #2563eb);">CartApp/</span>              # Shopping cart & order processing
│   ├── __init__.py         # Package initialization
│   ├── admin.py            # Cart and order admin interface
│   ├── apps.py             # App configuration
│   ├── models.py           # Cart, order, and line item models
│   ├── tests.py            # Cart and checkout test cases
│   ├── urls.py             # Cart and checkout URL patterns
│   ├── views.py            # Cart management and checkout views
│   ├── context_processors/ # Global cart data processors
│   ├── migrations/         # Database migrations for cart models
│   └── templatetags/       # Custom template tags for cart
│
├── 📁 <span style="color: var(--vscode-textLink-foreground, #2563eb);">CompareApp/</span>           # Product comparison functionality
│   ├── __init__.py         # Package initialization
│   ├── admin.py            # Comparison admin configuration
│   ├── apps.py             # App configuration
│   ├── models.py           # Comparison and history models
│   ├── tests.py            # Comparison feature test cases
│   ├── urls.py             # Comparison URL patterns
│   ├── views.py            # Product comparison views
│   ├── context_processors/ # Global comparison data processors
│   ├── migrations/         # Database migrations for comparison models
│   └── templatetags/       # Custom template tags for comparisons
│
├── 📁 <span style="color: var(--vscode-textLink-foreground, #2563eb);">PCBuilderApp/</span>         # PC configuration builder
│   ├── __init__.py         # Package initialization
│   ├── admin.py            # PC Builder admin interface
│   ├── apps.py             # App configuration
│   ├── models.py           # PC build configuration models
│   ├── tests.py            # PC Builder test cases
│   ├── urls.py             # PC Builder URL patterns
│   ├── views.py            # PC configuration views and logic
│   └── migrations/         # Database migrations for builder models
│
├── 📁 <span style="color: var(--vscode-textLink-foreground, #2563eb);">ProductsApp/</span>          # Product catalog & inventory
│   ├── __init__.py         # Package initialization
│   ├── admin.py            # Product admin configuration
│   ├── apps.py             # App configuration
│   ├── models.py           # Product models (CPU, GPU, etc.)
│   ├── tests.py            # Product catalog test cases
│   ├── urls.py             # Product URL patterns
│   ├── views.py            # Product listing and detail views
│   ├── migrations/         # Database migrations for product models
│   └── templatetags/       # Custom template tags for products
│
├── 📁 <span style="color: var(--vscode-textLink-foreground, #2563eb);">WishlistApp/</span>          # User wishlists & favorites
│   ├── __init__.py         # Package initialization
│   ├── admin.py            # Wishlist admin interface
│   ├── apps.py             # App configuration
│   ├── models.py           # Wishlist and favorite item models
│   ├── tests.py            # Wishlist feature test cases
│   ├── urls.py             # Wishlist URL patterns
│   ├── views.py            # Wishlist management views
│   ├── context_processors/ # Global wishlist data processors
│   └── migrations/         # Database migrations for wishlist models
│
├── 📁 <span style="color: var(--vscode-textLink-foreground, #2563eb);">TechReform/</span>           # Main project settings
│   ├── __init__.py         # Package initialization
│   ├── asgi.py             # ASGI configuration
│   ├── settings.py         # Project settings and configurations
│   ├── urls.py             # Main URL routing configuration
│   └── wsgi.py             # WSGI configuration for deployment
│
├── 📁 <span style="color: var(--vscode-textLink-foreground, #2563eb);">templates/</span>            # HTML templates
│   ├── base.html           # Base template with common structure
│   ├── auth/               # Authentication templates
│   ├── blog/               # Blog and content templates
│   ├── cart/               # Cart and checkout templates
│   ├── compare/            # Product comparison templates
│   ├── pcbuilder/          # PC Builder templates
│   ├── product/            # Product catalog templates
│   ├── static/             # Static template parts
│   ├── user/               # User profile templates
│   └── wishlist/           # Wishlist templates
│
├── 📁 <span style="color: var(--vscode-textLink-foreground, #2563eb);">static/</span>               # Static files (CSS, JS, images)
│   └── index/              # Core static assets
│
├── 📁 <span style="color: var(--vscode-textLink-foreground, #2563eb);">media/</span>                # User uploaded files
│   ├── blog/               # Blog post images
│   ├── profile_images/     # User profile photos
│   └── *_images/           # Product category images
│
├── 📁 <span style="color: var(--vscode-textLink-foreground, #2563eb);">theme/</span>                # Tailwind CSS theme
│   ├── __init__.py         # Package initialization
│   ├── apps.py             # Tailwind app configuration
│   ├── static/             # Compiled CSS output
│   ├── static_src/         # Tailwind source files
│   └── templates/          # Tailwind-specific templates
│
├── 📁 <span style="color: var(--vscode-textLink-foreground, #2563eb);">tests/</span>                # Automated test suites
│   ├── Cart_Checkout.py    # E-commerce workflow tests
│   ├── Create_Blog.py      # Blog functionality tests
│   ├── PC_Builder.py       # PC builder logic tests
│   ├── SignUp_Login.py     # Authentication flow tests
│   └── User_Management.py  # User profile and management tests
│
├── 📄 <span style="color: var(--vscode-textLink-foreground, #2563eb);">manage.py</span>             # Django management script
└── 📄 <span style="color: var(--vscode-textLink-foreground, #2563eb);">requirements.txt</span>      # Python dependencies
</div>

<div style="display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 15px;">
  <div style="flex: 1; min-width: 300px; background-color: var(--vscode-editor-background, #f5f5f5); border-radius: 6px; padding: 15px; color: var(--vscode-editor-foreground, #333);">
    <h4 style="margin-top: 0; margin-bottom: 10px; color: var(--vscode-editor-foreground, #333); border-bottom: 1px solid var(--vscode-panel-border, #ddd); padding-bottom: 5px;">
      🔐 Security Features
    </h4>
    <ul style="padding-left: 20px; margin-top: 10px; margin-bottom: 0;">
      <li><strong>CSRF Protection</strong>: Cross-site request forgery prevention</li>
      <li><strong>Password Validation</strong>: Strong password enforcement</li>
      <li><strong>Role-based Access</strong>: Permission controls via custom decorators</li>
      <li><strong>Session Security</strong>: Secure cookie handling and timeout</li>
      <li><strong>XSS Prevention</strong>: Template escaping and content sanitization</li>
    </ul>
  </div>

  <div style="flex: 1; min-width: 300px; background-color: var(--vscode-editor-background, #f5f5f5); border-radius: 6px; padding: 15px; color: var(--vscode-editor-foreground, #333);">
    <h4 style="margin-top: 0; margin-bottom: 10px; color: var(--vscode-editor-foreground, #333); border-bottom: 1px solid var(--vscode-panel-border, #ddd); padding-bottom: 5px;">
      🔌 Middleware & Extensions
    </h4>
    <ul style="padding-left: 20px; margin-top: 10px; margin-bottom: 0;">
      <li><strong>Security Middleware</strong>: HTTPS and security headers</li>
      <li><strong>Authentication Middleware</strong>: User request association</li>
      <li><strong>Session Middleware</strong>: User state management</li>
      <li><strong>CKEditor</strong>: Rich text content creation</li>
      <li><strong>Browser Reload</strong>: Development auto-refresh</li>
      <li><strong>Tailwind CSS</strong>: Utility-first styling framework</li>
    </ul>
  </div>
</div>

<div style="display: flex; flex-wrap: wrap; gap: 15px;">
  <div style="flex: 1; min-width: 300px; background-color: var(--vscode-editor-background, #f5f5f5); border-radius: 6px; padding: 15px; color: var(--vscode-editor-foreground, #333);">
    <h4 style="margin-top: 0; margin-bottom: 10px; color: var(--vscode-editor-foreground, #333); border-bottom: 1px solid var(--vscode-panel-border, #ddd); padding-bottom: 5px;">
      📦 Database Structure
    </h4>
    <ul style="padding-left: 20px; margin-top: 10px; margin-bottom: 0;">
      <li><strong>User Models</strong>: Extended user profiles with custom fields</li>
      <li><strong>Product Models</strong>: Specialized models for each component type</li>
      <li><strong>E-commerce Models</strong>: Cart, order, and payment processing</li>
      <li><strong>Content Models</strong>: Blog posts, categories, and comments</li>
      <li><strong>Builder Models</strong>: PC configurations and compatibility rules</li>
      <li><strong>Support Models</strong>: Customer tickets and interactions</li>
    </ul>
  </div>

  <div style="flex: 1; min-width: 300px; background-color: var(--vscode-editor-background, #f5f5f5); border-radius: 6px; padding: 15px; color: var(--vscode-editor-foreground, #333);">
    <h4 style="margin-top: 0; margin-bottom: 10px; color: var(--vscode-editor-foreground, #333); border-bottom: 1px solid var(--vscode-panel-border, #ddd); padding-bottom: 5px;">
      🌐 URL Structure
    </h4>
    <ul style="padding-left: 20px; margin-top: 10px; margin-bottom: 0; font-family: monospace; font-size: 14px;">
      <li><code>/</code> - Homepage and product catalog</li>
      <li><code>/auth/</code> - User authentication and management</li>
      <li><code>/cart/</code> - Shopping cart and checkout</li>
      <li><code>/pc-builder/</code> - PC configuration tool</li>
      <li><code>/compare/</code> - Product comparison system</li>
      <li><code>/wishlist/</code> - User wishlists management</li>
      <li><code>/blog/</code> - Blog content and articles</li>
      <li><code>/admin/</code> - Staff administration interface</li>
    </ul>
  </div>
</div>

<h3 style="color: var(--vscode-editor-foreground, #333); margin-top: 20px; margin-bottom: 15px;">Application Components</h3>

<div style="display: flex; flex-wrap: wrap; gap: 15px; margin-top: 15px;">
  <!-- ProductsApp -->
  <div style="flex: 1; min-width: 300px; border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 6px; padding: 15px;">
    <h4 style="color: var(--vscode-editor-foreground, #333); margin-top: 0; border-bottom: 1px solid var(--vscode-panel-border, #ddd); padding-bottom: 8px;">
      ProductsApp - Product Catalog
    </h4>
    <ul style="padding-left: 20px; margin-bottom: 0; color: var(--vscode-editor-foreground, #333);">
      <li><strong>Models</strong>: CPU, GPU, Motherboard, RAM, SSD, HDD, Cooler, PSU, Casing, Monitor, Keyboard, Mouse, Headphone</li>
      <li><strong>Features</strong>: Specifications management, pricing, inventory, categorization</li>
      <li><strong>Image Management</strong>: Multiple product images with optimized storage</li>
      <li><strong>Search</strong>: Advanced filtering by specifications and price ranges</li>
      <li><strong>Views</strong>: Catalog browsing, product details, featured products</li>
      <li><strong>API</strong>: Product data endpoints for PC Builder and comparison tools</li>
    </ul>
  </div>

  <!-- AuthApp -->
  <div style="flex: 1; min-width: 300px; border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 6px; padding: 15px;">
    <h4 style="color: var(--vscode-editor-foreground, #333); margin-top: 0; border-bottom: 1px solid var(--vscode-panel-border, #ddd); padding-bottom: 8px;">
      AuthApp - Authentication & Support
    </h4>
    <ul style="padding-left: 20px; margin-bottom: 0; color: var(--vscode-editor-foreground, #333);">
      <li><strong>User Management</strong>: Extended user profiles with role-based permissions</li>
      <li><strong>Customer Support</strong>: Ticket system with categories and response tracking</li>
      <li><strong>Security</strong>: Secure authentication with password validation</li>
      <li><strong>Roles</strong>: Admin, Staff, Content Manager, Blogger, Customer, Guest</li>
      <li><strong>Email Integration</strong>: Account verification and password reset</li>
      <li><strong>Decorators</strong>: Custom access control for role-specific features</li>
    </ul>
  </div>
</div>

<div style="display: flex; flex-wrap: wrap; gap: 15px; margin-top: 15px;">
  <!-- CartApp -->
  <div style="flex: 1; min-width: 300px; border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 6px; padding: 15px;">
    <h4 style="color: var(--vscode-editor-foreground, #333); margin-top: 0; border-bottom: 1px solid var(--vscode-panel-border, #ddd); padding-bottom: 8px;">
      CartApp - Shopping & Orders
    </h4>
    <ul style="padding-left: 20px; margin-bottom: 0; color: var(--vscode-editor-foreground, #333);">
      <li><strong>Cart Management</strong>: Session-based and user-linked shopping carts</li>
      <li><strong>Order Processing</strong>: Complete order lifecycle with status tracking</li>
      <li><strong>Shipping</strong>: Address management and shipping calculations</li>
      <li><strong>Payment Integration</strong>: Ready for multiple payment gateway integration</li>
      <li><strong>Context Processors</strong>: Global cart data for all templates</li>
      <li><strong>Order History</strong>: User-accessible purchase records and status</li>
    </ul>
  </div>

  <!-- PCBuilderApp -->
  <div style="flex: 1; min-width: 300px; border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 6px; padding: 15px;">
    <h4 style="color: var(--vscode-editor-foreground, #333); margin-top: 0; border-bottom: 1px solid var(--vscode-panel-border, #ddd); padding-bottom: 8px;">
      PCBuilderApp - PC Configuration
    </h4>
    <ul style="padding-left: 20px; margin-bottom: 0; color: var(--vscode-editor-foreground, #333);">
      <li><strong>Component Selection</strong>: Interactive PC building interface with filtering</li>
      <li><strong>Compatibility Checking</strong>: Real-time validation of component combinations</li>
      <li><strong>Build Management</strong>: Save, share, and manage PC configurations</li>
      <li><strong>Power Calculation</strong>: Estimate total system power requirements</li>
      <li><strong>Performance Metrics</strong>: Expected performance scores for gaming and tasks</li>
      <li><strong>Cart Integration</strong>: One-click add all components to cart</li>
    </ul>
  </div>
</div>

<div style="display: flex; flex-wrap: wrap; gap: 15px; margin-top: 15px;">
  <!-- CompareApp -->
  <div style="flex: 1; min-width: 300px; border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 6px; padding: 15px;">
    <h4 style="color: var(--vscode-editor-foreground, #333); margin-top: 0; border-bottom: 1px solid var(--vscode-panel-border, #ddd); padding-bottom: 8px;">
      CompareApp - Product Comparison
    </h4>
    <ul style="padding-left: 20px; margin-bottom: 0; color: var(--vscode-editor-foreground, #333);">
      <li><strong>Multi-Product Comparison</strong>: Compare up to 4 products side-by-side</li>
      <li><strong>Category-Specific Views</strong>: Tailored comparison views for each product type</li>
      <li><strong>Comparison History</strong>: Track previously compared products</li>
      <li><strong>Highlight Differences</strong>: Visual indicators for key specification differences</li>
      <li><strong>Context Processors</strong>: Global comparison data for all templates</li>
      <li><strong>Export Options</strong>: Save comparison data as PDF or share via link</li>
    </ul>
  </div>

  <!-- WishlistApp -->
  <div style="flex: 1; min-width: 300px; border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 6px; padding: 15px;">
    <h4 style="color: var(--vscode-editor-foreground, #333); margin-top: 0; border-bottom: 1px solid var(--vscode-panel-border, #ddd); padding-bottom: 8px;">
      WishlistApp - User Favorites
    </h4>
    <ul style="padding-left: 20px; margin-bottom: 0; color: var(--vscode-editor-foreground, #333);">
      <li><strong>Wishlist Management</strong>: Save products for future purchase</li>
      <li><strong>Multiple Lists</strong>: Create and organize multiple themed wishlists</li>
      <li><strong>Sharing</strong>: Share wishlists with friends and family</li>
      <li><strong>Stock Notifications</strong>: Alert users when wishlist items are available</li>
      <li><strong>Price Tracking</strong>: Monitor price changes on wishlist items</li>
      <li><strong>Context Processors</strong>: Global wishlist data for all templates</li>
    </ul>
  </div>
</div>

<div style="display: flex; flex-wrap: wrap; gap: 15px; margin-top: 15px;">
  <!-- BlogApp -->
  <div style="flex: 1; min-width: 300px; border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 6px; padding: 15px;">
    <h4 style="color: var(--vscode-editor-foreground, #333); margin-top: 0; border-bottom: 1px solid var(--vscode-panel-border, #ddd); padding-bottom: 8px;">
      BlogApp - Content Management
    </h4>
    <ul style="padding-left: 20px; margin-bottom: 0; color: var(--vscode-editor-foreground, #333);">
      <li><strong>Rich Text Editor</strong>: CKEditor integration for content creation</li>
      <li><strong>SEO Features</strong>: URL slugs, meta tags, and search optimization</li>
      <li><strong>Category System</strong>: Organize content with categories and tags</li>
      <li><strong>Comment System</strong>: User engagement through comments</li>
      <li><strong>Author Management</strong>: Content attribution and writer profiles</li>
      <li><strong>Content Types</strong>: Blog posts, tutorials, product reviews, news updates</li>
    </ul>
  </div>

  <!-- TechReform Core -->
  <div style="flex: 1; min-width: 300px; border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 6px; padding: 15px;">
    <h4 style="color: var(--vscode-editor-foreground, #333); margin-top: 0; border-bottom: 1px solid var(--vscode-panel-border, #ddd); padding-bottom: 8px;">
      TechReform Core - Project Foundation
    </h4>
    <ul style="padding-left: 20px; margin-bottom: 0; color: var(--vscode-editor-foreground, #333);">
      <li><strong>Settings Configuration</strong>: Environment-specific application settings</li>
      <li><strong>URL Routing</strong>: Central request dispatcher to application views</li>
      <li><strong>Middleware Stack</strong>: Request/response processing pipeline</li>
      <li><strong>Template Structure</strong>: Base templates and inheritance patterns</li>
      <li><strong>Static Asset Management</strong>: CSS, JavaScript, and media handling</li>
      <li><strong>Deployment Configuration</strong>: WSGI/ASGI setup for production</li>
    </ul>
  </div>
</div>
</div>

## 🚀 Quick Start

<div style="border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 8px; padding: 20px; margin-bottom: 20px;">
<h3 style="margin-top: 0; color: var(--vscode-editor-foreground, #333);">📋 Prerequisites</h3>

<p style="color: var(--vscode-editor-foreground, #333);">Before you begin, ensure you have the following installed:</p>

<table style="width: 100%; border-collapse: collapse;">
<tr style="background-color: var(--vscode-editor-selectionBackground, rgba(0, 120, 215, 0.1));">
<th style="padding: 10px; text-align: left; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">Requirement</th>
<th style="padding: 10px; text-align: left; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">Version</th>
<th style="padding: 10px; text-align: left; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">Purpose</th>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">🐍 <strong>Python</strong></td>
<td style="padding: 10px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">3.8+</td>
<td style="padding: 10px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">Backend runtime</td>
</tr>
<tr style="background-color: var(--vscode-editor-selectionBackground, rgba(0, 120, 215, 0.1));">
<td style="padding: 10px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">📦 <strong>Node.js</strong></td>
<td style="padding: 10px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">16+</td>
<td style="padding: 10px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">Frontend tooling</td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">📥 <strong>npm</strong></td>
<td style="padding: 10px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">8+</td>
<td style="padding: 10px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">Package management</td>
</tr>
<tr style="background-color: var(--vscode-editor-selectionBackground, rgba(0, 120, 215, 0.1));">
<td style="padding: 10px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">🔄 <strong>Git</strong></td>
<td style="padding: 10px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">Latest</td>
<td style="padding: 10px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">Version control</td>
</tr>
</table>

<h3 style="margin-top: 20px; color: var(--vscode-editor-foreground, #333);">⚡ Installation</h3>

<div style="border: 1px solid var(--vscode-panel-border, #ddd); background-color: var(--vscode-editor-background, #f5f5f5); border-radius: 8px; padding: 15px; margin-bottom: 15px;">
<h4 style="margin-top: 0; color: var(--vscode-editor-foreground, #333);">1. 📥 Clone the Repository</h4>
<pre style="background-color: var(--vscode-dropdown-background, #1e293b); color: var(--vscode-dropdown-foreground, #e2e8f0); padding: 10px; border-radius: 5px; overflow-x: auto;"><code>git clone https://github.com/SharifdotG/TechReform-BD-2.git
cd TechReform-BD-2</code></pre>
</div>

<div style="border: 1px solid var(--vscode-panel-border, #ddd); background-color: var(--vscode-editor-background, #f5f5f5); border-radius: 8px; padding: 15px; margin-bottom: 15px;">
<h4 style="margin-top: 0; color: var(--vscode-editor-foreground, #333);">2. 🐍 Create Virtual Environment</h4>

<p style="color: var(--vscode-editor-foreground, #333);"><strong>Windows (PowerShell):</strong></p>
<pre style="background-color: var(--vscode-dropdown-background, #1e293b); color: var(--vscode-dropdown-foreground, #e2e8f0); padding: 10px; border-radius: 5px; overflow-x: auto;"><code>pip install virtualenv
python -m venv venv
venv\Scripts\Activate.ps1</code></pre>

<p style="color: var(--vscode-editor-foreground, #333);"><strong>macOS/Linux:</strong></p>
<pre style="background-color: var(--vscode-dropdown-background, #1e293b); color: var(--vscode-dropdown-foreground, #e2e8f0); padding: 10px; border-radius: 5px; overflow-x: auto;"><code>pip install virtualenv
python -m venv venv
source venv/bin/activate</code></pre>
</div>

<div style="border: 1px solid var(--vscode-panel-border, #ddd); background-color: var(--vscode-editor-background, #f5f5f5); border-radius: 8px; padding: 15px; margin-bottom: 15px;">
<h4 style="margin-top: 0; color: var(--vscode-editor-foreground, #333);">3. 📦 Install Python Dependencies</h4>
<pre style="background-color: var(--vscode-dropdown-background, #1e293b); color: var(--vscode-dropdown-foreground, #e2e8f0); padding: 10px; border-radius: 5px; overflow-x: auto;"><code>pip install -r requirements.txt</code></pre>
</div>

<div style="border: 1px solid var(--vscode-panel-border, #ddd); background-color: var(--vscode-editor-background, #f5f5f5); border-radius: 8px; padding: 15px; margin-bottom: 15px;">
<h4 style="margin-top: 0; color: var(--vscode-editor-foreground, #333);">4. 🎨 Install Node.js Dependencies (for Tailwind CSS)</h4>
<pre style="background-color: var(--vscode-dropdown-background, #1e293b); color: var(--vscode-dropdown-foreground, #e2e8f0); padding: 10px; border-radius: 5px; overflow-x: auto;"><code>cd theme/static_src
npm install
cd ../..</code></pre>
</div>

<div style="border: 1px solid var(--vscode-panel-border, #ddd); background-color: var(--vscode-editor-background, #f5f5f5); border-radius: 8px; padding: 15px; margin-bottom: 15px;">
<h4 style="margin-top: 0; color: var(--vscode-editor-foreground, #333);">5. ⚙️ Environment Setup (Optional)</h4>
<pre style="background-color: var(--vscode-dropdown-background, #1e293b); color: var(--vscode-dropdown-foreground, #e2e8f0); padding: 10px; border-radius: 5px; overflow-x: auto;"><code># Create .env file
cp .env.example .env
# Edit .env with your configuration</code></pre>
</div>

<div style="border: 1px solid var(--vscode-panel-border, #ddd); background-color: var(--vscode-editor-background, #f5f5f5); border-radius: 8px; padding: 15px; margin-bottom: 15px;">
<h4 style="margin-top: 0; color: var(--vscode-editor-foreground, #333);">6. 🗄️ Database Setup</h4>
<pre style="background-color: var(--vscode-dropdown-background, #1e293b); color: var(--vscode-dropdown-foreground, #e2e8f0); padding: 10px; border-radius: 5px; overflow-x: auto;"><code>python manage.py makemigrations
python manage.py migrate</code></pre>
</div>

<div style="border: 1px solid var(--vscode-panel-border, #ddd); background-color: var(--vscode-editor-background, #f5f5f5); border-radius: 8px; padding: 15px; margin-bottom: 15px;">
<h4 style="margin-top: 0; color: var(--vscode-editor-foreground, #333);">7. 👤 Create Superuser</h4>
<pre style="background-color: var(--vscode-dropdown-background, #1e293b); color: var(--vscode-dropdown-foreground, #e2e8f0); padding: 10px; border-radius: 5px; overflow-x: auto;"><code>python manage.py createsuperuser</code></pre>
</div>

<div style="border: 1px solid var(--vscode-panel-border, #ddd); background-color: var(--vscode-editor-background, #f5f5f5); border-radius: 8px; padding: 15px; margin-bottom: 15px;">
<h4 style="margin-top: 0; color: var(--vscode-editor-foreground, #333);">8. 📂 Collect Static Files</h4>
<pre style="background-color: var(--vscode-dropdown-background, #1e293b); color: var(--vscode-dropdown-foreground, #e2e8f0); padding: 10px; border-radius: 5px; overflow-x: auto;"><code>python manage.py collectstatic</code></pre>
</div>

<div style="border: 1px solid var(--vscode-panel-border, #ddd); background-color: var(--vscode-editor-background, #f5f5f5); border-radius: 8px; padding: 15px; margin-bottom: 15px;">
<h4 style="margin-top: 0; color: var(--vscode-editor-foreground, #333);">9. 🏃 Run Development Server</h4>
<p style="color: var(--vscode-editor-foreground, #333);"><strong>Terminal 1</strong> - Django Development Server:</p>
<pre style="background-color: var(--vscode-dropdown-background, #1e293b); color: var(--vscode-dropdown-foreground, #e2e8f0); padding: 10px; border-radius: 5px; overflow-x: auto;"><code>python manage.py runserver</code></pre>

<p style="color: var(--vscode-editor-foreground, #333);"><strong>Terminal 2</strong> - Tailwind CSS Compilation:</p>
<pre style="background-color: var(--vscode-dropdown-background, #1e293b); color: var(--vscode-dropdown-foreground, #e2e8f0); padding: 10px; border-radius: 5px; overflow-x: auto;"><code>python manage.py tailwind start</code></pre>
</div>

<div style="border: 1px solid var(--vscode-panel-border, #ddd); background-color: var(--vscode-editor-background, #f5f5f5); border-radius: 8px; padding: 15px; margin-bottom: 15px;">
<h4 style="margin-top: 0; color: var(--vscode-editor-foreground, #333);">10. 🌐 Access the Application</h4>
<table style="width: 100%; border-collapse: collapse;">
<tr style="background-color: var(--vscode-editor-selectionBackground, rgba(0, 120, 215, 0.1));">
<th style="padding: 10px; text-align: left; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">Service</th>
<th style="padding: 10px; text-align: left; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">URL</th>
<th style="padding: 10px; text-align: left; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">Description</th>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">🏠 <strong>Main Site</strong></td>
<td style="padding: 10px; border: 1px solid var(--vscode-panel-border, #ddd);"><a href="http://localhost:8000" style="color: var(--vscode-textLink-foreground, #2563eb); text-decoration: none;">http://localhost:8000</a></td>
<td style="padding: 10px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">Main application interface</td>
</tr>
<tr style="background-color: var(--vscode-editor-selectionBackground, rgba(0, 120, 215, 0.1));">
<td style="padding: 10px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">⚙️ <strong>Admin Panel</strong></td>
<td style="padding: 10px; border: 1px solid var(--vscode-panel-border, #ddd);"><a href="http://localhost:8000/admin" style="color: var(--vscode-textLink-foreground, #2563eb); text-decoration: none;">http://localhost:8000/admin</a></td>
<td style="padding: 10px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">Django admin interface</td>
</tr>
</table>
</div>
</div>

## 🛠️ Development

### Code Quality

- **PEP 8**: Python code follows PEP 8 style guidelines
- **Ruff**: Ultra-fast Python linter and code formatter
- **Type Hints**: Type annotations for better code maintainability
- **Pre-commit Hooks**: Automated code quality checks

### Database Management

```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (development only)
python manage.py flush

# Load sample data
python manage.py loaddata fixtures/sample_data.json
```

### Code Formatting and Linting

```bash
# Format code with Ruff
ruff format .

# Check and fix linting issues
ruff check --fix .

# Check code without making changes
ruff check .

# Run type checking (if using mypy)
mypy .
```

### Tailwind CSS Development

```bash
# Start Tailwind CSS watch mode
python manage.py tailwind start

# Build for production
python manage.py tailwind build

# Install Tailwind dependencies
python manage.py tailwind install
```

## 📦 Dependencies

### 🔧 Core Dependencies

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **Django** | 5.1.4 | Web framework with MVT architecture | [📖 Docs](https://www.djangoproject.com/) |
| **Pillow** | 11.0.0 | Image processing for products and avatars | [📖 Docs](https://pillow.readthedocs.io/) |
| **django-ckeditor** | 6.7.1 | Rich text editor for blog content | [📖 Docs](https://django-ckeditor.readthedocs.io/) |
| **django-tailwind** | 3.8.0 | Tailwind CSS integration | [📖 Docs](https://django-tailwind.readthedocs.io/) |
| **python-slugify** | 8.0.4 | URL-friendly slug generation for SEO | [📖 Docs](https://github.com/un33k/python-slugify) |
| **requests** | 2.32.3 | HTTP client for external API integrations | [📖 Docs](https://requests.readthedocs.io/) |
| **markdown-it-py** | 3.0.0 | Markdown rendering for blog posts | [📖 Docs](https://markdown-it-py.readthedocs.io/) |

### 🛠️ Development Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| **django-browser-reload** | 1.18.0 | Auto-reload during development |
| **django-extensions** | 3.2.3 | Additional management commands |
| **django-environ** | 0.11.2 | Environment variable management |

### 🚀 Production Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| **gunicorn** | 21.2.0 | WSGI HTTP Server |
| **whitenoise** | 6.6.0 | Static file serving |
| **psycopg2-binary** | 2.9.10 | PostgreSQL adapter |
| **redis** | 5.0.1 | Caching and session storage |
| **celery** | 5.3.4 | Asynchronous task processing |

### 🔐 Authentication

The API uses Django's built-in session authentication and supports:

- 🍪 **Session-based authentication** for web interface
- 🎫 **Token-based authentication** for mobile apps
- 🔑 **JWT authentication** for SPA applications

## 🧪 Testing

<div style="border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 8px; padding: 20px; margin-bottom: 20px;">
<h3 style="margin-top: 0; color: var(--vscode-editor-foreground, #333);">📊 Test Coverage</h3>

<table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
<tr style="background-color: var(--vscode-editor-selectionBackground, rgba(0, 120, 215, 0.1));">
<th style="padding: 12px; text-align: left; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">Test Type</th>
<th style="padding: 12px; text-align: left; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">Coverage</th>
<th style="padding: 12px; text-align: left; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">Description</th>
</tr>
<tr>
<td style="padding: 12px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);"><span style="font-weight: bold;">✅ Unit Tests</span></td>
<td style="padding: 12px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">Individual components</td>
<td style="padding: 12px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">Testing models, views, and forms in isolation</td>
</tr>
<tr style="background-color: var(--vscode-editor-selectionBackground, rgba(0, 120, 215, 0.1));">
<td style="padding: 12px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);"><span style="font-weight: bold;">🔄 Integration Tests</span></td>
<td style="padding: 12px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">End-to-end workflows</td>
<td style="padding: 12px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">Cart-to-checkout, PC builder functionality</td>
</tr>
<tr>
<td style="padding: 12px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);"><span style="font-weight: bold;">🔐 Authentication Tests</span></td>
<td style="padding: 12px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">User management</td>
<td style="padding: 12px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">Registration, login, role-based access</td>
</tr>
<tr style="background-color: var(--vscode-editor-selectionBackground, rgba(0, 120, 215, 0.1));">
<td style="padding: 12px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);"><span style="font-weight: bold;">🎯 Functional Tests</span></td>
<td style="padding: 12px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">User journeys</td>
<td style="padding: 12px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">Testing major features across the platform</td>
</tr>
<tr>
<td style="padding: 12px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);"><span style="font-weight: bold;">⚡ Performance Tests</span></td>
<td style="padding: 12px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">Load testing</td>
<td style="padding: 12px; border: 1px solid var(--vscode-panel-border, #ddd); color: var(--vscode-editor-foreground, #333);">High-traffic scenario validation</td>
</tr>
</table>

<h3 style="color: var(--vscode-editor-foreground, #333);">📁 Test Files Structure</h3>

<p style="color: var(--vscode-editor-foreground, #333);">The project includes comprehensive test suites organized by functionality:</p>

<div style="background-color: var(--vscode-editor-background, #f5f5f5); border-radius: 8px; padding: 15px; margin-bottom: 20px; font-family: monospace; white-space: pre; overflow-x: auto; color: var(--vscode-editor-foreground, #333);">
tests/
├── 🛒 <span style="font-weight: bold;">Cart_Checkout.py</span>           # E-commerce workflow tests
├── 📝 <span style="font-weight: bold;">Create_Blog.py</span>             # Blog functionality tests
├── 🖥️ <span style="font-weight: bold;">PC_Builder.py</span>              # PC builder logic tests
├── 🔐 <span style="font-weight: bold;">SignUp_Login.py</span>            # Authentication flow tests
├── 👥 <span style="font-weight: bold;">User_Management.py</span>         # User profile and management tests
└── 📋 <span style="font-weight: bold;">*_report.html</span>             # HTML test reports with coverage
</div>

<h3 style="color: var(--vscode-editor-foreground, #333);">🏃 Running Tests</h3>

<div style="border: 1px solid var(--vscode-panel-border, #ddd); background-color: var(--vscode-editor-background, #f5f5f5); border-radius: 8px; padding: 15px; margin-bottom: 15px;">
<h4 style="margin-top: 0; color: var(--vscode-editor-foreground, #333);">Run All Tests</h4>
<pre style="background-color: var(--vscode-dropdown-background, #1e293b); color: var(--vscode-dropdown-foreground, #e2e8f0); padding: 10px; border-radius: 5px; overflow-x: auto;"><code>python manage.py test</code></pre>
</div>

<div style="border: 1px solid var(--vscode-panel-border, #ddd); background-color: var(--vscode-editor-background, #f5f5f5); border-radius: 8px; padding: 15px; margin-bottom: 15px;">
<h4 style="margin-top: 0; color: var(--vscode-editor-foreground, #333);">Run Specific Test File</h4>
<pre style="background-color: var(--vscode-dropdown-background, #1e293b); color: var(--vscode-dropdown-foreground, #e2e8f0); padding: 10px; border-radius: 5px; overflow-x: auto;"><code>python manage.py test tests.Cart_Checkout</code></pre>
</div>

<div style="border: 1px solid var(--vscode-panel-border, #ddd); background-color: var(--vscode-editor-background, #f5f5f5); border-radius: 8px; padding: 15px; margin-bottom: 15px;">
<h4 style="margin-top: 0; color: var(--vscode-editor-foreground, #333);">Run with Coverage Report</h4>
<pre style="background-color: var(--vscode-dropdown-background, #1e293b); color: var(--vscode-dropdown-foreground, #e2e8f0); padding: 10px; border-radius: 5px; overflow-x: auto;"><code>coverage run --source='.' manage.py test
coverage report
coverage html</code></pre>
</div>
</div>

## 🤝 Contributing

We welcome contributions to **TechReform BD 2**! Here's how you can help make this project even better:

### 🚀 Development Workflow

1. 🍴 **Fork the repository**
2. 🌿 **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. ✨ **Make your changes and add tests**
4. ✅ **Ensure tests pass**: `python manage.py test`
5. 🎨 **Format and lint code**: `ruff format . && ruff check --fix .`
6. 📝 **Commit changes**: `git commit -m 'Add amazing feature'`
7. 🚀 **Push to branch**: `git push origin feature/amazing-feature`
8. 📋 **Open a Pull Request**

### 📏 Code Standards

| Standard | Tool/Guideline | Purpose |
|----------|---------------|---------|
| 🐍 **Python Style** | PEP 8 + Ruff | Consistent code formatting |
| 📝 **Commit Messages** | Conventional Commits | Clear change tracking |
| 🧪 **Testing** | Django TestCase | Quality assurance |
| 📖 **Documentation** | Markdown + Docstrings | Code understanding |
| 🔄 **Compatibility** | Semantic Versioning | Backward compatibility |

### 🔄 Pull Request Process

- [ ] ✍️ Update README.md with details of changes if needed
- [ ] 📦 Update requirements.txt if you add dependencies
- [ ] 🔢 Increase version numbers following [Semantic Versioning](https://semver.org/)
- [ ] ✅ Ensure CI/CD pipeline passes
- [ ] 👀 Request review from maintainers

### 🎯 Contribution Areas

We especially welcome contributions in these areas:

- 🐛 **Bug Fixes**: Report and fix issues
- ✨ **New Features**: Implement feature requests
- 📖 **Documentation**: Improve project documentation
- 🧪 **Testing**: Add test coverage
- 🎨 **UI/UX**: Enhance user interface and experience
- ⚡ **Performance**: Optimize application performance

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Django Team**: For the excellent web framework
- **Tailwind CSS**: For the utility-first CSS framework
- **CKEditor**: For the rich text editing capabilities
- **Contributors**: All developers who contributed to this project

## 📞 Support

### Getting Help

- **Issues**: Report bugs and request features on [GitHub Issues](../../issues)
- **Discussions**: Join community discussions on [GitHub Discussions](../../discussions)

---

## 🗺️ Roadmap

<div style="border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 10px; padding: 20px; margin-bottom: 30px;">
<h3 style="color: var(--vscode-editor-foreground, #333); margin-top: 0;">Version 2.0 (Upcoming)</h3>

<div style="display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0;">
  <div style="background-color: var(--vscode-editor-background, #f5f5f5); border-left: 4px solid var(--vscode-symbolIcon-colorCustomization, #059669); border-radius: 5px; padding: 10px 15px; flex: 1; min-width: 250px;">
    <h4 style="margin: 0 0 10px 0; color: var(--vscode-editor-foreground, #333);">🤖 AI-Powered PC Builder</h4>
    <p style="margin: 0; font-size: 14px; color: var(--vscode-editor-foreground, #333);">Advanced system with personalized recommendations based on usage patterns, budget constraints, and performance requirements</p>
  </div>

  <div style="background-color: var(--vscode-editor-background, #f5f5f5); border-left: 4px solid var(--vscode-symbolIcon-colorCustomization, #0369a1); border-radius: 5px; padding: 10px 15px; flex: 1; min-width: 250px;">
    <h4 style="margin: 0 0 10px 0; color: var(--vscode-editor-foreground, #333);">📊 Real-time Price Comparison</h4>
    <p style="margin: 0; font-size: 14px; color: var(--vscode-editor-foreground, #333);">Live comparison with multiple local vendors to ensure maximum transparency and competitive pricing</p>
  </div>
</div>

<div style="display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0;">
  <div style="background-color: var(--vscode-editor-background, #f5f5f5); border-left: 4px solid var(--vscode-symbolIcon-colorCustomization, #7c3aed); border-radius: 5px; padding: 10px 15px; flex: 1; min-width: 250px;">
    <h4 style="margin: 0 0 10px 0; color: var(--vscode-editor-foreground, #333);">⭐ Enhanced User Reviews</h4>
    <p style="margin: 0; font-size: 14px; color: var(--vscode-editor-foreground, #333);">Comprehensive ratings system with verified purchase badges, photo uploads, and detailed product experiences</p>
  </div>

  <div style="background-color: var(--vscode-editor-background, #f5f5f5); border-left: 4px solid var(--vscode-symbolIcon-colorCustomization, #c026d3); border-radius: 5px; padding: 10px 15px; flex: 1; min-width: 250px;">
    <h4 style="margin: 0 0 10px 0; color: var(--vscode-editor-foreground, #333);">💬 Community Forum</h4>
    <p style="margin: 0; font-size: 14px; color: var(--vscode-editor-foreground, #333);">User discussion platform for tech advice, build showcases, and community support</p>
  </div>
</div>

<div style="display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0;">
  <div style="background-color: var(--vscode-editor-background, #f5f5f5); border-left: 4px solid var(--vscode-symbolIcon-colorCustomization, #db2777); border-radius: 5px; padding: 10px 15px; flex: 1; min-width: 250px;">
    <h4 style="margin: 0 0 10px 0; color: var(--vscode-editor-foreground, #333);">📱 Mobile Applications</h4>
    <p style="margin: 0; font-size: 14px; color: var(--vscode-editor-foreground, #333);">Native iOS and Android apps for enhanced mobile experience with push notifications</p>
  </div>

  <div style="background-color: var(--vscode-editor-background, #f5f5f5); border-left: 4px solid var(--vscode-symbolIcon-colorCustomization, #ea580c); border-radius: 5px; padding: 10px 15px; flex: 1; min-width: 250px;">
    <h4 style="margin: 0 0 10px 0; color: var(--vscode-editor-foreground, #333);">🚚 Delivery Services Integration</h4>
    <p style="margin: 0; font-size: 14px; color: var(--vscode-editor-foreground, #333);">Connection with local delivery services APIs for real-time tracking and faster delivery</p>
  </div>
</div>

<h3 style="color: var(--vscode-editor-foreground, #333); margin-top: 30px;">Version 2.1 (Future)</h3>

<div style="display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0;">
  <div style="background-color: var(--vscode-editor-background, #f5f5f5); border-left: 4px solid var(--vscode-symbolIcon-colorCustomization, #2563eb); border-radius: 5px; padding: 10px 15px; flex: 1; min-width: 250px;">
    <h4 style="margin: 0 0 10px 0; color: var(--vscode-editor-foreground, #333);">🧠 AI Product Recommendations</h4>
    <p style="margin: 0; font-size: 14px; color: var(--vscode-editor-foreground, #333);">Smart suggestions based on user browsing behavior and purchase history</p>
  </div>

  <div style="background-color: var(--vscode-editor-background, #f5f5f5); border-left: 4px solid var(--vscode-symbolIcon-colorCustomization, #4f46e5); border-radius: 5px; padding: 10px 15px; flex: 1; min-width: 250px;">
    <h4 style="margin: 0 0 10px 0; color: var(--vscode-editor-foreground, #333);">🇧🇩 Bengali Localization</h4>
    <p style="margin: 0; font-size: 14px; color: var(--vscode-editor-foreground, #333);">Complete language support for Bengali to serve local users better</p>
  </div>
</div>

<div style="display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0;">
  <div style="background-color: var(--vscode-editor-background, #f5f5f5); border-left: 4px solid var(--vscode-symbolIcon-colorCustomization, #0891b2); border-radius: 5px; padding: 10px 15px; flex: 1; min-width: 250px;">
    <h4 style="margin: 0 0 10px 0; color: var(--vscode-editor-foreground, #333);">🔍 AR Component Visualization</h4>
    <p style="margin: 0; font-size: 14px; color: var(--vscode-editor-foreground, #333);">Augmented reality features to visualize components in real space</p>
  </div>

  <div style="background-color: var(--vscode-editor-background, #f5f5f5); border-left: 4px solid var(--vscode-symbolIcon-colorCustomization, #9333ea); border-radius: 5px; padding: 10px 15px; flex: 1; min-width: 250px;">
    <h4 style="margin: 0 0 10px 0; color: var(--vscode-editor-foreground, #333);">🎮 Gamification</h4>
    <p style="margin: 0; font-size: 14px; color: var(--vscode-editor-foreground, #333);">Community points, badges, and rewards for active participation</p>
  </div>
</div>

<div style="display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0;">
  <div style="background-color: var(--vscode-editor-background, #f5f5f5); border-left: 4px solid var(--vscode-symbolIcon-colorCustomization, #16a34a); border-radius: 5px; padding: 10px 15px; flex: 1; min-width: 250px;">
    <h4 style="margin: 0 0 10px 0; color: var(--vscode-editor-foreground, #333);">📊 Admin Analytics</h4>
    <p style="margin: 0; font-size: 14px; color: var(--vscode-editor-foreground, #333);">Advanced dashboard with sales insights, user behavior, and inventory management</p>
  </div>

  <div style="background-color: var(--vscode-editor-background, #f5f5f5); border-left: 4px solid var(--vscode-symbolIcon-colorCustomization, #ca8a04); border-radius: 5px; padding: 10px 15px; flex: 1; min-width: 250px;">
    <h4 style="margin: 0 0 10px 0; color: var(--vscode-editor-foreground, #333);">🏪 Multi-vendor Marketplace</h4>
    <p style="margin: 0; font-size: 14px; color: var(--vscode-editor-foreground, #333);">Platform expansion to include vetted vendors with fair pricing commitments</p>
  </div>
</div>
</div>

---

<div style="border: 1px solid var(--vscode-panel-border, #ddd); border-radius: 10px; padding: 30px; margin-top: 30px; background-color: var(--vscode-editor-background, #f5f5f5);">
  <div style="text-align: center;">
    <img src="https://img.shields.io/badge/⚡-Revolutionizing%20Tech%20Shopping-2563eb?style=for-the-badge" alt="Revolutionizing Tech Shopping"/>
  </div>

  <h2 style="margin: 20px 0; color: var(--vscode-editor-foreground, #333); text-align: center;">Join the TechReform Movement</h2>

  <p style="max-width: 800px; margin: 0 auto 20px auto; font-size: 16px; color: var(--vscode-editor-foreground, #333); text-align: center;">
    TechReform BD 2 is more than just an e-commerce platform — it's a movement to transform the PC component market in Bangladesh through fair pricing, transparency, and reliable service. Join us in our mission to make quality technology accessible to everyone.
  </p>

  <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin-top: 20px;">
    <a href="https://github.com/yourusername/TechReform-BD-2/issues" style="text-decoration: none;">
      <div style="background-color: var(--vscode-button-background, #2563eb); color: var(--vscode-button-foreground, white); padding: 10px 20px; border-radius: 5px; font-weight: bold;">
        Report Issues
      </div>
    </a>
    <a href="https://github.com/yourusername/TechReform-BD-2/discussions" style="text-decoration: none;">
      <div style="background-color: var(--vscode-button-secondaryBackground, #059669); color: var(--vscode-button-secondaryForeground, white); padding: 10px 20px; border-radius: 5px; font-weight: bold;">
        Join Discussions
      </div>
    </a>
    <a href="#" style="text-decoration: none;">
      <div style="background-color: var(--vscode-button-background, #7c3aed); color: var(--vscode-button-foreground, white); padding: 10px 20px; border-radius: 5px; font-weight: bold;">
        Subscribe to Updates
      </div>
    </a>
  </div>

  <p style="margin-top: 30px; font-size: 14px; color: var(--vscode-descriptionForeground, #4b5563); text-align: center;">
    <strong>Made with ❤️ by the TechReform BD 2 Team</strong>
  </p>
</div>
