# BudgetBuddy

### CS 122 Final Project

**Team Members:**

- Aung Bo Bo
- Aye Nyein Kyaw

## Description

**BudgetBuddy** is a simple budgeting tool developed as the final project for CS 122. The application helps you manage and track your finances efficiently.

## Features

- Easy-to-use interface
- Add, edit, and track your expenses
- Visual summaries of your budgeting habits

## How to Run the Project

To get **BudgetBuddy** up and running, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/aungbbo/budget-buddy.git
   cd budget-buddy
   ```

2. **Install [uv](https://github.com/astral-sh/uv) (if you haven't already):**

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install the dependencies:**

   ```bash
   uv sync
   ```

4. **Run the application:**
   ```bash
   uv run app.py
   ```

The app should now be running locally. Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser to use BudgetBuddy.

5. **Run tests with uv**
   run unittest discovery:
   ```bash
   uv run python -m unittest discover -s tests -p "test_*_unittest.py
   ```

   or simply:
    ```bash
    uv run python -m unittest
   ```

    If you prefer pytest, you can run:
   ```bash
       uv run pytest -q
   ```
