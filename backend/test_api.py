#!/usr/bin/env python3
"""
Test API to verify Hidden Gems are being sent correctly
"""

import requests
import json

def test_api():
    """Test the API endpoint"""
    
    print("🌐 Testing API Hidden Gems Response")
    print("=" * 50)
    
    try:
        response = requests.get('http://localhost:8000/api/dashboard/GLV')
        if response.status_code == 200:
            data = response.json()
            developers = data.get('developers', [])
            print(f'✅ API returned {len(developers)} developers')
            
            hidden_gems = [dev for dev in developers if dev.get('is_hidden_gem', False)]
            print(f'✅ Hidden gems in API response: {len(hidden_gems)}')
            
            if hidden_gems:
                print(f'\nHidden Gems from API:')
                for gem in hidden_gems:
                    name = gem.get('name', 'Unknown')
                    is_gem = gem.get('is_hidden_gem', False)
                    quadrant = gem.get('quadrant', 0)
                    impact = gem.get('raw_impact', 0)
                    visibility = gem.get('raw_visibility', 0)
                    print(f'  - {name}: is_hidden_gem={is_gem}, quadrant={quadrant}, impact={impact:.2f}, visibility={visibility:.2f}')
            else:
                print('❌ No hidden gems found in API response!')
                
                # Debug: show all developers with their quadrant info
                print('\nAll developers:')
                for dev in developers[:5]:  # Show first 5
                    name = dev.get('name', 'Unknown')
                    is_gem = dev.get('is_hidden_gem', False)
                    quadrant = dev.get('quadrant', 0)
                    print(f'  - {name}: is_hidden_gem={is_gem}, quadrant={quadrant}')
                    
        else:
            print(f'❌ API error: {response.status_code}')
            print(response.text)
    except Exception as e:
        print(f'❌ Could not connect to API: {e}')
        print('Make sure backend is running: python backend/main.py')

if __name__ == "__main__":
    test_api()