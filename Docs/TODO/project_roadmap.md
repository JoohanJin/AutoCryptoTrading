# Auto Crypto Trading Bot – Roadmap Notes

This document captures the outstanding TODO items from the master list and adds context, possible sub‑tasks, and any caveats. Keep the original items intact; if something becomes unnecessary note it rather than deleting it.

---

## Exception Handling
- **Custom Exception Hierarchy**  
  - Draft domain-specific base exceptions (e.g., `AutoTradeError`, `ExchangeError`, `RiskViolationError`).  
  - Map network/SDK errors into the new hierarchy to standardise logging and retries.
- **Construct the Risk Model**  
  - Define quantitative limits (position sizing, max drawdown, leverage caps).  
  - Embed guardrails in TradeManager; raise the new risk exceptions when breached.  
  - Optional: persist recent risk metrics so the CLI can report status.

## API Service Interface Layer (DIP)
- Specify abstract interfaces for REST/WebSocket clients so higher layers depend on protocols, not concrete SDKs.  
- Provide adapters for Binance/MEXC implementing the interface; use dependency injection to swap them in tests.  
- Note: If a full interface layer feels heavy right now, start with protocol typing and expand later.

## Base API Service Layer Refactor
- Consolidate shared HTTP concerns (auth signing, retries, response parsing) into a reusable helper.  
- Remove duplicated logic across `binance.base_sdk`, `mexc.base_sdk`, sdk/base classes.  
- Ensure logging and error translation use the new exception hierarchy.

## Technical Analysis Module
- Extract indicators/calculations from managers into a dedicated module (e.g., `analysis/technical.py`).  
- Provide pure functions/classes so they are easy to unit test and reuse.  
- Optional: add a strategy registry so multiple indicator stacks can coexist.

## Factory Design Architecture
- Finalise the `ServiceFactory` plan (see `cli_and_factory_refactor.md`).  
- Ensure factories consume CLI-managed configuration to instantiate asset-specific TradeManagers, data collectors, and pipelines.  
- Add validation so misconfigured assets fail fast with actionable errors.

## Comprehensive Unit Testing (Top Priority)
- Aim for coverage across managers, pipelines, analysis, and factories.  
- Mock external dependencies (REST/WebSocket) to keep tests deterministic.  
- Integrate into CI workflow; fail builds when critical modules lack tests.  
- Consider snapshot tests for CLI output and configuration commands.

## Async Implementation
- Evaluate moving blocking I/O (REST polling, websocket callbacks) onto asyncio.  
- Identify modules that would benefit most (e.g., concurrent data feeds).  
- Plan migration path—may start with async wrappers while keeping core logic synchronous to avoid a big-bang rewrite. Optional if current threading suffices.

## Network API Refactor
- **MexC WebSocket Retry (High Priority)**  
  - Ensure auto-reconnect logic handles auth, resubscriptions, and exponential backoff.  
  - Add metrics/logging for reconnect attempts to monitor stability.
- **Binance REST Retry**  
  - Centralise retry/backoff for REST calls with idempotency awareness.  
- **MexC REST Retry**  
  - Mirror the Binance approach; respect exchange-specific rate limits.  
- **Response Type Handling**  
  - Standardise response parsing and typing so callers receive predictable data structures.  
  - Optional: introduce pydantic/dataclasses for validation.

## Deployment / Ops Completed Items
- ✅ Submit address proof to Binance.  
  - ☐ Verify Windows laptop IP is cleared to send trading orders (observe live order placement).  
  - ☐ Confirm open-order polling continues to work post-IP validation.
- ✅ Deploy v1_0_0 → v1_0_2.  
  - ✅ Linux/Windows servers provisioned.  
  - ✅ Feature set implemented.  
  - ✅ Docker container prepared.  
  - Optional follow-up: automate GHCR push + server rollout (see overall DevOps plan).
