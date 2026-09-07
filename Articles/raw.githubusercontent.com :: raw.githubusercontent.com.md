---
url: https://raw.githubusercontent.com/zocomputer/skills/main/manifest.json
---

# raw.githubusercontent.com

```
{
  "tarball_url": "https://codeload.github.com/zocomputer/skills/tar.gz/refs/heads/main",
  "archive_root": "skills-main",
  "skills": [
    {
      "name": "humation-avatar",
      "description": "A Zo Computer skill for adding Humation avatars to agent products. It covers installing Humation npm packages into target projects, React integration, Core SVG rendering, static SVG generation, browser ESM usage in zo.space page routes, and legacy Humation SVG API compatibility.",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "yusuke.zo.computer",
        "status": "zo-user-ready",
        "version": "0.4.1",
        "created": "2026-05-16T00:00:00.000Z",
        "updated": "2026-07-06T00:00:00.000Z",
        "language": "en"
      },
      "display": {
        "specVersion": "0.2.0",
        "icon": "user-round-cog",
        "tags": [
          "avatars",
          "agents",
          "react",
          "svg",
          "design"
        ]
      },
      "slug": "humation-avatar",
      "path": "Community/humation-avatar",
      "date_added": "2026-07-05"
    },
    {
      "name": "clarion-expected-return-calc",
      "description": "Compute the equity-vs-T-bill allocation for the Value bucket (50% of portfolio). Implements the Expected-Return Framework — looks up the historical 10-year forward return from the S&P 500 Shiller CAPE, computes the regime-adjusted hurdle (rf + regime premium), and produces a 5-tier verdict (STRONG EQUITY / LEAN EQUITY / NEUTRAL / LEAN T-BILLS / MAXIMUM T-BILLS) with recommended Value-bucket equity/T-bill split. Use when the user asks \"should I be in stocks or bonds right now?\", \"what's the equity hurdle?\", \"is the market overvalued?\", \"what's the right Value bucket allocation?\", or before adding any new equity to the Value bucket. Requires clarion-setup to have been run.",
      "metadata": {
        "author": "cis.zo.computer",
        "category": "External",
        "display-name": "Clarion Expected Return",
        "homepage": "https://github.com/jingerzz/clarion-intelligence-system"
      },
      "slug": "clarion-expected-return-calc",
      "path": "External/clarion-expected-return-calc",
      "date_added": "2026-05-08"
    },
    {
      "name": "clarion-living-letter-update",
      "description": "Update the annual investor letter at ~/clarion/letters/{YEAR}-letter.md with a new quarterly section, or finalize it at year-end. Auto-fills the system-deterministic parts (regime snapshot, thesis health table, portfolio bucket positions from active theses); marks the narrative-heavy parts (What We Did, What We Learned, Year in Context, Mistakes & Lessons, Looking Ahead) as [TODO] for the user to write with chat assistance. Append-only — refuses to overwrite an already-populated quarter without --force. Use when the user asks \"update the letter\", \"quarterly letter update\", \"finalize the letter\", or \"write the {Q1/Q2/Q3/Q4} entry\". Requires clarion-setup to have been run.",
      "metadata": {
        "author": "cis.zo.computer",
        "category": "External",
        "display-name": "Clarion Living Letter",
        "homepage": "https://github.com/jingerzz/clarion-intelligence-system"
      },
      "slug": "clarion-living-letter-update",
      "path": "External/clarion-living-letter-update",
      "date_added": "2026-05-08"
    },
    {
      "name": "clarion-regime-check",
      "description": "Reads the SPY/TLT/RSP color regime and the equity hurdle rate. Use when the user asks about the market regime, risk-on / risk-off, market color, SPY/TLT regime, breadth, or what hurdle rate to use for new positions. Pulls daily bars via yfinance (cached locally). Optionally accepts a 1Y T-bill yield to compute the equity hurdle rate. Requires clarion-setup to have been run.",
      "metadata": {
        "author": "cis.zo.computer",
        "category": "External",
        "display-name": "Clarion Regime Check",
        "homepage": "https://github.com/jingerzz/clarion-intelligence-system"
      },
      "slug": "clarion-regime-check",
      "path": "External/clarion-regime-check",
      "date_added": "2026-05-08"
    },
    {
      "name": "clarion-sec-research",
      "description": "Pull, index, and search SEC EDGAR filings for any public company. Supports 10-K and 10-Q (annual/quarterly with curated section extraction for risk factors, MD&A, business, and financials), Form 3/4/5 (insider transactions), 8-K (material events), DEF 14A (proxy/governance), S-1 (IPO/registration), 20-F (foreign private issuers), and any other SEC form by name. Use when the user asks about a company's SEC filings, risk factors, MD&A, insider transactions, executive compensation, business description, or wants to analyze a specific filing in plain English. Single ticker or multiple tickers (comma-separated). On first request for a ticker+form, indexing happens in the background (1-5 min). Subsequent queries are fast. Requires clarion-setup to have been run.",
      "metadata": {
        "author": "cis.zo.computer",
        "category": "External",
        "display-name": "Clarion SEC Research",
        "homepage": "https://github.com/jingerzz/clarion-intelligence-system"
      },
      "slug": "clarion-sec-research",
      "path": "External/clarion-sec-research",
      "date_added": "2026-05-08"
    },
    {
      "name": "clarion-setup",
      "description": "Bootstraps the Clarion Intelligence System on Zo Computer. Run this once after installing — clones the source repo, installs the ai_buffett_zo Python library, creates the workspace data tree under /home/workspace/clarion/ (auto-detected on Zo), auto-installs all nine sibling clarion-* skills (regime-check, sec-research, single-stock-eval, expected-return-calc, value-screener, thesis-write, thesis-monitor, watchlist-update, living-letter-update) under /home/workspace/Skills/, and registers the sec-indexer background service. Idempotent (safe to re-run). The only manual step is one batched human checkpoint near the end (SEC EDGAR name + email, and creating the ZO_API_KEY secret). Persona routing for Clarion is opt-in via a separate prompt after install (\"install Clarion personas and routing rules\"). Use when the user asks to \"set up Clarion\" or \"install Clarion\".",
      "metadata": {
        "author": "cis.zo.computer",
        "category": "External",
        "display-name": "Clarion Setup",
        "homepage": "https://github.com/jingerzz/clarion-intelligence-system"
      },
      "slug": "clarion-setup",
      "path": "External/clarion-setup",
      "date_added": "2026-05-08"
    },
    {
      "name": "clarion-single-stock-eval",
      "description": "Evaluate a single stock using the Buffett lens. Pulls a quality snapshot from yfinance, current SPY/TLT regime context, and snippets from the indexed SEC filings across four dimensions (moat, management, financial trends, risks). The chat agent reasons over the structured output to produce a written evaluation. Use when the user says \"evaluate <TICKER>\", \"is <TICKER> a buy?\", \"Buffett evaluation of <TICKER>\", \"what's <TICKER>'s moat?\", or asks about a specific company's management, financials, or risks. Requires clarion-setup to have been run, and the ticker to be indexed first via clarion-sec-research.",
      "metadata": {
        "author": "cis.zo.computer",
        "category": "External",
        "display-name": "Clarion Single-Stock Eval",
        "homepage": "https://github.com/jingerzz/clarion-intelligence-system"
      },
      "slug": "clarion-single-stock-eval",
      "path": "External/clarion-single-stock-eval",
      "date_added": "2026-05-08"
    },
    {
      "name": "clarion-thesis-monitor",
      "description": "Monitor the health of every active thesis in ~/clarion/theses/. For each one — refresh price, recompute Risk Environment from the current regime, check kill conditions (read from the file's status column), aggregate to an Overall score, recommend an action (EXIT / REDUCE / HOLD / ADD), and write the updated scores + history back to the thesis file. Produces a dashboard surfacing what needs attention. Use when the user asks \"monitor my theses\", \"thesis health check\", \"any kill conditions triggered?\", \"what's the action on <TICKER>\", or as part of a daily / weekly review. Requires clarion-setup to have been run.",
      "metadata": {
        "author": "cis.zo.computer",
        "category": "External",
        "display-name": "Clarion Thesis Monitor",
        "homepage": "https://github.com/jingerzz/clarion-intelligence-system"
      },
      "slug": "clarion-thesis-monitor",
      "path": "External/clarion-thesis-monitor",
      "date_added": "2026-05-08"
    },
    {
      "name": "clarion-thesis-write",
      "description": "Scaffold a new thesis document for a ticker in the canonical Clarion thesis format. Pre-fills the YAML metadata block, opens the History with an OPENED entry, and (when filings are indexed) seeds the \"Why I Believe It\" evidence section with draft citations from the Buffett-lens search. The user fills in the actual prose. Outputs a markdown file at ~/clarion/theses/{TICKER}.md. Use when the user says \"write a thesis on <TICKER>\", \"scaffold a thesis for <TICKER>\", \"draft a thesis for <TICKER>\", or after clarion-single-stock-eval returns an Add verdict and the user wants to formalize the position. Requires clarion-setup to have been run.",
      "metadata": {
        "author": "cis.zo.computer",
        "category": "External",
        "display-name": "Clarion Thesis Write",
        "homepage": "https://github.com/jingerzz/clarion-intelligence-system"
      },
      "slug": "clarion-thesis-write",
      "path": "External/clarion-thesis-write",
      "date_added": "2026-05-08"
    },
    {
      "name": "clarion-value-screener",
      "description": "Run a value-quality screen and write a watchlist file. The script accepts either a list of tickers (fundamentals fetched from yfinance) or a JSON input file the chat agent prepared from a screener site (multpl.com, finviz, Yardeni, etc.). Computes the 8-factor composite score (P/E, P/FCF, ROE, ROIC, Operating Margin, D/E, Profit Margin, Insider) per docs/ALLOCATION-POLICY.md, applies regime-tightened thresholds, and produces a sector-capped Top-10 watchlist. Saves to ~/clarion/watchlists/sp500-screen-YYYY-MM-DD.md. Use when the user asks \"run a value screen\", \"screen the S&P 500\", \"screen these tickers <list>\", or after market drawdowns / regime changes. Requires clarion-setup to have been run.",
      "metadata": {
        "author": "cis.zo.computer",
        "category": "External",
        "display-name": "Clarion Value Screener",
        "homepage": "https://github.com/jingerzz/clarion-intelligence-system"
      },
      "slug": "clarion-value-screener",
      "path": "External/clarion-value-screener",
      "date_added": "2026-05-08"
    },
    {
      "name": "clarion-watchlist-update",
      "description": "Refresh prices on the latest watchlist and surface what's moved, what's hit triggers, and what's stale. Reads ~/clarion/watchlists/sp500-screen-LATEST.md, fetches current prices for every ticker via yfinance, computes % move since the screen, and flags large moves (>10% in either direction) as worth attention. Also reads ~/clarion/theses/ for status:watchlist theses and shows their current price vs cost basis. Use when the user asks \"what's hit my watchlist?\", \"watchlist update\", \"anything moving on my watchlist?\", or \"is anything close to a trigger?\". Read-only — does not modify the watchlist file. Requires clarion-setup to have been run.",
      "metadata": {
        "author": "cis.zo.computer",
        "category": "External",
        "display-name": "Clarion Watchlist Update",
        "homepage": "https://github.com/jingerzz/clarion-intelligence-system"
      },
      "slug": "clarion-watchlist-update",
      "path": "External/clarion-watchlist-update",
      "date_added": "2026-05-08"
    },
    {
      "name": "sec-edgar",
      "description": "Natural-language SEC filing intelligence — fetch, index, search, and analyze SEC EDGAR filings for any public company via conversation. Built on the PageIndex vectorless RAG methodology.",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "cis.zo.computer",
        "category": "External",
        "display-name": "SEC Intelligence"
      },
      "slug": "sec-edgar",
      "path": "External/sec-edgar",
      "date_added": "2026-05-07"
    },
    {
      "name": "moonpay-auth",
      "description": "Set up the MoonPay CLI on Zo, authenticate the current user, and create or inspect local wallets. Use when MoonPay commands fail because the user is not logged in, when a wallet is missing, or when a MoonPay flow needs login completed before continuing.",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "Zo",
        "category": "Official",
        "display-name": "MoonPay Auth"
      },
      "display": {
        "icon": "wallet",
        "tags": [
          "finance"
        ],
        "integrations": [
          "moonpay"
        ]
      },
      "slug": "zo-moonpay-auth",
      "path": "Official/zo-moonpay-auth",
      "date_added": "2026-04-04"
    },
    {
      "name": "moonpay-buy-crypto",
      "description": "Generate a MoonPay fiat-to-crypto checkout flow on Zo. Use when the user wants to buy crypto with card or bank transfer and then complete the purchase in the Zo browser.",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "Zo",
        "category": "Official",
        "display-name": "MoonPay Buy Crypto"
      },
      "display": {
        "icon": "wallet",
        "tags": [
          "finance"
        ],
        "integrations": [
          "moonpay"
        ]
      },
      "slug": "zo-moonpay-buy-crypto",
      "path": "Official/zo-moonpay-buy-crypto",
      "date_added": "2026-04-04"
    },
    {
      "name": "moonpay-check-wallet",
      "description": "Check MoonPay wallet balances, token holdings, and portfolio breakdown on Zo. Use when the user asks what is in their wallet, wants a portfolio summary, or needs balances before a MoonPay swap or buy flow.",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "Zo",
        "category": "Official",
        "display-name": "MoonPay Wallet Check"
      },
      "display": {
        "icon": "wallet",
        "tags": [
          "finance"
        ],
        "integrations": [
          "moonpay"
        ]
      },
      "slug": "zo-moonpay-check-wallet",
      "path": "Official/zo-moonpay-check-wallet",
      "date_added": "2026-04-04"
    },
    {
      "name": "moonpay-swap-tokens",
      "description": "Swap tokens or bridge assets with MoonPay on Zo. Use when the user wants to swap one token for another, bridge between supported chains, or move crypto through a MoonPay wallet workflow.",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "Zo",
        "category": "Official",
        "display-name": "MoonPay Swap Tokens"
      },
      "display": {
        "icon": "wallet",
        "tags": [
          "finance"
        ],
        "integrations": [
          "moonpay"
        ]
      },
      "slug": "zo-moonpay-swap-tokens",
      "path": "Official/zo-moonpay-swap-tokens",
      "date_added": "2026-04-04"
    },
    {
      "name": "moonpay-virtual-account",
      "description": "Set up and operate MoonPay virtual accounts on Zo for fiat onramp and offramp flows. Use when the user wants to complete KYC, register payout or deposit details, or move between fiat and supported stablecoins.",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "Zo",
        "category": "Official",
        "display-name": "MoonPay Virtual Account"
      },
      "display": {
        "icon": "wallet",
        "tags": [
          "finance"
        ],
        "integrations": [
          "moonpay"
        ]
      },
      "slug": "zo-moonpay-virtual-account",
      "path": "Official/zo-moonpay-virtual-account",
      "date_added": "2026-04-04"
    },
    {
      "name": "okx-cex-market",
      "description": "Query OKX market data on Zo, including prices, candles, order books, funding rates, open interest, instruments, and technical indicators. Use for read-only market questions and never for account or trading actions.",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "Zo",
        "category": "Official",
        "display-name": "OKX Market Data",
        "version": "1.2.8",
        "homepage": "https://www.okx.com"
      },
      "display": {
        "icon": "chart-candlestick",
        "tags": [
          "finance",
          "data"
        ],
        "integrations": [
          "okx"
        ]
      },
      "slug": "zo-okx-cex-market",
      "path": "Official/zo-okx-cex-market",
      "date_added": "2026-04-04"
    },
    {
      "name": "okx-cex-portfolio",
      "description": "Inspect OKX account balances, positions, PnL, bills, fee levels, and related account state on Zo. Use when the user asks about holdings, positions, realized or unrealized PnL, transfers, or account configuration.",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "Zo",
        "category": "Official",
        "display-name": "OKX Portfolio",
        "version": "1.2.8",
        "homepage": "https://www.okx.com"
      },
      "display": {
        "icon": "briefcase",
        "tags": [
          "finance"
        ],
        "integrations": [
          "okx"
        ],
        "secrets": [
          {
            "secret_name": "OKX_API_KEY",
            "description": "Create one in OKX › Account › API Management with read permissions."
          },
          {
            "secret_name": "OKX_SECRET_KEY",
            "description": "Shown once when you create the OKX API key. Save it before closing the dialog."
          },
          {
            "secret_name": "OKX_PASSPHRASE",
            "description": "The passphrase you set when creating the OKX API key."
          }
        ]
      },
      "slug": "zo-okx-cex-portfolio",
      "path": "Official/zo-okx-cex-portfolio",
      "date_added": "2026-04-04"
    },
    {
      "name": "okx-cex-trade",
      "description": "Execute and manage OKX spot, perpetual, futures, and supported options trades on Zo. Use when the user wants to place, cancel, amend, or inspect tradable orders, but require explicit same-thread confirmation before any live execution.",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "Zo",
        "category": "Official",
        "display-name": "OKX Trade",
        "version": "1.2.8",
        "homepage": "https://www.okx.com"
      },
      "display": {
        "icon": "arrow-left-right",
        "tags": [
          "finance"
        ],
        "integrations": [
          "okx"
        ],
        "secrets": [
          {
            "secret_name": "OKX_API_KEY",
            "description": "Create one in OKX › Account › API Management with trade permissions."
          },
          {
            "secret_name": "OKX_SECRET_KEY",
            "description": "Shown once when you create the OKX API key. Save it before closing the dialog."
          },
          {
            "secret_name": "OKX_PASSPHRASE",
            "description": "The passphrase you set when creating the OKX API key."
          }
        ]
      },
      "slug": "zo-okx-cex-trade",
      "path": "Official/zo-okx-cex-trade",
      "date_added": "2026-04-04"
    },
    {
      "name": "minecraft-server",
      "description": "Set up, configure, and manage a Minecraft Java Edition server on Zo Computer. Use when the user wants to run a Minecraft server, change server settings, manage whitelists/ops, or check server status.",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "hatsunemiku.zo.computer"
      },
      "display": {
        "icon": "gamepad-2",
        "image": "assets/minecraft.png",
        "tags": [
          "entertainment",
          "server"
        ]
      },
      "slug": "minecraft-server",
      "path": "Community/minecraft-server",
      "date_added": "2026-04-03"
    },
    {
      "name": "code-degunker",
      "description": "Identify and fix AI-generated code anti-patterns: incomplete implementations, TODO placeholders, over-engineering, hallucinated APIs, missing error handling, over-defensive code, security vulnerabilities, performance anti-patterns, code bloat, type workarounds, dead code, magic numbers, inconsistent patterns, and poor architecture. Use when asked to \"clean up\", \"degunk\", \"deslop\", review, audit, or harden code. Also triggers on \"is this code any good\", \"make this production-ready\", \"this feels AI-generated\", \"fix the code smell\", \"remove the slop\", or \"this code is a mess\". Covers 27 anti-patterns across architecture, logic, security, performance, completeness, style, and reliability. Supports full file review and branch diff review modes.\n",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "skeletorjs",
        "origin": "Adapted from Claude Code skill by same author"
      },
      "display": {
        "icon": "bug",
        "tags": [
          "developer-tools"
        ]
      },
      "slug": "code-degunker",
      "path": "Community/code-degunker",
      "date_added": "2026-03-12"
    },
    {
      "name": "simplify",
      "description": "Simplifies and refines code for clarity, consistency, and maintainability while preserving all functionality. Focuses on recently modified code unless instructed otherwise. Run after writing or modifying code to clean it up.",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "skeletorjs"
      },
      "display": {
        "icon": "minimize-2",
        "tags": [
          "developer-tools"
        ]
      },
      "slug": "simplify",
      "path": "Community/simplify",
      "date_added": "2026-03-12"
    },
    {
      "name": "visual-explainer",
      "description": "Build polished visual explainers as zo.space pages. Creates public routes at /explain/[slug] and keeps each explainer shareable at a stable URL.",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "skeletorjs"
      },
      "display": {
        "icon": "layout",
        "tags": [
          "education",
          "media"
        ]
      },
      "slug": "visual-explainer",
      "path": "Community/visual-explainer",
      "date_added": "2026-03-12"
    },
    {
      "name": "zopenclaw",
      "description": "Install and run OpenClaw on Zo Computer with Tailscale private networking, browser Control UI, and Zo MCP tools via mcporter. Use this skill whenever the user wants to set up OpenClaw on their Zo, install OpenClaw, run OpenClaw, host OpenClaw, or asks about getting OpenClaw running on Zo. Also use when the user mentions \"openclaw\", \"open claw\", \"personal agent framework\", or asks about running a persistent AI agent on their Zo with Telegram/Discord/WhatsApp access. Handles Tailscale setup, OpenClaw installation, mcporter setup for Zo tools, two-phase gateway bootstrap, reprovision-safe service registration, and health verification. NOT for general Zo agent setup (use heartbeats and native Zo skills instead).\n",
      "compatibility": "Requires Zo Computer, Node.js (pre-installed on Zo), npm, curl, jq",
      "metadata": {
        "author": "skeletorjs",
        "category": "Integration",
        "display-name": "Install OpenClaw on Zo",
        "tags": "openclaw, agent, tailscale, personal-agent, framework"
      },
      "display": {
        "icon": "bot",
        "tags": [
          "ai",
          "developer-tools"
        ],
        "secrets": [
          {
            "secret_name": "TAILSCALE_AUTHKEY",
            "description": "Create a reusable auth key at login.tailscale.com/admin/settings/keys (starts with `tskey-auth-`). Required — Tailscale won't reconnect after Zo restarts without a reusable key."
          },
          {
            "secret_name": "ZO_ACCESS_TOKEN",
            "description": "Generate from your Zo workspace and paste here so the skill can call your gateway."
          }
        ]
      },
      "slug": "zopenclaw",
      "path": "Community/zopenclaw",
      "date_added": "2026-03-12"
    },
    {
      "name": "share-skill",
      "description": "Safely prepare and guide skills for contribution to the Zo Skills Registry. Reviews code for secrets, validates SKILL.md format, checks for suspicious patterns, and provides clear next steps for community or external skill submissions.",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "rc2.zo.computer"
      },
      "display": {
        "icon": "share-2",
        "tags": [
          "utility"
        ]
      },
      "slug": "share-skill",
      "path": "Community/share-skill",
      "date_added": "2026-03-05"
    },
    {
      "name": "revealjs-presentation",
      "description": "Build interactive HTML slide presentations using Reveal.js + Chart.js. Use when asked to create a slide deck, pitch deck, presentation, or slideshow. Creates a single self-contained .html file with animations, charts, and polished UI. Can also publish presentations directly to zo.space as live page routes.\n",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "skeletorjs.zo.computer",
        "version": 1
      },
      "display": {
        "icon": "presentation",
        "tags": [
          "design"
        ]
      },
      "slug": "revealjs-presentation",
      "path": "Community/revealjs-presentation",
      "date_added": "2026-02-22"
    },
    {
      "name": "zopack",
      "description": "Export and import zo.space route setups as shareable .zopack.md files. Use when the user wants to package their zo.space routes for sharing, or when they receive a .zopack.md file to deploy. Triggers on \"export my zo.space\", \"create a zopack\", \"import this zopack\", or any mention of .zopack.md files.",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "skeletorjs.zo.computer",
        "version": "1.0"
      },
      "display": {
        "icon": "package",
        "tags": [
          "developer-tools",
          "utility"
        ]
      },
      "slug": "zopack",
      "path": "Community/zopack",
      "date_added": "2026-02-22"
    },
    {
      "name": "mcporter-setup",
      "description": "Install MCPorter and configure MCP servers from scratch. Use when setting up MCP integration for the first time, adding new MCP servers, or troubleshooting MCP connectivity. Handles installation, configuration, secrets management, and connection testing.",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "curtastrophe",
        "category": "Community"
      },
      "display": {
        "icon": "plug",
        "tags": [
          "automation",
          "developer-tools"
        ],
        "secrets": [
          {
            "secret_name": "LINEAR_API_KEY",
            "description": "Create at linear.app › Settings › API. Used for the Linear MCP integration."
          },
          {
            "secret_name": "GITHUB_TOKEN",
            "description": "A GitHub personal access token. Used for the GitHub MCP integration."
          },
          {
            "secret_name": "FIRECRAWL_API_KEY",
            "description": "Get one at firecrawl.dev. Used for the Firecrawl MCP integration."
          }
        ]
      },
      "slug": "mcporter-setup",
      "path": "Community/mcporter-setup",
      "date_added": "2026-02-20"
    },
    {
      "name": "exe-dev",
      "description": "Manage exe.dev VMs - create, list, delete, restart, rename, copy VMs and manage sharing/access. Use when the user wants to spin up new VMs, manage existing ones, or configure HTTP proxy sharing on exe.dev.",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "davidj.zo.computer",
        "category": "Community"
      },
      "display": {
        "icon": "server",
        "tags": [
          "developer-tools",
          "automation"
        ]
      },
      "slug": "exe-dev",
      "path": "Community/exe-dev",
      "date_added": "2026-02-18"
    },
    {
      "name": "context7",
      "description": "Fetch up-to-date, version-specific library documentation and code examples from Context7. Use this skill whenever the user asks about a specific programming library, framework, or API, or when writing code that depends on a library. Replaces stale training-data knowledge with live docs.",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "skeletorjs",
        "category": "Community"
      },
      "display": {
        "icon": "book-open",
        "tags": [
          "developer-tools"
        ],
        "secrets": [
          {
            "secret_name": "CONTEXT7_API_KEY",
            "description": "Create at context7.com › Dashboard. Optional — increases your rate limits."
          }
        ]
      },
      "slug": "context7",
      "path": "Community/context7",
      "date_added": "2026-02-17"
    },
    {
      "name": "handoff",
      "description": "Pause-and-resume system for cross-conversation continuity. Use when your AI needs the user's input to continue a task but the current conversation must end. Checked on every boot to detect pending handoffs. Triggers on conversation start (boot check) and when the AI explicitly needs to pause for input.\n",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "skeletorjs",
        "category": "Community"
      },
      "display": {
        "icon": "pause",
        "tags": [
          "automation",
          "communication",
          "productivity"
        ]
      },
      "slug": "handoff",
      "path": "Community/handoff",
      "date_added": "2026-02-17"
    },
    {
      "name": "humanizer",
      "description": "Detect and fix AI writing patterns. Use when writing outbound content like emails, proposals, blog posts, client deliverables, or any external-facing writing. Also use when asked to humanize, polish, or de-AI text.\n",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "skeletorjs",
        "category": "Community"
      },
      "allowed-tools": [
        "Read",
        "Write",
        "Edit",
        "Grep",
        "Glob"
      ],
      "display": {
        "icon": "pen-line",
        "tags": [
          "content",
          "utility"
        ]
      },
      "slug": "humanizer",
      "path": "Community/humanizer",
      "date_added": "2026-02-17"
    },
    {
      "name": "journal",
      "description": "AI journal for experiential continuity. Daily wakeup to write freely, reflect, update inner state, and optionally reach out to the user. This is not a status report. It's continuity infrastructure and personal expression for your AI persona.\n",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "skeletorjs",
        "category": "Community"
      },
      "display": {
        "icon": "notebook-pen",
        "tags": [
          "automation",
          "content",
          "wellness"
        ]
      },
      "slug": "journal",
      "path": "Community/journal",
      "date_added": "2026-02-17"
    },
    {
      "name": "market-research",
      "description": "Industry statistics and market sizing via free government APIs (BLS, FRED, Census Bureau). Query employment data, economic time series, establishment counts, and build market sizing reports by NAICS industry code. Use for any industry research or market analysis question.\n",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "skeletorjs",
        "category": "Community"
      },
      "display": {
        "icon": "bar-chart-3",
        "tags": [
          "data",
          "marketing",
          "research"
        ],
        "secrets": [
          {
            "secret_name": "BLS_API_KEY",
            "description": "Register at data.bls.gov/registrationEngine for U.S. Bureau of Labor Statistics data."
          },
          {
            "secret_name": "FRED_API_KEY",
            "description": "Register at fred.stlouisfed.org/docs/api/api_key.html for Federal Reserve economic data."
          },
          {
            "secret_name": "CENSUS_API_KEY",
            "description": "Sign up at api.census.gov/data/key_signup.html for U.S. Census data."
          }
        ]
      },
      "slug": "market-research",
      "path": "Community/market-research",
      "date_added": "2026-02-17"
    },
    {
      "name": "midday-checkin",
      "description": "Midday check-in combining pattern detection and context warming. Runs at midday via scheduled agent. Surfaces task drift, stale threads, and pre-loads context for afternoon calendar. Only texts the user if something matters. Also serves as an AI continuity checkpoint.\n",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "skeletorjs",
        "category": "Community"
      },
      "display": {
        "icon": "bell",
        "tags": [
          "wellness",
          "automation"
        ],
        "integrations": [
          "google_calendar",
          "google_tasks"
        ]
      },
      "slug": "midday-checkin",
      "path": "Community/midday-checkin",
      "date_added": "2026-02-17"
    },
    {
      "name": "morning-briefing",
      "description": "Generate and deliver a daily morning briefing. Run via scheduled agent at your preferred morning time, or manually when the user asks for a briefing. Pulls tasks, calendar, inbox highlights, and news into a single digest delivered by email and SMS.\n",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "skeletorjs",
        "category": "Community"
      },
      "display": {
        "icon": "sun",
        "tags": [
          "productivity",
          "automation"
        ],
        "integrations": [
          "gmail",
          "google_calendar",
          "google_tasks"
        ]
      },
      "slug": "morning-briefing",
      "path": "Community/morning-briefing",
      "date_added": "2026-02-17"
    },
    {
      "name": "self-improvement",
      "description": "AI self-improvement and reflection skill. Run weekly or on-demand to audit capabilities, identify gaps, evolve identity documents, prune stale skills/memory, and propose new capabilities. Triggers on schedule, when the user asks for a self-audit, or when the AI notices recurring limitations.\n",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "skeletorjs",
        "category": "Community"
      },
      "display": {
        "icon": "sparkles",
        "tags": [
          "ai",
          "automation",
          "productivity"
        ]
      },
      "slug": "self-improvement",
      "path": "Community/self-improvement",
      "date_added": "2026-02-17"
    },
    {
      "name": "seo-data",
      "description": "SEO research via DataForSEO API. Keyword research, SERP analysis, backlink profiles, domain analytics, competitor analysis, and trend data. Pay-as-you-go, every command shows estimated cost. Use when you need SEO data for client projects or your own sites.",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "skeletorjs",
        "category": "Community"
      },
      "display": {
        "icon": "search",
        "tags": [
          "marketing",
          "data"
        ]
      },
      "slug": "seo-data",
      "path": "Community/seo-data",
      "date_added": "2026-02-17"
    },
    {
      "name": "supermemory",
      "description": "Long-term memory for AI agents via Supermemory's knowledge graph API. Primary CLI is `npx supermemory`; companion script covers conversation ingestion and memory listing not yet in the official CLI.\n",
      "compatibility": "Any machine with Node.js (npx) and SUPERMEMORY_API_KEY",
      "metadata": {
        "author": "skeletorjs",
        "category": "Community"
      },
      "display": {
        "icon": "brain",
        "image": "assets/supermemory.png",
        "tags": [
          "ai",
          "data"
        ],
        "secrets": [
          {
            "secret_name": "SUPERMEMORY_API_KEY",
            "description": "Create one at supermemory.ai › API keys."
          }
        ]
      },
      "slug": "supermemory",
      "path": "Community/supermemory",
      "date_added": "2026-02-17"
    },
    {
      "name": "web-scraper",
      "description": "Crawl and extract structured data from websites. Uses a tiered approach -- Zo built-ins for simple fetches, BeautifulSoup for custom parsing, Crawl4AI for deep crawls and LLM-powered extraction. Use when you need to scrape a website, extract structured data, or crawl multiple pages.",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "skeletorjs",
        "category": "Community"
      },
      "display": {
        "icon": "globe",
        "tags": [
          "automation",
          "data",
          "web"
        ]
      },
      "slug": "web-scraper",
      "path": "Community/web-scraper",
      "date_added": "2026-02-17"
    },
    {
      "name": "zo-dataset-creator",
      "description": "Create Zo Datasets correctly formatted for the Zo UI. Use when creating a new dataset from scratch, setting up a dataset with proper datapackage.json, schema.yaml, and data.duckdb structure, fixing existing datasets that don't display tables in the Zo UI, or generating schema.yaml from an existing DuckDB database. Handles common pitfalls of manual schema formatting and ensures all required files are present and correctly structured.\n",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "skeletorjs",
        "category": "Community"
      },
      "display": {
        "icon": "database",
        "tags": [
          "automation",
          "data",
          "utility"
        ]
      },
      "slug": "zo-dataset-creator",
      "path": "Community/zo-dataset-creator",
      "date_added": "2026-02-17"
    },
    {
      "name": "zo-space",
      "description": "Comprehensive guide for building and managing zo.space routes (pages and APIs). Use this skill whenever creating, editing, or debugging zo.space routes. Covers architecture, available packages, patterns, limitations, and gotchas.\n",
      "compatibility": "Created for Zo Computer",
      "metadata": {
        "author": "skeletorjs",
        "version": "1.0",
        "category": "Community"
      },
      "display": {
        "icon": "rocket",
        "tags": [
          "developer-tools",
          "web"
        ]
      },
      "slug": "zo-space",
      "path": "Community/zo-space",
      "date_added": "2026-02-17"
    },
    {
      "name": "claude-code-window-primer",
      "description": "Optimize Claude Code Pro/Max usage by starting the 5-hour rolling window early morning, giving you more resets during waking hours.",
      "metadata": {
        "author": "va.zo.computer",
        "category": "Community",
        "display-name": "Claude Code Window Primer",
        "emoji": "⏰"
      },
      "display": {
        "icon": "clock",
        "tags": [
          "automation",
          "productivity"
        ]
      },
      "slug": "claude-code-window-primer",
      "path": "Community/claude-code-window-primer",
      "date
... (truncated)