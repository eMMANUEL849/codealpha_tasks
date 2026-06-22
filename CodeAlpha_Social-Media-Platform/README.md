# SocialSpace – Mini Social Media Platform

A full-stack social media web application built with **Django** (backend) and **HTML/CSS/JavaScript** (frontend) as part of the CodeAlpha internship tasks.

---

## Features

| Feature | Details |
|---|---|
| **User Profiles** | Avatar, bio, website, follower/following/post counts |
| **Posts** | Create text posts with optional image, delete your own posts |
| **Comments** | Add and delete comments (AJAX – no page reload) |
| **Likes** | Toggle like/unlike on any post (AJAX) |
| **Follow System** | Follow/unfollow users; followers & following modals on profile |
| **Feed** | Home feed shows posts from people you follow |
| **Explore** | Search users and posts; browse trending content |
| **Real-time Notifications** | Toast pop-ups + bell badge for likes, comments, and new followers (10-second polling) |
| **Notifications Page** | Full history of all interactions with unread highlighting |
| **Authentication** | Register, login, logout with form validation |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3 · Django 6 |
| Database | SQLite (via Django ORM) |
| Frontend | HTML5 · CSS3 · Vanilla JavaScript (AJAX fetch) |
| Image handling | Pillow |

---

## Project Structure

```
CodeAlpha_Social-Media-Platform/
├── socialplatform/          # Django project settings & root URLs
│   ├── settings.py
│   └── urls.py
├── core/                    # Main application
│   ├── models.py            # Profile, Post, Like, Comment, Follow, Notification
│   ├── views.py             # All views + JSON API endpoints
│   ├── forms.py             # Register, Login, Post, Profile, Comment forms
│   ├── urls.py              # URL routing
│   └── admin.py             # Admin registrations
├── templates/
│   ├── base.html            # Navbar, toast container, notification polling
│   ├── feed.html            # Home feed with post composer
│   ├── profile.html         # User profile with followers/following modals
│   ├── explore.html         # Search & trending posts
│   ├── notifications.html   # Notification history
│   ├── edit_profile.html    # Profile settings
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   └── partials/
│       └── post_card.html   # Reusable post card component
├── static/
│   ├── css/style.css        # Full CSS with variables, responsive layout
│   └── js/main.js           # AJAX interactions + real-time notification polling
├── media/                   # Uploaded avatars and post images
└── manage.py
```

---

## Database Models

```
User (Django built-in)
 └── Profile        – bio, avatar, website
 └── Post           – content, image, author
     └── Like       – user + post (unique together)
     └── Comment    – author, post, content
 └── Follow         – follower + following (unique together)
 └── Notification   – recipient, sender, type (like/comment/follow), post, is_read
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/codealpha_tasks.git
cd codealpha_tasks/Social-Media-Platform

# 2. Install dependencies
pip install django pillow

# 3. Apply migrations
python manage.py migrate

# 4. (Optional) Create a superuser for admin access
python manage.py createsuperuser

# 5. Run the development server
python manage.py runserver
```

Open your browser at **http://127.0.0.1:8000**

---

## Demo Accounts

You can seed sample data by running:

```bash
python manage.py shell < seed.py
```

Or register your own account at `/register/`.

---

## Real-time Notifications

The notification system uses **client-side polling** (every 10 seconds):

1. When a user likes a post, comments, or follows someone a `Notification` record is created in the database.
2. The frontend polls `/api/notifications/unread/` every 10 s.
3. New notifications appear as **toast pop-ups** (bottom-right) and update the **bell badge** in the navbar.
4. Visiting `/notifications/` or clicking the bell marks all as read.

---

## Pages & URLs

| URL | Page |
|---|---|
| `/` | Home feed (auth required) |
| `/register/` | Create account |
| `/login/` | Sign in |
| `/explore/` | Search & explore |
| `/profile/<username>/` | User profile |
| `/settings/profile/` | Edit profile |
| `/notifications/` | Notification history |
| `/admin/` | Django admin panel |

---

## Screenshots

> Register → Login → Feed → Profile → Notifications

---

## License

This project was built as part of the **CodeAlpha** internship program.
