# Website Weakness Scanner

A modular Python tool to audit HTTP headers, cookies, and HTML forms for common security weaknesses.

**A Python-based tool to automate basic website security checks for developers.**

This tool is designed for **developers or testers** who want to quickly identify common security oversights in their websites. It automates the task of checking headers, cookies, and forms, ensuring that basic security measures aren’t missed during development.

---

## **Workflow / How it Works**

1. **User Input**

   * The scanner prompts the user to enter a website URL.
   * Input is validated and normalized to ensure it is a proper HTTP or HTTPS URL.
   * **Valid input examples:**

     * `google.com`
     * `https://linkedin.com`
     * `http://example.org`
   * **Invalid input examples:**

     * `google`
     * `linkedin`
     * `justtext`
   * Invalid URLs trigger an error and the user is prompted to try again.

2. **Request & Response**

   * The scanner sends a request to the URL and retrieves the response.
   * If the site redirects, the final destination is followed and used for analysis.
   * Response data captured includes:

     * Status code
     * Headers
     * Cookies
     * HTML body

3. **HTML Parsing**

   * The raw HTML is parsed into a DOM structure.
   * Forms are extracted from the page (input fields, methods, CSRF tokens if present).
   * If no forms are found or parsing fails, the tool logs an **error finding** instead of crashing.

4. **Analyzers**
   The scanner runs multiple independent analyzers:

   * **Header Analyzer:**

     * Checks common security headers:

       * Content-Security-Policy (CSP)
       * X-Frame-Options
       * X-Content-Type-Options
       * Referrer-Policy
       * Strict-Transport-Security (HSTS)
     * Reports **present / missing**.
   * **Cookie Analyzer:**

     * Checks cookie security attributes:

       * Secure flag (HTTPS only)
       * HttpOnly
       * SameSite
     * Reports **absent, unsafe, or error** if cookies cannot be read.
   * **Form Analyzer:**

     * Checks forms for:

       * Method type (GET / POST)
       * Presence of CSRF tokens
     * Reports **safe / missing protections / error** if forms cannot be analyzed.

5. **Reporting**

   * Generates a structured report with **all findings**:

     * Severity (LOW / MEDIUM)
     * Status (present, missing, error, absent)
     * Why it matters (brief explanation of potential risk)
     * Remediation tip (what developer should do)
   * Ensures visual separation for readability.
   * If one analyzer fails, the tool continues executing the others.

6. **Interactive Loop**

   * After a scan, the user can enter another URL to scan.
   * Type `exit` to quit the program.
   * Ensures the user has time to read the report before the program ends.

---

## **Example Findings**

* **[MEDIUM] Content-Security-Policy**

  * Status: missing
  * Why it matters: Controls which resources the browser is allowed to load.
  * Remediation: Define a Content-Security-Policy header to restrict allowed resources.

* **[LOW] X-Frame-Options**

  * Status: present
  * Why it matters: Prevents the page from being embedded in frames or iframes.
  * Remediation: Add the X-Frame-Options header to control iframe embedding.

* **[LOW] Cookie Analysis**

  * Status: error
  * Why it matters: Could not read cookies from response.
  * Remediation: Inspect cookies manually.

* **[LOW] Form Analysis**

  * Status: error
  * Why it matters: Form analysis could not be completed.
  * Remediation: Manually inspect forms if applicable.

---

## **Who Is This For?**

* **Web developers** who want to ensure they haven’t skipped basic security checks during development.
* **Testers / QA engineers** who need a quick check for header, cookie, and form protections.
* Not designed as a full penetration testing tool or a network vulnerability scanner.

---

## **Error Handling & Stability**

* If **any step fails** (HTTP request fails, HTML cannot be parsed, analyzers throw exceptions), the program:

  * Does not crash
  * Logs an **error finding** instead
  * Continues executing the remaining analyzers

This ensures developers get as much useful information as possible even if part of the scan cannot be completed.

---

## **Requirements**

* Python 3.8+
* Libraries:

  * `requests`
  * `beautifulsoup4`

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## **How to Run**

```bash
python main.py
```

* Follow prompts to enter URLs.
* Type `exit` to quit.

---

