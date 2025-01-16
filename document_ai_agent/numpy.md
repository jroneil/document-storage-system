The error you're encountering is due to a **compatibility issue between NumPy 1.x and NumPy 2.2.1**. Some of your dependencies (e.g., `scikit-learn`, `pandas`, or other scientific computing libraries) were compiled with NumPy 1.x and are not yet compatible with NumPy 2.2.1.

Let’s resolve this step by step.

---

### 1. **Downgrade NumPy to Version 1.x**

The easiest solution is to downgrade NumPy to a version below 2.0. This will ensure compatibility with your existing dependencies.

Run the following command:

```bash
pip install "numpy<2"
```

This will install the latest version of NumPy 1.x (e.g., `numpy==1.26.4`).

---

### 2. **Reinstall Affected Packages**

After downgrading NumPy, reinstall any packages that might have been affected by the NumPy upgrade. For example:

```bash
pip install --force-reinstall scikit-learn pandas
```

---

### 3. **Check for Specific Incompatible Packages**

If the error persists, identify the specific package causing the issue. The error message usually mentions the problematic module. For example, if `scikit-learn` is the issue, you can try reinstalling it:

```bash
pip install --force-reinstall scikit-learn
```

---

### 4. **Upgrade Dependencies**

If possible, upgrade your dependencies to versions that support NumPy 2.x. For example:

```bash
pip install --upgrade scikit-learn pandas
```

However, not all packages may have updated versions that support NumPy 2.x yet. In that case, downgrading NumPy is the best solution.

---

### 5. **Use a Virtual Environment**

If you’re not already using a virtual environment, create one to isolate your project dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Then, install the dependencies again:

```bash
pip install -r requirements.txt
```

---

### 6. **Update `requirements.txt`**

If you’re using a `requirements.txt` file, update it to pin NumPy to a version below 2.0:

```plaintext
numpy<2
```

Then, reinstall all dependencies:

```bash
pip install -r requirements.txt
```

---

### 7. **Alternative: Use `conda`**

If you’re using Anaconda or Miniconda, you can use `conda` to manage your dependencies. `conda` handles compatibility issues better than `pip` in some cases.

1. Create a new `conda` environment:
   ```bash
   conda create -n document-ai-agent python=3.11
   conda activate document-ai-agent
   ```

2. Install the dependencies:
   ```bash
   conda install numpy scikit-learn pandas flask
   ```

3. Install the remaining dependencies using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

---

### 8. **Rebuild Affected Modules**

If you’re developing a custom module or using a package that needs to be rebuilt, ensure that it’s compiled with `pybind11>=2.12` and NumPy 2.x. For example:

```bash
pip install pybind11>=2.12
```

Then, rebuild the module:

```bash
python setup.py build
python setup.py install
```

---

### 9. **Debugging Tips**

If the issue persists:
1. **Check for Open Issues**:
   - Search for open issues on the GitHub repositories of the affected packages (e.g., `scikit-learn`, `pandas`).
   - Check the [NumPy GitHub repository](https://github.com/numpy/numpy/issues) for related issues.

2. **Use a Docker Container**:
   - Use a Docker container with a preconfigured environment to avoid compatibility issues. Here’s an example `Dockerfile`:

     ```Dockerfile
     FROM python:3.11-slim

     WORKDIR /app

     COPY requirements.txt .
     RUN pip install --no-cache-dir -r requirements.txt

     COPY . .

     EXPOSE 5000

     CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
     ```

   - Build and run the Docker container:
     ```bash
     docker build -t document-ai-agent .
     docker run -p 5000:5000 document-ai-agent
     ```

---

### Updated `requirements.txt` (Example)

Here’s an example `requirements.txt` with pinned versions for compatibility:

```plaintext
Flask==2.3.2
Flask-SQLAlchemy==3.0.5
PyPDF2==3.0.1
python-docx==0.8.11
pdf2image==1.16.3
pytesseract==0.3.10
Pillow==10.0.1
keybert==0.7.0
transformers==4.30.2
sentence-transformers==2.2.2
sumy==0.10.0
textblob==0.17.1
scikit-learn==1.3.0
numpy<2
gunicorn==21.2.0
```

---

### Summary of Steps

1. Downgrade NumPy to version 1.x:
   ```bash
   pip install "numpy<2"
   ```

2. Reinstall affected packages:
   ```bash
   pip install --force-reinstall scikit-learn pandas
   ```

3. Update `requirements.txt` to pin NumPy to version 1.x.

4. Use a virtual environment or `conda` to isolate dependencies.

5. If necessary, rebuild custom modules with `pybind11>=2.12`.

---

Let me know if you need further assistance!