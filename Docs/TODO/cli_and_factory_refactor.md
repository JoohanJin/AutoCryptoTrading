# CLI & Factory Refactor Plan

## Overview
Add a management CLI so the trading bot can be started, restarted, stopped, or terminated without manual container work. Refactor object construction so each asset (BTC, XRP, etc.) uses a dedicated configuration bundle resolved via a factory. This eliminates downtime when onboarding a new market.

## CLI Lifecycle Controller
- Build a small `argparse`/`click` entry point (e.g. `python -m cli manage`) exposing verbs: `start`, `stop`, `restart`, `status`.
- When running in Docker, have subcommands wrap `docker compose up/down` or hit a supervisor API; otherwise use `subprocess` or a lightweight service manager (`systemd`, `pm2`).
- Ensure commands trap signals and shut down the bot gracefully (flush logs, close websockets).
- Optional: expose `--asset` to control which market instance is affected, enabling multiple assets to run concurrently.

## Factory for Asset-Specific Wiring (via CLI)
- Extend the CLI with commands like `cli assets list`, `cli assets configure --asset XRP --tp 0.15 --sl 0.05`, so operators can adjust live settings without editing files.
- Store asset configuration in a structured backend (YAML/JSON, SQLite, or environment overrides) and let the CLI read/write those entries safely.
- `ServiceFactory.create_trade_manager(asset)` pulls the latest config (possibly reloaded at runtime) and instantiates:
  - data feed / collectors tailored to that asset,
  - the TradeManager with injected dependencies and updated risk parameters,
  - shared utilities (score mappers, telegram bots) drawn from config.
- Adding or tweaking an asset becomes a CLI operation (`cli assets add --asset XRP --symbol XRP_USDT --leverage 5`), enabling config-only deployments with no downtime.

## Deployment Flow
1. Push code → GitHub Actions runs tests and builds the Docker image.
2. Image is published to GHCR with branch/sha tags.
3. Server pulls the latest tag automatically (Watchtower, script, or Action via SSH).
4. Use the CLI to start/stop/restart the target asset instance (`cli manage start --asset XRP`), achieving near-zero downtime while new assets come online.

## Next Steps
- [ ] Draft CLI skeleton with `click` and process control helpers.
- [ ] Extract asset configs into a dedicated module (e.g. `config/assets.yaml`).
- [ ] Implement `ServiceFactory` with dependency injection logic.
- [ ] Update Docs once MVP CLI & factory ship; add usage examples.
