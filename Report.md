# TechReform BD v2 Project Report

## Table of Contents

- [TechReform BD v2 Project Report](#techreform-bd-v2-project-report)
  - [Table of Contents](#table-of-contents)
    - [1. Motivation](#1-motivation)
    - [2. Problem Statement](#2-problem-statement)
    - [3. Objectives \& Project Output](#3-objectives--project-output)
    - [4. Effect on Society](#4-effect-on-society)
    - [5. Requirement Analysis](#5-requirement-analysis)
    - [6. Methodology](#6-methodology)
      - [1. Entity-Relationship (ER) Diagram](#1-entity-relationship-er-diagram)
      - [2. Data Flow Diagram (DFD)](#2-data-flow-diagram-dfd)
      - [3. Activity Diagram](#3-activity-diagram)
      - [4. Sequence Diagrams](#4-sequence-diagrams)
      - [5. Gantt Chart - Project Timeline](#5-gantt-chart---project-timeline)
    - [7. Final Result \& Testing](#7-final-result--testing)
    - [8. Project Management](#8-project-management)
    - [9. Version Control, Finance, Conclusion/Future Work](#9-version-control-finance-conclusionfuture-work)
    - [10. References](#10-references)
    - [Appendix A: Report Quality/Formatting/Referencing](#appendix-a-report-qualityformattingreferencing)
    - [Appendix A: CEP Mapping](#appendix-a-cep-mapping)

### 1. Motivation

The primary motivation behind "TechReform BD v2" is to revolutionize how PC components are purchased in Bangladesh, ensuring users get fair prices and reliable after-sales service. The project aims to create a transparent and user-friendly online platform where technology enthusiasts can buy components at or near Manufacturer's Suggested Retail Price (MSRP). This is achieved by fundamentally altering the traditional supply chain, moving from an often opaque "importer -> multiple intermediaries -> supplier -> user" model to a more direct "manufacturer -> authorized local supplier/TechReform BD -> user" model.

Existing systems and local market practices often involve multiple layers of intermediaries, leading to inflated prices, limited availability of niche products, and challenges in accessing timely and authentic warranty or RMA (Return Merchandise Authorization) services directly from manufacturers. "TechReform BD v2" intends to address these critical pain points.

Two examples of similar or existing systems are:

1. **PCPartPicker (Global):**

    - **Description:** PCPartPicker is a widely recognized platform that allows users to select individual computer components and checks for compatibility issues. It provides price comparisons from various retailers and enables users to share their builds.
    - **Gaps/Improvements addressed by TechReform BD v2:** While PCPartPicker is excellent for compatibility checking and price aggregation from various retailers (often reflecting existing market prices), it doesn't inherently address the issue of inflated prices due to local supply chain inefficiencies or lack of direct manufacturer access. "TechReform BD v2" aims to go a step further by actively working to establish a supply channel that offers components closer to MSRP. It will provide a localized experience for Bangladesh, including local payment gateways and support, with a core focus on fair pricing and direct-from-manufacturer warranty benefits. The integrated blog and e-commerce backend will support this by educating users about fair pricing and warranty processes.

2. **Star Tech (Bangladesh):**
    - **Description:** Star Tech is a prominent e-commerce platform and retailer in Bangladesh that sells a wide range of tech products, including computer components, laptops, and accessories. They have physical stores and an online presence.
    - **Gaps/Improvements addressed by TechReform BD v2:** While established retailers like Star Tech provide accessibility to products, pricing can still be influenced by traditional multi-layered distribution networks. "TechReform BD v2" aims to differentiate itself by focusing on the "manufacturer -> supplier -> user" model to offer more competitive pricing, potentially closer to MSRP. Furthermore, by fostering closer ties with manufacturers or their primary authorized distributors, the project aims to ensure users receive the best possible after-market service, RMA, and warranty support, which can sometimes be a complex process with traditional retail channels. The platform's PC building tools and community features will also empower users with knowledge about fair value and service expectations.

"TechReform BD v2" seeks to fill these gaps by offering a tailored, all-in-one solution that prioritizes fair pricing and reliable after-sales support for the Bangladeshi tech community. By streamlining the supply chain and fostering direct or near-direct relationships with manufacturers, the project aims to empower users with access to components at or near MSRP, along with the assurance of authentic warranty and RMA services. This, combined with e-commerce, a sophisticated PC builder, product comparison tools, and a community blog, will create a truly reformed tech purchasing experience.

### 2. Problem Statement

The core problem "TechReform BD v2" aims to solve is the prevalence of inflated pricing for PC components and the often cumbersome after-sales service experience faced by technology consumers and PC enthusiasts in Bangladesh. The traditional "importer -> multiple intermediaries -> supplier -> user" model frequently results in prices significantly above the Manufacturer's Suggested Retail Price (MSRP). This lack of price transparency and direct access to manufacturer-backed support creates several challenges:

- **Inflated Component Prices:** Consumers often pay a premium for PC components due to multiple layers in the supply chain, each adding their margin. This makes building or upgrading PCs more expensive than it needs to be, limiting accessibility.
- **Difficulty in Accessing Fair Deals:** It is challenging for users to ascertain fair market prices and find components at or near MSRP, leading to a sense of uncertainty and potential overpayment.
- **Complex and Unreliable After-Sales Service/RMA:** Navigating warranty claims and RMA processes can be difficult when dealing with multiple intermediaries. Users may face delays, unclear procedures, or even denial of legitimate claims, diminishing the value of their purchases and trust in brands.
- **Limited Availability of Authentic Products with Full Warranty:** The convoluted supply chain can sometimes lead to a grey market where product authenticity and the validity of manufacturer warranties are questionable.
- **Information Asymmetry:** Users may lack clear information about official warranty terms and procedures directly from manufacturers, relying instead on retailer-specific policies which might not always align.
- **Complexity of Custom PC Building:** While a secondary issue, building a custom PC is made more daunting when coupled with the uncertainty of fair pricing and reliable component sourcing.

"TechReform BD v2" addresses these issues by creating an integrated web application that champions a "manufacturer -> authorized local supplier/TechReform BD -> user" model. This platform will provide a comprehensive product catalog with transparent pricing aiming for MSRP, an intuitive PC builder, robust product comparison, secure user authentication, and streamlined access to manufacturer-backed warranty and RMA information and processes. The goal is to ensure users get the right deal directly and the best possible after-market service.

### 3. Objectives & Project Output

**Objectives:**

The primary objectives of "TechReform BD v2" are:

1. **To establish a platform offering PC components at or near MSRP:** By streamlining the supply chain to a "manufacturer -> authorized local supplier/TechReform BD -> user" model, thereby eliminating unnecessary intermediary costs.
2. **To ensure transparent pricing:** Clearly displaying component prices and how they align with MSRP, empowering users to make informed purchasing decisions.
3. **To facilitate reliable and direct after-sales service:** Providing clear pathways for users to access manufacturer-backed warranty and RMA services.
4. **To develop a user-friendly e-commerce interface:** Enabling users to easily browse, search, and purchase components.
5. **To implement an intuitive Custom PC Builder tool:** Allowing users to select components, check for compatibility, and create custom PC configurations with fairly priced parts.
6. **To provide robust product comparison functionality:** Enabling users to compare specifications, features, and prices (benchmarked against MSRP where possible).
7. **To establish a secure user authentication and profile management system:** For order tracking, saved builds, and managing warranty/RMA information.
8. **To create a blog/community section:** To educate users on fair pricing, consumer rights, warranty processes, and general tech knowledge.
9. **To ensure a responsive and accessible design:** Making the platform usable across various devices.
10. **To offer an administrative backend:** For managing products (with MSRP data), orders, user queries related to RMA/warranty, and content.

**Project Output:**

The project output for "TechReform BD v2" is a **web application**. This will be accessible via standard web browsers, providing a comprehensive online platform focused on fair pricing and reliable support for PC components in Bangladesh.

### 4. Effect on Society

"TechReform BD v2," by focusing on providing PC components at or near MSRP and ensuring reliable manufacturer-backed after-sales service, has the potential to create significant positive effects on society in Bangladesh:

1. **Increased Affordability and Accessibility of Technology:**

    - By reducing the cost of components through a streamlined supply chain, the project can make PC ownership and upgrades more affordable for a wider segment of the population, including students, aspiring professionals, and small businesses.
    - This increased accessibility is crucial for enhancing digital literacy, supporting education, fostering innovation, and enabling greater participation in the digital economy.

2. **Empowerment of Consumers and Fair Market Practices:**

    - Transparent pricing at or near MSRP empowers consumers to make informed decisions and avoid overpaying, fostering a fairer marketplace.
    - Easy access to genuine manufacturer warranties and RMA processes protects consumer rights and builds trust, reducing the frustration and financial loss associated with poor after-sales service.
    - The platform can educate consumers about their rights and what to expect in terms of product quality and support, shifting the power dynamic towards the end-user.

3. **Stimulation of the Local Tech Ecosystem:**

    - While aiming for a direct model, the platform could still partner with _authorized_ local suppliers who adhere to fair pricing and service standards, thus supporting ethical local businesses.
    - A more vibrant and knowledgeable community of PC builders and tech enthusiasts, fostered by the platform, can lead to increased demand for diverse components and potentially spur local innovation in tech-related services.

4. **Enhanced Trust and Reduced E-waste:**

    - Reliable products with dependable warranty support mean components are less likely to be prematurely discarded. Users are more inclined to seek repairs or replacements under warranty, potentially reducing e-waste from faulty or unsupported goods.
    - Promoting genuine products combats the circulation of counterfeit or substandard components, which often have shorter lifespans and contribute more to e-waste.

5. **Fostering a Knowledgeable Consumer Base:**
    - The integrated blog and community features, by focusing on fair pricing, warranty education, and component knowledge, can create a more informed consumer base. This knowledge helps users demand better products and services market-wide.

**Potential Negative Impacts (and Mitigation):**

- **Disruption to Traditional Retailers:** The model might pose a challenge to traditional retailers who rely on multi-layered distribution. [Mitigation: TechReform BD v2 could potentially offer partnership models for established retailers willing to adapt to transparent pricing and service standards, or focus on educating the market to drive broader change.]
- **Logistical Challenges:** Ensuring consistent supply and efficient direct/near-direct shipping across Bangladesh could be a hurdle. [Mitigation: Phased rollout, strategic partnerships with reputable logistics providers.]

Overall, "TechReform BD v2" is envisioned to have a strong positive societal impact by making technology more affordable and reliable, empowering consumers, promoting fair market practices, and contributing to a more knowledgeable and sustainable tech ecosystem in Bangladesh.

### 5. Requirement Analysis

**Basic Requirement (Functional Requirements):**

Based on the project structure (AuthApp, BlogApp, CartApp, CompareApp, PCBuilderApp, ProductsApp, WishlistApp), the functional requirements of "TechReform BD v2" include:

1. **User Authentication & Management:**
    - User registration (e.g., name, email, password).
    - User login and logout.
    - Password recovery/reset.
    - User profile management (e.g., view/edit personal details, order history, saved builds).
2. **Product Catalog & Browsing:**
    - Display a list of products with categories (CPU, GPU, Motherboard, RAM, SSD, HDD, PSU, Casing, Cooler, Peripherals etc.).
    - Search functionality for products.
    - Filtering and sorting options for products (e.g., by price, brand, specifications).
    - Detailed product pages with specifications, images, descriptions, and user reviews/ratings.
3. **Custom PC Builder:**
    - Interface to select components for a new PC build.
    - Compatibility checking between selected components (e.g., CPU socket vs. motherboard, RAM type, PSU wattage).
    - Real-time price calculation for the build.
    - Ability to save and share custom builds.
4. **Product Comparison:**
    - Ability to select multiple products for side-by-side comparison of specifications and features.
5. **Shopping Cart Management:**
    - Add products/custom builds to the cart.
    - View and modify cart contents (e.g., change quantity, remove items).
    - Calculate total price including taxes and shipping (if applicable).
6. **Wishlist Management:**
    - Add products to a personal wishlist.
    - View and manage wishlist items.
7. **Checkout and Order Processing:**
    - Secure checkout process.
    - Integration with payment gateways [TO BE VERIFIED/FILLED: Specify payment gateways if known].
    - Order confirmation and notification.
    - Order history tracking for users.
8. **Blog/Content Management:**
    - Admin interface to create, edit, and publish blog posts (articles, reviews, guides).
    - User interface to read and comment on blog posts.
    - Categorization and tagging of blog posts.
9. **Admin Panel:**
    - Management of products (add, edit, delete, manage stock).
    - Management of product categories and brands.
    - User management.
    - Order management and fulfillment.
    - Content management for the blog.
    - View site analytics/reports [TO BE VERIFIED/FILLED: If planned].

**Technical Requirement:**

- **Chosen Design Process Model:**

  - **Model:** **Agile (specifically Scrum or Kanban)** is inferred or highly recommended for a project like "TechReform BD v2".
  - **Justification:**
    - **Iterative Development:** Web applications of this nature benefit from iterative development, allowing for features to be developed, tested, and released in cycles. This helps in gathering early feedback and adapting to changing requirements.
    - **Flexibility:** The tech market and user preferences can evolve. Agile allows for flexibility in accommodating new features or modifications throughout the development lifecycle.
    - **Collaboration:** Agile promotes close collaboration between developers, and potentially stakeholders (if user feedback is actively sought). Given the team structure (multiple members), Agile methodologies facilitate better coordination.
    - **Rapid Prototyping:** Features like the PC builder or product comparison can be complex. Agile allows for building core functionality first and then incrementally adding enhancements.
    - **Continuous Improvement:** Regular reviews and retrospectives in Agile help in refining the development process and the product itself.

- **Design Pattern(s) Used:**

  - **Model-View-Template (MVT):**

    - **Explanation:** Since the project uses Django (as indicated by manage.py, `settings.py` in TechReform, and Django in requirements.txt), it inherently follows the MVT architectural pattern.
      - **Model:** Represents the data structure and interacts with the database. In "TechReform BD v2", models would define products, users, orders, blog posts, PC builds, etc. (evident in `models.py` files within each app).
      - **View:** Handles the request-response logic. It fetches data from models, processes it, and selects an appropriate template to render. In Django, views are Python functions or classes that take a web request and return a web response (evident in `views.py` files).
      - **Template:** Defines the presentation layer – how the data is displayed to the user. Django templates are typically HTML files with special syntax to display dynamic data (evident in the templates directory).
    - **Justification:** MVT promotes separation of concerns, making the codebase more organized, maintainable, and scalable. It allows front-end and back-end development to occur more independently.

  - **Other Potential Patterns (to be verified from deeper code analysis):**
    - **Repository Pattern:** Might be used for abstracting data access logic, though Django's ORM often serves this purpose.
    - **Factory Pattern:** Could be used for creating complex objects, perhaps in the PC builder logic.
    - **Observer Pattern:** Could be used for notifications (e.g., when an order status changes).
    - `[TO BE VERIFIED/FILLED: Further analysis of specific app logic in AuthApp/forms.py, views.py etc. might reveal more granular design patterns.]`

### 6. Methodology

**Diagrams:**

For "TechReform BD v2", several types of diagrams have been created to provide comprehensive system documentation and understanding of the system architecture:

#### 1. Entity-Relationship (ER) Diagram

![ER Diagram](diagrams/ER_Diagram/ER_Diagram.png)

The ER diagram illustrates the database schema and relationships between different entities in the TechReform system. Key components include:

- **User Management:** User, UserProfile entities with one-to-one relationship for extended user information
- **Product Catalog:** BaseProduct entity serving as parent for all product types (CPU, GPU, Motherboard, etc.) with polymorphic relationships
- **E-commerce Core:** Cart, CartItem, Order, OrderItem, and ShippingAddress entities handling the shopping workflow
- **Content Management:** BlogPost, Comment, Category entities for the blog system
- **Advanced Features:** WishList, PCBuilder, CompareProduct, and SupportTicket entities for enhanced user experience

The diagram shows proper normalization with foreign key relationships, ensuring data integrity and efficient querying.

#### 2. Data Flow Diagram (DFD)

The Data Flow Diagrams provide a hierarchical view of data movement through the system:

**Level 0 - Context Diagram:**
![DFD Context](diagrams/Data_Flow_Diagram/Data_Flow_Diagram_Level_0_Context_Diagram.png)

Shows the system boundaries with external entities (Customer, Admin, Staff, Payment Gateway, Email Service) and their high-level interactions with the TechReform system.

**Level 1 - System Overview:**
![DFD Level 1](diagrams/Data_Flow_Diagram/Data_Flow_Diagram_Level_1_System_Overview.png)

Breaks down the system into major processes:

1. User Management
2. Product Catalog
3. Shopping Cart
4. Order Processing
5. Blog System
6. PC Builder
7. Support System

**Level 2 - Detailed Process Diagrams:**

- **Product Catalog System:** ![Product Catalog DFD](diagrams/Data_Flow_Diagram/Data_Flow_Diagram_Level_2_Product_Catalog_System.png)
- **Order Processing System:** ![Order Processing DFD](diagrams/Data_Flow_Diagram/Data_Flow_Diagram_Level_2_Order_Processing_System.png)
- **PC Builder System:** ![PC Builder DFD](diagrams/Data_Flow_Diagram/Data_Flow_Diagram_Level_2_PC_Builder_System.png)
- **Blog System:** ![Blog System DFD](diagrams/Data_Flow_Diagram/Data_Flow_Diagram_Level_2_Blog_System.png)
- **Support System:** ![Support System DFD](diagrams/Data_Flow_Diagram/Data_Flow_Diagram_Level_2_Support_System.png)

These detailed DFDs show specific data flows, processes, and data stores for each subsystem, providing clear understanding of how data moves through different parts of the application.

#### 3. Activity Diagram

![Activity Diagram](diagrams/Activity_Diagram/Activity_Diagram.png)

The Activity Diagram maps out the complete user journey through the TechReform system, showing:

- **User Authentication Flow:** Guest vs. authenticated user paths
- **Product Browsing:** Search, filter, and view product details
- **Shopping Experience:** Add to cart, wishlist, comparison, and PC builder workflows
- **Checkout Process:** Guest checkout vs. user checkout with saved addresses
- **Payment Processing:** Multiple payment methods including COD and online payments
- **Blog Interaction:** Reading posts, commenting (requires authentication)
- **PC Builder Workflow:** Component selection, compatibility checking, saving builds

The diagram uses decision points, parallel activities, and merge nodes to show the complex user interactions and system responses.

#### 4. Sequence Diagrams

Multiple sequence diagrams illustrate key system interactions:

**User Registration and Login:**
![User Auth Sequence](diagrams/Sequence_Diagram/Sequence_Diagram_User_Registration_Login_Sequence.png)

Shows the complete authentication workflow including user creation, profile setup via Django signals, and login process.

**Shopping Cart and Checkout:**
![Cart Checkout Sequence](diagrams/Sequence_Diagram/Sequence_Diagram_Shopping_Cart_Checkout_Sequence.png)

Details the e-commerce workflow from adding items to cart through order completion, including cart management, order creation, and address handling.

**Product Search and Filter:**
![Product Search Sequence](diagrams/Sequence_Diagram/Sequence_Diagram_Product_Search_Filter_Sequence.png)

Demonstrates the product discovery process with search queries, filtering, and dynamic result updates.

**PC Builder Configuration:**
![PC Builder Sequence](diagrams/Sequence_Diagram/Sequence_Diagram_PC_Builder_Configuration_Sequence.png)

Shows the complex PC building process including component selection, compatibility checking, and configuration saving.

**Blog Post Creation and Comment:**
![Blog Sequence](diagrams/Sequence_Diagram/Sequence_Diagram_Blog_Post_Creation_Comment_Sequence.png)

Illustrates content management workflow for blog posts and user interaction through comments.

**Order Processing and Status Update:**
![Order Processing Sequence](diagrams/Sequence_Diagram/Sequence_Diagram_Order_Processing_Status_Update_Sequence.png)

Details the order fulfillment process from placement to delivery with status updates.

**Support Ticket Management:**
![Support Sequence](diagrams/Sequence_Diagram/Sequence_Diagram_Support_Ticket_Management_Sequence.png)

Shows customer support workflow including ticket creation, staff assignment, and resolution tracking.

#### 5. Gantt Chart - Project Timeline

The project includes comprehensive Gantt charts showing the development timeline:

**Development Timeline:**
![Development Gantt](diagrams/Gantt_Chart/Gantt_Chart_Development.png)

Shows the 8-week development schedule with parallel workstreams for frontend, backend, and design work across three team members:

- **Sharif:** Frontend Developer (React/Django Templates, JavaScript, CSS/Tailwind)
- **Priom:** Backend Developer (Django, Python, Database, APIs)
- **Shorna:** UI/UX Designer (Design Systems, User Experience, Prototyping)

**Key Milestones:**
![Milestones Gantt](diagrams/Gantt_Chart/Gantt_Chart_Key_Milestones.png)

Highlights critical project milestones including Backend Foundation Complete, Frontend Core Complete, Feature Integration Done, and Production Ready.

**Technical Stack Integration:**
![Technical Integration Gantt](diagrams/Gantt_Chart/Gantt_Chart_Technical_Stack_Integration_Timeline.png)

Details the integration timeline for different technical components showing dependencies between backend development, frontend implementation, and system integration phases.

**Software Process Model:**

- **Chosen Model:** **Agile (likely Scrum or a Kanban-like approach)**.

  - **Justification:** As mentioned in Requirement Analysis, Agile is suitable for iterative development, flexibility, and collaboration, which are beneficial for a web application like "TechReform BD v2" developed by a small team.

- **How this model was implemented (Inferred/Suggested):**

  - **Scrum Implementation (if applicable):**
    - **Sprints:** The project would be divided into fixed-length iterations (e.g., 2-4 weeks) called sprints.
    - **Product Backlog:** A prioritized list of all features, requirements, and tasks (e.g., "Implement user registration," "Develop PC builder UI," "Integrate payment gateway"). This would be derived from the functional requirements.
    - **Sprint Planning:** At the start of each sprint, the team selects a set of tasks from the Product Backlog to complete in the Sprint Backlog.
    - **Daily Stand-ups (Daily Scrum):** Short daily meetings to discuss progress, impediments, and plans for the day.
    - **Sprint Review:** At the end of each sprint, the team demonstrates the completed work to stakeholders (if any) or for internal review.
    - **Sprint Retrospective:** The team reflects on the sprint to identify what went well and what could be improved in the next sprint.
  - **Kanban Implementation (if applicable):**
    - **Visual Workflow:** A Kanban board (physical or digital, e.g., Trello, Jira, GitHub Projects) would be used to visualize the workflow (e.g., columns like "To Do," "In Progress," "Testing," "Done").
    - **Work in Progress (WIP) Limits:** Limits on the number of tasks in each stage to ensure focus and flow.
    - **Continuous Flow:** Tasks are pulled into the workflow as capacity allows, rather than in fixed sprints. This is suitable for continuous delivery and maintenance.
  - **General Agile Practices:**
    - **Version Control:** Regular commits to a VCS like Git (as implied by the prompt mentioning a VCS link). Branching strategies (e.g., feature branches) would be used.
    - **Automated Testing:** Implementation of unit tests (e.g., test_support_system.py, login_test.py, register_test.py) and potentially integration tests.
    - **Continuous Integration/Continuous Deployment (CI/CD) - Aspirational/Potential:** While not explicitly stated, a mature Agile process might involve CI/CD pipelines to automate testing and deployment.

- **Sample Code Demonstrating Aspects of Software Process Model Implementation:**

  - **Placeholder for CI/CD Pipeline Snippet (e.g., GitHub Actions workflow file `.github/workflows/django.yml`):**

            ```yaml
            # .github/workflows/django.yml
            # This is a placeholder example of a GitHub Actions workflow for a Django project.
            # Actual implementation would depend on specific project needs and hosting.
            name: Django CI

            on:
              push:
                branches: [ main, develop ]
              pull_request:
                branches: [ main, develop ]

            jobs:
              build:
                runs-on: ubuntu-latest
                strategy:
                  max-parallel: 4
                  matrix:
                    python-version: [3.9, 3.10, 3.11] # Match project's Python version

                steps:
                - uses: actions/checkout@v3
                - name: Set up Python ${{ matrix.python-version }}
                  uses: actions/setup-python@v3
                  with:
                    python-version: ${{ matrix.python-version }}
                - name: Install Dependencies
                  run: |
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                - name: Run Tests
                  run: |
                    # Assuming 'manage.py test' runs all tests in the project
                    # Or specify app names: python manage.py test AuthApp BlogApp ProductsApp
                    python manage.py test
                # - name: Lint with Flake8 (Example)
                #   run: |
                #     pip install flake8
                #     flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
                #     flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
            ```

  - **Placeholder for Sprint Backlog Example (Conceptual Markdown):**

            ```markdown
            ## Sprint 2 Backlog (Example)
            **Sprint Goal:** Implement core PC Builder functionality and product display.

            - **User Story 1 (PC Builder UI):** As a user, I want to select a CPU and see compatible motherboards, so I can start building my PC.
                - Task 1.1: Design PC Builder component selection interface.
                - Task 1.2: Develop front-end for CPU selection.
                - Task 1.3: Develop back-end logic to fetch compatible motherboards based on CPU.
                - Task 1.4: Unit tests for motherboard compatibility logic.
            - **User Story 2 (Product Listing):** As a user, I want to view a list of available CPUs with their basic details (name, price), so I can choose one.
                - Task 2.1: Create Django model for CPU products.
                - Task 2.2: Create Django view to list CPUs.
                - Task 2.3: Create Django template to display CPU list.
                - Task 2.4: Populate sample CPU data.
            - **Bug Fix 1:** Fix login page styling issue on mobile.
            - **Tech Debt 1:** Refactor database connection pooling.
            ```

**Project Developing Resources:**

Based on requirements.txt and common Django project structures:

1. **Models (Conceptual - defined in `models.py` of each app):**
    - User profiles, product information, categories, brands, shopping carts, orders, wishlists, PC build configurations, blog posts, comments.
2. **Design Patterns:**
    - **MVT (Model-View-Template):** Core architectural pattern of Django.
    - Others as potentially identified (Repository, Factory, etc.).
3. **Frameworks:**
    - **Django:** (Version 5.1.4 from requirements.txt) High-level Python web framework used for the backend development, ORM, templating, routing, admin panel.
    - **[TO BE VERIFIED/FILLED: Frontend Framework/Libraries e.g., Tailwind CSS (implied by `django-tailwind`), Bootstrap, React, Vue, or just plain HTML/CSS/JS. The static_src might contain clues if it uses a CSS preprocessor or JS bundler setup.]**
4. **APIs (Application Programming Interfaces):**
    - **Internal APIs:** Django REST framework might be used to create APIs if there's a decoupled frontend or mobile app planned, or for AJAX interactions. (Check `urls.py` and `views.py` for API endpoint definitions).
    - **External APIs (Potential):**
        - Payment Gateway APIs (e.g., Stripe, PayPal, local Bangladeshi gateways like bKash, Nagad) for processing transactions. `[TO BE VERIFIED/FILLED]`
        - Social Login APIs (e.g., Google, Facebook) if social login is a feature. `[TO BE VERIFIED/FILLED]`
        - Shipping/Logistics APIs if integrated for order fulfillment. `[TO BE VERIFIED/FILLED]`
5. **Datasets (Primarily managed within the application database):**
    - Product data (specifications, images, prices, stock).
    - User data.
    - Order data.
    - Blog content.
    - Compatibility rules for PC components (this might be a significant dataset to curate or source).
6. **Key Libraries (from requirements.txt):**
    - `Pillow==11.0.0`: For image processing (e.g., product images, user avatars).
    - `requests==2.32.3`: For making HTTP requests (e.g., to external APIs).
    - `python-slugify==8.0.4`: For generating URL-friendly slugs from strings (e.g., for product or blog post URLs).
    - `django-tailwind==3.8.0`: Integrates Tailwind CSS with Django projects.
    - `django-browser-reload==1.18.0`: For automatic browser reloading during development.
    - `Jinja2==3.1.6`: Templating engine (though Django has its own, Jinja2 might be used by `django-tailwind` or other components).
    - `markdown-it-py==3.0.0`: For rendering Markdown content (likely for blog posts).
    - `sqlparse==0.5.2`: Used by Django debug toolbar and other tools.
    - `asgiref==3.8.1`: ASGI (Asynchronous Server Gateway Interface) implementation, for Django's async capabilities.
7. **Development Tools:**
    - Python (Version implied by `cpython-313` in `__pycache__` suggests Python 3.13, but requirements.txt doesn't specify a Python version directly).
    - pip (for package management).
    - Git (for version control).
    - A code editor/IDE (like VS Code).
    - A database system (e.g., SQLite for development - db.sqlite3 is present, PostgreSQL/MySQL for production).
8. **Static Files & Media:**
    - static directory: For CSS, JavaScript, static images.
    - media directory: For user-uploaded content like product images, profile pictures.
    - placeholder directory: Contains placeholder images, likely used during early development or for UI mockups.

### 7. Final Result & Testing

**Final Result:**

The final result of "TechReform BD v2" will be a fully functional, deployed web application accessible via a URL. Key characteristics and functionalities of the final product will include:

1. **Homepage:** An engaging landing page showcasing featured products, popular PC builds, latest blog posts, and clear navigation to different sections of the site.
2. **User Accounts:** Secure registration, login, and profile management where users can view their order history, saved PC builds, and wishlists.
3. **Product Listings & Pages:** Well-organized product categories, powerful search and filtering, and detailed product pages with high-quality images, specifications, pricing, stock status, and user reviews.
4. **PC Builder Tool:** An interactive and intuitive interface allowing users to select components (CPU, motherboard, RAM, GPU, SSD/HDD, PSU, Casing, Cooler) with real-time compatibility checks and price updates. Users will be able to save their builds and add them to the cart.
5. **Comparison Tool:** A feature allowing users to select multiple products and compare their specifications and features side-by-side.
6. **Shopping Cart & Checkout:** A seamless shopping cart experience with easy modification of items and a secure, multi-step checkout process integrated with relevant payment gateways for the Bangladeshi market.
7. **Blog Section:** A content-rich blog with articles, reviews, and guides on technology, PC building, and gaming, with options for users to comment and interact.
8. **Responsive Design:** The website will be fully responsive, providing an optimal viewing and interaction experience across desktops, tablets, and mobile devices.
9. **Admin Panel:** A comprehensive backend interface for administrators to manage products, inventory, orders, users, and blog content.

**Sample Images (Description of what should be included):**

Since I cannot generate actual images, here's a description of the types of screenshots that should be included in the report:

- **Screenshot of the Homepage:** Showcasing the overall design, branding, and key navigation elements.
- **Screenshot of a Product Listing Page:** Displaying how multiple products are listed with filters and sorting options.
- **Screenshot of a Single Product Detail Page:** Highlighting product images, specifications, price, and "Add to Cart" / "Add to Wishlist" buttons.
- **Screenshot of the PC Builder Interface:** Showing the component selection process and compatibility indicators.
- **Screenshot of the Product Comparison Page:** Illustrating how selected products are compared.
- **Screenshot of the Shopping Cart Page:** Showing items in the cart with quantities and total price.
- **Screenshot of a User Profile/Dashboard:** Displaying user-specific information like order history or saved builds.
- **Screenshot of a Blog Post:** Showing the layout of an article with text and images.
- **Screenshot of the Admin Panel (e.g., Product Management section):** Demonstrating backend functionality.

**Results of Testing Scripts:**

The report should include summaries or snippets of the output from testing scripts. The project structure indicates the presence of test files (test_support_system.py, login_test.py, register_test.py, and `tests.py` in various apps).

- **Unit Test Results:**

  - **Description:** Show the output from running Django's test runner (e.g., `python manage.py test`). This output typically includes the number of tests run, number of passes, number of failures, and any errors encountered.
  - **Example Snippet (Conceptual):**

            ```
            Found 85 test(s).
            Creating test database for alias 'default'...
            System check identified no issues (0 silenced).
            .....................................................................................
            ----------------------------------------------------------------------
            Ran 85 tests in 10.321s

            OK
            Destroying test database for alias 'default'...
            ```

  - Or, if there were failures:

            ```
            FAIL: test_login_with_invalid_credentials (AuthApp.tests.LoginTest)
            ----------------------------------------------------------------------
            Traceback (most recent call last):
              File "d:\Programming\VSCode\TechReform-BD\AuthApp\login_test.py", line 25, in test_login_with_invalid_credentials
                self.assertContains(response, "Invalid credentials")
            AssertionError: False is not true : Response did not contain "Invalid credentials"
            ...
            Ran 85 tests in 12.500s

            FAILED (failures=1)
            ```

- **Integration Test Results (if applicable):**
  - **Description:** If specific integration tests are written (e.g., testing the flow from adding to cart to checkout), their success/failure status should be reported. This might involve more descriptive logging or custom reports.
- **Code Coverage Reports:**

  - **Description:** Include a summary from a code coverage tool (e.g., `coverage.py`). This shows what percentage of the codebase is covered by tests.
  - **Example Snippet (Conceptual, from `coverage report`):**

            ```
            Name                               Stmts   Miss  Cover
            ------------------------------------------------------
            AuthApp/__init__.py                    0      0   100%
            AuthApp/forms.py                      25      2    92%
            AuthApp/models.py                     15      0   100%
            AuthApp/views.py                      50      5    90%
            ...
            ProductsApp/models.py                 40      1    98%
            ------------------------------------------------------
            TOTAL                                530     30    94%
            ```

- **Manual Testing Checklist/Report Summary:**
  - **Description:** A summary of manual testing performed for key user flows (e.g., user registration, product purchase, PC building). This would list test cases, expected results, actual results, and pass/fail status.
  - The login_report.html and register_report.html files in the root directory might be outputs from such testing (possibly using a tool like Selenium or Playwright with HTML reporting). These should be summarized or referenced.

The goal is to demonstrate that the application has been thoroughly tested and meets the functional requirements with a high degree of reliability.

### 8. Project Management

**Project Timeline (Suggested, based on Agile/Scrum):**

This is a suggested timeline assuming a Scrum-based Agile approach with 2-week sprints. The actual timeline would depend on team size, velocity, and unforeseen challenges.

- **Sprint 0: Project Setup & Initial Planning (1-2 Weeks)**

  - Week 1: Define project scope, high-level requirements, technology stack finalization. Setup version control, development environments, project management tools. Initial database schema design.
  - Week 2: Create initial product backlog. Detailed planning for Sprint 1. Basic project structure and app layout.

- **Sprint 1: Core Authentication & Product Display (2 Weeks)**

  - Implement user registration and login (AuthApp).
  - Basic product model and admin interface for adding products (ProductsApp).
  - Display product listings and detail pages (ProductsApp).
  - Setup base templates and static file handling.

- **Sprint 2: Cart & Wishlist Functionality (2 Weeks)**

  - Implement shopping cart functionality (add, view, update, remove) (CartApp).
  - Implement wishlist functionality (WishlistApp).
  - Basic user profile page.

- **Sprint 3: PC Builder - Phase 1 (Core Logic) (2 Weeks)**

  - Develop models for PC components and compatibility rules (PCBuilderApp, ProductsApp).
  - Implement core logic for selecting components and basic compatibility checks.
  - Admin interface for managing component data and compatibility rules.

- **Sprint 4: PC Builder - Phase 2 (UI & Integration) (2 Weeks)**

  - Develop user interface for the PC Builder.
  - Integrate PC builder with product details and cart.
  - Allow saving of custom builds to user profiles.

- **Sprint 5: Product Comparison & Advanced Search/Filtering (2 Weeks)**

  - Implement product comparison feature (CompareApp).
  - Enhance product search with advanced filters (e.g., by brand, price range, specifications).

- **Sprint 6: Blog Implementation (2 Weeks)**

  - Develop models and views for blog posts and comments (BlogApp).
  - Admin interface for managing blog content.
  - User interface for reading and commenting on blog posts.

- **Sprint 7: Checkout Process & Payment Integration (2 Weeks)**

  - Implement order models and checkout workflow.
  - Integrate with a chosen payment gateway [TO BE VERIFIED/FILLED: Specify gateway].
  - Order confirmation emails and order history for users.

- **Sprint 8: Admin Panel Enhancements & User Profile (2 Weeks)**

  - Enhance admin panel for comprehensive management (orders, users, content).
  - Flesh out user profile features (edit details, view all orders, manage saved builds/wishlists).

- **Sprint 9: Testing, Refinement & UI Polish (2 Weeks)**

  - Comprehensive testing (unit, integration, user acceptance testing).
  - Bug fixing and performance optimization.
  - UI/UX refinement based on feedback.
  - Ensure responsiveness across devices.

- **Sprint 10: Final Testing, Documentation & Deployment Preparation (2 Weeks)**

  - Final round of testing.
  - Preparation of user documentation and project report.
  - Setup production environment and prepare for deployment.

- **Post-Sprint: Deployment & Go-Live (1 Week)**
  - Deploy to production server.
  - Post-deployment checks and monitoring.

**Total Estimated Duration:** Approximately 20-24 weeks (5-6 months), adjustable based on team velocity and complexity.

**Gantt Chart (Outline of what it would contain):**

A Gantt chart would visually represent the project schedule. Since I cannot generate an image, here's an outline of tasks and dependencies:

| Task ID | Task Name                                         | Duration (Weeks) | Start Date (Example) | End Date (Example) | Dependencies | Assigned To (Example) |
| ------- | ------------------------------------------------- | ---------------- | -------------------- | ------------------ | ------------ | --------------------- |
| 1.0     | **Phase 1: Planning & Setup**                     |                  |                      |                    |              |                       |
| 1.1     | Project Definition & Scope                        | 1                | 2025-06-02           | 2025-06-06         |              | Team                  |
| 1.2     | Tech Stack & Environment Setup                    | 1                | 2025-06-02           | 2025-06-06         |              | Team                  |
| 1.3     | Initial Product Backlog & Sprint 0 Plan           | 1                | 2025-06-09           | 2025-06-13         | 1.1          | Team                  |
| 2.0     | **Phase 2: Core Features (Sprints 1-2)**          |                  |                      |                    |              |                       |
| 2.1     | User Authentication (AuthApp)                     | 2                | 2025-06-16           | 2025-06-27         | 1.3          | Member A, B           |
| 2.2     | Basic Product Catalog (ProductsApp)               | 2                | 2025-06-16           | 2025-06-27         | 1.3          | Member C              |
| 2.3     | Cart & Wishlist (CartApp, WishlistApp)            | 2                | 2025-06-30           | 2025-07-11         | 2.1, 2.2     | Member A, C           |
| 3.0     | **Phase 3: PC Builder (Sprints 3-4)**             |                  |                      |                    |              |                       |
| 3.1     | PC Builder Backend Logic (PCBuilderApp)           | 2                | 2025-07-14           | 2025-07-25         | 2.2          | Member B, C           |
| 3.2     | PC Builder UI & Integration                       | 2                | 2025-07-28           | 2025-08-08         | 3.1          | Member A, B           |
| 4.0     | **Phase 4: Advanced Features (Sprints 5-6)**      |                  |                      |                    |              |                       |
| 4.1     | Product Comparison (CompareApp)                   | 2                | 2025-08-11           | 2025-08-22         | 2.2          | Member C              |
| 4.2     | Blog Implementation (BlogApp)                     | 2                | 2025-08-25           | 2025-09-05         | 2.1          | Member A              |
| 5.0     | **Phase 5: E-commerce & Admin (Sprints 7-8)**     |                  |                      |                    |              |                       |
| 5.1     | Checkout & Payment Gateway                        | 2                | 2025-09-08           | 2025-09-19         | 2.3          | Member B, C           |
| 5.2     | Admin Panel & User Profile Enhancements           | 2                | 2025-09-22           | 2025-10-03         | 2.1, 5.1     | Team                  |
| 6.0     | **Phase 6: Testing & Deployment (Sprints 9-10+)** |                  |                      |                    |              |                       |
| 6.1     | Comprehensive Testing & UI Polish                 | 2                | 2025-10-06           | 2025-10-17         | All previous | Team                  |
| 6.2     | Final Testing, Docs & Deployment Prep             | 2                | 2025-10-20           | 2025-10-31         | 6.1          | Team                  |
| 6.3     | Deployment & Go-Live                              | 1                | 2025-11-03           | 2025-11-07         | 6.2          | Team                  |

**Note:** The Gantt chart would typically be created using project management software (e.g., Microsoft Project, Jira, Asana, or even a detailed spreadsheet). It would include milestones (e.g., "End of Sprint 1," "PC Builder Alpha Ready") and visually show task dependencies and critical paths. The "Assigned To" would list the project members responsible for each task.

### 9. Version Control, Finance, Conclusion/Future Work

**Version Control System (VCS):**

- **System Used:** Git (inferred from the prompt mentioning a "VCS Link" which is typically a Git repository hosting service like GitHub or GitLab).
- **Snapshots of Commits:**
  - A snapshot of the version control system commits would typically be a screenshot from the Git hosting platform (e.g., GitHub's commit history page) or the output of `git log` from the command line.
  - **What it would show:**
    - **Commit Hash:** A unique identifier for each commit.
    - **Author:** The project member who made the commit (e.g., Sharif Md. Yousuf, Noor Mohammed Priom, Shornali Akter).
    - **Date & Time:** When the commit was made.
    - **Commit Message:** A brief description of the changes made in that commit (e.g., "Implemented user login functionality," "Fixed bug in cart total calculation," "Added CPU models to database").
    - **Branch Information:** It might also show commits on different branches (e.g., `main`, `develop`, feature branches like `feat/pc-builder`) and merge commits.
  - **Importance:** This demonstrates active development, collaboration among team members, and a chronological record of how the project evolved. It highlights the iterative nature of the development process.

**Finance Management:**

- For a student project like "TechReform BD v2," direct financial management (revenue, expenses, profit/loss) is typically not a core component unless it's part of a specific business plan simulation.
- **Aspects that might be considered (if applicable):**
  - **Hosting Costs:** If deployed to a cloud platform (e.g., AWS, Heroku, PythonAnywhere), there might be minor hosting fees, especially if exceeding free tier limits.
  - **Domain Name Registration:** Cost of registering a domain name for the web application.
  - **Third-party API Costs:** Some APIs (e.g., advanced payment gateways, specialized data APIs) might have subscription fees, though free tiers are often used for student projects.
  - **Software/Tool Licenses:** Most tools used (Python, Django, VS Code, Git) are open-source and free.
- **Statement for the Report:**
  - "As 'TechReform BD v2' is an academic project, extensive finance management modules tracking revenue or detailed operational expenses were not implemented. Potential future costs would involve web hosting, domain registration, and any premium third-party API subscriptions. For the scope of this project, financial considerations were limited to utilizing free and open-source tools and services where possible."
  - Alternatively: `[N/A or TO BE FILLED MANUALLY if specific financial simulations were part of the project requirements]`

**Conclusion/Future Work:**

- **Conclusion:**
  - "TechReform BD v2" successfully aimed to develop a comprehensive web application serving as an e-commerce platform, custom PC builder, and tech community hub tailored for the Bangladeshi market. The project implemented key features including user authentication, product catalog management, an interactive PC builder with compatibility checks, shopping cart and wishlist functionalities, and a blog system. Built using Python and the Django framework, the MVT architecture ensured a modular and maintainable codebase. The development process, guided by Agile principles, allowed for iterative progress and adaptation. The final application provides a solid foundation for a user-centric online destination for tech enthusiasts in Bangladesh.
- **Future Work/Enhancements:**
  - **Advanced AI-Powered PC Builder:** Integrate AI to suggest builds based on user needs (e.g., gaming, video editing, budget) or to optimize component selection.
  - **Real-time Price Comparison:** Integrate APIs from multiple local vendors for real-time price comparisons.
  - **User Reviews and Ratings System:** More detailed user reviews for products and builds.
  - **Community Forum:** Expand the blog into a full-fledged forum for user discussions, Q&A, and build showcases.
  - **Mobile Application:** Develop native mobile apps (iOS/Android) for an enhanced mobile experience.
  - **Integration with Local Delivery Services:** API integration for streamlined order fulfillment.
  - **Enhanced Admin Analytics:** More detailed sales, user behavior, and inventory analytics for administrators.
  - **Localization:** Support for Bengali language interface.
  - **Gamification:** Introduce points or badges for community participation or build sharing.
  - **Augmented Reality (AR) Feature:** Allow users to visualize PC components or builds in their physical space using AR.
- **Learnings from this Project:**
  - **The Art of Project Management:**
    - Learned the importance of clear requirements definition, task breakdown, and realistic timeline estimation.
    - Experienced the benefits of Agile methodologies (e.g., sprints, regular check-ins) in managing complex tasks and adapting to changes.
    - Understood the significance of effective communication and coordination within a development team.
  - **Distributed and Collaborative Software Development:**
    - Gained practical experience with version control systems (Git) for managing code contributions from multiple developers, including branching, merging, and resolving conflicts.
    - Learned to work effectively as a team, dividing tasks, sharing knowledge, and integrating individual components into a cohesive whole.
    - Appreciated the role of project management and communication tools in facilitating remote or distributed collaboration.
  - **Risk Analysis for Developing Complex Software-Intensive Systems:**
    - Identified potential risks such as scope creep, technical challenges (e.g., complex compatibility logic for PC builder), integration issues with third-party APIs, and team member availability.
    - Learned the importance of proactive risk identification and mitigation strategies (e.g., thorough planning, modular design, regular testing, contingency planning).
    - Understood that complex systems require robust testing at various levels (unit, integration, user acceptance) to ensure reliability and quality.

### 10. References

The report for "TechReform BD v2" would typically cite a variety of sources. Here are types of references that might be included:

1. **Framework and Library Documentation:**

    - Django Project Documentation: `https://docs.djangoproject.com/`
    - Python Standard Library Documentation: `https://docs.python.org/3/`
    - Documentation for specific Django packages used (e.g., `django-tailwind`, `Pillow`, `requests` from their respective official sites or PyPI).
    - [If a specific front-end framework like React or Vue was used, its documentation would be listed here.]
    - Tailwind CSS Documentation: `https://tailwindcss.com/docs/`

2. **Design Patterns and Software Engineering Principles:**

    - Books or articles on software design patterns (e.g., "Design Patterns: Elements of Reusable Object-Oriented Software" by Gamma et al., or web resources explaining MVC/MVT).
    - Resources on Agile methodologies or Scrum (e.g., `https://www.scrum.org/`, `https://www.atlassian.com/agile`).

3. **Similar Systems (for comparative analysis in Motivation):**

    - PCPartPicker: `https://pcpartpicker.com/`
    - Star Tech: `https://www.startech.com.bd/`
    - [Any other e-commerce or PC building websites researched.]

4. **Technical Articles and Tutorials:**

    - Specific blog posts, tutorials, or Stack Overflow answers that helped solve particular technical challenges during development (e.g., implementing a specific Django feature, integrating an API).

5. **Database Design Resources:**

    - Articles or books on relational database design, ER diagrams.

6. **Version Control Resources:**

    - Pro Git book (online): `https://git-scm.com/book/`
    - GitHub or GitLab documentation.

7. **Societal Impact Research (if specific data was cited):**
    - Articles or studies on the impact of e-commerce, digital literacy, or online communities in Bangladesh or similar contexts.

**Example Format (to be consistent):**

- [1] Django Software Foundation. "Django documentation". Retrieved from [https://docs.djangoproject.com/en/stable/](https://docs.djangoproject.com/en/stable/) (Accessed: May 25, 2025).
- [2] Tailwind Labs Inc. "Tailwind CSS Documentation". Retrieved from [https://tailwindcss.com/docs](https://tailwindcss.com/docs) (Accessed: May 25, 2025).
- [3] "PCPartPicker". Retrieved from [https://pcpartpicker.com/](https://pcpartpicker.com/) (Accessed: May 25, 2025).

`[TO BE FILLED: Actual list of references used during the project and report writing should be compiled here, following a consistent citation style like IEEE, APA, or MLA as required by the course.]`

---

### Appendix A: Report Quality/Formatting/Referencing

**Maintaining High Report Quality:**

1. **Clarity and Conciseness:**
    - Write in clear, straightforward language. Avoid jargon where possible, or explain it if necessary.
    - Be concise and to the point. Avoid unnecessary repetition or overly lengthy paragraphs.
2. **Professional Tone:**
    - Maintain a formal and objective tone throughout the report.
    - Avoid colloquialisms or overly casual language.
3. **Logical Structure:**
    - Ensure the report flows logically from one section to the next.
    - Use headings and subheadings effectively to organize content (as provided in the prompt).
    - Start each section with a brief introduction to its purpose.
4. **Accuracy and Detail:**
    - Ensure all information presented is accurate and, where appropriate, supported by evidence (from codebase analysis, research, or testing).
    - Provide sufficient detail to allow the reader to understand the project's scope, design, implementation, and outcomes.
5. **Visual Aids:**
    - Use diagrams, screenshots, and code snippets appropriately to illustrate points and break up large blocks of text. Ensure they are relevant, clear, and well-labeled.
    - For diagrams, ensure they are legible and follow standard conventions (e.g., for ERDs, DFDs, UML).
6. **Proofreading and Editing:**
    - Thoroughly proofread the entire report for grammatical errors, spelling mistakes, and typos.
    - Consider reading it aloud or having a peer review it.
    - Check for consistency in terminology and formatting.

**Formatting:**

1. **Consistent Font and Sizing:** Use a standard, readable font (e.g., Times New Roman, Arial, Calibri) and consistent font sizes for headings, subheadings, and body text.
2. **Margins and Spacing:** Use standard margins (e.g., 1 inch) and appropriate line spacing (e.g., 1.5 or double-spaced for body text, single-spaced for code blocks or captions).
3. **Headings and Subheadings:** Use a clear hierarchy of headings (e.g., H1, H2, H3) with consistent formatting (bold, font size).
4. **Page Numbering:** Include page numbers.
5. **Table of Contents:** For a lengthy report, a table of contents is highly recommended.
6. **Lists:** Use bullet points or numbered lists for clarity when presenting multiple items or steps.
7. **Code Blocks:** Format code snippets clearly, using a monospaced font and appropriate indentation. Indicate the language if possible.
8. **Captions:** Provide clear captions for all figures (diagrams, screenshots) and tables.

**Referencing:**

1. **Choose a Style:** Select a standard referencing style (e.g., IEEE, APA, MLA, Harvard) as specified by your course or institution and use it consistently throughout the report.
2. **In-text Citations:**
    - Every piece of information, idea, or quote taken from an external source must be cited in the text where it is used.
    - Follow the chosen style's format for in-text citations (e.g., `[1]` for IEEE, `(Author, Year)` for APA).
3. **Reference List/Bibliography:**
    - Include a complete list of all cited sources at the end of the report.
    - The list should be formatted according to the chosen referencing style.
    - Ensure every in-text citation corresponds to an entry in the reference list, and vice-versa.
4. **Accuracy of References:** Double-check that all details in the reference list (author names, titles, dates, URLs) are accurate and complete.
5. **Plagiarism:** Be extremely careful to avoid plagiarism. Always cite your sources properly. Paraphrase information in your own words and still provide a citation. Use quotation marks for direct quotes.
6. **Tools:** Consider using reference management software (e.g., Zotero, Mendeley, EndNote) to help organize references and generate citations and bibliographies in the correct format.

By adhering to these guidelines, the project report will be professional, easy to read, credible, and meet academic standards.

---

### Appendix A: CEP Mapping

**Knowledge Areas (Ks):**

- **K3: Design and Development of Solutions (or K4: Design - if K3 is more about broader engineering solutions)**

  - **How addressed by 'TechReform BD v2':** This project directly addresses K3/K4 through the entire process of designing and developing the web application. This includes:
    - Conceptualizing the system architecture (MVT pattern).
    - Designing the database schema (ER diagrams, Django models for `Product`, `User`, `Order`, `PCBuild`, etc.).
    - Designing user interfaces and user experience (UI for product browsing, PC builder, cart, blog).
    - Implementing core functionalities like user authentication, product management, the PC builder logic (including compatibility checks), e-commerce transactions, and content management.
    - Selecting appropriate technologies and frameworks (Python, Django, potentially front-end libraries).
  - **Mapping to COs/POs (General Example - to be adapted to specific course/program outcomes):**
    - **COx:** Ability to design and develop software solutions for complex problems.
    - **POy:** Engineering Knowledge / Design/development of solutions.

- **K5: Tools and Technologies**

  - **How addressed by 'TechReform BD v2':** The project necessitates the use and understanding of various modern software development tools and technologies:
    - **Programming Language:** Python.
    - **Web Framework:** Django (including its ORM, templating engine, admin panel).
    - **Database:** SQLite (for development), potentially PostgreSQL/MySQL for production.
    - **Version Control System:** Git and platforms like GitHub/GitLab.
    - **Front-end Technologies:** HTML, CSS, JavaScript. Libraries/Frameworks like Tailwind CSS.
    - **Development Environment:** Code editors (VS Code), virtual environments.
    - **Testing Tools/Frameworks:** Django's built-in test framework, potentially `pytest`.
    - **Package Management:** `pip`.
  - **Mapping to COs/POs:**
    - **COx:** Proficiency in using modern engineering tools and technologies for software development.
    - **POy:** Modern Tool Usage.

- **K6: Professionalism and Ethics**
  - **How addressed by 'TechReform BD v2':**
    - **Project Management:** Adhering to a project timeline, managing tasks, and collaborating within a team (Sharif, Noor, Shornali) demonstrates professionalism.
    - **Code Quality & Documentation:** Writing maintainable code, commenting, and preparing a project report reflect professional software engineering practices.
    - **User Data Privacy (Ethical Consideration):** Implementing secure user authentication and (implicitly) handling user data responsibly (e.g., for registration, orders) touches upon ethical considerations in software.
    - **Intellectual Property:** Using open-source frameworks and libraries correctly (acknowledging licenses if required, though often permissive).
    - **Accessibility (Potential Ethical Consideration):** Designing a user-friendly and potentially accessible website.
  - **Mapping to COs/POs:**
    - **COx:** Understanding of professional and ethical responsibilities in engineering.
    - **POy:** The Engineer and Society / Ethics.

**Professional Skills (Ps):**

- **P1: Problem Analysis**

  - **How addressed by 'TechReform BD v2':**
    - Identifying the core problem: the fragmented experience for tech consumers and PC builders in Bangladesh.
    - Analyzing existing systems (PCPartPicker, Star Tech) to understand gaps and opportunities.
    - Breaking down the overall problem into smaller, manageable functional requirements for each app module (AuthApp, ProductsApp, PCBuilderApp, etc.).
  - **Mapping to COs/POs:**
    - **COx:** Ability to identify, formulate, and analyze complex engineering problems.
    - **POy:** Problem Analysis.

- **P3: Communication**

  - **How addressed by 'TechReform BD v2':**
    - **Team Communication:** Collaboration among project members (Sharif, Noor, Shornali) requires effective communication for task coordination, resolving issues, and integrating work.
    - **Written Communication:** This project report itself is a major exercise in written communication, detailing the project's motivation, design, methodology, and results.
    - **Code as Communication:** Well-commented and structured code communicates design intent to other developers (and future self).
    - **Commit Messages:** Clear Git commit messages communicate changes effectively.
  - **Mapping to COs/POs:**
    - **COx:** Ability to communicate effectively on complex engineering activities, both orally and in writing.
    - **POy:** Communication.

- **P7: Teamwork**
  - **How addressed by 'TechReform BD v2':**
    - The project is explicitly a team effort involving Sharif Md. Yousuf, Noor Mohammed Priom, and Shornali Akter.
    - Successful completion requires division of labor (e.g., different members might focus on different apps or features), integration of individual contributions, and collaborative problem-solving.
    - Using version control (Git) facilitates teamwork in a software development context.
    - Agile practices (daily stand-ups, sprint reviews if used) foster teamwork.
  - **Mapping to COs/POs:**
    - **COx:** Ability to function effectively as an individual and as a member or leader in diverse teams.
    - **POy:** Individual and Team Work.

**Attitudes (As):**

- **A1: Lifelong Learning**

  - **How addressed by 'TechReform BD v2':**
    - Learning and applying a complex web framework like Django.
    - Keeping up with best practices in web development, database design, and potentially front-end technologies.
    - Researching similar systems and new technologies (e.g., for future enhancements like AI).
    - Troubleshooting and learning from errors and challenges encountered during development.
  - **Mapping to COs/POs:**
    - **COx:** Recognition of the need for, and an ability to engage in, independent and life-long learning.
    - **POy:** Life-long Learning.

- **A4: Ethical and Social Responsibility**
  - **How addressed by 'TechReform BD v2':**
    - **Societal Impact:** Considering the effect of the project on society (as detailed in Section 4), such as increasing tech accessibility and empowering consumers.
    - **Data Privacy:** Designing systems that handle user data (registration, orders) securely and responsibly.
    - **Honest Representation:** Providing accurate product information and avoiding deceptive practices in an e-commerce context.
    - **Accessibility (if considered):** Striving to make the platform usable by a wide range of users, including those with disabilities.
    - **Responsible E-waste (Future Consideration):** Acknowledging the potential for e-waste and considering mitigations.
  - **Mapping to COs/POs:**
    - **COx:** Understanding of the impact of engineering solutions in a societal and environmental context, and demonstration of the knowledge of, and need for sustainable development.
    - **POy:** The Engineer and Society / Ethics / Environment and Sustainability.

`[Note: The specific COs (Course Outcomes) and POs (Program Outcomes) would need to be taken from the CSE-322 course syllabus and the academic program's defined outcomes to make the mapping precise.]`
