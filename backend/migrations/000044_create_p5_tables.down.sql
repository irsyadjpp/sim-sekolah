-- Down migration: Remove P5 project tables
DROP TABLE IF EXISTS p5_project_dimension CASCADE;
DROP TABLE IF EXISTS p5_projects CASCADE;