# 📤 Publish to GitHub + post on LinkedIn

## 🔐 Important security note first
You shared your GitHub **password** in chat. Please **change it now** (github.com → Settings → Password),
and in future never paste passwords anywhere — not even here. Two reasons:
1. Anything typed in a chat can be logged. Treat that password as compromised.
2. GitHub **no longer accepts your account password** for uploading code anyway — it requires either the
   **GitHub Desktop app** (which logs in safely through your browser) or a **Personal Access Token**.

I can't log into your account or push code on your behalf from here — and that's by design, for your safety.
But the steps below take about 5 minutes and need **no token and no commands**.

## 🧹 Quick cleanup before you publish
In this `Project1` folder, delete these (cloud-sync locked them so they couldn't be removed automatically):
- the hidden **`.git`** folder (a broken partial one) — turn on "Hidden items" in File Explorer's View menu
- the old **`carousel/`** folder (outdated 12-rule images) — the current images are in **`slides/`**
- **`carousel_v2/`** if present (a leftover test folder)

---

## Option A — GitHub Desktop (easiest, no password/token)
1. Install **GitHub Desktop**: https://desktop.github.com → sign in (it opens your browser to log in safely).
2. **File → Add Local Repository →** choose this `Project1` folder → click **create a repository here**.
3. Name it `decode-your-pattern`, click **Create Repository**.
4. Click **Publish repository** (uncheck "private" if you want the live demo public) → **Publish**.
5. Done. 🎉

## Option B — Command line (needs a Personal Access Token, not your password)
Create a token at github.com → Settings → Developer settings → Personal access tokens → "Generate new token (classic)",
tick `repo`. Use that token as the password when git asks.
```bash
git init
git add -A
git commit -m "Decode Your Pattern: interactive article, 58-question assessment, carousel"
git branch -M main
git remote add origin https://github.com/AntaraBarman/decode-your-pattern.git
git push -u origin main
```

---

## 🌐 Turn on the live demo (GitHub Pages)
Repo → **Settings → Pages** → Source = **Deploy from a branch**, Branch = **main**, folder = **/ (root)** → **Save**.
After ~1 minute it's live at `https://AntaraBarman.github.io/decode-your-pattern/`.
- `index.html` (the colourful article) opens first.
- Its "Decode your pattern" button links to the assessment.

## 💼 Post on LinkedIn
1. Copy the caption from `LINKEDIN_POST.md`.
2. New post → image/document icon → upload all 17 images from the **`slides/`** folder in order (00 → 16).
3. Paste the caption. Post.
4. Put the **live link** and **repo link** in the **first comment**.

---

## 👍 Per-level reactions — already working, nothing to do
Each rule on the article page has live 👍 ❤️ 🔥 👎 reactions whose counts are **shared across everyone**
who visits. They use a free, no-signup counter service (abacus). If that service is ever unreachable, the
buttons quietly fall back to counting on each visitor's own device, so the page never breaks.

## 🔢 Visitor counter
You chose to skip this for now. If you change your mind later, tell me and I'll add a free live visitor
count (it needs a small no-signup counter service, same idea as the reactions).

That's it — your playable article and honest pattern report are live, shareable, and interactive. 🚀
