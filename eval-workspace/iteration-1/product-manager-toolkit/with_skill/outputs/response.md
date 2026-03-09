# Automated Invoice Processing — MVP User Stories

## Epic: Invoice Processing Automation

**Epic Goal:** Enable users to upload PDF invoices, extract key fields automatically, and export structured data to accounting software.

**Primary Persona:** Accounts Payable Clerk — processes 50-200 invoices/month, needs speed and accuracy, uses QuickBooks/Xero/NetSuite.

---

### US-001: Upload PDF Invoices

**Priority:** Critical | **Points:** 5

```
As an Accounts Payable Clerk,
I want to upload one or more PDF invoices,
So that I can begin automated data extraction without manual data entry.
```

**Acceptance Criteria:**

1. **Given** the user is on the invoice processing dashboard, **When** they click "Upload Invoices," **Then** a file picker opens accepting `.pdf` files only.

2. **Given** the user selects up to 20 PDF files (max 10MB each), **When** they confirm the upload, **Then** all files upload with a progress indicator and each appears in the processing queue within 5 seconds.

3. **Given** the user drags PDF files onto the upload zone, **When** they drop the files, **Then** the system accepts them identically to the file picker flow.

4. **Given** the user uploads a non-PDF file (e.g., .jpg, .docx), **When** the upload is attempted, **Then** the system rejects it with the message "Only PDF files are supported" and does not add it to the queue.

5. **Given** the user uploads a PDF exceeding 10MB, **When** the upload is attempted, **Then** the system rejects it with the message "File exceeds 10MB limit" and suggests compressing the file.

6. **Given** a network interruption during upload, **When** connectivity resumes, **Then** the system retries the failed upload automatically or surfaces a "Retry" button.

---

### US-002: Extract Key Invoice Fields

**Priority:** Critical | **Points:** 8

```
As an Accounts Payable Clerk,
I want the system to automatically extract vendor name, invoice number, date, due date, total amount, tax, and line items from uploaded invoices,
So that I can eliminate manual data entry and reduce errors.
```

**Acceptance Criteria:**

1. **Given** a PDF invoice is uploaded and queued, **When** extraction completes, **Then** the system populates: vendor name, invoice number, invoice date, due date, subtotal, tax amount, total amount, and currency — each with a confidence score (0-100%).

2. **Given** the invoice contains line items, **When** extraction completes, **Then** each line item includes: description, quantity, unit price, and line total.

3. **Given** extraction completes, **When** any field has a confidence score below 80%, **Then** that field is highlighted in amber and flagged "Needs Review."

4. **Given** extraction completes, **When** the user views the results, **Then** the original PDF is displayed side-by-side with extracted fields for visual verification.

5. **Given** a scanned (image-based) PDF is uploaded, **When** extraction runs, **Then** the system applies OCR and extracts fields with the same structure as text-based PDFs.

6. **Given** a corrupted or password-protected PDF is uploaded, **When** extraction is attempted, **Then** the system marks it as "Extraction Failed" with a reason and prompts the user to re-upload.

7. **Given** a batch of 20 invoices, **When** extraction runs, **Then** all invoices complete processing within 60 seconds total.

---

### US-003: Review and Correct Extracted Data

**Priority:** High | **Points:** 5

```
As an Accounts Payable Clerk,
I want to review extracted invoice data and correct any errors before exporting,
So that I can ensure data accuracy without re-entering the entire invoice.
```

**Acceptance Criteria:**

1. **Given** extraction is complete, **When** the user opens the review screen, **Then** all extracted fields are displayed in editable form fields alongside the source PDF.

2. **Given** a field is flagged "Needs Review," **When** the user clicks on it, **Then** the corresponding region on the PDF is highlighted so the user can verify the source.

3. **Given** the user edits a field value, **When** they save changes, **Then** the system persists the correction, removes the "Needs Review" flag, and sets confidence to 100%.

4. **Given** the user has reviewed all flagged fields, **When** no "Needs Review" flags remain, **Then** the invoice status changes to "Verified" and the "Export" action becomes enabled.

5. **Given** the user wants to skip review, **When** all fields have confidence ≥95%, **Then** the invoice is auto-marked "Verified" and available for immediate export.

6. **Given** the user modifies line items (add, edit, or delete a row), **When** they save, **Then** the subtotal and total recalculate automatically.

---

### US-004: Export Invoices to Accounting Software

**Priority:** High | **Points:** 5

```
As an Accounts Payable Clerk,
I want to export verified invoice data to my accounting software (QuickBooks, Xero, or NetSuite),
So that I can complete the AP workflow without switching between systems.
```

**Acceptance Criteria:**

1. **Given** the user has connected their accounting platform via OAuth in settings, **When** they click "Export" on a verified invoice, **Then** the invoice data is pushed to the connected platform and the status updates to "Exported."

2. **Given** the user selects multiple verified invoices, **When** they click "Export Selected," **Then** all selected invoices are exported in a single batch and each status updates to "Exported."

3. **Given** the accounting platform returns a validation error (e.g., unknown vendor), **When** the export fails, **Then** the system displays the specific error, sets status to "Export Failed," and allows the user to correct and retry.

4. **Given** no accounting integration is connected, **When** the user clicks "Export," **Then** the system offers CSV download as a fallback with columns matching the standard import format of QuickBooks, Xero, and NetSuite.

5. **Given** an invoice was previously exported, **When** the user attempts to export it again, **Then** the system warns "This invoice was already exported on [date]. Export again?" requiring confirmation to prevent duplicates.

---

### US-005: View Invoice Processing History

**Priority:** Medium | **Points:** 3

```
As an Accounts Payable Clerk,
I want to view a searchable history of all processed invoices,
So that I can track processing status, find past invoices, and audit the AP pipeline.
```

**Acceptance Criteria:**

1. **Given** the user navigates to "Invoice History," **When** the page loads, **Then** a table displays all invoices sorted by upload date (newest first) with columns: vendor, invoice number, date, amount, status (Queued / Extracted / Verified / Exported / Failed).

2. **Given** the user types in the search bar, **When** they enter a vendor name, invoice number, or amount, **Then** results filter in real-time (within 300ms) across all fields.

3. **Given** the user clicks a filter chip for status (e.g., "Needs Review"), **When** applied, **Then** only invoices matching that status are displayed and the count updates.

4. **Given** the user clicks on an invoice row, **When** the detail view opens, **Then** it shows the full extracted data, the original PDF, edit history, and export timestamps.

---

## MVP Summary

| ID | Story | Points | Priority |
|----|-------|--------|----------|
| US-001 | Upload PDF Invoices | 5 | Critical |
| US-002 | Extract Key Invoice Fields | 8 | Critical |
| US-003 | Review and Correct Extracted Data | 5 | High |
| US-004 | Export to Accounting Software | 5 | High |
| US-005 | View Invoice Processing History | 3 | Medium |
| | **Total** | **26** | |

**Sprint fit:** At ~28-point velocity, this MVP is achievable in a single sprint with the extraction engine (US-002) as the critical-path item. If capacity is tighter, US-005 can defer to sprint 2 as a stretch goal.
