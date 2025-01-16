No, you **do not need to install WSL every time** you build or run a Docker container. Once WSL 2 is set up on your Windows machine, it remains available for all future Docker builds and runs. Here's how it works:

---

### 1. **One-Time WSL 2 Setup**

You only need to install and configure WSL 2 **once**. After that, Docker will use WSL 2 as its backend automatically.

#### Steps to Install WSL 2 (One-Time Setup):

1. **Enable WSL**:
   - Open PowerShell as Administrator and run:
     ```powershell
     wsl --install
     ```
   - This installs WSL 2 and a default Linux distribution (e.g., Ubuntu).

2. **Restart Your Computer**:
   - After installation, restart your computer to apply the changes.

3. **Set WSL 2 as the Default Backend in Docker Desktop**:
   - Open Docker Desktop settings.
   - Go to **General** and ensure "Use the WSL 2 based engine" is checked.
   - Go to **Resources > WSL Integration** and enable integration with your WSL 2 distro (e.g., Ubuntu).

4. **Verify WSL 2 Installation**:
   - Open a terminal and run:
     ```bash
     wsl --list --verbose
     ```
   - Ensure your Linux distribution is using WSL 2 (e.g., `VERSION 2`).

---

### 2. **Using WSL 2 for Docker**

Once WSL 2 is set up, Docker Desktop will automatically use it as the backend. You don't need to reinstall or reconfigure WSL 2 for future Docker builds or runs.

#### How Docker Uses WSL 2:
- Docker Desktop integrates with WSL 2 to provide a Linux environment for running containers.
- You can use Docker commands (e.g., `docker build`, `docker run`) directly from your Windows terminal (PowerShell, Command Prompt) or from within a WSL 2 terminal (e.g., Ubuntu).

---

### 3. **Building and Running Docker Containers**

After WSL 2 is set up, you can build and run Docker containers as usual:

#### From Windows Terminal:
```bash
docker build -t document-ai-agent .
docker run -p 5000:5000 document-ai-agent
```

#### From WSL 2 Terminal:
1. Open your WSL 2 terminal (e.g., Ubuntu).
2. Navigate to your project directory.
3. Run Docker commands:
   ```bash
   docker build -t document-ai-agent .
   docker run -p 5000:5000 document-ai-agent
   ```

---

### 4. **Benefits of Using WSL 2 with Docker**

- **Faster Builds**: WSL 2 provides better file system performance compared to the traditional Hyper-V backend.
- **Native Linux Environment**: Containers run in a true Linux environment, avoiding compatibility issues.
- **Seamless Integration**: Docker commands work the same way in Windows terminals and WSL 2 terminals.

---

### 5. **Troubleshooting WSL 2 and Docker**

If Docker is not using WSL 2 after setup:

1. **Check WSL 2 Integration**:
   - Open Docker Desktop settings.
   - Go to **Resources > WSL Integration** and ensure your WSL 2 distro is enabled.

2. **Restart Docker Desktop**:
   - Restart Docker Desktop to apply the changes.

3. **Verify WSL 2 Version**:
   - Run the following command to ensure your Linux distro is using WSL 2:
     ```bash
     wsl --list --verbose
     ```
   - If it's using WSL 1, upgrade it to WSL 2:
     ```bash
     wsl --set-version <distro-name> 2
     ```

---

### Summary

- **WSL 2 is a one-time setup**. Once installed and configured, Docker will use it automatically for all future builds and runs.
- You can use Docker commands from either the Windows terminal or the WSL 2 terminal.
- WSL 2 improves Docker performance on Windows by providing a native Linux environment.

Let me know if you encounter any issues during setup!