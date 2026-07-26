#!/bin/bash
# PM Agent CLI Interface
# Usage: ./pm-cli.sh [command] [args]

cd /root/dev/agentic-pipeline

case "$1" in
  research)
    echo "🚀 Starting Keyword Research..."
    python3 agents/pm/agent.py
    ;;
  
  status)
    echo "📊 Current Status:"
    docker exec agentic-pipeline-neo4j bin/cypher-shell -u neo4j -p "Agentic2026SecurePass" \
      "MATCH (n) RETURN labels(n)[0] as type, count(*) as count ORDER BY count DESC;"
    ;;
  
  keywords)
    echo "🔍 Keywords in Neo4j:"
    docker exec agentic-pipeline-neo4j bin/cypher-shell -u neo4j -p "Agentic2026SecurePass" \
      "MATCH (k:Keyword) RETURN k.term, k.volume, k.difficulty ORDER BY k.volume DESC LIMIT 10;"
    ;;
  
  *)
    echo "PM Agent CLI"
    echo "Usage: $0 {research|status|keywords}"
    echo ""
    echo "Commands:"
    echo "  research  - Run keyword research pipeline"
    echo "  status    - Show Neo4j database status"
    echo "  keywords  - List keywords in Neo4j"
    exit 1
    ;;
esac
