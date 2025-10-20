# Response Parsing Helper Notes

## Summary
Implemented `CommonBaseSDK.parse_response` using Pydantic so REST clients can
optionally validate payloads before returning them. The helper lives in
`src/sdk/base_sdk.py` and is now used by the Binance and MEXC base callers.

## Expected Usage
- Callers can pass a Pydantic model into `parse_response(response, model=...)` to
  receive a validated object (or list of objects) instead of raw dictionaries.
- When no model is supplied, the helper falls back to returning the decoded JSON
  (dict/list) or text body.
- Validation errors raise `ValueError`, allowing higher layers to log or retry.

## Follow-Up Ideas
- Define concrete response models for critical endpoints to take advantage of
  the validation step.
- Capture metadata (status code, headers) in a typed envelope if future use
  cases require more context.
