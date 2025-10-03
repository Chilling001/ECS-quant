"""
Simple test to verify the Streamlit app structure and components.
"""
import sys

def test_requirements():
    """Test that requirements.txt has been updated."""
    with open('requirements.txt', 'r') as f:
        content = f.read()
    
    required = ['streamlit', 'yfinance', 'openai']
    missing = []
    
    for req in required:
        if req.lower() not in content.lower():
            missing.append(req)
    
    if missing:
        print(f"❌ Missing requirements: {', '.join(missing)}")
        return False
    else:
        print("✅ requirements.txt updated correctly")
        return True

def test_app_exists():
    """Test that app.py exists and has correct structure."""
    try:
        with open('app.py', 'r') as f:
            content = f.read()
        
        required_components = {
            'Streamlit import': 'import streamlit as st',
            'StrategyEngine import': 'from strategy_engine import StrategyEngine',
            'Sidebar config': 'st.sidebar',
            'Trading symbols input': 'text_input',
            'Levels input': 'number_input',
            'Drawdown slider': 'slider',
            'Run Bot button': 'Run Bot',
            'AI chat': 'AI Portfolio Manager',
        }
        
        all_present = True
        for name, component in required_components.items():
            if component not in content:
                print(f"❌ Missing: {name}")
                all_present = False
        
        if all_present:
            print("✅ app.py has all required components")
        return all_present
    except FileNotFoundError:
        print("❌ app.py not found")
        return False

def test_strategy_engine_exists():
    """Test that strategy_engine.py exists and has correct structure."""
    try:
        with open('strategy_engine.py', 'r') as f:
            content = f.read()
        
        required_methods = [
            'def get_market_data',
            'def run_strategy',
            'def get_ai_advice',
            'def place_mock_trade',
            'def chat_with_ai',
            'yf.download',
            'st.secrets'
        ]
        
        all_present = True
        for method in required_methods:
            if method not in content:
                print(f"❌ Missing: {method}")
                all_present = False
        
        if all_present:
            print("✅ strategy_engine.py has all required methods")
        return all_present
    except FileNotFoundError:
        print("❌ strategy_engine.py not found")
        return False

def test_ai_manager_updated():
    """Test that ai_manager.py has been updated to new OpenAI API."""
    try:
        with open('ai_manager.py', 'r') as f:
            content = f.read()
        
        has_new_api = 'from openai import OpenAI' in content
        has_client_init = 'self.client = OpenAI' in content
        has_new_call = 'self.client.chat.completions.create' in content
        has_old_call = 'openai.ChatCompletion.create' in content
        
        if has_new_api and has_client_init and has_new_call and not has_old_call:
            print("✅ ai_manager.py updated to new OpenAI API")
            return True
        else:
            print("❌ ai_manager.py not fully updated")
            return False
    except FileNotFoundError:
        print("❌ ai_manager.py not found")
        return False

def test_secrets_template():
    """Test that secrets template exists."""
    try:
        with open('.streamlit/secrets.toml.example', 'r') as f:
            content = f.read()
        if 'OPENAI_API_KEY' in content:
            print("✅ secrets.toml.example created")
            return True
        else:
            print("❌ secrets.toml.example missing OPENAI_API_KEY")
            return False
    except FileNotFoundError:
        print("❌ .streamlit/secrets.toml.example not found")
        return False

def main():
    print("=" * 60)
    print("Testing Streamlit App Migration")
    print("=" * 60)
    print()
    
    tests = [
        ("Requirements", test_requirements),
        ("App.py", test_app_exists),
        ("Strategy Engine", test_strategy_engine_exists),
        ("AI Manager Update", test_ai_manager_updated),
        ("Secrets Template", test_secrets_template),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\nTesting: {name}")
        print("-" * 60)
        results.append(test_func())
    
    print()
    print("=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    
    if all(results):
        print("\n🎉 All tests passed! Migration complete!")
        return 0
    else:
        print("\n⚠️ Some tests failed. Please review above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
