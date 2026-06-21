# ADR 0002: AI Tool Registry Pattern

## Status
Accepted

## Context
The `AIService` class currently contains a large `if-elif` block to execute different AI tools. This violates the Single Responsibility Principle and the Open/Closed Principle. Adding a new tool requires modifying the core `AIService` class, increasing the risk of regressions and making the file excessively large.

## Decision
We will implement a Tool Registry Pattern. 
- Individual tools will be encapsulated in their own handler functions or classes.
- A centralized `ToolRegistry` will manage the mapping between tool names, their schemas, and their execution handlers.
- `AIService` will delegate tool execution to this registry.

## Consequences
- **Positive:** Tools become modular, independently testable, and easier to extend. `AIService` becomes leaner and focused solely on orchestration.
- **Negative:** Introduces an extra layer of abstraction, which requires developers to register tools explicitly.
