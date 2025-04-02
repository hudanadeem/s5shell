# ☁️ S5Shell - AWS S3 Storage Shell

**S5Shell** is a custom command-line shell interface built in Python that interacts with AWS S3 buckets. Designed as a learning project to understand AWS CLI behavior and S3 storage operations, it supports file upload, bucket creation, navigation, and local command execution — all inside a shell-like interface.

---

## 📦 Features

- 🌐 Connects to AWS S3 using a config file
- 📁 Create and navigate S3 buckets/paths
- ⬆️ Upload local files to S3 (`locs3cp`)
- 📂 List contents of current S3 path or bucket
- 🖥️ Run local OS shell commands like `ls`, `pwd`, etc.
- 💻 Compatible with both **Windows** and **Mac/Linux**
- 🚪 Type `exit` or `quit` to leave the shell

---
## 🧑‍💻 Tech Stack

| Technology | Description |
|------------|-------------|
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="30"/> **Python** | The primary language used for the shell. |
|  **AWS S3** | Cloud storage used for file management. |
|  **Boto3** | AWS SDK for Python, used to interact with AWS S3. |
| <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-original.svg" width="30"/> **Git** | Version control for managing the source code. |
---

## 📂 Git Clone Instructions

To get started, clone the repository:

```bash
git clone https://github.com/hudanadeem/s5shell.git
cd s5shell
```

---

## 🛠 Setup Instructions

### ✅ Prerequisites

- Python 3.x
- `boto3` library
- AWS access key and secret stored in a config file

---

### 📁 Step 1: AWS Credentials Setup

Create a file named `S5-S3.conf` in the same directory with the following format:

```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

---

### 🐍 Step 2: Install Dependencies

```bash
pip install boto3
```

---

### ▶️ Step 3: Run the Shell

```bash
python a1.py
```

---

## 💡 OS Compatibility

This script detects if you're on **Windows** and adjusts `ls`, `pwd`, etc., to `dir` and `cd` accordingly:

```python
if platform.system() == "Windows":
    line = line.replace("ls", "dir").replace("pwd", "cd")
```

So:
- ✅ On **Windows**: You can type Unix-like commands (`ls`, `pwd`)
- ✅ On **Mac/Linux**: It should run natively with no changes

---

## 🧠 Commands Overview

| Command            | Description                                               |
|--------------------|-----------------------------------------------------------|
| `create_bucket /<bucket>`   | Create a new S3 bucket                          |
| `chlocn /<bucket>/<path>`   | Change S3 working directory                     |
| `cwlocn`                     | Show current S3 path                           |
| `list`                       | List contents of current S3 location or all buckets |
| `locs3cp <local> <s3_path>`  | Copy a local file to an S3 destination          |
| `exit` or `quit`             | Exit the S5 shell                               |

> Example:
```bash
S5> create_bucket /test-bucket
S5> chlocn /test-bucket
S5> locs3cp resume.pdf /test-bucket/resume.pdf
```

---

## 🔚 Exit

Type `exit` or `quit` to leave the shell at any time.

---
