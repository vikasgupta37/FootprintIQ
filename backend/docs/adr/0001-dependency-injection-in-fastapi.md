# ADR 0001: Dependency Injection in FastAPI

## Status
Accepted

## Context
Our FastAPI routes currently instantiate services directly (e.g., `service = CarbonService(db)`). This tight coupling between the API layer and the service layer makes unit testing difficult, as we cannot easily inject mock services. It also violates the Dependency Inversion Principle (SOLID).

## Decision
We will use FastAPI's built-in dependency injection system (`Depends()`) to inject services into our route handlers. We will create a new module `app/api/dependencies/services.py` containing provider functions for each service.

## Consequences
- **Positive:** Improved testability and decoupling of controllers from service implementations. Easier to switch out implementations if needed.
- **Negative:** Slightly more boilerplate in the `deps` module, though it centralizes service creation logic.
