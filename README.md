# Minecraft-name-checker
NAMEGEN generates 3-5 character Minecraft usernames using random letters/numbers or dictionary words. Checks availability via Mojang API (✅ available, ❌ taken), supports multithreading, logs successes/invalids, handles rate-limits, Ctrl+C safe, optional Discord webhook notifications, and works on mobile (Pydroid 3). And made with AI

## Features of NAMEGEN

- **Random Username Generation**
  - Generates usernames with 3, 4, or 5 characters.
  - Supports letters and numbers.

- **Dictionary Mode**
  - Generates usernames using real English words.
  - Automatically switches APIs if one fails.
  - Notifies user if all dictionary APIs are unavailable.

- **Username Availability Check**
  - Checks usernames against the Mojang API.
  - ✅ Green = available
  - ❌ Red = taken
  - Handles rate-limits gracefully.

- **Multithreading Support**
  - Can run multiple threads for faster generation.
  - Threads are configurable by the user.

- **Ctrl+C Safe**
  - Stop generation safely without losing logs.
  - Sends final results to webhook if enabled.

- **Discord Webhook Integration**
  - Optional webhook notifications for successes.
  - Sends final summary with success, invalid, and retry counts.

- **Logging**
  - Stores available usernames in `success.txt`.
  - Stores invalid usernames in `invalid.txt`.
  - Counts retries for failed requests.

- **Mobile-Friendly**
  - Works on Pydroid 3 and similar Python mobile environments.

- **Customizable Delay**
  - Lower generation delay to avoid rate-limits.
