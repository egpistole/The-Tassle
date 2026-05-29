# GradRegistry — Complete Deployment Guide
### Written for absolute beginners. No coding experience required.

---

## Before We Start: A Few Plain-English Definitions

Don't worry if you've never heard these terms before — we'll explain every single one as we go.

| Term | What it actually means |
|------|------------------------|
| **Terminal** | A text-only window where you type commands to control your computer, like a chat window but for talking to the computer itself |
| **Command** | A short instruction you type and press Enter to make the computer do something |
| **Virtual environment** | A private, self-contained box just for this project's tools — keeps things tidy so it doesn't mess with anything else on your computer |
| **Dependencies** | Extra pieces of software our app needs to run, listed in `requirements.txt` |
| **Database** | A file that stores all your users, registry items, and party details |
| **Environment variable** | A secret setting stored outside the code — like a password you tell the app privately |
| **Production** | When your app is live on the internet for real people to use |
| **Deploy** | Putting your app on a server so the internet can reach it |
| **Server** | A computer that runs 24/7 so your website is always available |

---

# PART 1 — Local Setup (Running On Your Own Computer)

This gets the app running on your own computer so you can see it in your browser before putting it online.

---

## Step 1: Check That Python Is Installed

**What is Python?** Python is the programming language this app is written in. Your computer needs it to run the app.

### On a Mac:
1. Press **Command + Space** to open Spotlight Search
2. Type **Terminal** and press Enter — a window with a black or white background and a blinking cursor appears. That's your Terminal.
3. In the Terminal, type exactly this and press Enter:
   ```
   python3 --version
   ```
4. **Success looks like:** You see something like `Python 3.11.4` — any number starting with 3 is fine.
5. **If you see "command not found":** Go to https://www.python.org/downloads/ and click the big yellow "Download Python" button. Run the installer, then come back and try again.

### On Windows:
1. Press the **Windows key**, type **Command Prompt**, and press Enter. That dark window is your Terminal equivalent.
2. Type this and press Enter:
   ```
   python --version
   ```
3. **Success looks like:** `Python 3.11.4` or similar.
4. **If it says "not recognized":** Download Python from https://www.python.org/downloads/ — **important:** during installation, check the box that says "Add Python to PATH" before clicking Install.

---

## Step 2: Get the Project Files Onto Your Computer

**If you received a ZIP file:**
1. Find the ZIP file (probably in your Downloads folder)
2. Double-click it to unzip it — a folder called `grad-registry` will appear
3. Move that folder somewhere easy to find, like your Desktop

**If you received the files another way:**
Make sure you have a folder called `grad-registry` containing `app.py`, `models.py`, etc.

---

## Step 3: Open Your Terminal IN the Project Folder

This is important — your Terminal needs to be "inside" the grad-registry folder.

