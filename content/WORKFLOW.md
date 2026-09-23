# Content Workflow - Zernio Social Media Scheduling

## Architecture

Each topic gets **3 separate files** in `content/topics/`:
- `topic01-linkedin-may22.md` - LinkedIn version
- `topic01-xpersonal-may22.md` - X Personal (@VishalIPatil)
- `topic01-xwefab-may22.md` - X WeFab (@wefabdotAI)

## Why Separate Files?

1. **No parsing bugs** - No section extraction that can fail
2. **Clear separation** - Each file has one job
3. **Easy editing** - Edit one platform without touching others
4. **Formatting preserved** - Blank lines (paragraph breaks) stay intact

## Scheduling

Run the scheduler:
```bash
node zernio-schedule-from-files.mjs
```

This reads all files from `content/topics/` and schedules them to Zernio.

## Posting Schedule (IST)
- **LinkedIn**: 8:00 AM IST = 2:30 AM UTC
- **X Personal**: 6:00 AM IST = 12:30 AM UTC
- **X WeFab**: 7:00 PM IST = 1:30 PM UTC

## Zernio Status Behavior
- Posts are created as `draft` status with `scheduledAt` timestamp
- Zernio auto-publishes at the scheduled time
- Status changes to `published` after going live
- `draft` + future `scheduledAt` = will auto-publish

## Content Generation

1. Write content in the combined draft file (`DRAFTS-WEFAB-30DAY-MASTER.md` or `DRAFTS-WEFAB-30DAY-FULL.md`)
2. Run `node split-topics.mjs` to generate separate files
3. Run `node zernio-schedule-from-files.mjs` to schedule

## Files
- `content/topics/` - All per-platform content files
- `zernio-schedule-from-files.mjs` - Main scheduling script
- `split-topics.mjs` - Split combined drafts into separate files
- `zernio-config.mjs` - API keys and account IDs

## Important Notes
- Zernio API creates posts as `draft` by design - they auto-publish at `scheduledAt`
- Do NOT try to change status via PUT/PATCH - Zernio ignores it
- Each post is platform-specific - no cross-platform contamination
