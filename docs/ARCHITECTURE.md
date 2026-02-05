# MVC Architecture Documentation

## Django's MVT vs Classical MVC

Django uses the **MVT (Model-View-Template)** pattern, which is a variant of the classical MVC pattern. Here's how they map:

| Classical MVC | Django MVT | Location in Project |
|---------------|------------|---------------------|
| **Model** | Model | `encyclopedia/models.py` |
| **Controller** | View | `encyclopedia/views.py` |
| **View** | Template | `encyclopedia/templates/` |

### Why the naming difference?

- **Django's "View"** = In classical MVC, this would be the **Controller**
- **Django's "Template"** = In classical MVC, this would be the **View**
- **Django's "Model"** = Same as classical MVC **Model**

For documentation purposes, we refer to Django components using classical MVC terminology to align with academic requirements.

---

## Project Architecture

### Model Layer (Domain/Data)

**Location:** `encyclopedia/models.py`

**Purpose:** Encapsulates domain entities, business rules, and data access.

**Models:**
- `Period` - Geological time periods (Triassic, Jurassic, Cretaceous)
- `Dinosaur` - Dinosaur species with characteristics
- `UserProfile` - Extended user information and game stats
- `AlbumItem` - User's dinosaur collection tracking
- `GameScore` - Scores from mini-games

**Key Principles:**
- Models contain domain logic and validation
- No raw SQL; uses Django ORM
- Relationships defined through ForeignKey and OneToOneField

---

### Controller Layer (Business Logic/Orchestration)

**Location:** `encyclopedia/views.py` + `encyclopedia/services.py`

**Purpose:** Coordinates requests, processes business logic, and prepares responses.

#### Controllers (views.py)

**Authentication Controllers:**
- `login_view()` - Handles user authentication
- `register_view()` - Creates new user accounts
- `logout_view()` - Terminates user session
- `guest_login_view()` - Guest access

**Main Application Controllers:**
- `home_view()` - Landing page with navigation
- `map_view()` - Geological period explorer
- `gallery_list_view()` - Dinosaur browser with filters
- `dinosaur_detail_view()` - Individual dinosaur details
- `library_view()` - Educational content
- `profile_view()` - User statistics and settings
- `puzzleaurus_view()` - Puzzle game interface

#### Services (services.py)

**Purpose:** Separates reusable business logic from controllers.

**Functions:**
- `get_dinosaurs_by_period()` - Filter dinosaurs
- `get_user_progress()` - Calculate collection progress
- `update_user_tokens()` - Game currency management
- `collect_dinosaur()` - Add to user collection
- `save_game_score()` - Record game results

**Key Principles:**
- Controllers receive HTTP requests and return HTTP responses
- Controllers delegate business logic to services
- No direct template rendering logic in services
- Services are reusable across multiple controllers

---

### View Layer (Presentation)

**Location:** `encyclopedia/templates/`

**Purpose:** Renders HTML for user interface. Templates contain NO business logic.

**Template Structure:**
```
templates/
├── base.html              # Base layout with navigation
├── auth/
│   ├── login.html        # Login page
│   └── register.html     # Registration page
├── home.html             # Landing page
├── map.html              # Geological map
├── gallery/
│   ├── list.html         # Dinosaur list
│   └── detail.html       # Dinosaur details
├── library.html          # Educational content
├── profile.html          # User profile
└── puzzleaurus.html      # Game interface
```

**Key Principles:**
- Templates only display data passed from controllers
- No database queries in templates
- No business logic in templates
- Uses Django template language for rendering

---

## Data Flow (MVC Pattern)

### Request Flow

```
1. User Request (Browser)
   ↓
2. URL Router (urls.py)
   ↓
3. CONTROLLER (views.py)
   ├─→ calls SERVICE (services.py)
   │   ├─→ queries MODEL (models.py)
   │   └─→ returns data
   └─→ prepares context
   ↓
4. VIEW/Template (templates/)
   ↓
5. HTTP Response (HTML)
   ↓
6. User sees rendered page
```

### Example: Viewing Gallery

1. **Request:** User clicks "Gallery" → `/gallery/`
2. **Router:** `urls.py` routes to `gallery_list_view()`
3. **Controller:** `views.gallery_list_view()` is called
   - Checks request parameters (period filter, search query)
   - Calls `services.get_dinosaurs_by_period()`
4. **Service:** `services.get_dinosaurs_by_period()`
   - Queries `Dinosaur.objects.filter()`
5. **Model:** Django ORM fetches from database
6. **Controller:** Prepares context `{'dinosaurs': queryset, ...}`
7. **View:** Renders `gallery/list.html` with context
8. **Response:** HTML page sent to browser

---

## Separation of Concerns

### ✅ Good Practices (Followed)

- **Models** contain only database structure and domain logic
- **Controllers** coordinate flow but don't contain business rules
- **Services** contain reusable business logic
- **Templates** only display data, no logic

### ❌ Anti-Patterns (Avoided)

- ❌ Templates making database queries
- ❌ Controllers containing complex business logic
- ❌ Models rendering HTML
- ❌ Views (templates) accessing services directly

---

## URL Routing

**Location:** `encyclopedia/urls.py`

Maps URLs to controllers:

| URL | Controller | MVC Layer |
|-----|-----------|-----------|
| `/login/` | `login_view()` | Controller |
| `/register/` | `register_view()` | Controller |
| `/home/` | `home_view()` | Controller |
| `/map/` | `map_view()` | Controller |
| `/gallery/` | `gallery_list_view()` | Controller |
| `/gallery/<id>/` | `dinosaur_detail_view()` | Controller |
| `/library/` | `library_view()` | Controller |
| `/profile/` | `profile_view()` | Controller |
| `/puzzleaurus/` | `puzzleaurus_view()` | Controller |

---

## Project Structure

```
dino_encyclopedia/          # Django project configuration
├── settings.py            # Application settings
└── urls.py                # Main URL routing

encyclopedia/              # Main application (MVC components)
├── models.py             # MODEL: Domain entities
├── views.py              # CONTROLLER: Request handlers
├── services.py           # Business logic layer
├── urls.py               # URL routing
├── admin.py              # Django admin configuration
├── templates/            # VIEW: HTML templates
│   ├── base.html
│   ├── home.html
│   ├── map.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── gallery/
│   │   ├── list.html
│   │   └── detail.html
│   ├── library.html
│   ├── profile.html
│   └── puzzleaurus.html
└── management/
    └── commands/
        └── seed.py        # Database seeding

static/                    # Static files (CSS, images)
├── css/
│   └── style.css
└── images/

docs/                      # Documentation
├── ARCHITECTURE.md       # This file
└── diagrams/             # UML diagrams
    ├── source/           # Mermaid source files
    └── rendered/         # SVG/PNG exports

manage.py                  # Django management script
requirements.txt           # Python dependencies
```

---

## Technology Stack

- **Language:** Python 3.12+
- **Framework:** Django 5.0
- **Database:** SQLite
- **Frontend:** Django Templates + Bootstrap 5
- **Package Manager:** pip
- **Development Server:** Django runserver

---

## Summary

This project demonstrates a **classical MVC architecture** implemented with Django:

1. **Models** manage data and domain logic
2. **Controllers** (Django views) orchestrate requests and responses
3. **Views** (Django templates) present data to users
4. **Services** provide reusable business logic

The architecture ensures **separation of concerns**, making the codebase maintainable, testable, and educational.
