"""
Plain language content for fullshtack.
No jargon. No mystery. Just explanations that make sense.
"""

# The main pitch
HERO_TITLE = "fullshtack"
HERO_SUBTITLE = "the whole thing. no mystery meat."

LANDING_PITCH = """
**Look.**

Those AI website builders are neat. Type a wish, get a website. Magic.

But here's what they don't tell you:

The moment you need to change something *real* - not the color, not the font,
the actual thing it *does* - you're standing in a codebase you've never seen before,
built by an AI that already forgot why it made the choices it made.

You didn't build it. You ordered it. And now you're stuck reverse-engineering
your own project.

---

**This is different.**

We're not going to generate a website for you while you watch.

We're going to build it *with* you. Step by step. In plain English.

You'll know where everything is because you put it there.
You'll understand why it works because we explained it like humans,
not like a CS textbook trying to impress other CS textbooks.

Is it slower than typing "make me an Airbnb clone"?
Yeah.

Will you actually know what the hell you have at the end?
Also yeah.

---

**This is for people who want to learn the shit by doing the shit.**

Not by watching an AI do the shit and hoping you absorb it through vibes.
"""

# Step explanations - what we're actually doing at each stage
STEP_EXPLANATIONS = {
    "project": {
        "title": "what are we building?",
        "subtitle": "let's start with the basics, in normal words",
        "explanation": """
Before we write a single line of code, let's just talk about what you're making.

Not "define your project requirements" - just... what is it?
A tool for tracking something? A site where people can do a thing?
An app that connects people who have X with people who need X?

Tell me like you'd tell a friend who asked "so what are you working on?"
        """,
        "why_this_matters": """
Here's why we do this first: every decision that comes after flows from this.

If you're building a blog, you need posts and maybe comments.
If you're building a marketplace, you need sellers, buyers, and listings.
If you're building a tool, you need users and whatever they're tracking.

The clearer you are now, the less "wait, I need to redo everything" later.
        """
    },

    "nouns": {
        "title": "what are the nouns?",
        "subtitle": "the things your app keeps track of",
        "explanation": """
Every app is basically: people doing things with stuff.

Let's figure out what "stuff" your app has.

- Users (obviously, almost always)
- But what else? Products? Posts? Messages? Properties? Tasks?

Just list the nouns. The things. We'll figure out how they connect in a sec.

*Tech translation: this is "data modeling" or "defining your schema" -
but those words don't help you think clearly about what you actually need.*
        """,
        "why_this_matters": """
Your database is just a filing cabinet for these nouns.

Each noun becomes a "table" - a spreadsheet, basically.
Each thing you track about that noun becomes a "column" in the spreadsheet.

A User might have: email, name, password (encrypted), when they signed up.
A Post might have: title, content, who wrote it, when.

This is the skeleton of your app. Everything else hangs off of it.
        """
    },

    "auth": {
        "title": "how do people get in?",
        "subtitle": "the login situation",
        "explanation": """
Does your app need user accounts?

If yes: how should people log in?

- **Just email & password** - the classic
- **Google/social login** - one click, uses their existing account
- **Both** - let them choose
- **No login needed** - it's a public tool, no accounts required

*Tech translation: this is "authentication" - but that word makes it sound
more complicated than "checking if someone is who they say they are."*
        """,
        "why_this_matters": """
Auth touches everything. It's not just the login page.

It's: who can see what? Who can edit what? What happens when you're not logged in?

We set this up properly now so you're not hacking it in later and creating
security holes because you're tired and it's 2am.
        """
    },

    "pages": {
        "title": "what pages exist?",
        "subtitle": "the screens people actually see",
        "explanation": """
Let's map out your app like a house.

What rooms are there? Front door (home page), obviously. Then what?

- A page where people sign up?
- A page where they see their stuff?
- A page where they create new stuff?
- A settings page?

Just list them. We'll worry about what's on each page in a minute.

*Tech translation: this is "routing" - but it's really just
"what URLs exist and what do you see when you go there."*
        """,
        "why_this_matters": """
Your pages are the skeleton of the user experience.

Each page usually does one main thing:
- Show a list of things
- Show one thing in detail
- Let you create/edit a thing
- Let you configure settings

Knowing your pages means knowing what components you'll need.
And which nouns show up where.
        """
    },

    "styling": {
        "title": "pick a vibe",
        "subtitle": "how should this thing look?",
        "explanation": """
We're not going to pretend CSS isn't annoying. It is.

But picking a general direction now saves hours of "why doesn't this look right" later.

Pick a vibe:

- **Clean & Corporate** - Lots of white space, professional, trustworthy
- **Friendly & Rounded** - Softer edges, warmer colors, approachable
- **Minimal & Sharp** - Less is more, stark contrasts, modern
- **Brutalist & Weird** - Intentionally raw, anti-design design

*Tech translation: this determines your CSS framework, spacing scale,
border radius defaults, and color palette - but you don't need to know that.*
        """,
        "why_this_matters": """
A consistent visual language makes your app feel "finished" even when it's not.

We'll set up design tokens (fancy word for "the handful of colors,
fonts, and sizes you'll reuse everywhere") so everything matches automatically.

You can always change it later. But having a starting point beats
staring at an unstyled page wondering where to begin.
        """
    }
}

