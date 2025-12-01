import ast
import os
import sys


def check_syntax(file_path):
    """Check Python syntax for a file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse the AST to check syntax
        ast.parse(content)
        return True, "OK"
    except SyntaxError as e:
        return False, f"Syntax Error: {e}"
    except Exception as e:
        return False, f"Error: {e}"


def test_all_python_files():
    """Test all Python files in the project"""
    print("=" * 60)
    print("PREDICTEL - Python Syntax Checker")
    print("=" * 60)

    # Files to check
    python_files = [
        "Home.py",
        "style.py",
        "pages/Input_Data.py",
        "pages/Preprocessing_Data.py",
        "pages/Test_Data.py",
        "pages/Visualisasi_Data.py",
        "pages/About_Us.py",
    ]

    all_good = True

    for file_path in python_files:
        if os.path.exists(file_path):
            is_valid, message = check_syntax(file_path)
            status = "✅ PASS" if is_valid else "❌ FAIL"
            print(f"{status} {file_path}: {message}")
            if not is_valid:
                all_good = False
        else:
            print(f"⚠️  MISSING {file_path}: File not found")
            all_good = False

    print("-" * 60)

    if all_good:
        print("🎉 ALL FILES PASSED SYNTAX CHECK!")
        print("✅ PREDICTEL is ready to run")
        print("✅ No syntax errors detected")
        print("✅ All Python files are valid")
    else:
        print("❌ SOME FILES HAVE ISSUES!")
        print("⚠️  Please fix the errors above before running")

    print("=" * 60)
    return all_good


def test_imports():
    """Test critical imports"""
    print("\n🔍 Testing Critical Imports...")

    critical_imports = ["streamlit", "pandas", "numpy", "sklearn", "matplotlib"]

    optional_imports = ["seaborn", "plotly"]

    import_issues = []

    for module in critical_imports:
        try:
            __import__(module)
            print(f"✅ {module}: Available")
        except ImportError:
            print(f"❌ {module}: MISSING (REQUIRED)")
            import_issues.append(module)

    for module in optional_imports:
        try:
            __import__(module)
            print(f"✅ {module}: Available (Enhanced mode)")
        except ImportError:
            print(f"⚠️  {module}: Not available (Fallback mode)")

    if import_issues:
        print(f"\n❌ Missing required modules: {', '.join(import_issues)}")
        print("💡 Run: pip install " + " ".join(import_issues))
        return False
    else:
        print("\n✅ All required imports available!")
        return True


def main():
    """Main test function"""
    print("Starting PREDICTEL System Check...\n")

    # Test 1: Syntax check
    syntax_ok = test_all_python_files()

    # Test 2: Import check
    imports_ok = test_imports()

    # Final result
    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)

    if syntax_ok and imports_ok:
        print("🎉 PREDICTEL SYSTEM CHECK PASSED!")
        print("✅ All syntax is valid")
        print("✅ All required libraries available")
        print("🚀 Ready to launch with: streamlit run Home.py")
        return 0
    else:
        print("❌ PREDICTEL SYSTEM CHECK FAILED!")
        if not syntax_ok:
            print("❌ Syntax errors need to be fixed")
        if not imports_ok:
            print("❌ Missing required libraries")
        print("🔧 Please resolve issues before launching")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
