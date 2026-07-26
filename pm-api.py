#!/usr/bin/env python3
"""
PM Agent REST API
Usage: curl http://localhost:8080/research
"""

from flask import Flask, jsonify, request
import subprocess
import json
import re

app = Flask(__name__)

@app.route('/research', methods=['POST'])
def research():
    """Trigger keyword research"""
    data = request.get_json() or {}
    seed_keywords = data.get('keywords', ['AI procurement software'])
    
    result = subprocess.run(
        ['python3', '/root/dev/agentic-pipeline/agents/pm/agent.py'],
        capture_output=True, text=True,
        env={**os.environ, 'SEED_KEYWORDS': json.dumps(seed_keywords)}
    )
    
    # Extract JSON
    json_match = re.search(r'\{[^{}]*\}', result.stdout, re.DOTALL)
    if json_match:
        return jsonify(json.loads(json_match.group()))
    else:
        return jsonify({'error': 'Parse error', 'output': result.stdout[:500]}), 500

@app.route('/status', methods=['GET'])
def status():
    """Get Neo4j status"""
    result = subprocess.run(
        ['docker', 'exec', 'agentic-pipeline-neo4j', 'bin/cypher-shell',
         '-u', 'neo4j', '-p', 'Agentic2026SecurePass',
         'MATCH (n) RETURN labels(n)[0] as type, count(*) as count;'],
        capture_output=True, text=True
    )
    
    # Parse table output
    lines = result.stdout.strip().split('\n')[1:]  # Skip header
    nodes = {}
    for line in lines:
        parts = line.split(',')
        if len(parts) >= 2:
            node_type = parts[0].strip().strip('"')
            count = int(parts[1].strip())
            nodes[node_type] = count
    
    return jsonify({'neo4j_nodes': nodes})

@app.route('/keywords', methods=['GET'])
def keywords():
    """List keywords in Neo4j"""
    result = subprocess.run(
        ['docker', 'exec', 'agentic-pipeline-neo4j', 'bin/cypher-shell',
         '-u', 'neo4j', '-p', 'Agentic2026SecurePass',
         'MATCH (k:Keyword) RETURN k.term, k.volume, k.difficulty ORDER BY k.volume DESC;'],
        capture_output=True, text=True
    )
    
    # Parse CSV output
    lines = result.stdout.strip().split('\n')[1:]
    keyword_list = []
    for line in lines:
        parts = line.split(',')
        if len(parts) >= 3:
            keyword_list.append({
                'term': parts[0].strip().strip('"'),
                'volume': int(parts[1].strip()),
                'difficulty': int(parts[2].strip())
            })
    
    return jsonify({'keywords': keyword_list})

if __name__ == '__main__':
    import os
    print("🚀 PM Agent API starting on http://localhost:8080")
    print("Endpoints:")
    print("  POST /research - Start keyword research")
    print("  GET  /status   - Neo4j status")
    print("  GET  /keywords - List keywords")
    app.run(host='0.0.0.0', port=8080, debug=False)
