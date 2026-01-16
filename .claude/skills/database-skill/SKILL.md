---
name: database-skill
description: Use this Skill when designing databases, creating tables, managing migrations, and defining schemas for applications.
---

# Database Skill – Tables, Migrations & Schema Design

## Instructions

Follow these steps whenever database structure or schema management is required.

### 1. Schema Planning
- Identify entities (users, orders, products, etc.)
- Define relationships (one-to-one, one-to-many, many-to-many)
- Choose appropriate primary keys
- Normalize data to avoid redundancy

### 2. Table Creation
- Define table names clearly and consistently
- Use appropriate data types for each column
- Add primary keys and indexes
- Apply constraints (NOT NULL, UNIQUE, FOREIGN KEY)

### 3. Relationships
- Use foreign keys to enforce data integrity
- Decide cascade rules (ON DELETE, ON UPDATE)
- Avoid circular dependencies
- Index foreign keys for performance

### 4. Migrations
- Create migration files for schema changes
- Ensure migrations are reversible (up/down)
- Apply migrations in order
- Never edit applied migrations directly

### 5. Schema Evolution
- Add new columns via migrations
- Avoid destructive changes in production
- Use defaults for new non-null fields
- Deprecate fields safely

### 6. Performance & Optimization
- Add indexes to frequently queried columns
- Avoid over-indexing
- Use appropriate data types for size efficiency
- Analyze query performance regularly

### 7. Best Practices
- Use consistent naming conventions
- Keep schema simple and readable
- Backup database before migrations
- Test migrations in staging environments

---

**Use this Skill whenever database structure, migrations, or schema design is involved in a project.**