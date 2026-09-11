"""
custom_tech_skills.py

ESCO is a stable, broad labor-market taxonomy — it deliberately does NOT
track fast-moving specific tools, frameworks, and platforms. This module
supplements ESCO with exactly those things, so the skill matcher can catch
resume mentions of e.g. "Kubernetes" or "React" that ESCO will never contain.

This list is intentionally a plain Python list (not pulled from an external
source) since there's no single authoritative "current tech tools" taxonomy
the way there is for broad competencies. Extend it over time as you notice
gaps in real resumes.
"""

CUSTOM_TECH_SKILLS = [
    # Programming languages
    "Python", "Java", "JavaScript", "TypeScript", "Go", "Rust", "C++", "C#",
    "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R",

    # Web frameworks
    "React", "Angular", "Vue.js", "Next.js", "Django", "Flask", "FastAPI",
    "Spring Boot", "Express.js", "Ruby on Rails", "ASP.NET",

    # Cloud & infrastructure
    "AWS", "Azure", "Google Cloud Platform", "GCP", "EC2", "S3", "Lambda",
    "Docker", "Kubernetes", "Terraform", "Ansible", "Jenkins",
    "GitHub Actions", "CircleCI",

    # Data & messaging
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "Kafka", "RabbitMQ",
    "Elasticsearch", "Snowflake", "BigQuery", "dbt", "Airflow",

    # ML / data science
    "TensorFlow", "PyTorch", "scikit-learn", "Pandas", "NumPy",
    "Hugging Face", "spaCy", "Keras", "XGBoost", "LangChain",

    # BI & analytics tools
    "Tableau", "Power BI", "Looker", "Google Analytics",

    # Dev practices / tools
    "Git", "GitHub", "GitLab", "CI/CD", "Microservices", "REST API",
    "GraphQL", "gRPC", "Agile", "Scrum", "Unit Testing",
]