# Component explanations
COMPONENT_EXPLANATIONS = {
    "button": {
        "what_it_is": "A clickable thing that does something when you click it.",
        "what_it_needs": "Text to display, and what should happen when clicked.",
        "common_uses": "Submit forms, trigger actions, navigate somewhere.",
        "gotchas": "Buttons inside forms behave differently than buttons outside forms."
    },
    "form": {
        "what_it_is": "A container for inputs that collects data and sends it somewhere.",
        "what_it_needs": "Input fields, a submit button, and somewhere to send the data.",
        "common_uses": "Sign up, log in, create/edit anything, search.",
        "gotchas": "Always validate on the server too. Never trust the browser alone."
    },
    "input": {
        "what_it_is": "A box where someone types something.",
        "what_it_needs": "A label (what to type), a name (how to identify it), and validation (what counts as valid).",
        "common_uses": "Email, password, names, search queries, any text.",
        "gotchas": "Use the right type (email, password, number) - it changes the keyboard on mobile."
    },
    "card": {
        "what_it_is": "A contained box that groups related content together.",
        "what_it_needs": "Content to display. Usually has a consistent structure (image, title, description, action).",
        "common_uses": "Displaying items in a list/grid - products, posts, users, anything.",
        "gotchas": "Keep cards in a grid consistent. Same info in the same places."
    },
    "nav": {
        "what_it_is": "The menu that lets people move between pages.",
        "what_it_needs": "Links to your pages. Usually shows different options for logged-in vs logged-out users.",
        "common_uses": "Header navigation, sidebar navigation, mobile hamburger menu.",
        "gotchas": "Should clearly show where you currently are."
    },
    "modal": {
        "what_it_is": "A popup that appears over the page, demanding attention.",
        "what_it_needs": "Content to display, a way to close it, and a trigger to open it.",
        "common_uses": "Confirmations ('are you sure?'), quick forms, important alerts.",
        "gotchas": "Don't overuse. If everything is a modal, nothing is."
    },
    "table": {
        "what_it_is": "Data organized in rows and columns. A spreadsheet view.",
        "what_it_needs": "Column headers and row data. Often needs sorting and filtering.",
        "common_uses": "Admin panels, data-heavy views, comparison features.",
        "gotchas": "Terrible on mobile. Consider card layouts for smaller screens."
    },
    "list": {
        "what_it_is": "Items displayed one after another, vertically.",
        "what_it_needs": "Items to display. Usually each item is clickable.",
        "common_uses": "Messages, notifications, simple item displays.",
        "gotchas": "Long lists need pagination or infinite scroll. Don't load 10,000 items."
    }
}


# Error messages in plain language
ERROR_MESSAGES = {
    "empty_name": "You gotta call it something. What's the working title?",
    "empty_description": "Even a rough idea helps. What does it do, in a sentence?",
    "no_nouns": "Every app tracks *something*. What are the things in yours?",
    "no_pages": "People need somewhere to go. What's the first page they see?",
    "duplicate_noun": "You already have one of those. Did you mean something different?",
    "invalid_path": "Page paths should look like /something or /something/else - no spaces, lowercase.",
}


# Success messages
SUCCESS_MESSAGES = {
    "project_saved": "got it. we know what we're building now.",
    "nouns_saved": "nice. your data model makes sense.",
    "auth_saved": "login situation: handled.",
    "pages_saved": "your app has a map now.",
    "style_saved": "looking good. well, it will be.",
    "all_done": "nice. you have a working app skeleton. you know where everything is. nothing weird hiding in the closet."
}


# AI explanation templates
def explain_like_human(tech_concept: str) -> str:
    """Translate tech jargon to normal words."""
    translations = {
        "api endpoint": "a spot where your app sends/receives data",
        "database query": "asking your database for specific information",
        "authentication": "checking if someone is who they say they are",
        "authorization": "checking if someone is allowed to do what they're trying to do",
        "middleware": "code that runs between 'request comes in' and 'response goes out'",
        "state management": "keeping track of what's happening in your app right now",
        "component": "a reusable piece of your interface",
        "props": "the settings/data you pass into a component",
        "hook": "a way to tap into React's features in a function",
        "schema": "the structure of your data - what fields exist and what type they are",
        "migration": "a script that changes your database structure",
        "orm": "code that lets you talk to your database using your programming language instead of SQL",
        "rest api": "a standard way to structure your app's data endpoints",
        "crud": "create, read, update, delete - the four basic things you do with data",
        "jwt": "a secure token that proves someone is logged in",
        "session": "remembering who someone is while they're using your app",
        "environment variables": "secret settings that shouldn't be in your code",
        "deployment": "putting your app on the internet so people can use it",
        "ssl/https": "encryption that keeps data safe between the user and your server",
        "cors": "browser security that controls which sites can talk to your app",
    }

    return translations.get(tech_concept.lower(), f"'{tech_concept}' - honestly, look this one up, it's context-dependent")
