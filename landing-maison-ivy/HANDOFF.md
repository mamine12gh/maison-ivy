I'm continuing the build of my Shopify landing page for a kids' voice sticker printer. Read everything below before doing anything, then confirm your plan with me.

## Who I am and the brand
- Store: Maison Ivy (Shopify, domain maison-ivy.com, currency USD, Basic plan). The brand is Maison Ivy: do not invent another brand, and never use the name "Stickerbox".
- Product name: "The Idea Printer". Slogan: "If they can say it, it prints it." Button label everywhere: "Get my Idea Printer →".
- Page language: English.

## Where my documents are
GitHub repo: github.com/mamine12gh/maison-ivy (public), branch `claude/landing-page-conversion-mockup-onwtns`, folder `landing-maison-ivy/`:
- `docs/MaisonIvy_2_Proposition_finale.pdf`: the final proposal. It is the source of truth: follow its structure religiously (sections S0 to S17, in order), its copy, offer, visual identity and image prompts (IMG-01 to IMG-28).
- `docs/MaisonIvy_1_Analyse_des_options.pdf`: why each choice was made (3 options per element, scored).
- `maquette/index.html`: the interactive mockup (French version of the page). Published at https://claude.ai/artifact/QZkYRYDgmFcEyFKdrbbq9S
- `shopify/`: the theme files already uploaded to Shopify (section, layout, template, snippet) and local render screenshots in `shopify/preview/`.
- The original plan PDF ("Plan de landing page · Imprimante à stickers vocale", 11/10/2026) is the strategy behind all of this; I can upload it again if needed.

## What already exists in Shopify
- Products (all DRAFT):
  - The Idea Printer, gid://shopify/Product/8803438854305, handle `the-idea-printer`, option "Kit": Starter Kit $79 (variant 48122369933473), Creative Kit $99 (48122369966241, pre-selected on the page), Siblings Kit $149 (48122369999009). Template suffix: `idea-printer`.
  - Idea Printer Refill - 5 Rolls, $25 (handle `idea-printer-refill-5-rolls`)
  - Washable Markers - Set of 12, $12 (handle `washable-markers-set-of-12`)
  - Sticker Binder, $9 (handle `sticker-binder`)
- Themes: the live theme is "Updated copy of Atelier" (MAIN, gid://shopify/OnlineStoreTheme/154886209697). The landing page lives ONLY in the unpublished copy "Atelier - Idea Printer landing" (gid://shopify/OnlineStoreTheme/155219165345), in these files:
  - `sections/idea-printer-landing.liquid` (the whole page S0-S17, self-contained CSS/JS, settings for values to confirm, image slots as "Image" blocks)
  - `layout/idea-printer.liquid` (minimal layout: no store menu or footer)
  - `templates/product.idea-printer.json`
  - `snippets/ip-media.liquid` (shows the image, or a placeholder labelled with its ID and the size to produce)
  - `snippets/ip-url-test.liquid` is a leftover test file to delete in the code editor.
- The page has not yet been checked in a real browser on the store, only rendered locally.

## Technical lessons already learned
- The Shopify connector cannot write to the live (MAIN) theme or delete theme files; it can write to unpublished themes.
- themeFilesUpsert: GraphQL documents are limited to 16 KB, so large files are uploaded with body type URL pointing to the raw GitHub file at a specific commit SHA (the repo is public). Check the result with the file's checksumMd5.
- Section schema limits: at most 40 settings, labels at most 70 characters, header content at most 50 characters. A rejected file fails silently in the async job: test a small file with body type TEXT to see the error message.

## Rules to keep
- No fake urgency (no countdown, no fake stock). The only deadline is the real Christmas shipping date.
- No invented reviews or testimonials on a published page: the examples are labelled EXAMPLE and must be replaced or switched off (section setting "Show example testimonials and reviews") before publishing.
- The stickers in the ideas gallery must be real prints from the machine, never AI drawings.
- No crossed-out "usual price": the savings shown are the real sum of the items sold separately.
- Values still to confirm with the supplier/sample: stickers per roll (60), battery life (4 h), size and weight, minimum age (4), voice handling, Wi-Fi setup, content filters, Christmas deadline (December 18), contact email (hello@maison-ivy.com does not exist yet).

## What I want you to do now
1. Open my Shopify admin in Chrome, open the theme "Atelier - Idea Printer landing" in the theme editor, and preview the product "The Idea Printer". Check every section on mobile and desktop against the final proposal, and list anything broken or different.
2. Fix what is broken, in the repo files first, then upload them to the unpublished theme (never touch the live theme without asking me).
3. Then help me with the next steps: images (using the prompts in the proposal and my product reference photos), real reviews app, activating the products, and going live.

Ask me before any action that publishes something, changes the live theme, or makes products visible to customers.
