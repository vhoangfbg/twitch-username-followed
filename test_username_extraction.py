#!/usr/bin/env python3
"""
Script test để kiểm tra việc trích xuất username
"""

from email_reader import read_followed_usernames, extract_username_from_url, is_valid_username

def test_username_extraction():
    """Test các function trích xuất username"""
    
    print("🧪 Testing username extraction functions...")
    
    # Test URL extraction
    test_urls = [
        "https://www.twitch.tv/shroud",
        "https://twitch.tv/ninja/videos",
        "twitch.tv/pokimane",
        "https://www.twitch.tv/tfue?collection=123",
        "https://twitch.tv/email-unsubscribe",  # Should be invalid
        "https://twitch.tv/a",  # Too short
        "https://twitch.tv/this_username_is_way_too_long_for_twitch"  # Too long
    ]
    
    print("\n📋 Testing URL extraction:")
    for url in test_urls:
        username = extract_username_from_url(url)
        valid = is_valid_username(username) if username else False
        print(f"  {url} -> {username} ({'✅ Valid' if valid else '❌ Invalid'})")
    
    # Test valid username function
    test_usernames = [
        "shroud",           # Valid
        "ninja_fortnite",   # Valid
        "pokimane",         # Valid
        "a",                # Too short
        "email-unsubscribe", # Invalid keyword
        "test@user",        # Invalid characters
        "normaluser123",    # Valid
        "",                 # Empty
        "verylongusernamethatexceedslimit"  # Too long
    ]
    
    print("\n✅ Testing username validation:")
    for username in test_usernames:
        valid = is_valid_username(username)
        print(f"  '{username}' -> {'✅ Valid' if valid else '❌ Invalid'}")
    
    print("\n🔍 Testing email reading (requires config.json)...")
    try:
        usernames = read_followed_usernames()
        if usernames:
            print(f"✅ Found {len(usernames)} usernames:")
            for username in sorted(usernames)[:10]:  # Show first 10
                print(f"  • {username}")
            if len(usernames) > 10:
                print(f"  ... and {len(usernames) - 10} more")
        else:
            print("ℹ️ No usernames found")
    except Exception as e:
        print(f"❌ Error reading emails: {e}")
        print("💡 Make sure config.json exists with valid credentials")

if __name__ == "__main__":
    test_username_extraction()
