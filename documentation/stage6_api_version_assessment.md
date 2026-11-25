# Stage 6 — MoSPI CPI API version assessment (18 November 2026)

## Finding

There are two distinct API descriptions and their parameters must not be conflated.

1. The current eSankhyiki CPI catalogue labels its API v2.0.0, documents `GET /api/cpi/getCPIData`, calls it open/guest-access with optional bearer token, and describes paginated JSON responses. The full OpenAPI schema did not render in the research environment.
2. The separate official MoSPI CPI API user manual documents the older registration/login flow, a 15-minute token and says unauthenticated requests return only the first 10 records. It shows the older `/api/getCPIIndex` group/subgroup path.
3. The publicly indexed `nso-india/esankhyiki-mcp` CPI Swagger document is version 1.0.11 and defines `/api/cpi/getCPIIndex`, with bearer-token security and parameters including `base_year`, `series`, `year`, `month_code`, `state_code`, `group_code`, `subgroup_code`, `sector_code`, `limit`, `page` and `Format`. It identifies state code 99 as All India, and sector codes 1–3 for Rural/Urban/Combined. The item endpoint's state/sector parameters are restricted to the 2024 base.

These are not proven to be interchangeable specifications. A direct API request from this execution environment did not return a usable payload, and the container network did not resolve the MoSPI hosts. Therefore the CPI API is a documented acquisition route, not a completed data retrieval. The project must record the exact live schema and request payload before pulling any records.

## What this means for the project

- Prefer the CPI Warehouse export if the team can access it, archiving the untouched source bytes and filters.
- Otherwise inspect the live v2.0.0 OpenAPI definition and test a very small known query against an official press-release value before downloading the full 2013–2025 Urban group panel.
- Do not assume v1.0.11 parameter names work against `getCPIData`.
- Do not treat ten-row Swagger samples or truncated output as the complete dataset.
- Save all response pages and the exact metadata/schema; hash the untouched responses before cleaning.

## Sources

- Current eSankhyiki CPI catalogue: https://esankhyiki.mospi.gov.in/macroindicators?product=cpi&tab=api
- Official CPI API user manual: https://www.api.mospi.gov.in/API/CPI%20API%20User%20Manual.pdf
- Publicly indexed CPI Swagger v1.0.11: https://github.com/nso-india/esankhyiki-mcp/blob/main/swagger/swagger_user_cpi.yaml
- MoSPI CPI Warehouse/FAQ: https://cpi.mospi.gov.in/ and https://mospi.gov.in/faq
