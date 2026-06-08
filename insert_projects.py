import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

projects = [

    (
        "VisiTrack",
        "Visitor management system for tracking and managing visitor records efficiently.",
        "Python, Flask, SQLite",
        "https://github.com/yourusername/visitrack"
    ),

    (
        "College Event Management Website",
        "Web platform for event registration and management in college.",
        "HTML, CSS, JavaScript, Flask",
        "https://github.com/yourusername/event-management"
    ),

    (
        "Personal Portfolio Website",
        "Responsive full-stack portfolio website showcasing projects and skills.",
        "Flask, SQLite, HTML, CSS, JavaScript",
        "https://github.com/yourusername/portfolio"
    )

]

cursor.executemany("""
INSERT INTO projects
(title, description, tech_stack, github_link)
VALUES (?, ?, ?, ?)
""", projects)

conn.commit()
conn.close()

print("Projects inserted successfully!")