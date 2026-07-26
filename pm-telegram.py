#!/usr/bin/env python3
"""
PM Agent Telegram Bot Interface
Usage: Send messages to bot, it runs PM agent commands
"""

import os
import sys
import subprocess
import json

# Telegram bot token (get from @BotFather)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

def send_message(text):
    """Send message to Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print(f"📱 Telegram: {text}")
        return
    
    import requests
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown'
    })

def handle_command(cmd, args):
    """Handle PM agent commands"""
    if cmd == 'research':
        send_message("🔍 Starting keyword research...")
        result = subprocess.run(
            ['python3', '/root/dev/agentic-pipeline/agents/pm/agent.py'],
            capture_output=True, text=True
        )
        # Extract JSON result
        import re
        json_match = re.search(r'\{[^{}]*\}', result.stdout, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            if data.get('success'):
                keywords = data.get('researcher', {}).get('result', {}).get('total_keywords', 0)
                send_message(f"✅ Research complete!\n\n📊 Keywords: {keywords}\n💾 Stored in Neo4j")
            else:
                send_message(f"❌ Error: {data.get('error', 'Unknown')}")
        else:
            send_message(f"⚠️ Output: {result.stdout[:500]}")
    
    elif cmd == 'status':
        result = subprocess.run(
            ['docker', 'exec', 'agentic-pipeline-neo4j', 'bin/cypher-shell',
             '-u', 'neo4j', '-p', 'Agentic2026SecurePass',
             'MATCH (n) RETURN labels(n)[0] as type, count(*) as count;'],
            capture_output=True, text=True
        )
        send_message(f"📊 Neo4j Status:\n```\n{result.stdout}\n```")
    
    else:
        send_message(f"❓ Unknown command: {cmd}\n\nAvailable: research, status")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: pm-telegram.py <command> [args]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    handle_command(cmd, args)