### On a Mac:
1. Open **Finder** and navigate to your `grad-registry` folder
2. Right-click (or Control-click) the folder
3. Select **"New Terminal at Folder"** (if you don't see this, go to System Settings → Privacy & Security → Full Disk Access and enable Terminal)
4. A Terminal window opens that's already in your folder ✓

**Alternative Mac method:**
1. Open Terminal normally
2. Type `cd ` (with a space after it — don't press Enter yet)
3. Drag the `grad-registry` folder from Finder into the Terminal window — the path fills in automatically
4. Now press Enter

### On Windows:
1. Open your `grad-registry` folder in File Explorer
2. Click in the address bar at the top (where it shows the folder path)
3. Type `cmd` and press Enter — a Command Prompt opens inside that folder ✓

**How to confirm you're in the right place:** Type `dir` (Windows) or `ls` (Mac) and press Enter. You should see files like `app.py`, `models.py`, `requirements.txt` listed.

---

## Step 4: Create a Virtual Environment

**Why do this?** A virtual environment is like a clean room just for this project. It prevents this app's tools from interfering with anything else on your computer.

Type this command and press Enter:

**Mac/Linux:**
```
python3 -m venv venv
```

**Windows:**
```
python -m venv venv
```

**What's happening:** Python creates a new folder called `venv` inside your project. This is the "clean room."

**Success looks like:** The command finishes with no red error text. A new `venv` folder appears.

---

## Step 5: Activate the Virtual Environment

**Why?** You need to "step into" the clean room before using it.

**Mac/Linux:**
```
source venv/bin/activate
```

**Windows:**
```
venv\Scripts\activate
```

**Success looks like:** Your command prompt now shows `(venv)` at the very beginning of the line, like this:
```
(venv) your-computer:grad-registry you$
```
That `(venv)` means you're inside the virtual environment. 

**⚠️ Important:** Every time you close and reopen your Terminal, you'll need to run this activate command again before working on the project.

**Troubleshooting (Windows):** If you see "cannot be loaded because running scripts is disabled," type this and press Enter:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try the activate command again.

---

## Step 6: Install the App's Dependencies

**What are dependencies?** They're extra pieces of software our app needs — like Flask (the web framework), SQLAlchemy (the database tool), etc. They're all listed in `requirements.txt`.

With your virtual environment active (you see `(venv)` in your prompt), type:

```
pip install -r requirements.txt
```

**What's happening:** `pip` is Python's package installer. It reads `requirements.txt` and downloads everything on the list.

**Success looks like:** Lots of text scrolls by showing packages being downloaded and installed, ending with "Successfully installed..." and a list of package names. This can take 1–3 minutes.

**If you see errors:** Make sure you see `(venv)` in your prompt first. If not, go back to Step 5.

---

## Step 7: Set Up the Database

**What is the database?** It's a file (like a very organized spreadsheet) that stores all your app's data — user accounts, registry items, party details. We need to create it.

Run this command:
```
flask db-init
```

Or if that doesn't work:
```
python -c "from app import create_app; from models import db; app = create_app(); app.app_context().push(); db.create_all(); print('Done!')"
```

**Success looks like:** You see `Done!` and a new file called `grad_registry.db` appears in your folder.

---

## Step 8: Create a Secret Key

**What is a secret key?** It's a long random password the app uses internally to keep sessions and forms secure. You need to set it before running.

Create a file called `.env` in your `grad-registry` folder. You can do this in any text editor (Notepad on Windows, TextEdit on Mac set to plain text).

Put exactly this content in the file:

```
SECRET_KEY=change-this-to-any-long-random-string-you-make-up
FLASK_ENV=development
```

Replace `change-this-to-any-long-random-string-you-make-up` with anything you want — mash the keyboard for 30 characters. Example: `zxq99KLmP3rainbow77Tuesday!cats`

Save the file as `.env` (with the dot at the start, no other extension).

**⚠️ Mac note:** Files starting with `.` are hidden by default. In Finder, press **Command + Shift + .** to toggle hidden files visible.

---

## Step 9: Run the App!

Type this command:
```
flask run
```

**Success looks like:**
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

Open your web browser and go to: **http://127.0.0.1:5000**

You should see the GradRegistry homepage! 🎉

**To stop the app:** Go back to Terminal and press **Ctrl+C**.

---

# PART 2 — Preparing for Production

Before putting your app on the internet, a few things need to change.

---

## Understanding Environment Variables

**What are environment variables?** They're settings you give the app privately — outside the code itself. This way your passwords and secret keys aren't stored in files that could be shared accidentally.

For production, you'll need these variables (we'll show you exactly where to enter them in Part 3):

| Variable | What it does | Example value |
|----------|-------------|---------------|
| `SECRET_KEY` | Secures sessions and forms | `any-long-random-string-50+chars` |
| `DATABASE_URL` | Tells the app where the database is | Provided automatically by Railway/Render |
| `FLASK_ENV` | Tells the app it's in production mode | `production` |

**How to make a good SECRET_KEY:** Go to https://djecrety.ir/ and click Generate — copy that string.

---

## What Is PostgreSQL and Why Switch?

**SQLite** (what we use locally) is a single file — great for development on your laptop, but not reliable when many people visit at once on a live server.

**PostgreSQL** is a proper database server designed to handle many users simultaneously. Railway and Render provide it automatically — you don't install anything yourself. When you connect your app to their PostgreSQL service, they give you a `DATABASE_URL` that you paste in as an environment variable. The app handles the rest.

---

## What Is Gunicorn?

**Gunicorn** (pronounced "green unicorn") is a production-grade web server. When you run `flask run` locally, it uses a tiny built-in server meant for testing only — it can only handle one visitor at a time. Gunicorn handles many visitors at once properly.

It's already in `requirements.txt`, so it's installed. On Railway and Render, they'll ask how to start your app — you'll tell them:
```
gunicorn app:application
```
This means: "Use Gunicorn to run the `application` object from `app.py`."

---

# PART 3 — Deploying Live (Step-by-Step for Render — Free Tier)

**Render** (render.com) is the easiest free option. It gives you a live URL like `gradregistry.onrender.com` for free.

---

## Step 1: Create a Render Account

1. Go to **https://render.com**
2. Click **"Get Started for Free"**
3. Sign up with your GitHub account (or create a free GitHub account first at https://github.com)
4. **What is GitHub?** It's a website that stores code online — Render reads your code from there to deploy it.

---

## Step 2: Put Your Code on GitHub

**What is a repository?** It's a project folder stored on GitHub.

1. Go to **https://github.com** and log in
2. Click the **+** button in the top right → **"New repository"**
3. Name it `grad-registry`, make it **Private**, click **"Create repository"**
4. On the next screen, under "…or push an existing repository," you'll see commands. We'll use GitHub Desktop instead:

**Using GitHub Desktop (easiest):**
1. Download **GitHub Desktop** from https://desktop.github.com
2. Sign in with your GitHub account
3. Click **File → Add Local Repository**
4. Find your `grad-registry` folder
5. Click **"Publish repository"** → make it Private → click Publish
6. Your code is now on GitHub ✓

**Before pushing: Create a `.gitignore` file** in your `grad-registry` folder containing:
```
venv/
*.db
.env
__pycache__/
*.pyc
instance/
```
This prevents your virtual environment, database, and secret `.env` file from being uploaded to GitHub.

---

## Step 3: Create a PostgreSQL Database on Render

1. In your Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Give it a name like `gradregistry-db`
3. Choose **Free** tier
4. Click **"Create Database"**
5. Wait about 1 minute for it to be ready
6. Click on it, and find the **"Internal Database URL"** — copy it and save it somewhere. It starts with `postgresql://...`

---

## Step 4: Create the Web Service on Render

1. Click **"New +"** → **"Web Service"**
2. Click **"Connect account"** if prompted, then select your `grad-registry` GitHub repository
3. Fill in the settings:

   | Setting | What to enter |
   |---------|--------------|
   | **Name** | `gradregistry` (or anything you like) |
   | **Region** | Choose whichever is closest to you |
   | **Branch** | `main` |
   | **Root Directory** | Leave blank |
   | **Runtime** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `gunicorn app:application` |
   | **Plan** | Free |

4. Scroll down to **"Environment Variables"** and click **"Add Environment Variable"** for each:

   | Key | Value |
   |-----|-------|
   | `SECRET_KEY` | Your long random string (from djecrety.ir) |
   | `DATABASE_URL` | The PostgreSQL URL you copied in Step 3 |
   | `FLASK_ENV` | `production` |

5. Click **"Create Web Service"**

---

## Step 5: Wait for Deployment

Render will:
1. Download your code from GitHub
2. Install all dependencies
3. Start your app with Gunicorn

**This takes 3–5 minutes the first time.**

You'll see a log of what's happening. When it says **"Your service is live 🎉"** — you're done!

**Success looks like:** A green "Live" badge next to your service name, and a URL like `https://gradregistry.onrender.com` at the top of the page.

Click the URL — your app is live on the internet!

---

## Step 6: Initialize the Database on the Live Server

The database tables need to be created on the live server too.

1. In your Render service page, click the **"Shell"** tab
2. A terminal opens — type this command:
   ```
   python -c "from app import create_app; from models import db; app = create_app(); app.app_context().push(); db.create_all(); print('Done!')"
   ```
3. Press Enter — you should see `Done!`

Your live database is ready. ✓

---

## Connecting a Custom Domain (Optional)

If you own a domain name (like `www.sarahjohnsongrads.com`), you can point it to your Render app:

1. In your Render service, click **"Settings"** → **"Custom Domains"** → **"Add Custom Domain"**
2. Enter your domain name and click **"Save"**
3. Render shows you two DNS records to add (a CNAME or A record)
4. Log in to wherever you bought your domain (GoDaddy, Namecheap, Google Domains, etc.)
5. Find the DNS settings (sometimes called "DNS Management" or "Name Servers")
6. Add the records Render showed you — exactly as shown
7. Wait up to 48 hours for the domain to connect (usually much faster — often under 1 hour)

---

# PART 4 — Post-Deployment Checklist

Run through these tests after deploying to make sure everything works.

---

## ✅ Basic Functionality

- [ ] Visit your app URL — the homepage loads without errors
- [ ] Click **"Register"** — fill in a name, email, and password and submit
- [ ] You're logged in and see the dashboard
- [ ] Click **"Edit Profile"** — fill in your graduation details and save
- [ ] Toggle **"Make my page public"** to ON and save
- [ ] Add a party details entry with a date and location
- [ ] Add at least 2 registry items (with a price and external URL)
- [ ] Add an external registry link (paste any URL, like amazon.com)

## ✅ Guest/Public Experience

- [ ] Copy your shareable link from the dashboard
- [ ] Open it in a **private/incognito browser window** (so you're not logged in)
- [ ] Your public profile loads — you can see your name, party details, and registry
- [ ] Click a registry item's **"View Item"** link — it opens the product page in a new tab ✓
- [ ] Click your external registry card — it opens in a new tab ✓
- [ ] Click **"Mark as Purchased"** on an item — the item shows as claimed afterward

## ✅ Search Page

- [ ] Go to the search page (linked in the nav)
- [ ] Search your own name — your profile card appears
- [ ] Click the card — goes to your public profile

## ✅ Account Settings

- [ ] Go to Account Settings from the nav
- [ ] Change your email — confirm it updates
- [ ] Log out and log back in with your new email

## ✅ External Links

All links to outside websites should:
- Open in a **new tab** (not replace your current page)
- Actually work (not give a 404 error)

## ✅ Mobile Check

- [ ] Open your app on a phone or tablet
- [ ] The layout adjusts — text is readable, buttons are tappable, nothing overflows off the screen

---

## Common Issues and Fixes

**App won't start on Render / shows "Build Failed":**
- Click "Logs" on your Render service to read the error
- Most common cause: a typo in the Start Command — make sure it says `gunicorn app:application`

**Database errors after deploying:**
- You likely skipped Step 6 (initializing the database). Go to the Shell tab and run the `db.create_all()` command again.

**SECRET_KEY error:**
- Make sure you added the `SECRET_KEY` environment variable in Render. It cannot be blank.

**"Internal Server Error" on pages:**
- Check the Render logs (Logs tab). The error will be clearly described there.

**Free tier goes to sleep:**
- Render's free tier spins down after 15 minutes of inactivity. The first visit after sleep takes ~30 seconds to wake up. This is normal for the free tier. Upgrade to a paid plan ($7/month) to stay always-on.

**Forgot your password:**
- On the login page, ask your database admin (you!) to reset it via the Render Shell:
  ```
  python -c "
  from app import create_app
  from models import db, User
  app = create_app()
  with app.app_context():
      u = User.query.filter_by(email='your@email.com').first()
      u.set_password('newpassword123')
      db.session.commit()
      print('Password updated')
  "
  ```

---

## Keeping Your App Updated

When you make changes to the code and want them live:

1. Make your changes in your `grad-registry` folder
2. Open GitHub Desktop → you'll see the changed files listed
3. Write a short note in the "Summary" box (like "Added new feature")
4. Click **"Commit to main"**
5. Click **"Push origin"**
6. Render automatically detects the new code and redeploys — takes 2–3 minutes

---

*You did it! Your graduation registry app is live on the internet. 🎓*
