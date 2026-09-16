# Migrations

The development application creates its schema automatically to make the local demo runnable. For production, initialize Alembic with the chosen PostgreSQL URL and commit generated revisions; never mutate a deployed schema manually.
