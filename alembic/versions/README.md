# Alembic migration revisions live here.
#
# The existing database was created from the raw SQL in
# Database/asparagus_management_project/*.sql. To adopt Alembic without
# recreating tables:
#
#   1) Generate a baseline that reflects the current schema:
#        alembic revision --autogenerate -m "baseline existing schema"
#   2) Mark the live database as already at that revision (no DDL is run):
#        alembic stamp head
#
# From then on, new schema changes are added with:
#        alembic revision --autogenerate -m "describe change"
#        alembic upgrade head
