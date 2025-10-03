#!/usr/bin/env python3
"""
Test script for Streamlit dashboard functionality.
Validates the streamlit_app.py without actually running the server.
"""

def test_streamlit_imports():
    """Test that streamlit app can be imported."""
    print("Testing Streamlit app imports...")
    try:
        import streamlit
        print("✓ Streamlit imported")
    except ImportError:
        print("✗ Streamlit not installed")
        return False
    
    try:
        import streamlit_app
        print("✓ streamlit_app module imported")
    except Exception as e:
        print(f"✗ streamlit_app import failed: {e}")
        return False
    
    return True


def test_streamlit_structure():
    """Test that streamlit app has required structure."""
    print("\nTesting Streamlit app structure...")
    
    with open('streamlit_app.py', 'r') as f:
        content = f.read()
    
    checks = [
        ('Page configuration', 'st.set_page_config' in content),
        ('Dashboard page', 'page == "Dashboard"' in content),
        ('Configuration page', 'page == "Configuration"' in content),
        ('AI Assistant page', 'page == "AI Assistant"' in content),
        ('Logs page', 'page == "Logs"' in content),
        ('Bot initialization', 'def initialize_bot' in content),
        ('Session state', 'st.session_state' in content),
        ('Sidebar navigation', 'st.sidebar' in content),
        ('Account metrics', 'st.metric' in content),
        ('Data tables', 'pd.DataFrame' in content),
        ('Chat interface', 'chat_history' in content),
        ('Log display', 'st.text_area' in content),
        ('Start/Stop controls', 'Start Bot' in content and 'Stop Bot' in content),
        ('Configuration save', 'Save Configuration' in content),
    ]
    
    all_passed = True
    for name, result in checks:
        status = '✓' if result else '✗'
        print(f'{status} {name}')
        if not result:
            all_passed = False
    
    return all_passed


def test_helper_scripts():
    """Test that helper scripts exist and are valid."""
    print("\nTesting helper scripts...")
    
    import os
    
    checks = [
        ('run_dashboard.py exists', os.path.exists('run_dashboard.py')),
        ('run_dashboard.py is executable', os.access('run_dashboard.py', os.X_OK)),
        ('STREAMLIT_GUIDE.md exists', os.path.exists('STREAMLIT_GUIDE.md')),
        ('STREAMLIT_UI.md exists', os.path.exists('STREAMLIT_UI.md')),
    ]
    
    all_passed = True
    for name, result in checks:
        status = '✓' if result else '✗'
        print(f'{status} {name}')
        if not result:
            all_passed = False
    
    return all_passed


def test_requirements():
    """Test that streamlit is in requirements.txt."""
    print("\nTesting requirements.txt...")
    
    with open('requirements.txt', 'r') as f:
        content = f.read()
    
    checks = [
        ('streamlit in requirements', 'streamlit' in content),
    ]
    
    all_passed = True
    for name, result in checks:
        status = '✓' if result else '✗'
        print(f'{status} {name}')
        if not result:
            all_passed = False
    
    return all_passed


def test_forex_bot_integration():
    """Test that forex_bot.py supports streamlit mode."""
    print("\nTesting forex_bot.py integration...")
    
    with open('forex_bot.py', 'r') as f:
        content = f.read()
    
    checks = [
        ('Streamlit mode detection', '--web' in content or 'streamlit' in content.lower()),
        ('GUI mode option', '--gui' in content),
    ]
    
    all_passed = True
    for name, result in checks:
        status = '✓' if result else '✗'
        print(f'{status} {name}')
        if not result:
            all_passed = False
    
    return all_passed


def main():
    """Run all tests."""
    print("=" * 60)
    print("Streamlit Dashboard Tests")
    print("=" * 60)
    print()
    
    results = []
    
    results.append(('Imports', test_streamlit_imports()))
    results.append(('Structure', test_streamlit_structure()))
    results.append(('Helper Scripts', test_helper_scripts()))
    results.append(('Requirements', test_requirements()))
    results.append(('Integration', test_forex_bot_integration()))
    
    print()
    print("=" * 60)
    print("Test Results")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = '✓ PASSED' if passed else '✗ FAILED'
        print(f'{status}: {name}')
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("✓ All tests passed!")
        print("\nYou can now run the dashboard with:")
        print("  streamlit run streamlit_app.py")
        print("or")
        print("  python run_dashboard.py")
    else:
        print("✗ Some tests failed. Please review the output above.")
    
    print()


if __name__ == "__main__":
    main()
