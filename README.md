# turonsf.com

Hugo static site for Michael Turon for SFUSD Board of Education.

## Local build

```bash
hugo --minify
```

## Local preview

```bash
hugo server --bind 127.0.0.1 --baseURL http://127.0.0.1:1313/
```

## Live blockers before production

- Replace the Brevo placeholder URL in `hugo.toml`.
- Fill the live Umami `umami_website_id`.
- Verify ActBlue, Action Network, and Brevo backend destinations.
- Complete Sam Ray and Lauren Turon preflight review.
