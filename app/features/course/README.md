## Course Feature

This feature handles course creation, Excel import, JSON generation, and course-related validation.

Module layout:
- `routes.py`: all `course` routes and blueprint registration.
- `services.py`: course upload processing and persistence.
- `validator.py`: validations for course metadata and Excel payload.
- `importers.py`: database import helpers.
- `mappers.py`: Excel and JSON mapping logic.
- `parsers.py`: Excel and JSON parsing logic.
