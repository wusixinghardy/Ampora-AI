## 🧩 **Setup Guide — Backend (AI Career Tutor)**

Follow these steps to set up and run the backend locally.

---

### 🧱 1️⃣ Clone the repository

<pre class="overflow-visible!" data-start="328" data-end="434"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>git </span><span>clone</span><span> https://github.com/<your-org-or-username>/Ampora-Career.git
</span><span>cd</span><span> Ampora-Career/backend
</span></span></code></div></div></pre>

---

### 🧰 2️⃣ Create and activate a virtual environment

**Mac / Linux**

<pre class="overflow-visible!" data-start="511" data-end="584"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python3 -m venv venv-fastapi
</span><span>source</span><span> venv-fastapi/bin/activate
</span></span></code></div></div></pre>

**Windows (PowerShell)**

<pre class="overflow-visible!" data-start="611" data-end="680"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python -m venv venv-fastapi
venv-fastapi\Scripts\activate
</span></span></code></div></div></pre>

---

### 📦 3️⃣ Install all dependencies

Make sure your environment is active (`(venv-fastapi)` should appear in your terminal).

<pre class="overflow-visible!" data-start="813" data-end="882"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pip install --upgrade pip
pip install -r requirements.txt
</span></span></code></div></div></pre>

---

### 🔐 4️⃣ Set up environment variables

Create a `.env` file in the `/backend` folder with the following content:

<pre class="overflow-visible!" data-start="1005" data-end="1115"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>OPENAI_API_KEY</span><span>=sk-xxxxxxxxxxxxxxxxxxxxxxxx
</span><span>OPENAI_API_BASE</span><span>=https://api.openai.com/v1
</span><span>MODEL_NAME</span><span>=gpt-</span><span>4</span><span>o
</span></span></code></div></div></pre>

> 💡 **Note:**
>
> Each teammate must provide their own OpenAI API key from
>
> [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

---

### 🚀 5️⃣ Run the backend script

From the `/backend` directory, run:

<pre class="overflow-visible!" data-start="1352" data-end="1401"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python -m src.services.lecture_script
</span></span></code></div></div></pre>

This will:

* Print the model being used
* Generate a list of learning objectives
* Produce a complete lecture script

---

### 🧪 6️⃣ (Optional) Quick-run helper

To simplify running the project, you can create a `run_lecture.sh` script in `/backend`:

<pre class="overflow-visible!" data-start="1660" data-end="1754"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>#!/bin/bash</span><span>
</span><span>source</span><span> venv-fastapi/bin/activate
python -m src.services.lecture_script
</span></span></code></div></div></pre>

Make it executable:

<pre class="overflow-visible!" data-start="1776" data-end="1811"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>chmod</span><span> +x run_lecture.sh
</span></span></code></div></div></pre>

Then you can just run:

<pre class="overflow-visible!" data-start="1836" data-end="1867"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>bash run_lecture.sh
</span></span></code></div></div></pre>

---
