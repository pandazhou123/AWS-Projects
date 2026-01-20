# Project Title

## Overview
Brief description of the project and its purpose.

This project demonstrates how to **Host a Static Website** using AWS services, with an emphasis on cost efficiency, security best practices, and clean teardown.

---

## Architecture

This project uses Amazon S3 static website hosting to serve a simple, serverless website.

Four S3 buckets are created:
- `example.com` – primary bucket hosting the website content
- `www.example.com` – secondary bucket configured to redirect all requests to `example.com`
- `example.com-logs` - logging bucket for Primary Bucket
- `example.com-cf-logs` - CloudFront Logging Bucket

## CloudFront Distribution
- Set Origin to be Primary S3 Bucket
- Set Log Destination to be CF Logging Bucket

## Server Logging Buckets
- Set **Bucket Policy** on Primary S3 Bucket to Allow Logging
- On Primary S3 Bucket, set logging destination to Logging Bucket in Server Access Logs


### Design Rationale
Separating the root domain and `www` subdomain ensures a consistent user experience by redirecting all traffic to a single canonical domain.
