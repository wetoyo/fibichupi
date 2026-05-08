# System Blueprint (_a.k.a._ "Design Doc")

## TNPG: Fibichupi
## project: name
## Target ship date: {2026-06-05}

---

#### roster: Wesley Leon (PM), Kyle Liu, Jake Liu, Mottaqi


| Name | Email | Primary Role | Secondary Role |
|---|---|---|---|
|Wesley Leon|wesleyl30@nycstudents.net| | |
|Kyle Liu|kylel114@nycstudents.net| | |
|Jake Liu|jakel110@nycstudents.net| | |
|Mottaqi|mottaqia2789@nycstudents.net| | |

---


# Summary
We are making a polymarket clone, using github commits as currency. Users will be able to create bets that they will release decisions on, and also bet on bets.

## Problem Being Solved
This app is for people who want to bet on anything going on in the world using a fake currency.

## Target Users

Who will use this system?

- users who want to practice betting on prediction markets
- users who want to have fun


## Why This Project Matters
An risk-free alternative to other prediction markets.

---

# Minimum Viable Product (MVP) Scope

## Core Features (Required for Final Submission)
Features that **must** be completed:
1. betting
2. price graph

## Stretch Features (Only if MVP is Complete)
1. leaderboard

## Explicit Non-Goals

Features intentionally excluded:
-
-

---

# Technology Stack

| Layer | Selected Tool |
|---|---|
| Backend Framework | Flask |
| Frontend Framework | tailwind |
| Database | SQLite |
| Authentication | Flask sessions |
| ORM / DB Library | none |

## Why This Stack Was Chosen
We are using Flask because it is what we are most familiar with. We chose to use Tailwind because it does not use a default theme like Bootstrap or Foundation, allowing our team greater control over our styling. We want to use a database structure that is easy to use and perform efficient data retrieval and management, so we decided on SQLite's relational database.

---

# Team Ownership Plan

Each member must own meaningful deliverables.

| Team Member | Primary Ownership | Secondary Ownership | Specific Deliverables |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
| | | | |

---

# Component map

{Insert your mermaid(or equivalent)-generated diagram here}

# Site map

{Insert your mermaid(or equivalent)-generated diagram here}
eg...
```
Landing Page
   ↓
Login / Register
   ↓
Dashboard
   ├── Feature A
   ├── Feature B
   └── Profile
```

## Key User Stories
### eg0
As a __________, I want to __________ so that...

### eg1
As a __________, I want to __________ so that...

### eg2
As a __________, I want to __________ so that...



# Database Design

{Insert your table/document organizational structure here}


# Testing Plan
{Delineate here your plan for testing each component}

# Timeline
## Week 1 Goals: login and register setup, homepage set up with questions
## Week 2 Goals: users able to bet on questions
## Week 3 Goals: clean up design of app
## Internal Deadlines:
{List milestones your team has identified, in the order they must be completed. Set a target completion date for each.}


# Completion Criteria (_a.k.a._ "Definition of 'Done'")
Project is considered complete when all of the following are true:
1. users can bet on Questions
2. users are rewarded accordingly to the result of the question

# Open Questions
{Delineate anything undecided here}
