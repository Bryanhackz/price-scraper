# Security Policy

## Supported Versions
Currently, only the latest `main` branch is supported.

## Scope
This is a local command-line tool. It is not exposed as a network service. The user explicitly provides the target URL, so Server-Side Request Forgery (SSRF) is not applicable in its current form. The primary security focus is on the safe parsing of untrusted HTML and ensuring the tool does not get blocked by target servers.

## Reporting a Vulnerability
Please do not report security vulnerabilities through public GitHub issues. Send an email to **br4yangil006@gmail.com**. You should receive a response within 48 hours.

Please include:
- Type of issue (e.g., HTML parser crash, arbitrary file write)
- Full paths of source file(s) related to the issue
- Step-by-step instructions to reproduce the issue
- Impact of the issue
